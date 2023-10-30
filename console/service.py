from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta

from database.database import salary_collection


# Поиск данных в базе
async def find_data(user_input: dict):
    try:
        data = await salary_collection.find(
            {"dt": {
                "$gte": datetime.fromisoformat(
                    user_input["dt_from"]),
                "$lte": datetime.fromisoformat(
                    user_input["dt_upto"])}}).to_list(
            None)
    except ValueError:
        return False
    return data


# Функция агрегации статистических данных помесячно
async def month(user_input):
    list_salary = []
    list_date = []
    data_list = await find_data(user_input)
    months = (
            datetime.fromisoformat(
                user_input["dt_upto"]).month -
            datetime.fromisoformat(user_input["dt_from"]).month)
    for month in range(0, months + 1):
        dt_month = datetime.fromisoformat(
            user_input["dt_from"][:10]) + relativedelta(months=month)
        list_date.append(dt_month.isoformat())
        list_salary.append(sum([month['value'] for month in data_list if
                                (month[
                                     "dt"
                                 ].month == dt_month.month and
                                 month["dt"].year == dt_month.year)]))
    return {"dataset": list_salary, "labels": list_date}


# Функция агрегации статистических данных ежедневно
async def day(user_input):
    list_salary = []
    list_date = []
    data_list = await find_data(user_input)
    dt = (datetime.fromisoformat(user_input[
                                     "dt_upto"
                                 ]) - datetime.fromisoformat(
        user_input["dt_from"]))
    for day in range(0, int(dt.days) + 1):
        dt_day = datetime.fromisoformat(user_input[
                                            "dt_from"
                                        ][:10]) + timedelta(days=day)
        list_date.append(dt_day.isoformat())
        list_salary.append(sum([day['value'] for day in data_list if (
                day["dt"].day == dt_day.day and
                day["dt"].month == dt_day.month and
                day["dt"].year == dt_day.year)]))
    return {"dataset": list_salary, "labels": list_date}


# Функция агрегации статистических данных почасово
async def hour(user_input):
    list_salary = []
    list_date = []
    data_list = await find_data(user_input)
    if not data_list:
        return print("Не верно выбран тип данных")
    else:
        days = (datetime.fromisoformat(user_input[
                                           "dt_upto"]
                                       ).day -
                datetime.fromisoformat(user_input["dt_from"]).day)
        hours = (datetime.fromisoformat(user_input[
                                            "dt_upto"]
                                        ).hour -
                 datetime.fromisoformat(user_input["dt_from"]).hour)
        all_hours = days * 24 + hours
        for hour in range(0, all_hours + 1):
            dt_hours = datetime.fromisoformat(user_input[
                                                  "dt_from"
                                              ][:10]) + timedelta(hours=hour)
            list_date.append(dt_hours.isoformat())
            list_salary.append(sum([hour['value'] for hour in data_list if (
                    hour["dt"].day == dt_hours.day and
                    hour["dt"].month == dt_hours.month and
                    hour["dt"].year == dt_hours.year and
                    hour["dt"].hour == dt_hours.hour)]))
        return {"dataset": list_salary, "labels": list_date}
