import  requests
from flask import Flask, request, jsonify, json
import urllib.request


import urllib.parse
app = Flask(__name__)
# cookie_json = """
# [
#     {
#         "domain": ".facebook.com",
#         "expirationDate": 1724033786.268623,
#         "hostOnly": false,
#         "httpOnly": true,
#         "name": "datr",
#         "path": "/",
#         "sameSite": "no_restriction",
#         "secure": true,
#         "session": false,
#         "storeId": null,
#         "value": "fVMHZPVsvIum8AWajr7hvGG8"
#     },
#     {
#         "domain": ".facebook.com",
#         "expirationDate": 1720969492,
#         "hostOnly": false,
#         "httpOnly": false,
#         "name": "fbl_ci",
#         "path": "/",
#         "sameSite": "no_restriction",
#         "secure": true,
#         "session": false,
#         "storeId": null,
#         "value": "988100872341208"
#     },
#     {
#         "domain": ".facebook.com",
#         "expirationDate": 1697520799.799278,
#         "hostOnly": false,
#         "httpOnly": true,
#         "name": "fr",
#         "path": "/",
#         "sameSite": "no_restriction",
#         "secure": true,
#         "session": false,
#         "storeId": null,
#         "value": "0vw96Fn1BTWbCA6PF.AWXHfoniOH4q-SC9ZRJ4Kvxurl4.Bkt3Wh.SA.AAA.0.0.Bkt3Wh.AWVL-FU-QOQ"
#     },
#     {
#         "domain": ".www.facebook.com",
#         "expirationDate": 1724304066,
#         "hostOnly": false,
#         "httpOnly": false,
#         "name": "m_ls",
#         "path": "/",
#         "sameSite": "no_restriction",
#         "secure": true,
#         "session": false,
#         "storeId": null,
#         "value": "%7B%22c%22%3A%7B%221%22%3A%22HCwAABaYihQW6KKx2w0TBRaS-5e5ir8tAA%22%2C%222%22%3A%22GSwVQBxMAAAWRhbk1eDKDBYAABV-HEwAABaCAhbq1eDKDBYAABYoAA%22%2C%2295%22%3A%22HCwAABbGBBaetZD1CxMFFpL7l7mKvy0A%22%7D%2C%22d%22%3A%22d145873d-e826-44aa-8f48-ea5b635ce9e4%22%2C%22s%22%3A%221%22%2C%22u%22%3A%22ywmwc8%22%7D"
#     },
#     {
#         "domain": ".facebook.com",
#         "expirationDate": 1721280800.799265,
#         "hostOnly": false,
#         "httpOnly": true,
#         "name": "xs",
#         "path": "/",
#         "sameSite": "no_restriction",
#         "secure": true,
#         "session": false,
#         "storeId": null,
#         "value": "7%3ADYNAMiFLjB9pmw%3A2%3A1678209186%3A-1%3A14929%3A%3AAcVfQhCh31nZ0yq_z7V4q-RKxZt2GBHQhGV2clN_O7Dw"
#     },
#     {
#         "domain": ".facebook.com",
#         "expirationDate": 1720969492,
#         "hostOnly": false,
#         "httpOnly": false,
#         "name": "fbl_st",
#         "path": "/",
#         "sameSite": "strict",
#         "secure": true,
#         "session": false,
#         "storeId": null,
#         "value": "100434730%3BT%3A28157224"
#     },
#     {
#         "domain": ".facebook.com",
#         "expirationDate": 1690038291.96528,
#         "hostOnly": false,
#         "httpOnly": false,
#         "name": "locale",
#         "path": "/",
#         "sameSite": "no_restriction",
#         "secure": true,
#         "session": false,
#         "storeId": null,
#         "value": "vi_VN"
#     },
#     {
#         "domain": ".facebook.com",
#         "expirationDate": 1721280800.799217,
#         "hostOnly": false,
#         "httpOnly": false,
#         "name": "c_user",
#         "path": "/",
#         "sameSite": "no_restriction",
#         "secure": true,
#         "session": false,
#         "storeId": null,
#         "value": "100039780400841"
#     },
#     {
#         "domain": ".facebook.com",
#         "hostOnly": false,
#         "httpOnly": false,
#         "name": "presence",
#         "path": "/",
#         "sameSite": null,
#         "secure": true,
#         "session": true,
#         "storeId": null,
#         "value": "C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1689744088561%2C%22v%22%3A1%7D"
#     },
#     {
#         "domain": ".facebook.com",
#         "expirationDate": 1690348891,
#         "hostOnly": false,
#         "httpOnly": false,
#         "name": "dpr",
#         "path": "/",
#         "sameSite": "no_restriction",
#         "secure": true,
#         "session": false,
#         "storeId": null,
#         "value": "0.8999999761581421"
#     },
#     {
#         "domain": ".facebook.com",
#         "expirationDate": 1720969492,
#         "hostOnly": false,
#         "httpOnly": false,
#         "name": "fbl_cs",
#         "path": "/",
#         "sameSite": "no_restriction",
#         "secure": true,
#         "session": false,
#         "storeId": null,
#         "value": "AhDpAnD8XOY%2BQ1mdFTCpIT8gGE1laHBxQmdjbGw2cmJWK2tOc1dyeUltaw"
#     },
#     {
#         "domain": ".facebook.com",
#         "expirationDate": 1697217896.73501,
#         "hostOnly": false,
#         "httpOnly": true,
#         "name": "m_page_voice",
#         "path": "/",
#         "sameSite": "no_restriction",
#         "secure": true,
#         "session": false,
#         "storeId": null,
#         "value": "100039780400841"
#     },
#     {
#         "domain": ".facebook.com",
#         "expirationDate": 1712769188.565503,
#         "hostOnly": false,
#         "httpOnly": true,
#         "name": "sb",
#         "path": "/",
#         "sameSite": "no_restriction",
#         "secure": true,
#         "session": false,
#         "storeId": null,
#         "value": "fVMHZKbd29ShKlbgk9C57LkB"
#     },
#     {
#         "domain": ".facebook.com",
#         "expirationDate": 1690348888,
#         "hostOnly": false,
#         "httpOnly": false,
#         "name": "wd",
#         "path": "/",
#         "sameSite": "lax",
#         "secure": true,
#         "session": false,
#         "storeId": null,
#         "value": "1728x912"
#     },
#     {
#         "domain": ".facebook.com",
#         "expirationDate": 1697209492,
#         "hostOnly": false,
#         "httpOnly": false,
#         "name": "wl_cbv",
#         "path": "/",
#         "sameSite": "no_restriction",
#         "secure": true,
#         "session": false,
#         "storeId": null,
#         "value": "v2%3Bclient_version%3A2288%3Btimestamp%3A1689433491"
#     }
# ]
# """
#
# # cookies = {
# #     "datr": "wZytZJ4b0WxLNY0zfsMeEQEW",
# #     "fr" : "0FcrbPUqDxLrE4pRf.AWX7bJ0arCiSjVLxF_22v39R06U.BktogL.0g.AAA.0.0.BktpV1.AWX_J23UJvI",
# #     "xs" : "40%3AfmcgtJoVddrtkw%3A2%3A1689099584%3A-1%3A13332%3A%3AAcWTtJ11-eeU-7_AkXJnrYETwPMnVF_8lMURg6rvTks",
# #     "fr" : "0FcrbPUqDxLrE4pRf.AWX7bJ0arCiSjVLxF_22v39R06U.BktogL.0g.AAA.0.0.BktpV1.AWX_J23UJvI",
# #     "fr" : "0FcrbPUqDxLrE4pRf.AWX7bJ0arCiSjVLxF_22v39R06U.BktogL.0g.AAA.0.0.BktpV1.AWX_J23UJvI",
# #     "fr" : "0FcrbPUqDxLrE4pRf.AWX7bJ0arCiSjVLxF_22v39R06U.BktogL.0g.AAA.0.0.BktpV1.AWX_J23UJvI",
# #     "fr" : "0FcrbPUqDxLrE4pRf.AWX7bJ0arCiSjVLxF_22v39R06U.BktogL.0g.AAA.0.0.BktpV1.AWX_J23UJvI",
# #     "fr" : "0FcrbPUqDxLrE4pRf.AWX7bJ0arCiSjVLxF_22v39R06U.BktogL.0g.AAA.0.0.BktpV1.AWX_J23UJvI",
# #     "fr" : "0FcrbPUqDxLrE4pRf.AWX7bJ0arCiSjVLxF_22v39R06U.BktogL.0g.AAA.0.0.BktpV1.AWX_J23UJvI"
# #
# # }
#
# def convert_json_to_cookie(cookie_json):
#     # Chuyển đổi đoạn mã JSON thành dạng cookie của requests
#     cookies = {}
#     for cookie in json.loads(cookie_json):
#         cookies[cookie["name"]] = cookie["value"]
#     return cookies
#
#     # Chuyển đoạn mã JSON thành dạng cookie của requests
# cookies = convert_json_to_cookie(cookie_json)

    # Thực hiện yêu cầu GET với các cookie đã có
response = requests.get("https://www.facebook.com/profile.php?id=100090937081290&__tn__=-UK*F")
# response = urllib.request.urlopen('')
# html_content = response.read().decode('utf-8')
print(response.text)
