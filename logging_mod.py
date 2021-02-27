from reusepatterns.singletones import Singleton
import time
import os


class ConsoleWriter:

    def write(self, text):
        print(text)


class FileWriter:

    def __init__(self, file_name):
        self.file_name = file_name

    def write(self, text):
        with open(f'{os.getcwd()}/log/{self.file_name}', 'a', encoding='utf-8') as f:
            f.write(f'{text}\n')


class Logger(metaclass=Singleton):

    def __init__(self, name, writer=ConsoleWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        text = f'log---->{text}'
        self.writer.write(text) 

def debug(func):
    def inner(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print('DEBUG------->', func.__name__, end - start)
        return result
    return inner