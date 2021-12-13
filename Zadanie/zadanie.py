#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import jsonschema


def select(line, flights, nom):
    """Выбор рейсов по типу самолёта"""
    count = 0
    print(line)
    print(
        '| {:^4} | {:^20} | {:^15} | {:^16} |'.format(
            "№",
            "Место прибытия",
            "Номер самолёта",
            "Тип"))
    print(line)
    for i, num in enumerate(flights, 1):
        if nom.upper() == num.get('value', ''):
            count += 1
            print(
                '| {:<4} | {:<20} | {:<15} | {:<16} |'.format(
                    count,
                    num.get('stay', ''),
                    num.get('number', ''),
                    num.get('value', 0)))
    print(line)


def table(line, flights):
    """Вывод скиска рейсов"""
    print(line)
    print(
        '| {:^4} | {:^20} | {:^15} | {:^16} |'.format(
            "№",
            "Место прибытия",
            "Номер самолёта",
            "Тип"))
    print(line)
    for i, num in enumerate(flights, 1):
        print(
            '| {:<4} | {:<20} | {:<15} | {:<16} |'.format(
                i,
                num.get('stay', ''),
                num.get('number', ''),
                num.get('value', 0)
            )
        )
    print(line)


def add(flights):
    """Добавление нового рейса"""
    value = input('Введите тип самолёта: ').upper()
    number = input('Введите номер самолёта: ').upper()
    stay = input('Введите место прибытия: ').upper()
    air = {
        'number': number,
        'stay': stay,
        'value': value
    }
    flights.append(air)
    if len(flights) > 1:
        flights.sort(key=lambda x: x.get('stay', ''))


def saving(file_name, flights):
    with open('json/'+file_name, "w", encoding="utf-8") as file_out:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        print("Файл сохранён")
        json.dump(flights, file_out, ensure_ascii=False, indent=4)


def opening(file_name):
    """Загрузить всех работников из файла JSON."""
    # Открыть файл с заданным именем для чтения.
    with open('json/'+file_name, "r", encoding="utf-8") as f_in:
        file = json.load(f_in)
        print("Файл загружен")
        with open('json/check.json') as check:
            schema = json.load(check)
            validator = jsonschema.Draft7Validator(schema)
            try:
                if not validator.validate(file):
                    print("Нет ошибок валидации")
            except jsonschema.exceptions.ValidationError:
                print("Ошибка валидации", list(validator.iter_errors(file)))
                exit()
        return file


def main():
    flights = []
    print('Список комманд: \n exit - Завершить работу'
          ' \n add - Добавить рейс \n'
          ' list - Показать список рейсов'
          ' \n select - Выбрать рейсы по типу самолёте\n'
          'save - Сохранить изменения в файле\n'
          'load - Загрузить файл')
    line = '+-{}-+-{}-+-{}-+-{}-+'.format(
        '-' * 4,
        '-' * 20,
        '-' * 15,
        '-' * 16
    )
    while True:
        com = input('Введите команду: ').lower()
        if com == 'exit':
            break
        elif com == "add":
            add(flights)
        elif com == 'list':
            table(line, flights)
        elif com.startswith('select '):
            part = com.split(maxsplit=1)
            select(line, flights, part[1])
        elif com.startswith("save "):
            # Разбить команду на части для выделения имени файла.
            parts = com.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]
            # Сохранить данные в файл с заданным именем.
            saving(file_name, flights)
        elif com.startswith("load "):
            # Разбить команду на части для выделения имени файла.
            parts = com.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]
            # Сохранить данные в файл с заданным именем.
            flights = opening(file_name)
        else:
            print(f"Неизвестная команда {com}", file=sys.stderr)


if __name__ == '__main__':
    main()
