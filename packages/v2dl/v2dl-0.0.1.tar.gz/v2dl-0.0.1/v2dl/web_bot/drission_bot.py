import os
import sys
import time
import random

from DrissionPage import ChromiumPage, ChromiumOptions
from DrissionPage.common import By, wait_until
from DrissionPage.errors import ElementNotFoundError, WaitTimeoutError

from .base import BaseBot, BaseBehavior, BaseScroll


class DrissionBot(BaseBot):
    def __init__(self, config, close_browser, logger):
        super().__init__(config, close_browser, logger)
        self.config = config
        self.init_driver()
        self.cloudflare = DriCloudflareHandler(self.page, self.logger)

    def init_driver(self):
        user_data_dir = self.config.chrome.profile_path
        if not os.path.exists(user_data_dir):
            os.makedirs(user_data_dir)
            self.new_profile = True
        else:
            self.new_profile = False

        # subprocess of chrome: Drission terminate chrome anyway

        co = ChromiumOptions()
        # co.use_system_user_path()
        co.set_user_data_path(user_data_dir)
        self.page = ChromiumPage(addr_or_opts=co)
        self.page.set.scroll.smooth(on_off=True)
        self.page.set.scroll.wait_complete(on_off=True)

        self.scroll = DriScroll(self.page, self.config, self.logger)
        self.human = DriBehavior()

    def close_driver(self):
        if self.close_browser:
            self.page.quit()

    def auto_page_scroll(
        self, url: str, max_retry: int = 3, page_sleep: int = 5, fast_scroll: bool = False
    ) -> str:
        """
        Scroll page automatically with retries and Cloudflare challenge handle.

        Args:
            url: Target URL
            max_retry: Maximum number of retry attempts
            fast_scroll: Whether to use fast scrolling behavior

        Returns:
            str: Page HTML content or error message
        """
        response: str = ""

        # page_sleep_time: tuple[int, int] = (20, 40) if fast_scroll else (5, 15)
        scroll_down = self.page.scroll.to_bottom if fast_scroll else self.scroll.scroll_to_bottom

        for attempt in range(max_retry):
            try:
                self.page.get(url)

                # handle page redirection fail
                if not self.page.states.is_alive:
                    page_alive = self.handle_redirection_fail(url, max_retry, page_sleep)
                    if not page_alive:
                        self.logger.error("Reconnection fail. Please check your network status.")
                        break

                # handle challenges
                # self.page.wait.load_start()
                self.page.wait.ele_displayed("xpath://div[@class='album-photo my-2']", timeout=5)
                if self.cloudflare.handle_simple_block(attempt, max_retry):
                    continue

                # main business
                self.handle_login()
                scroll_down()
                response = self.page.html

                # Sleep to avoid Cloudflare blocking
                self.logger.debug("捲動結束，暫停作業避免封鎖。")
                DriBehavior.random_sleep(page_sleep, page_sleep + 5)
                break

            except Exception as e:
                self.logger.error(
                    f"Request failed - Attempt {attempt + 1}/{max_retry}. Error: {str(e)}",
                    exc_info=True,
                )
                self.human.random_sleep(page_sleep, page_sleep + 5)

        if not response:
            error_msg = f"Failed to retrieve URL after {max_retry} attempts: '{url}'"
            self.logger.error(error_msg)
            return error_msg
        return response

    def handle_redirection_fail(self, url: str, max_retry: int, sleep_time: int) -> bool:
        if self.page.url == url and self.page.states.is_alive:
            return True
        retry = 1
        while retry <= max_retry:
            self.logger.error(f"Connection failed - Attempt {retry + 1}/{max_retry}")
            self.human.random_sleep(sleep_time, sleep_time + 5 * random.uniform(1, retry * 5))

            if self.cloudflare.handle_simple_block(retry, max_retry):
                self.logger.critical("Failed to solve Cloudflare turnstile challenge")
                continue

            self.page.get(url)
            retry += 1
            if self.page.url == url and self.page.states.is_alive:
                return True

        return self.page.url == url and self.page.states.is_alive

    def handle_login(self):
        success = False
        if "用戶登錄" in self.page.html:
            self.logger.info("Login page detected - Starting login process")
            try:
                if self.email is None or self.password is None:
                    self.logger.critical("Email and password not provided")
                    sys.exit("Automated login failed.")

                # self.handle_cloudflare_recaptcha()

                BaseBehavior.random_sleep(0.1, 0.3)
                email_field = self.page("#email")
                password_field = self.page("#password")

                self.human_like_type(email_field, self.email)
                BaseBehavior.random_sleep(0.01, 0.3)
                self.human_like_type(password_field, self.password)
                BaseBehavior.random_sleep(0.01, 0.5)

                # Already checked by default
                # remember_checkbox = self.page('#remember')
                # remember_checkbox.click()

                login_button = self.page(
                    'x://button[contains(text(), "登錄") and @class="btn btn-primary btn-block"]'
                )
                login_button.click()

                self.human.random_sleep(3, 5)

                if "用戶登錄" not in self.page.html:
                    self.logger.info("Login successful")
                    success = True
                else:
                    self.logger.error("Login failed - Checking error messages")
                    self.check_login_errors()
                    return

            except ElementNotFoundError as e:
                self.logger.error(f"Login form element not found: {str(e)}")
            except WaitTimeoutError as e:
                self.logger.error(f"Timeout waiting for element: {str(e)}")
            except Exception as e:
                self.logger.error(f"Unexpected error during login: {str(e)}")

        else:
            success = True

        if not success:
            self.logger.critical("Automated login failed. Please login yourself.")
            sys.exit("Automated login failed.")

    def check_login_errors(self):
        error_message = self.page.ele("@class=alert-danger")
        if error_message:
            self.logger.error(f"Login error message: {error_message.text}")
        else:
            self.logger.warning(
                "No specific error message found - Login failed for unknown reasons"
            )

    def human_like_type(self, element, text):
        for char in text:
            element.input(char)
            self.human.random_sleep(0.001, 0.2)

    def scroll_page(self):
        scroll_length = random.randint(
            self.config.download.min_scroll_length,
            self.config.download.max_scroll_length,
        )
        self.page.scroll(pixel=scroll_length)
        # self.page.execute_script(f"window.scrollBy(0, {scroll_length});")


class DriCloudflareHandler:
    """
    Handles Cloudflare protection detection and bypass attempts.
    Includes methods for dealing with various Cloudflare challenges.
    """

    def __init__(self, page: ChromiumPage, logger):
        self.page = page
        self.logger = logger

    def handle_simple_block(self, attempt: int, retries: int) -> bool:
        """Check, handle, and return whether blocked or not"""
        blocked = False
        if self.is_simple_blocked():
            self.logger.info(f"Cloudflare challenge detected - Attempt {attempt + 1}/{retries}")
            blocked = self.handle_cloudflare_turnstile()
        return blocked

    def handle_hard_block(self) -> bool:
        """Check, log critical, and return whether blocked or not (This is a cloudflare WAF block)"""
        blocked = False
        if self.is_hard_block():
            self.logger.critical("Hard block detected by Cloudflare - Unable to proceed")
            blocked = True
        return blocked

    def is_simple_blocked(self) -> bool:
        title_check = any(text in self.page.title for text in ["請稍候...", "Just a moment..."])
        page_source_check = "Checking your" in self.page.html
        return title_check or page_source_check

    def is_hard_block(self) -> bool:
        is_blocked = "Attention Required! | Cloudflare" in self.page.title
        if is_blocked:
            self.logger.critical("Cloudflare hard block detected")
        return is_blocked

    def handle_cloudflare_turnstile(self) -> bool:
        """鬥志鬥勇失敗"""
        blocked = False
        try:
            container = self.page.ele(".cloudflare-container")
            turnstile_box = container.ele(".turnstile-box")
            turnstile_div = turnstile_box.ele("#cf-turnstile")
            pos = turnstile_div.rect.click_point()
            self.page.wait(2)
            # pyautogui.moveTo(pos[0], pos[1] + 61, duration=0.5)
            # pyautogui.click()
            self.page.wait(3)
            blocked = True
        except Exception as e:
            self.logger.error(f"Failed to solve new Cloudflare turnstile: {str(e)}", exc_info=True)
        return blocked

    def random_sleep(self, min_time, max_time):
        time.sleep(random.uniform(min_time, max_time))


class DriBehavior(BaseBehavior):
    @staticmethod
    def human_like_mouse_movement(page, element):
        # Get the element's position
        rect = element.rect
        action_x = random.randint(-100, 100)
        action_y = random.randint(-100, 100)

        # Move by offset and then to element
        page.mouse.move_to(x=rect["x"] + action_x, y=rect["y"] + action_y)
        page.mouse.move_to(rect["x"], rect["y"])
        DriBehavior.random_sleep(*BaseBehavior.pause_time)

    @staticmethod
    def human_like_click(page, element):
        DriBehavior.human_like_mouse_movement(page, element)
        page.mouse.click()
        DriBehavior.random_sleep(*BaseBehavior.pause_time)

    @staticmethod
    def human_like_type(element, text):
        for char in text:
            element.input(char)
            time.sleep(random.uniform(0.001, 0.2))
        DriBehavior.random_sleep(*BaseBehavior.pause_time)


class DriScroll(BaseScroll):
    def __init__(self, page: ChromiumPage, config, logger):
        super().__init__(config, logger)
        self.page = page
        self.page.set.scroll.smooth(on_off=True)

    def scroll_to_bottom(self):
        self.logger.info("開始捲動頁面")
        scroll_attempts = 0
        max_attempts = 45
        same_position_count = 0
        last_position = 0

        while scroll_attempts < max_attempts:
            scroll_attempts += 1

            current_position = self.get_scroll_position()
            page_height = self.get_page_height()

            if current_position == last_position:
                same_position_count += 1
                if same_position_count >= 3:
                    self.logger.debug(
                        f"連續三次偵測到相同位置，停止捲動。總共捲動 {scroll_attempts} 次"
                    )
                    break
            else:
                same_position_count = 0

            last_position = current_position

            self.perform_scroll_action()

            self.wait_for_content_load()

            self.continuous_scroll_count += 1
            if self.continuous_scroll_count >= self.max_continuous_scrolls:
                pause_time = random.uniform(3, 7)
                self.logger.debug(
                    f"連續捲動 {self.continuous_scroll_count} 次，暫停 {pause_time:.2f} 秒"
                )
                time.sleep(pause_time)
                self.continuous_scroll_count = 0
                self.max_continuous_scrolls = random.randint(3, 7)

        if scroll_attempts == max_attempts:
            self.logger.info(f"捲動結束，達到最大嘗試次數 ({max_attempts})，可能未完全捲動到底")
        else:
            self.logger.info("頁面捲動完成")

    def perform_scroll_action(self):
        action = random.choices(
            ["scroll_down", "scroll_up", "pause", "jump"],
            weights=[0.7, 0.1, 0.1, 0.001],
        )[0]

        if action == "scroll_down":
            scroll_length = random.randint(
                self.config.download.min_scroll_length,
                self.config.download.max_scroll_length,
            )
            self.logger.debug(f"嘗試向下捲動 {scroll_length} 像素")
            self.page.scroll.down(pixel=scroll_length)
            time.sleep(random.uniform(*BaseBehavior.pause_time))
        elif action == "scroll_up":
            scroll_length = random.randint(
                self.config.download.min_scroll_length,
                self.config.download.max_scroll_length,
            )
            self.logger.debug(f"嘗試向上捲動 {scroll_length} 像素")
            self.page.scroll.up(pixel=scroll_length)
        elif action == "pause":
            pause_time = random.uniform(1, 3)
            self.logger.debug(f"暫停 {pause_time:.2f} 秒")
            time.sleep(pause_time)
        elif action == "jump":
            self.logger.debug("跳轉到頁面底部")
            self.page.scroll.to_bottom()
            # self.page.scroll.to_see("@class=album-photo my-2")

    def safe_scroll(self, target_position):
        """DrissionPage does not need safe_scroll"""
        current_position = self.get_scroll_position()
        step = random.uniform(
            self.config.download.min_scroll_step,
            self.config.download.max_scroll_step,
        )

        while abs(current_position - target_position) > step:
            self.page.run_js(f"window.scrollTo(0, {current_position + step});")
            time.sleep(random.uniform(0.005, 0.1))
            new_position = self.get_scroll_position()
            if new_position == current_position:
                self.logger.debug(
                    f"無法繼續捲動，目標: {target_position}，當前: {current_position}"
                )
                break
            current_position = new_position
        self.page.run_js(f"window.scrollTo(0, {target_position});")
        return self.get_scroll_position()

    def get_scroll_position(self):
        page_location = self.page.rect.page_location
        return page_location[1]

    def get_page_height(self):
        return self.page.rect.size[1]

    def wait_for_content_load(self):
        try:
            # wait until the callable return true. default time_out=10
            wait_until(lambda: self.page.states.ready_state == "complete", timeout=5)
        except TimeoutError:
            self.logger.warning("等待新內容加載超時")
