import os
import json

from io import BytesIO
from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer


class ServerHandler(BaseHTTPRequestHandler): # класс запуска сервера
    def do_GET(self): # метод, передающий, что то после запроса
        print(os.curdir)
        print("GET request, Path:", self.path)
        if self.path.endswith(".png"):
            self.send_response(200)
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            with open(os.curdir + os.sep + "assets" + os.sep + os.sep + self.path, 'rb') as file:
                self.wfile.write(file.read())
        elif self.path.endswith(".css"):
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            with open(os.curdir + os.sep + "assets" + os.sep + self.path, 'rb') as file:
                self.wfile.write(file.read())

        elif list_of_pages("pages", self.path):  # если запрос прошел проверку в функции
            self.send_response(200)  # приуспешном соединении отправит код 200
            self.send_header('Content-type', 'text/html')  # HHTP заголовки, которые будут записаны в выходной поток
            self.end_headers()  # добавляет пустую строку (обозначающую конец заголовков HTTP в ответе) в буфер заголовков
            self.wfile.write(string_of_bytes_from_html(self.path))  # cодержит поток вывода для обратной записи ответа клиен

        else:
            self.send_error(404, "Page Not Found {}".format(self.path)) #в случае ошибки отправить код с текстом об ошибке

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        params = json.loads(urlparse(body).path.decode("utf-8"))
        print(params)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())


def server_thread(server_port):
    server_address = ('', server_port)
    httpd = HTTPServer(server_address, ServerHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

def list_of_pages(directory, path): # функция проверки содержимого запроса
    directory = os.listdir(directory)
    if path[path.find("/") + 1:] in directory or path == "/": # если в теле запроса есть имя страницы из паки Pages или слеш
        return True  # возвращаем правду
    else:
        return False

def string_of_bytes_from_html(reqest):
    file_name = reqest[reqest.find("/") + 1:]  # срезаем строку запроса от слеша
    if file_name == "":  # если получаем пустую строку в переменную загружаем имя главной страницы
        file_name = "index.html"
    with open(os.curdir + os.sep + "pages" + os.sep + file_name, 'rb') as file:
        string_of_bytes = b''.join(file.readlines())
        return string_of_bytes

if __name__ == '__main__':
    port = 8080
    print("Starting server at port %d" % port)
    server_thread(port)
