from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time




# Khởi tạo trình duyệt Firefox
driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
try:
    # Mở trang đăng nhập của Facebook
    driver.get("https://www.facebook.com/login")

    # Nhập thông tin đăng nhập (email hoặc số điện thoại và mật khẩu)
    email_or_phone = "van1973cute@gmail.com"
    password = "haudinhtruong20122002"



    email_phone_input = driver.find_element(By.ID,"email")
    email_phone_input.send_keys(email_or_phone)
    password_input = driver.find_element(By.ID,"pass")
    password_input.send_keys(password)

    #Thực hiện đăng nhập bằng cách nhấn Enter

    password_input.send_keys(Keys.ENTER)

    # Đợi một lúc để trang đăng nhập xử lý
    time.sleep(5)
    url = "https://www.facebook.com/quanganhdeptraivclluon"
    driver.get(url)
    response = driver.page_source
    if '<link rel="alternate" hreflang="x-default" href="https://www.facebook.com/' in response:
        href_start = response.find('<link rel="alternate" hreflang="x-default" href="') + len(
            '<link rel="alternate" hreflang="x-default" href="')
        href_end = response.find('"', href_start)
        href_content = response[href_start:href_end]

        style = 'green'
        print(style)
        # Kiểm tra trong response có <meta name="description" content=" hay không
        if '<meta name="description" content="' in response:
            meta_start = response.find('<meta name="description" content="') + len(
                '<meta name="description" content="')
            meta_end = response.find('&#x111', meta_start)
            name = response[meta_start:meta_end]
        else:
            name = ''
    elif '<id="facebook" class="no_js">' in response:
            # Trả về style màu đỏ
        style = 'red'
        print(style)







except Exception as e:
    print(f"Failed to log in to Facebook: {e}")

finally:
    # Đóng trình duyệt sau khi hoàn thành
    driver.quit()