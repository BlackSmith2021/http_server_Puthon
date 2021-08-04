import os
from jinja2 import Environment, FileSystemLoader


class Work_with_files: # класс для работа с файлами
    def string_of_bytes_from_html(reqest): # функция для обработки данных GET запроса и кодировки страний в байты
        file_name = reqest[reqest.find("/") + 1:]  # срезаем строку запроса от слеша
        if file_name == "":  # если получаем пустую строку в переменную загружаем имя главной страницы
            file_name = "index.html"
        with open(os.curdir + os.sep + "pages" + os.sep + file_name, 'rb') as file:
            string_of_bytes = b''.join(file.readlines())
            return string_of_bytes

    def list_of_pages(directory, path):  # функция проверки содержимого GET запроса
        directory = os.listdir(directory)
        if path[path.find(
                "/") + 1:] in directory or path == "/":  # если в теле запроса есть имя страницы из паки Pages или слеш
            return True  # возвращаем правду
        else:
            return False

    def date_of_post(req): # функция добавления на страницу test_post.html данных отправленных с помощью POST
        change_req = req[req.find("=") + 1:] # получение чистах данных, отправленных в форме
        env = Environment(loader=FileSystemLoader('pages')) # jina загрузчик указывающий на папку в которой лежит редактируемая страница
        template = env.get_template('test_post.html')  # создание обьекта для редактирования
        result = bytes(template.render(req=change_req), 'UTF-8')  # добавление переменной на страницу, кодировка страницы в байты
        return result
