import asyncio
import json

from console import service

# Запуск программы с проверками на ошибки
if __name__ == "__main__":
    user_input = input("Введите запрос: ")
    try:
        user_input = json.loads(user_input)
    except json.decoder.JSONDecodeError:
        print(
            'Невалидный запрос. '
            'Пример запроса:\n{"dt_from": '
            '"2022-09-01T00:00:00", "dt_upto": '
            '"2022-12-31T23:59:00", "group_type": '
            '"month"}')
    else:
        try:
            func = getattr(service, user_input["group_type"])
        except AttributeError:
            print("Нет такой группировки")
        else:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            print(loop.run_until_complete(func(user_input)))
            loop.close()
