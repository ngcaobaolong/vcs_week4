from importlib.metadata import requires
import socket, re
import argparse
from helper import getResponseRaw

parser = argparse.ArgumentParser(description='Download file from server')
parser.add_argument('--url', action='store', dest = 'target_host', help='an url to get title', required=True)
parser.add_argument('--remote-file', action='store', dest = 'remote_file', help='an url to get image', required=True)
parser.usage = parser.format_help()
args = parser.parse_args()
target_port = 80  
target_host = args.target_host
remote_file = args.remote_file

# create a socket object 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
 
# connect the client 
client.connect((target_host,target_port))  
 
# send some data 
request = (
    f'GET {remote_file} HTTP/1.1\r\n'
    f'Host: {target_host}\r\n'
    'Pragma: no-cache\r\n'
    'Cache-Control: no-cache\r\n'
    'Upgrade-Insecure-Requests: 1\r\n'
    'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36\r\n'
    'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'
    'Accept-Encoding: gzip, deflate\r\n'
    'Accept-Language: en-US,en;q=0.9\r\n'
    'Connection: close\r\n\r\n'
)
client.send(request.encode())  
 
# receive some data 
# response = client.recv(4096)  
response = getResponseRaw(client,target_host,request)
if b"200 OK" in response:
    print("Image found")
    f = open(remote_file.split("/")[-1], "wb")
    i = 10
    a = response.split(b"\r\n")
    for i in range(10,len(a)):
        f.write(response.split(b"\r\n")[i]+b"\r\n")
else:
    print("Image not found")
