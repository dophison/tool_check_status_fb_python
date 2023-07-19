import requests
from flask import Flask
import urllib.parse
import re
import html
app = Flask(__name__)


def read_file_content():
    with open('checkscam.txt', 'r', encoding='utf-8') as file:
        content = file.readlines()
    return content


@app.route('/')
def home():
    content = read_file_content()
    formatted_content = '<br>'.join(f"{index + 1}. {line}" for index, line in enumerate(content))
    return f"DANH SÁCH LINK FACEBOOK SCAM<br>{formatted_content}"


def read_debug_links():
    with open('debug_link.txt', 'r', encoding='utf-8') as file:
        links = file.readlines()
    return [link.strip() for link in links]


def convert_percent_encoded_to_unicode(text):
    decoded_text = urllib.parse.unquote(text)
    return decoded_text


def check_link_status(link):
    try:
        response = requests.get(link)
        if '<link rel="alternate" hreflang="x-default" href="https://www.facebook.com/' in response.text:
            href_start = response.text.find('<link rel="alternate" hreflang="x-default" href="') + len(
                '<link rel="alternate" hreflang="x-default" href="')
            href_end = response.text.find('"', href_start)
            href_content = response.text[href_start:href_end]
            style = 'green'
            # Kiểm tra trong response.text có <meta name="description" content=" hay không
            if '<meta name="description" content="' in response.text:
                meta_start = response.text.find('<meta name="description" content="') + len(
                    '<meta name="description" content="')
                meta_end = response.text.find('&#x111', meta_start)
                name = response.text[meta_start:meta_end]
            else:
                name = ''
            return href_content, name, style
        elif '<html lang="vi" id="facebook" class="no_js">' in response.text:
            # Trả về style màu đỏ
            style = 'red'
            return '','', style
        return ''
    except requests.exceptions.RequestException:
        return ''


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


@app.route('/status')
def status():
    debug_links = read_debug_links()
    result = []
    for link in debug_links:
        status, name, style = check_link_status(link)
        print(status)
        if status.startswith('https://www.facebook.com/'):
            name = convert_percent_encoded_to_unicode(name)
            result.append({'status': status, 'name': name, 'style': style})
        if status == '':
            status = link
            result.append({'status': status, 'name': "Unknown", 'style': style})
    formatted_content = '<br>'.join(
        f'<span style="color: {item["style"]}">{index + 1}. {item["name"]} ----> {item["status"]}  </span>'
        for index, item in enumerate(result)
    )
    return f"THÔNG TIN VỀ TÌNH TRẠNG HOẠT ĐỘNG<br>{formatted_content}"


if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
    app.run(debug=True)
