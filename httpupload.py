import socket, re
import argparse
from helper import getCookieString,getResponse,updateCookieList

target_host = ""
username = ""
password = ""
parser = argparse.ArgumentParser(description='User login')
parser.add_argument('--url', action='store', dest = 'target_host', help='url to login', required=True)
parser.add_argument('--username', action='store', dest = 'username', help='username to login', required=True)
parser.add_argument('--password', action='store', dest = 'password', help='password to login', required=True)

parser.usage = parser.format_help()
args = parser.parse_args()

target_port = 80
target_host = args.target_host
username = args.username
password = args.password
# create a socket object 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
 
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
)
response = getResponse(client, target_host, request)
updateCookieList(cookieList, response)

# Check if logged in
logInCookie = re.findall(r"Set-Cookie:( wordpress_logged_in.*?)[;|\r\n]", response)
if logInCookie:
    print("User test đăng nhập thành công")
else:
    print("User test đăng nhập thất bại")
    sys.exit(0)