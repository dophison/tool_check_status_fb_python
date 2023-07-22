import requests
from flask import Flask
import urllib.parse
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import os
from bs4 import BeautifulSoup
from datetime import datetime

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
            else:
                name = ''
            return href_content, name, style
        elif '<id="facebook" class="no_js">' in response:
            # Trả về style màu đỏ
            style = 'red'
            return '','', style
        return '','',''
    except requests.exceptions.RequestException:
        return '','','yellow'


def check_link_status_sign_in(response):
    try:
        if 'Bạn hiện không xem được nội dung này' in response:
            # Trả về style màu đỏ
            style = 'red'
            return '', '', style
        elif 'class="x6s0dn4 x9f619 x78zum5 x2lah0s x1hshjfz x1n2onr6 xng8ra x1pi30zi x1swvt13"' in response:
            start_tag = '<h1'
            end_tag = '</h1>'
            start_index = response.find(start_tag)
            if start_index != -1:
                end_index = response.find(end_tag, start_index + len(start_tag))
                first_string = response[start_index:end_index + len(end_tag)]
                # Tìm chuỗi thứ hai từ vị trí kết thúc của chuỗi đầu tiên
                second_start_index = response.find(start_tag, end_index + len(end_tag))
                second_end_index = response.find(end_tag, second_start_index + len(start_tag))
                second_string = response[second_start_index:second_end_index + len(end_tag)]
                # print(first_string)
                # print(second_string)
                if second_string.strip() == 'Thông báo' or second_string =='':
                    soup = BeautifulSoup(first_string, 'html.parser')
                    name = soup.text
                    style = 'green'
                    return '', name, style
                else:
                    soup_1 = BeautifulSoup(second_string, 'html.parser')
                    name = soup_1.text
                    style = 'green'
                    return '', name, style
        return '','','yellow'
    except requests.exceptions.RequestException:
        return '','','yellow'


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
    result_need_sign_in= []
    # Lấy thông tin đăng nhập (email hoặc số điện thoại và mật khẩu)
    # Bảo mật bằng cách set biến môi trường
    email_or_phone = os.environ.get("MY_EMAIL")
    password = os.environ.get("MY_PASSWORD")
    email_or_phone = "van" + email_or_phone
    password = "truong" + password

    try:
        #Duyệt qua danh sách các link
        for link in debug_links:
            driver.get(link)
            response = driver.page_source
            status, name, style = check_link_status(response)
            if status.startswith('https://www.facebook.com/'):
                #Đổi tên thành dạng unicode
                name = convert_percent_encoded_to_unicode(name)
                result.append({'status': status, 'name': name, 'style': style})
            if status == '':
                result_need_sign_in.append(link)
    finally:
        driver.quit()
    #Kiem tra cac link bằng đăng nhập
    try:
        #Khởi động lại browser
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        # Xử lý sign in facebook
        # print(email_or_phone)
        # print(password)
        driver.get("https://www.facebook.com/login")
        email_phone_input = driver.find_element(By.ID, "email")
        email_phone_input.send_keys(email_or_phone)
        password_input = driver.find_element(By.ID, "pass")
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)
        #Đợi trang xử lý (nếu đường truyền mạng không ổn định thì nên set lâu hơn)
        time.sleep(10)

        # for link in result_need_sign_in:
        #     print(link)
        #Duyệt qua từng link trong list result_need_sign_in
        for link in result_need_sign_in:
            driver.get(link)
            response_signin = driver.page_source
            status,name,style = check_link_status_sign_in(response_signin)
            status = link
            if name != '':
                result.append({'status': status, 'name': name, 'style': style})
            else:
                result.append({'status': status, 'name': "Unknown", 'style': style})
        result_need_sign_in.clear()
    finally:
        driver.quit()
    #Chỉnh format để hiển thị trên html với thẻ <br> là xuống dòng
    formatted_content = '<br>'.join(
        f'<span style="color: {item["style"]}">{index + 1}.{item["name"]} ----> {item["status"]}  </span>'
        for index, item in enumerate(result)
    )
    #Làm sạch list result
    result.clear()
    #Lưu vào file history với real time
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    title = f"Ngày giờ: {current_datetime}<br>THÔNG TIN VỀ TÌNH TRẠNG HOẠT ĐỘNG <br>"
    with open('history.html', 'a', encoding='utf-8') as file:
        file.write(title)
        file.write(formatted_content)
    return f"THÔNG TIN VỀ TÌNH TRẠNG HOẠT ĐỘNG<br>{formatted_content}"
@app.route('/history')
def history():
    with open('history.html', 'r', encoding='utf-8') as file:
        content = file.read()
    return content

if __name__ == '__main__':
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=5000)
    app.run(debug=True)
