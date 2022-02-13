from importlib.resources import path
import socket, re
import argparse
import magic
from helper import getCookieString,getResponse,updateCookieList,file_get_contents,post
from binascii import hexlify

target_host = ""
username = ""
password = ""
parser = argparse.ArgumentParser(description='User login')
parser.add_argument('--url', action='store', dest = 'target_host', help='url to login', required=True)
parser.add_argument('--username', action='store', dest = 'username', help='username to login', required=True)
parser.add_argument('--password', action='store', dest = 'password', help='password to login', required=True)
parser.add_argument('--file-path', action='store', dest = 'file_path', help='file path to upload', required=True)
parser.usage = parser.format_help()
args = parser.parse_args()

target_port = 80
target_host = args.target_host
username = args.username
password = args.password
file_path = args.file_path

mime = magic.Magic(mime=True)
file_content = file_get_contents(file_path, "rb")
# create a socket object 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
client.settimeout(0.5)
 
# connect the client 
client.connect((target_host,target_port))  
 
# send some data 
cookieList = ["wordpress_test_cookie=WP+Cookie+check"]
body = f'log={username}&pwd={password}&wp-submit=Log+in&testcookie=1'
# Log in

request = (
        f'POST /wp-login.php HTTP/1.1\r\n'
        f'Host: {target_host}\r\n'
        f'Content-Type: application/x-www-form-urlencoded\r\n'
        f'Content-Length: {len(body)}\r\n'
        f'Accept: text/html\r\n'
        f'Connection: keep-alive\r\n'
        f'Cookie: {getCookieString(cookieList)}\r\n'
        f'\r\n'
        f'{body}\r\n'
        f'\r\n'
)
response = getResponse(client, target_host, request)
updateCookieList(cookieList, response)
logInCookie = re.findall(r"Set-Cookie:( wordpress_logged_in.*?)[;|\r\n]", response)
if logInCookie:
    print("User test đăng nhập thành công")
else:
    print("User test đăng nhập thất bại")

# request the media page to find nonce
request = (
        f'GET /wp-admin/media-new.php HTTP/1.1\r\n'
        f'Host: {target_host}\r\n'
        f'Upgrade-Insecure-Requests: 1\r\n'
        f'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36\r\n'
        f'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'
        f'Cookie: {getCookieString(cookieList)}\r\n'
        f'Connection: close\r\n'
        f'\r\n'
        )
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
client.settimeout(10)
 
# connect the client 
client.connect((target_host,target_port))

response = getResponse(client, target_host, request)
# find nonce
test = re.search('"multipart_params":.*_wpnonce":"[0-9a-z]+"', response)
nonce = re.search('(?<=_wpnonce":")[0-9a-z]{10}', test.group(0))
nonce = nonce.group(0)
print(nonce)
file_name = file_path.split("\\")[-1]
body1 = (
        '------WebKitFormBoundaryHt2OjdVqVF0Xurbn\r\n'
        f'Content-Disposition: form-data; name="async-upload"; filename="{file_name}"\r\n'
        f'Content-Type: {mime.from_file(file_path)}\r\n\r\n')
        
body2 = ('\r\n'
        '------WebKitFormBoundaryHt2OjdVqVF0Xurbn\r\n'
        'Content-Disposition: form-data; name="html-upload"\r\n'
        '\r\n'
        'Upload\r\n'
        '------WebKitFormBoundaryHt2OjdVqVF0Xurbn\r\n'
        'Content-Disposition: form-data; name="post_id"\r\n'
        '\r\n'
        '0\r\n'
        '------WebKitFormBoundaryHt2OjdVqVF0Xurbn\r\n'
        'Content-Disposition: form-data; name="_wpnonce"\r\n'
        '\r\n'
        f'{nonce}\r\n'
        '------WebKitFormBoundaryHt2OjdVqVF0Xurbn\r\n'
        'Content-Disposition: form-data; name="_wp_http_referer"\r\n'
        '\r\n'
        '/wp-admin/media-new.php\r\n'
        '------WebKitFormBoundaryHt2OjdVqVF0Xurbn--\r\n'
)
body = b''.join([body1.encode(),file_content,body2.encode()])
request = (
        'POST /wp-admin/media-new.php HTTP/1.1\r\n'
        f'Host: {target_host}\r\n'
        'Cache-Control: max-age=0\r\n'
        f'Content-Length: {len(body)}\r\n'
        'Upgrade-Insecure-Requests: 1\r\n'
        'Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryHt2OjdVqVF0Xurbn\r\n'
        'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36\r\n'
        'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'
        'Accept-Encoding: gzip, deflate\r\n'
        'Accept-Language: en-US,en;q=0.9\r\n'
        f'Cookie: {getCookieString(cookieList)}\r\n'
        'Connection: close\r\n\r\n'
)
request = b''.join([request.encode(),body])

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
client.settimeout(0.5)
 
# connect the client 
client.connect((target_host,target_port))
response = post(client, target_host, request)
