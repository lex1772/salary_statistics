import os

import motor.motor_asyncio
from dotenv import load_dotenv, find_dotenv

# Загрузка файла .env с автоматическим поиском
load_dotenv(find_dotenv())


# Данные для соединения с базой данных
MONGO_DETAILS = os.getenv("MONGO")

# Подключение к базе данных
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

# Определяем базу данных
database = client.salary

# Определяем коллекции базы данных
salary_collection = database.get_collection("salary")
