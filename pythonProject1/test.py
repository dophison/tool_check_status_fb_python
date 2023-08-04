from selenium import webdriver
import requests
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
import re
import urllib.parse
from bs4 import BeautifulSoup


def check_link_status(response):
    try:
        if '<link rel="alternate" hreflang="x-default" href="https://www.facebook.com/' in response:
            href_start = response.find('<link rel="alternate" hreflang="x-default" href="') + len(
                '<link rel="alternate" hreflang="x-default" href="')
            href_end = response.find('"', href_start)
            href_content = response[href_start:href_end]
            style = 'green'
            # Kiểm tra trong response có <meta name="description" content=" hay không

                # meta_start = response.find('<meta name="description" content="') + len(
                #     '<meta name="description" content="')
                # meta_end = response.find('đang', meta_start)
                # name = response[meta_start:meta_end]
            soup = BeautifulSoup(response, 'html.parser')
            meta_tag = soup.find('meta', attrs={'name': 'description'})
            if meta_tag:
                name = meta_tag.get('content')
                sentences = name.split('.')
                if len(sentences) > 0:
                    name = sentences[0].strip()
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
def convert_percent_encoded_to_unicode(text):
    decoded_text = urllib.parse.unquote(text)
    return decoded_text

# Lấy thông tin đăng nhập (email hoặc số điện thoại và mật khẩu)
email_or_phone = os.environ.get("MY_EMAIL")
password = os.environ.get("MY_PASSWORD")
email_or_phone = "van" + email_or_phone
password = "truong" + password
print(email_or_phone)
print(password)


# Khởi tạo trình duyệt Firefox
driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
try:
    # Mở trang đăng nhập của Facebook
    # driver.get("https://www.facebook.com/login")
    #
    # email_phone_input = driver.find_element(By.ID,"email")
    # email_phone_input.send_keys(email_or_phone)
    # password_input = driver.find_element(By.ID,"pass")
    # password_input.send_keys(password)
    #
    # #Thực hiện đăng nhập bằng cách nhấn Enter
    #
    # password_input.send_keys(Keys.ENTER)
    #
    # # Đợi một lúc để trang đăng nhập xử lý
    # time.sleep(5)
    result_need_sign_in= []
    result = []
    url = "https://www.facebook.com/thduc.205.real"
    driver.get(url)
    response = driver.page_source
    with open('response_test', 'a', encoding='utf-8') as file:
        content = file.write(response)
    status, name, style = check_link_status(response)
    print(name,status)
    if status.startswith('https://www.facebook.com/'):
        # Đổi tên thành dạng unicode
        name = convert_percent_encoded_to_unicode(name)
        result.append({'status': status, 'name': name, 'style': style})
    if status == '':
        result_need_sign_in.append(url)




    # if 'style="height: 168px; width: 168px;' in response:
    #     style = 'red'
    #     print(style)
    # elif '' in response:
        # #Bỏ qua chuỗi đầu tiên
        # start_tag = '<h1 class="x1heor9g x1qlqyl8 x1pd3egz x1a2a7pz">'
        # start_index = response.find(start_tag)
        # if start_index != -1:
        #     # Bắt đầu tìm từ vị trí kết thúc của chuỗi đầu tiên
        #     end_index = response.find('</h1>', start_index)
        #     name = response[start_index + len(start_tag):end_index]
        #     style = 'green'
        #     print(style)
        #     print(name)
        # else:
        #     print('')
        # start_tag = '<h1'
        # end_tag = '</h1>'
        # start_index = response.find(start_tag)
        # if start_index != -1:
        #     end_index = response.find(end_tag, start_index + len(start_tag))
        #     first_string = response[start_index:end_index + len(end_tag)]
        #
        #     # Tìm chuỗi thứ hai từ vị trí kết thúc của chuỗi đầu tiên
        #     second_start_index = response.find(start_tag, end_index + len(end_tag))
        #     second_end_index = response.find(end_tag, second_start_index + len(start_tag))
        #     second_string = response[second_start_index:second_end_index + len(end_tag)]
        #
        #     print(first_string)
        #     print(second_string)
        #     if second_string.strip() == 'Thông báo':
        #         soup = BeautifulSoup(first_string, 'html.parser')
        #         name = soup.text
        #     else:
        #         soup_1 = BeautifulSoup(second_string, 'html.parser')
        #         name = soup_1.text
        #     style = 'green'
        #     print(style)
        #     print(name)
    # else:
    #     style = 'yellow'
    #     print(style)

except Exception as e:
    print(f"Failed to log in to Facebook: {e}")

finally:
    # Đóng trình duyệt sau khi hoàn thành
    driver.quit()