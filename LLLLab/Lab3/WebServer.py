# Python Version: Python 3.7
# Port: 12345

import socket
import os

host = 'localhost'
port = 12345

html_response_header = '''HTTP/1.1 200 OK
Content-Type: text/html

'''
image_response_header = '''HTTP/1.1 200 OK
Content-Type: image/png

'''
response_body = ''
response = ''.encode(encoding='utf-8')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(100)

LineSeparator = '\r\n\r\n'

print('The server is running')


def get_headers(request):
    headers_arr = request.split('\r\n')
    headers = {}
    for item__ in headers_arr[1:]:
        item_ = item__.split(': ')
        headers[item_[0]] = item_[1]
    return headers


while True:
    connection, address = s.accept()
    request = connection.recv(1024).decode(encoding='utf-8')
    request_text = request.split(LineSeparator)
    request_header = request_text[0]
    request_body = request_text[1]
    method = request_header.split(' ')[0]
    src = request_header.split(' ')[1]
    response_body = ''
    response = ''.encode(encoding='utf-8')

    print('Connect by:', address)
    print('Request is:\n', request_text)

    if method == 'GET':
        flag = src.split('.')[-1]
        if flag == 'html':
            if os.path.exists(src.split('/')[1]):
                print("success to find this html\n")
                res = open('.' + src, 'rb')
                html_file = res.read()
                response += (html_response_header.encode(encoding='utf-8'))
                response += (response_body.encode(encoding='utf-8') + html_file)
                res.close()
            else:
                print("error:404 not found\n")
                res = open('404.html', 'rb')
                error_file = res.read()
                response += (html_response_header.encode(encoding='utf-8'))
                response += (response_body.encode(encoding='utf-8') + error_file)
                res.close()
        elif flag == 'png':
            print(f'src is {src}\n')
            if os.path.exists(src.split('/')[1]):
                print("success to find this image\n")
                res = open('.' + src, 'rb')
                image_file = res.read()
                response += (image_response_header.encode(encoding='utf-8'))
                response += (response_body.encode(encoding='utf-8') + image_file)
                res.close()
            else:
                print("error:404 not found\n")
                res = open('404.html', 'rb')
                error_file = res.read()
                response += (html_response_header.encode(encoding='utf-8'))
                response += (response_body.encode(encoding='utf-8') + error_file)
                res.close()
        else:
            continue

    connection.sendall(response)
    connection.close()
