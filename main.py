import os
from work_files import Work_with_files
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

        elif Work_with_files.list_of_pages("pages", self.path):  # если запрос прошел проверку в функции
            self.send_response(200)  # приуспешном соединении отправит код 200
            self.send_header('Content-type', 'text/html')  # HHTP заголовки, которые будут записаны в выходной поток
            self.end_headers()  # добавляет пустую строку (обозначающую конец заголовков HTTP в ответе) в буфер заголовков
            self.wfile.write(Work_with_files.string_of_bytes_from_html(self.path))  # cодержит поток вывода для обратной записи ответа клиен

        else:
            self.send_error(404, "Page Not Found {}".format(self.path)) #в случае ошибки отправить код с текстом об ошибке

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # колличество символов, отправленых серверу
        body = self.rfile.read(content_length)  # тело запроса
        self.send_response(200)
        self.end_headers()
        d = body.decode('UTF-8')
        self.wfile.write(Work_with_files.date_of_post(d))


def server_thread(server_port):
    server_address = ('', server_port)
    httpd = HTTPServer(server_address, ServerHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

if __name__ == '__main__':
    port = 8080
    print("Starting server at port %d" % port)
    server_thread(port)
