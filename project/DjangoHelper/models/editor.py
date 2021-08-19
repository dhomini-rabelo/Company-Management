from pathlib import Path
from support import *
from django_class import DjangoBase
import io


class Editor(DjangoBase):
    def __init__(self, base_path: str, archive_path: str):
        self.base_path = self.adapt_path(base_path)
        self.archive_path = self.adapt_path(archive_path)
        self.path = f'{self.base_path}/{self.archive_path}'
        assert_file_existence(self.path)
        
    def reading(self, reading):
        if reading is None:
            return self.read(self.path)
        else:
            return reading
        
    def replace_code(self, current: str, new: str, reading: list = None):
        reading = self.reading(reading)
        print(reading)
        for line in reading:
            if line.startswith(current):
                pos = reading.index(line) # position
                reading[pos] = f'{new}\n'
                return reading
        return reading
        
        
    def get_line(self, code_line: str, reading: list = None):
        reading = self.reading(reading)
        for line in reading:
            if line.startswith(code_line):
                pos = reading.index(line) # position
                return pos
    
    def add_in_line(self, line_code, new: str, reading: list = None):
        reading = self.reading(reading)
        number_line = self.get_line(line_code) if isinstance(reading, str) else line_code
        if number_line is not None:
            current_line = reading[number_line][:-2]
            reading[number_line] = f'{current_line}{new}\n'
        return reading
        
        
    def insert_code(self, line: int, new: str, reading: list = None):
        reading = self.reading(reading)
        reading.insert(line, f'{new}\n')
        return reading
        
    def insert_comment(self, line:int, comment: str, reading: list = None):
        reading = self.reading(reading)
        reading.insert(line, f'# {comment}\n')
        return reading
        
    def update(self, reading: list):
        if check_null(reading):
            return
        print(reading)
        with io.open(self.path, mode='w', encoding='utf-8') as code_file:
            start = 1 if reading[0] == '\n' else 0
            for line in reading[start:]:
                code_file.write(line)
                
