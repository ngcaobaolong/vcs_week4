import socket, re
import argparse
from helper import getResponse

parser = argparse.ArgumentParser(description='Get website title')

parser.add_argument('--url', action='store', dest = 'target_host', help='an url to get title', required=True)
parser.usage = parser.format_help()
args = parser.parse_args()
target_port = 80  
target_host = args.target_host


# create a socket object 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
 
# connect the client 
client.connect((target_host,target_port))  
 
# send some data 
request = "GET / HTTP/1.1\r\nHost:%s\r\n\r\n" % target_host
client.send(request.encode())  
 
# receive some data 
# response = client.recv(4096)  
response = getResponse(client,target_host,request)

#display the title
title = re.findall("<title>(.*)</title>", response)[0]
print("Page title: " + title)