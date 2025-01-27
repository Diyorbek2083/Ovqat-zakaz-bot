import asyncio
from aiogram import Dispatcher, Bot
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.State import Start
from handlers.Admin_User import admin_router, user_router 
from data.databaza import AdminQoshish, Adminlar, Userlar, UserQoshish
from botun.Buttons import AdminButton, UserButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

teken = '7738866089:AAFALZGGXK7RlTWaAZt47EjSNUuuEPseSZA'

bot = Bot(token=teken)
dp = Dispatcher()

dp.include_router(admin_router)
dp.include_router(user_router)

@dp.message(Command('start'))
async def StartBot(message:Message,state:FSMContext):
    id = message.from_user.id
    print(id)
    if id in Adminlar():
        await message.answer(text=f"Assalomu aleykum {message.from_user.first_name}.\nSiz adminsiz", reply_markup=AdminButton)
        await state.set_state(Start.admin)
    else:
        if id not in Userlar():
            UserQoshish(tg_id=id, name=message.from_user.first_name, user=message.from_user.username)
        if UserButton()==None:
            await message.answer(text=f"Assalomu aleykum {message.from_user.first_name} botimizga xush kelibsiz.\nBizda hali maxsulotlar yo'q iltimos keyinroq qayta /start bering‼️")
        else:
            await message.answer_photo(photo='AgACAgIAAxkBAANhZ3I9OPow2mySc-ahVi7srTQNfisAApTvMRsdM5FLB6vL02jeczoBAAMCAANtAAM2BA' ,caption=f"Assalomu aleykum {message.from_user.first_name} botimizga xush kelibsiz.", reply_markup=UserButton())
            await state.set_state(Start.user)
    await message.delete()

async def main():
    await dp.start_polling(bot)

try:
    asyncio.run(main())
except Exception as e:
    print('Tugadi!', e)





##################################################################################################################################################################################




# import telebot
# from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# TOKEN = '7738866089:AAFALZGGXK7RlTWaAZt47EjSNUuuEPseSZA'
# bot = telebot.TeleBot(TOKEN)

# # Kommentlar ma'lumotlari
# comments = [
#     {"username": "User1", "text": "Bu birinchi komment."},
#     {"username": "User2", "text": "Ikkinchi komment."},
#     {"username": "User3", "text": "Uchinchi komment."},
#     {"username": "User4", "text": "To‘rtinchi komment."},
#     {"username": "User5", "text": "Beshinchi komment."},
# ]

# # Kommentni ko'rsatish funksiyasi
# def get_comment_page(page_number):
#     comment = comments[page_number]
#     markup = InlineKeyboardMarkup()
    
#     # Tugmalar
#     navigation_buttons = []
#     if page_number > 0:
#         navigation_buttons.append(InlineKeyboardButton("⬅️ Oldingi", callback_data=f"comment:{page_number-1}"))
#     if page_number < len(comments) - 1:
#         navigation_buttons.append(InlineKeyboardButton("Keyingi ➡️", callback_data=f"comment:{page_number+1}"))
    
#     # Ortga va o'qish tugmalari
#     markup.add(InlineKeyboardButton("Ortga qaytish", callback_data="back"))
#     markup.add(InlineKeyboardButton("📝 Kommentni o'qish", callback_data=f"read:{page_number}"))
#     if navigation_buttons:
#         markup.row(*navigation_buttons)
    
#     return f"Komment yozgan: {comment['username']}", markup

# # Boshlang'ich xabar
# @bot.message_handler(commands=['start'])
# def start(message):
#     markup = InlineKeyboardMarkup()
#     markup.add(InlineKeyboardButton("📝 Kommentlar", callback_data="comments"))
#     bot.send_message(message.chat.id, "Bo'limni tanlang:", reply_markup=markup)

# # Callbackni boshqarish
# @bot.callback_query_handler(func=lambda call: True)
# def callback(call):
#     if call.data == "comments":
#         # Birinchi kommentni ko'rsatish
#         text, markup = get_comment_page(0)
#         bot.edit_message_text(text, 
#                               chat_id=call.message.chat.id, 
#                               message_id=call.message.message_id, 
#                               reply_markup=markup)
#     elif call.data.startswith("comment:"):
#         # Sahifani o'zgartirish
#         page_number = int(call.data.split(":")[1])
#         text, markup = get_comment_page(page_number)
#         bot.edit_message_text(text, 
#                               chat_id=call.message.chat.id, 
#                               message_id=call.message.message_id, 
#                               reply_markup=markup)
#     elif call.data.startswith("read:"):
#         # Kommentni o'qish
#         page_number = int(call.data.split(":")[1])
#         comment = comments[page_number]
#         bot.answer_callback_query(call.id, f"Komment: {comment['text']}")
#     elif call.data == "back":
#         # Ortga qaytish
#         markup = InlineKeyboardMarkup()
#         markup.add(InlineKeyboardButton("📝 Kommentlar", callback_data="comments"))
#         bot.edit_message_text("Bo'limni tanlang:", 
#                               chat_id=call.message.chat.id, 
#                               message_id=call.message.message_id, 
#                               reply_markup=markup)

# bot.polling()



##################################################################################################################################################################################



# import telebot
# from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# TOKEN = '7738866089:AAFWe0AtLH_bQRmhgd_PTPiYLlSwI7twvDU'
# bot = telebot.TeleBot(TOKEN)

# # Foydalanuvchilar buyurtmalari (har bir foydalanuvchi uchun alohida saqlanadi)
# user_orders = {}

# # Buyurtma qo'shish funksiyasi
# def add_order(user_id, item):
#     if user_id not in user_orders:
#         user_orders[user_id] = []
#     user_orders[user_id].append(item)

# # Zakazlarni ko'rsatish funksiyasi
# def get_order_markup(user_id):
#     markup = InlineKeyboardMarkup()
#     if user_id in user_orders and user_orders[user_id]:
#         for idx, item in enumerate(user_orders[user_id]):
#             markup.add(InlineKeyboardButton(f"❌ {item}", callback_data=f"remove:{idx}"))
#         markup.add(InlineKeyboardButton("🗑️ Savatni tozalash", callback_data="clear"))
#         markup.add(InlineKeyboardButton("✅ Buyurtma qilish", callback_data="order"))
#     markup.add(InlineKeyboardButton("⬅️ Ortga", callback_data="back"))
#     return markup

# # Boshlang'ich xabar
# @bot.message_handler(commands=['start'])
# def start(message):
#     user_id = message.chat.id
#     # Sinov uchun bir nechta zakaz qo'shib qo'yamiz
#     add_order(user_id, "Burger")
#     add_order(user_id, "Coca-Cola")
#     add_order(user_id, "Fries")
    
#     markup = InlineKeyboardMarkup()
#     markup.add(InlineKeyboardButton("🍔 Zakaz qilish", callback_data="show_orders"))
#     bot.send_message(user_id, "Bo'limni tanlang:", reply_markup=markup)

# # Callbackni boshqarish
# @bot.callback_query_handler(func=lambda call: True)
# def callback(call):
#     user_id = call.message.chat.id
    
#     if call.data == "show_orders":
#         # Zakazlarni ko'rsatish
#         if user_id in user_orders and user_orders[user_id]:
#             order_text = "📋 Sizning buyurtmalaringiz:\n" + "\n".join([f"- {item}" for item in user_orders[user_id]])
#         else:
#             order_text = "🛒 Sizning savatingiz bo'sh."
#         bot.edit_message_text(order_text, 
#                               chat_id=user_id, 
#                               message_id=call.message.message_id, 
#                               reply_markup=get_order_markup(user_id))
    
#     elif call.data.startswith("remove:"):
#         # Buyurtmani o'chirish
#         idx = int(call.data.split(":")[1])
#         if user_id in user_orders and 0 <= idx < len(user_orders[user_id]):
#             removed_item = user_orders[user_id].pop(idx)
#             bot.answer_callback_query(call.id, f"❌ {removed_item} o'chirildi.")
#             callback_data = "show_orders"
#         else:
#             bot.answer_callback_query(call.id, "❗ Buyurtma topilmadi.")
        
#         # Savatni yangilash
#         if user_id in user_orders and user_orders[user_id]:
#             order_text = "📋 Sizning buyurtmalaringiz:\n" + "\n".join([f"- {item}" for item in user_orders[user_id]])
#         else:
#             order_text = "🛒 Sizning savatingiz bo'sh."
#         bot.edit_message_text(order_text, 
#                               chat_id=user_id, 
#                               message_id=call.message.message_id, 
#                               reply_markup=get_order_markup(user_id))

#     elif call.data == "clear":
#         # Savatni tozalash
#         user_orders[user_id] = []
#         bot.answer_callback_query(call.id, "🗑️ Savat tozalandi.")
#         bot.edit_message_text("🛒 Sizning savatingiz bo'sh.", 
#                               chat_id=user_id, 
#                               message_id=call.message.message_id, 
#                               reply_markup=get_order_markup(user_id))
    
#     elif call.data == "order":
#         # Buyurtma qilish
#         if user_id in user_orders and user_orders[user_id]:
#             bot.answer_callback_query(call.id, "✅ Buyurtmangiz qabul qilindi!")
#             bot.send_message(user_id, "Rahmat! Buyurtmangiz yaqin orada yetkaziladi.")
#             user_orders[user_id] = []  # Savatni tozalash
#         else:
#             bot.answer_callback_query(call.id, "❗ Savatingiz bo'sh.")
    
#     elif call.data == "back":
#         # Ortga qaytish
#         markup = InlineKeyboardMarkup()
#         markup.add(InlineKeyboardButton("🍔 Zakaz qilish", callback_data="show_orders"))
#         bot.edit_message_text("Bo'limni tanlang:", 
#                               chat_id=user_id, 
#                               message_id=call.message.message_id, 
#                               reply_markup=markup)

# bot.polling()





###############################################################################################


# from aiogram import Bot, Dispatcher, F, types
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
# from aiogram.utils.keyboard import InlineKeyboardBuilder
# from aiogram.filters.callback_data import CallbackData
# from aiogram.types.message import Message
# import asyncio
# import ssl
# import aiohttp

# # Bot token
# BOT_TOKEN = "7738866089:AAFALZGGXK7RlTWaAZt47EjSNUuuEPseSZA"

# # Product data
# # Product data with updated image URLs (replace with working URLs or local file IDs)
# products = [
#     {"name": "Cola", "price": 15000, "image": "https://via.placeholder.com/300?text=Cola"},
#     {"name": "Pepsi", "price": 14000, "image": "https://via.placeholder.com/300?text=Pepsi"},
#     {"name": "Fanta", "price": 16000, "image": "https://via.placeholder.com/300?text=Fanta"},
# ]


# # Callback data for pagination and actions
# class ProductCallback(CallbackData, prefix="product"):
#     action: str
#     index: int

# # Generate inline keyboard
# async def generate_keyboard(index: int):
#     keyboard = InlineKeyboardBuilder()
#     keyboard.button(
#         text="\u25C0 Orqaga", callback_data=ProductCallback(action="prev", index=index - 1).pack()
#     )
#     keyboard.button(
#         text="Savatga qo'shish", callback_data=ProductCallback(action="add", index=index).pack()
#     )
#     keyboard.button(
#         text="Keyingi \u25B6", callback_data=ProductCallback(action="next", index=index + 1).pack()
#     )
#     keyboard.adjust(3)
#     return keyboard.as_markup()

# # Send product message
# async def send_product_message(chat_id: int, index: int, bot: Bot):
#     if 0 <= index < len(products):
#         product = products[index]
#         photo = product.get("image")
#         caption = f"<b>Nomi:</b> {product['name']}\n<b>Narxi:</b> {product['price']} so'm"
#         keyboard = await generate_keyboard(index)
#         await bot.send_photo(
#             chat_id=chat_id,
#             photo=photo,
#             caption=caption,
#             parse_mode="HTML",
#             reply_markup=keyboard
#         )
#     else:
#         await bot.send_message(chat_id, "Mahsulot topilmadi!")

# # Handle start command
# async def start_handler(message: Message, bot: Bot):
#     await send_product_message(message.chat.id, 0, bot)

# # Handle callback queries
# async def callback_handler(query: CallbackQuery, callback_data: ProductCallback, bot: Bot):
#     action = callback_data.action
#     index = callback_data.index

#     if action == "prev":
#         index = index if index >= 0 else len(products) - 1
#         await send_product_message(query.message.chat.id, index, bot)
#     elif action == "next":
#         index = index if index < len(products) else 0
#         await send_product_message(query.message.chat.id, index, bot)
#     elif action == "add":
#         product = products[index]
#         await query.message.answer(f"{product['name']} savatga qo'shildi!")

#     await query.answer()

# # Main function to start the bot
# async def main():
#     ssl_context = ssl.create_default_context()
#     connector = aiohttp.TCPConnector(ssl=ssl_context)
#     bot = Bot(token=BOT_TOKEN, connector=connector)
#     dp = Dispatcher()

#     dp.message.register(start_handler, F.text == "/start")
#     dp.callback_query.register(callback_handler, ProductCallback.filter())

#     try:
#         await dp.start_polling(bot)
#     finally:
#         await bot.session.close()

# if __name__ == "__main__":
#     asyncio.run(main())
