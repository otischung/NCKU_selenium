from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By

import requests

import env


def main():
    # 隱藏自動化測試標籤
    option = webdriver.ChromeOptions()
    option.add_experimental_option("excludeSwitches", ["enable-automation"])
    option.add_experimental_option("useAutomationExtension", False)
    option.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=option)
    # 建立連線 session
    sess = requests.Session()
    
    # 開啟網頁
    driver.get("https://course.ncku.edu.tw/index.php")
    # 關閉 KUAP APP 訊息通知
    driver.find_element(By.CSS_SELECTOR, "#show_sp_msg .btn").click()
    # 點擊登入頁面
    # TODO: 頁面跳轉應可以加速
    driver.find_element(By.LINK_TEXT, "登入").click()
    # 儲存 Cookies
    cookies = driver.get_cookies()
    # 將 cookies 輸入至 session 裡面
    for c in cookies:
        sess.cookies.set(c["name"], c["value"])
    # 輸入帳號
    driver.find_element(By.ID, "user_id").send_keys(env.login["username"])
    # 輸入密碼
    driver.find_element(By.ID, "passwd").send_keys(env.login["passwd"])
    # 驗證碼
    captcha_url = driver.find_element(By.CSS_SELECTOR, ".click").get_attribute("src")
    img = Image.open(sess.get(captcha_url, stream=True).raw)  # https://stackoverflow.com/questions/7391945/how-do-i-read-image-data-from-a-url-in-python
    img.show()
    input()

    sess.close()


if __name__ == "__main__":
    main()
