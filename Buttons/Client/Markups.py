from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# Menu
btnProfile = KeyboardButton("Личный кабинет")
btnMagazin = KeyboardButton("Магазин")
btnBucket = KeyboardButton("Корзина")
btnContact = KeyboardButton("Контакты")

mainMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
mainMenu.add(btnProfile, btnMagazin, btnBucket, btnContact)