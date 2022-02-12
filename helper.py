import re
def getResponse(sck, host, request):
    sck.send(request.encode())         
    response = ""
    while True:
        try:
            data = sck.recv(2048)
            if not data:
                break
        except socket.timeout:
            break
        response += data.decode()
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