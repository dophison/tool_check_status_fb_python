import requests
from flask import Flask
import urllib.parse
import re
import html
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


app = Flask(__name__)
def read_file_content():
    with open('checkscam.txt', 'r', encoding='utf-8') as file:
        content = file.readlines()
    return content
def read_debug_links():
    with open('debug_link.txt', 'r', encoding='utf-8') as file:
        links = file.readlines()
    return [link.strip() for link in links]


def convert_percent_encoded_to_unicode(text):
    decoded_text = urllib.parse.unquote(text)
    return decoded_text


def check_link_status(response):
    try:
        if '<link rel="alternate" hreflang="x-default" href="https://www.facebook.com/' in response:
            href_start = response.find('<link rel="alternate" hreflang="x-default" href="') + len(
                '<link rel="alternate" hreflang="x-default" href="')
            href_end = response.find('"', href_start)
            href_content = response[href_start:href_end]
            style = 'green'
            # Kiểm tra trong response có <meta name="description" content=" hay không
            if '<meta name="description" content="' in response:
                meta_start = response.find('<meta name="description" content="') + len(
                    '<meta name="description" content="')
                meta_end = response.find('đang', meta_start)
                name = response[meta_start:meta_end]
                print(name)
            else:
                name = ''
            return href_content, name, style
        elif '<id="facebook" class="no_js">' in response:

            # Trả về style màu đỏ
            style = 'red'
            return '','', style
        return '','','red'
    except requests.exceptions.RequestException:
        return '','','red'


# Lấy name từ trong status có dạng https://www.facebook.com/people/abcxsttat\
def get_name_from_status(status):
    # Loại bỏ phần đầu của chuỗi status
    base_url = 'https://www.facebook.com/people/'
    name_start = len(base_url)
    # Tìm vị trí kết thúc của name trong chuỗi
    name_end = status.find('/', name_start)
    # Trích xuất name từ chuỗi
    name = status[name_start:name_end]
    return name


@app.route('/')
def home():
    content = read_file_content()
    formatted_content = '<br>'.join(f"{index + 1}. {line}" for index, line in enumerate(content))
    return f"DANH SÁCH LINK FACEBOOK SCAM<br>{formatted_content}"

@app.route('/status')
def status():

    debug_links = read_debug_links()
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    result = []
    # Mở trang đăng nhập của Facebook
    driver.get("https://www.facebook.com/login")

    # Nhập thông tin đăng nhập (email hoặc số điện thoại và mật khẩu)
    email_or_phone = "van1973cute@gmail.com"
    password = "haudinhtruong20122002"
    email_phone_input = driver.find_element(By.ID,"email")
    email_phone_input.send_keys(email_or_phone)
    password_input = driver.find_element(By.ID,"pass")
    password_input.send_keys(password)
    # Thực hiện đăng nhập bằng cách nhấn Enter
    password_input.send_keys(Keys.ENTER)

    try:
        for link in debug_links:
            driver.get(link)
            response = driver.page_source
            status, name, style = check_link_status(response)
            if status.startswith('https://www.facebook.com/'):
                name = convert_percent_encoded_to_unicode(name)
                result.append({'status': status, 'name': name, 'style': style})
            if status == '':
                status = link
                result.append({'status': status, 'name': "Unknown", 'style': style})
    finally:
        driver.quit()
    formatted_content = '<br>'.join(
        f'<span style="color: {item["style"]}">{index + 1}.{item["name"]} ----> {item["status"]}  </span>'
        for index, item in enumerate(result)
    )
    with open('history.html', 'w', encoding='utf-8') as file:
        file.write("THÔNG TIN VỀ TÌNH TRẠNG HOẠT ĐỘNG")
        file.write(formatted_content)

    return f"THÔNG TIN VỀ TÌNH TRẠNG HOẠT ĐỘNG<br>{formatted_content}"



if __name__ == '__main__':
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=5000)
    app.run(debug=True)
