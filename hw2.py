import os
import json
import hashlib
from collections.abc import Iterable


class Country:
    def __init__(self, country_data):
        self._data = country_data
        for attr, attr_data in country_data.items():
            setattr(self, attr, attr_data)
        if hasattr(self, 'name'):
            common_name = self.name.get('common')
            self.link = ''.join(['https://en.wikipedia.org/wiki/', common_name])

    def __str__(self):
        return '{} - {}'.format(self.name['common'], self.link)


class ListIterator(Iterable):

    def __init__(self, list_data, cursor=-1):
        self._list_data = list_data
        self._cursor = cursor

    def __next__(self):
        if self._cursor + 1 >= len(self._list_data):
            raise StopIteration
        self._cursor += 1
        return self._list_data[self._cursor]

    def __iter__(self):
        for item in self._list_data:
            yield item


class CountryIterator(ListIterator):

    def __iter__(self):
        for item in self._list_data:
            yield Country(item)


def country_generator(list_data):
    return (Country(item) for item in list_data)


def file_generator(path_to_file):
    gen = None
    with open(path_to_file, 'rb') as f:
        lines = f.readlines()
        gen = (
            hashlib.md5(line).hexdigest() for line in lines)

    return gen


if __name__=='__main__':
    base_path = os.path.abspath('.')
    data_file_path = os.path.join(base_path, 'data', 'countries.json')
    data = None
    with open(data_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if data:
        print(' ITERATOR ----------------------------------------')
        c = CountryIterator(data)
        for country in c:
            print(country)
        print(' GENERATOR ----------------------------------------')
        c_gen = country_generator(list_data=data)
        for item in c_gen:
            print(item)
        print('------HASH-----------')
        hs = file_generator(data_file_path)
        for item in hs:
            print(item)