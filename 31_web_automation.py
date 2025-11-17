"""
31. Web Automation - Selenium을 이용한 웹 자동화
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class WebAutomation:
    def __init__(self, headless=False):
        """웹 자동화 초기화"""
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def navigate(self, url):
        """URL 이동"""
        self.driver.get(url)
        print(f"Navigated to: {url}")

    def find_element(self, by, value):
        """요소 찾기"""
        return self.wait.until(EC.presence_of_element_located((by, value)))

    def click(self, by, value):
        """클릭"""
        element = self.find_element(by, value)
        element.click()

    def type_text(self, by, value, text):
        """텍스트 입력"""
        element = self.find_element(by, value)
        element.clear()
        element.send_keys(text)

    def get_text(self, by, value):
        """텍스트 가져오기"""
        element = self.find_element(by, value)
        return element.text

    def take_screenshot(self, filename='screenshot.png'):
        """스크린샷"""
        self.driver.save_screenshot(filename)
        print(f"Screenshot saved: {filename}")

    def execute_script(self, script):
        """JavaScript 실행"""
        return self.driver.execute_script(script)

    def close(self):
        """브라우저 닫기"""
        self.driver.quit()

# 사용 예제
if __name__ == '__main__':
    # Note: Selenium WebDriver가 설치되어 있어야 합니다
    print("Web Automation - Selenium wrapper")
    print("Install: pip install selenium")
    print("\nExample usage:")
    print("bot = WebAutomation()")
    print("bot.navigate('https://example.com')")
    print("bot.click(By.ID, 'button-id')")
    print("bot.type_text(By.NAME, 'search', 'query')")
    print("bot.take_screenshot('result.png')")
    print("bot.close()")
