import re,socket
def getResponse(sck, host, request):
    sck.sendall(request.encode())         
    response = ""
    while True:
        try:
            data = sck.recv(2048)
            if not data:
                break
        except socket.timeout:
            break
        # print(data)
        response += data.decode()
    sck.shutdown(socket.SHUT_RDWR)
    sck.close()
    return response

def getResponseRaw(sck, host, request):
    sck.sendall(request.encode())         
    response = b""
    while True:
        try:
            data = sck.recv(2048)
            if not data:
                break
        except socket.timeout:
            break
        # print(data)
        response += data
    sck.shutdown(socket.SHUT_RDWR)
    sck.close()
    return response

def post(sck,host,request):
    sck.sendall(request)         
    response = ""
    while True:
        try:
            data = sck.recv(2048)
            if not data:
                break
        except socket.timeout:
            break
        response += data.decode()
    sck.shutdown(socket.SHUT_RDWR)
    sck.close()
    return response

def getCookieString(listCookie):
    cookieString = ""
    for cookie in listCookie:
        cookieString += cookie + '; '
    cookieString = cookieString[:-2]
    return cookieString

def updateCookieList(cookieList, response):
    newCookies = re.findall(r"Set-Cookie: (.*?)[;|\r\n]", response)
    for cookie in newCookies:
        if cookie not in cookieList:
            cookieList.append(cookie)
    if not newCookies:
        return 0
    else:
        return 1

def file_get_contents(filename, mod):
    with open(filename, mode=mod) as f:
        return f.read()
