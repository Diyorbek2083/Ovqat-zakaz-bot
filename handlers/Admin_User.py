import asyncio
import re
import os
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from geopy.distance import geodesic
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from botun.Buttons import (
        c_p_button, a_r_admin, 
        bot_malumotlari, AdminSeeButton, 
        categorya_product, AdminButton, 
        CategoryaAddRemovReplay, ProductAddRemovReplay, 
        sorash, replay_buttons, replay_buttons_p,
        AdminRemovButtons, ortga, AdminIzohlar,
        user_bog, UserButton, Zakazlar, MaxsulotSoni,
        telephone, lacation, ZakazSoni, ProductIN
    )
from data.databaza import (
        baza, AddCategorya, AddProduct, 
        RemoveCategorya, UsersIzohlar,
        SavatRead, Adminlar
    )
from states.State import Start, mesages

### Admin statelari
class Admin(StatesGroup):
    button_add_remov_replay = State()
    admin_add_remov = State()
    reklama_yuborish = State()
    botni_tahrirlash = State()
    knopka_tekshirish = State()
    tasdiqlash = State()
    boglanish = State()
    yangi_malumot = State()
    malumot_tasdiqlash = State()
    izohlar_read = State()
    reklama_tasdiqlash = State()
    reklama_matn = State()
    admin_add = State()
    admin_tasdiqlash = State()
    admin_remov = State()
    a_r_r_button = State()
    catogorya_name = State()
    categorya_photo = State()
    categorya_remov = State()
    categorya_reply = State()
    replay_buttons = State()
    replay_tasdiqlash = State()
    categorya_id = State()
    producta_name = State()
    producta_narxi = State()
    producta_rasmi = State()
    producta_remov = State()
    producta_replay = State()
    producta_replay_call = State()
    admin_loc = State()
    javob = State()
    javob_tasdiqlash = State()

### User statelari
class User(StatesGroup):
    start = State()
    maxsulot_soni = State()
    izoh_yozish = State()
    user_tasdiqlash = State()
    zakaz_buton = State()
    telefon = State()
    locatsion = State()
    product_in = State()

### Router
admin_router = Router()
user_router = Router()


async def send_and_wait(call: CallbackQuery, text: str, reply_markup=None, state: State = None):
    """Send message and optionally set state."""
    await call.answer("Iltimos kuting...")
    await asyncio.sleep(1)
    if text:
        await call.message.answer(text=text, reply_markup=reply_markup)
    if state:
        await state.set_state(state)
    await call.message.delete()

###########################################################################################################

#### User start
@user_router.callback_query(F.data, Start.user)
async def UserStart(call:CallbackQuery, state:FSMContext):
    xabar = call.data
    if xabar == "ortga":
        await call.message.answer(text=f"Siz adminsiz", reply_markup=AdminButton)
        await state.set_state(Start.admin)
    elif xabar == 'boglanish':
        i = baza.read('malumotlar',"*",where_name='id = 1')
        await call.message.answer(text=f"🤖 Bizning bot: {i[0][1]}\n🙎‍♂️ Admin: {i[0][2]}\n🟥 Instagram kanal: instagram.com/{i[0][3]}\n📞 Telefon raqam: {i[0][4]}\n🚴‍♂️ Yetkazib berish masofasi: {i[0][7]} km\n\nBot haqidagi fikringizni yozib qoldirishingiz mumkin!", reply_markup=user_bog)
        await state.set_state(User.start)
    elif xabar == "zakaz_berish":
        if SavatRead(call.from_user.id) == True:
            savat = ""
            suma = 0
            for i in baza.read('savat','*',where_name=f'telegram_id={call.from_user.id}'):
                savat += f"{i[3]} -> {i[4]} so'm x {i[5]} ta = {i[4]*i[5]} so'm\n"
                suma += i[4]*i[5]
            await call.message.answer(text=F"👤 {call.from_user.first_name}ning SAVATI\n\n{savat}\n💰 Jami summa: {suma} so'm", reply_markup=ZakazSoni(call.from_user.id))
            await state.set_state(User.zakaz_buton)
        else:
            if call.from_user.id in Adminlar():
                await call.message.answer_photo(photo='AgACAgIAAxkBAANhZ3I9OPow2mySc-ahVi7srTQNfisAApTvMRsdM5FLB6vL02jeczoBAAMCAANtAAM2BA', caption="Hali hechnima tanlamagansiz oldin maxsulot tanlang!", reply_markup=AdminSeeButton())
            else:
                await call.message.answer_photo(photo='AgACAgIAAxkBAANhZ3I9OPow2mySc-ahVi7srTQNfisAApTvMRsdM5FLB6vL02jeczoBAAMCAANtAAM2BA', caption="Hali hechnima tanlamagansiz oldin maxsulot tanlang!", reply_markup=UserButton())
            await state.set_state(Start.user)
    else:
        await state.update_data(categorya_id=int(xabar.split('-')[-1]))
        if ProductAddRemovReplay(id=int(xabar.split('-')[-1]))!=None:
            a = baza.read('categorya','*',where_name=f"id = {int(xabar.split('-')[-1])}")
            await call.message.answer_photo(photo=a[0][2], caption=f"Categorya: {a[0][1]}", reply_markup=ProductAddRemovReplay(id=int(xabar.split('-')[-1])))
            await state.set_state(User.start)            
        else:
            if call.from_user.id in Adminlar():
                await call.message.answer_photo(photo='AgACAgIAAxkBAANhZ3I9OPow2mySc-ahVi7srTQNfisAApTvMRsdM5FLB6vL02jeczoBAAMCAANtAAM2BA', caption="Bu categroyada hali ovqat yo'q", reply_markup=AdminSeeButton())
            else:  
                await call.message.answer_photo(photo='AgACAgIAAxkBAANhZ3I9OPow2mySc-ahVi7srTQNfisAApTvMRsdM5FLB6vL02jeczoBAAMCAANtAAM2BA', caption="Bu categroyada hali ovqat yo'q", reply_markup=UserButton())
            await state.set_state(Start.user)
    await call.message.delete()

### User menyudagi zakaz berish knopkasi
@user_router.callback_query(F.data, User.zakaz_buton)
async def ZakazBerish(call:CallbackQuery, state:FSMContext):
    xabar = call.data
    if xabar == 'admin bosh menyuga qaytish':
        if call.from_user.id in Adminlar():
            await call.message.answer_photo(photo='AgACAgIAAxkBAANhZ3I9OPow2mySc-ahVi7srTQNfisAApTvMRsdM5FLB6vL02jeczoBAAMCAANtAAM2BA', caption="Siz adminsiz nima qilmoqchisiz?", reply_markup=AdminSeeButton())
        else:  
            await call.message.answer_photo(photo='AgACAgIAAxkBAANhZ3I9OPow2mySc-ahVi7srTQNfisAApTvMRsdM5FLB6vL02jeczoBAAMCAANtAAM2BA', caption="Yana buyirtma qilishni hohlaysizmi?", reply_markup=UserButton())
        await state.set_state(Start.user)
    elif xabar == "🛒 Savatni tozalash":
        baza.delete('savat', manzil_name=f'telegram_id = {call.from_user.id}')
        if call.from_user.id in Adminlar():
            await call.message.answer_photo(photo='AgACAgIAAxkBAANhZ3I9OPow2mySc-ahVi7srTQNfisAApTvMRsdM5FLB6vL02jeczoBAAMCAANtAAM2BA', caption="Savat tozalandi. Nima zakaz qilmoqchisiz?", reply_markup=AdminSeeButton())
        else:  
            await call.message.answer_photo(photo='AgACAgIAAxkBAANhZ3I9OPow2mySc-ahVi7srTQNfisAApTvMRsdM5FLB6vL02jeczoBAAMCAANtAAM2BA', caption="Savat tozalandi. Nima zakaz qilmoqchisiz?", reply_markup=UserButton())
        await state.set_state(Start.user)
    elif xabar == '✔️ Zakaz berish':
        await call.message.answer(text="Cantactingizni ulashing yoki telfon raqamingizni yozib yuboring", reply_markup=telephone)
        await state.set_state(User.telefon)
    elif xabar.startswith('-'):
        soni = int(xabar.split('_')[-1])
        id = int((xabar.split('_')[0]).split('-')[-1])
        if soni != 0:
            baza.update('savat',yangi_name=f'soni = {soni}', manzil_name=f'id = {id}')
        else:
            baza.delete('savat',manzil_name=f'id = {id}')
        if SavatRead(call.from_user.id) == True:
            savat = ""
            suma = 0
            for i in baza.read('savat','*',where_name=f'telegram_id={call.from_user.id}'):
                savat += f"{i[3]} -> {i[4]} so'm x {i[5]} ta = {i[4]*i[5]} so'm\n"
                suma += i[4]*i[5]
            await call.message.answer(text=F"👤 {call.from_user.first_name}ning SAVATI\n\n{savat}\n💰 Jami summa: {suma} so'm", reply_markup=ZakazSoni(call.from_user.id))
            await state.set_state(User.zakaz_buton)
        else:
            if call.from_user.id in Adminlar():
                await call.message.answer_photo(photo='AgACAgIAAxkBAANhZ3I9OPow2mySc-ahVi7srTQNfisAApTvMRsdM5FLB6vL02jeczoBAAMCAANtAAM2BA', caption="Savatdagi maxsulotlar o'chirildi!", reply_markup=AdminSeeButton())
            else:
                await call.message.answer_photo(photo='AgACAgIAAxkBAANhZ3I9OPow2mySc-ahVi7srTQNfisAApTvMRsdM5FLB6vL02jeczoBAAMCAANtAAM2BA', caption="Savatdagi maxsulotlar o'chirildi!", reply_markup=UserButton())
            await state.set_state(Start.user)
    elif xabar.startswith('+'):
        soni = int(xabar.split('_')[-1])
        id = int((xabar.split('_')[0]).split('+')[-1])
        baza.update('savat',yangi_name=f'soni = {soni}', manzil_name=f'id = {id}')
        if SavatRead(call.from_user.id) == True:
            savat = ""
            suma = 0
            for i in baza.read('savat','*',where_name=f'telegram_id={call.from_user.id}'):
                savat += f"{i[3]} -> {i[4]} so'm x {i[5]} ta = {i[4]*i[5]} so'm\n"
                suma += i[4]*i[5]
            await call.message.answer(text=F"👤 {call.from_user.first_name}ning SAVATI\n\n{savat}\n💰 Jami summa: {suma} so'm", reply_markup=ZakazSoni(call.from_user.id))
            await state.set_state(User.zakaz_buton)
    elif xabar.startswith('='):
        soni = int(xabar.split('_')[-1])
        id = int(xabar.split('_')[1])
        nomi = (xabar.split('_')[0]).split('=')[-1]
        pr = baza.read('product','*',where_name=f'name = "{nomi}"')
        await call.message.answer_photo(photo=pr[0][3], caption=f"Nomi: {nomi}\nNarxi: {pr[0][2]} so'm\n\n{soni} ta x {pr[0][2]} so'm = {soni*pr[0][2]} so'm", reply_markup=ProductIN(telegram_id=call.from_user.id, id=id, soni=soni))
        await state.set_state(User.product_in)
    await call.message.delete()


#### Producta ichidagi pagination
@user_router.callback_query(F.data, User.product_in)
async def ProductaIchi(call:CallbackQuery, state:FSMContext):
    xabar = call.data
    if xabar == 'ortga':
        if SavatRead(call.from_user.id) == True:
            savat = ""
            suma = 0
            for i in baza.read('savat','*',where_name=f'telegram_id={call.from_user.id}'):
                savat += f"{i[3]} -> {i[4]} so'm x {i[5]} ta = {i[4]*i[5]} so'm\n"
                suma += i[4]*i[5]
            await call.message.answer(text=F"👤 {call.from_user.first_name}ning SAVATI\n\n{savat}\n💰 Jami summa: {suma} so'm", reply_markup=ZakazSoni(call.from_user.id))
            await state.set_state(User.zakaz_buton)
        else:
            if call.from_user.id in Adminlar():
                await call.message.answer_photo(photo='AgACAgIAAxkBAANhZ3I9OPow2mySc-ahVi7srTQNfisAApTvMRsdM5FLB6vL02jeczoBAAMCAANtAAM2BA', caption="Savatdagi maxsulotlar o'chirildi!", reply_markup=AdminSeeButton())
            else:
                await call.message.answer_photo(photo='AgACAgIAAxkBAANhZ3I9OPow2mySc-ahVi7srTQNfisAApTvMRsdM5FLB6vL02jeczoBAAMCAANtAAM2BA', caption="Savatdagi maxsulotlar o'chirildi!", reply_markup=UserButton())
            await state.set_state(Start.user)
    elif xabar.endswith("o'chirish"):
        idd = int(xabar.split('_')[0])
        baza.delete('savat',manzil_name=f'id={idd}')
        if SavatRead(call.from_user.id) == True:
            a = baza.read('savat','*',f'telegram_id={call.from_user.id}')
            soni = int(a[0][-1])
            id = int(a[0][0])
            nomi = a[0][3]
            pr = baza.read('product','*',where_name=f'name = "{nomi}"')
            await call.message.answer_photo(photo=pr[0][3], caption=f"Nomi: {nomi}\nNarxi: {pr[0][2]} so'm\n\n{soni} ta x {pr[0][2]} so'm = {soni*pr[0][2]} so'm", reply_markup=ProductIN(telegram_id=call.from_user.id, id=id, soni=soni))
            await state.set_state(User.product_in)
        else:
            if call.from_user.id in Adminlar():
                await call.message.answer_photo(photo='AgACAgIAAxkBAANhZ3I9OPow2mySc-ahVi7srTQNfisAApTvMRsdM5FLB6vL02jeczoBAAMCAANtAAM2BA', caption="Savatdagi maxsulotlar o'chirildi!", reply_markup=AdminSeeButton())
            else:
                await call.message.answer_photo(photo='AgACAgIAAxkBAANhZ3I9OPow2mySc-ahVi7srTQNfisAApTvMRsdM5FLB6vL02jeczoBAAMCAANtAAM2BA', caption="Savatdagi maxsulotlar o'chirildi!", reply_markup=UserButton())
            await state.set_state(Start.user)
    elif xabar.startswith('-'):
        soni = int(xabar.split('_')[-1])
        id = int((xabar.split('_')[0]).split('-')[-1])
        if soni != 0:
            baza.update('savat', yangi_name=f"soni = {soni}", manzil_name=f"id = {id}")
            a = baza.read('savat', '*', where_name=f'id = {id}')
            pr = baza.read('product','*',where_name=f'name = "{a[0][3]}"')
            await call.message.answer_photo(photo=pr[0][3], caption=f"Nomi: {pr[0][1]}\nNarxi: {pr[0][2]} so'm\n\n{soni} ta x {pr[0][2]} so'm = {soni*pr[0][2]} so'm", reply_markup=ProductIN(telegram_id=call.from_user.id, id=id, soni=soni))
            await state.set_state(User.product_in)
        else:
            baza.delete('savat',manzil_name=f'id = {id}')
            if SavatRead(call.from_user.id) == True:
                savat = ""
                suma = 0
                for i in baza.read('savat','*',where_name=f'telegram_id={call.from_user.id}'):
                    savat += f"{i[3]} -> {i[4]} so'm x {i[5]} ta = {i[4]*i[5]} so'm\n"
                    suma += i[4]*i[5]
                await call.message.answer(text=F"👤 {call.from_user.first_name}ning SAVATI\n\n{savat}\n💰 Jami summa: {suma} so'm", reply_markup=ZakazSoni(call.from_user.id))
                await state.set_state(User.zakaz_buton)
            else:
                if call.from_user.id in Adminlar():
                    await call.message.answer_photo(photo='AgACAgIAAxkBAANhZ3I9OPow2mySc-ahVi7srTQNfisAApTvMRsdM5FLB6vL02jeczoBAAMCAANtAAM2BA', caption="Savatdagi maxsulotlar o'chirildi!", reply_markup=AdminSeeButton())
                else:
                    await call.message.answer_photo(photo='AgACAgIAAxkBAANhZ3I9OPow2mySc-ahVi7srTQNfisAApTvMRsdM5FLB6vL02jeczoBAAMCAANtAAM2BA', caption="Savatdagi maxsulotlar o'chirildi!", reply_markup=UserButton())
                await state.set_state(Start.user)
    elif xabar.startswith('+'):
        soni = int(xabar.split('_')[-1])
        id = int((xabar.split('_')[0]).split('+')[-1])
        baza.update('savat', yangi_name=f"soni = {soni}", manzil_name=f"id = {id}")
        a = baza.read('savat', '*', where_name=f'id = {id}')
        pr = baza.read('product','*',where_name=f'name = "{a[0][3]}"')
        await call.message.answer_photo(photo=pr[0][3], caption=f"Nomi: {pr[0][1]}\nNarxi: {pr[0][2]} so'm\n\n{soni} ta x {pr[0][2]} so'm = {soni*pr[0][2]} so'm", reply_markup=ProductIN(telegram_id=call.from_user.id, id=id, soni=soni))
        await state.set_state(User.product_in)
    elif xabar.startswith('keyingi'):
        id = int(xabar.split('_')[1])
        a = baza.read('savat', '*', where_name=f'id = {id}')
        pr = baza.read('product','*',where_name=f'name = "{a[0][3]}"')
        await call.message.answer_photo(photo=pr[0][3], caption=f"Nomi: {pr[0][1]}\nNarxi: {pr[0][2]} so'm\n\n{a[0][-1]} ta x {pr[0][2]} so'm = {int(a[0][-1])*pr[0][2]} so'm", reply_markup=ProductIN(telegram_id=call.from_user.id, id=id, soni=int(a[0][-1])))
        await state.set_state(User.product_in)
    elif xabar.startswith('oldingi'):
        id = int(xabar.split('_')[1])
        a = baza.read('savat', '*', where_name=f'id = {id}')
        pr = baza.read('product','*',where_name=f'name = "{a[0][3]}"')
        await call.message.answer_photo(photo=pr[0][3], caption=f"Nomi: {pr[0][1]}\nNarxi: {pr[0][2]} so'm\n\n{a[0][-1]} ta x {pr[0][2]} so'm = {int(a[0][-1])*pr[0][2]} so'm", reply_markup=ProductIN(telegram_id=call.from_user.id, id=id, soni=int(a[0][-1])))
        await state.set_state(User.product_in)
    await call.message.delete()


### Telefon raqamni ulashish
@user_router.message((F.contact|F.text), User.telefon)
async def TelefonRaqam(message:Message, state:FSMContext):
    tel = message.contact.phone_number if message.contact else None
    text = message.text if message.text else None
    if tel:
        await state.update_data(tel=tel)
        await message.answer(text="📍 Locatsiyangizni yuboring", reply_markup=lacation)
        await state.set_state(User.locatsion)
    elif text:
        pattern = r'^\+998(33|90|91|93|94|95|97|98|99|88)[0-9]{7}$'
        if re.match(pattern, text):
            await state.update_data(tel=text)
            await message.answer(text="📍 Locatsiyangizni yuboring", reply_markup=lacation)
            await state.set_state(User.locatsion)
        else:
            await message.answer(text="Itimos o'zbekiston raqamini kirting!\nMasalan: +998907002083", reply_markup=telephone)
            await state.set_state(User.telefon)
    await message.delete()
    
## Locatsiyani yuborish joyi
@user_router.message((F.text|F.location), User.locatsion)
async def LocatsiyaUlashish(message:Message, state:FSMContext):
    local = message.location if message.location else None
    text = message.text if message.text else None
    la = message.location.latitude
    lo = message.location.longitude
    print(la, lo)
    if local:
        manzil = baza.read('malumotlar','*',where_name='id = 1')
        shahar_markazi = (float(manzil[0][5]), float(manzil[0][6]))
        maks_masofa = int(manzil[0][7])
        def locatsiyani_tekshirish(foydalanuvchi_loc):
            masofa = geodesic(shahar_markazi, foydalanuvchi_loc).km
            if masofa <= maks_masofa:
                return True
            else:
                return False
        foydalanuvchi_locatsiyasi = (local.latitude, local.longitude)
        if locatsiyani_tekshirish(foydalanuvchi_locatsiyasi) == True:
            savat = ""
            suma = 0
            for i in baza.read('savat','*',where_name=f'telegram_id={message.from_user.id}'):
                savat += f"{i[3]} -> {i[4]} so'm x {i[5]} ta = {i[4]*i[5]} so'm\n"
                suma += i[4]*i[5]
            await message.answer(text=F"🔖 Sizning chekiniz\n{savat}💰 Jami summa: {suma} so'm\n\nTanlagan maxsulotlaringiz tez orada yetkazib beriladi")
            await message.bot.send_location(chat_id=6378609931, latitude=la, longitude=lo)
            await message.bot.send_message(chat_id=6378609931, text=f"👤 {message.from_user.first_name}ning SAVATI\n{savat}\n💰 Jami summa: {suma} so'm\n\nYangi zakaz ")
            await state.clear()
        if locatsiyani_tekshirish(foydalanuvchi_locatsiyasi) == False:
            if message.from_user.id in Adminlar():
                await message.answer_photo(photo='AgACAgIAAxkBAANhZ3I9OPow2mySc-ahVi7srTQNfisAApTvMRsdM5FLB6vL02jeczoBAAMCAANtAAM2BA', caption='Bizda siz yuborgan manzilga yetkazib berish xizmati yo\'q\nSiz adminsiz', reply_markup=AdminSeeButton())
            else:
                await message.answer_photo(photo='AgACAgIAAxkBAANhZ3I9OPow2mySc-ahVi7srTQNfisAApTvMRsdM5FLB6vL02jeczoBAAMCAANtAAM2BA' ,caption=f"Bizda siz yuborgan manzilga yetkazib berish xizmati yo\'q", reply_markup=UserButton())
            await state.set_state(Start.user)
        baza.delete('savat', manzil_name=f"telegram_id = {message.from_user.id}")
    elif text:
        await message.answer(text="Iltimos locatsiyangizni yuboring!", reply_markup=lacation)
        await state.set_state(User.locatsion)

#### User menyudagi knopkalarning ichi
@user_router.callback_query(F.data, User.start)
async def KnopkaTanlash(call:CallbackQuery, state:FSMContext):
    xabar = call.data
    if xabar == 'admin bosh menyuga qaytish':
        if call.from_user.id in Adminlar():
            await call.message.answer_photo(photo='AgACAgIAAxkBAANhZ3I9OPow2mySc-ahVi7srTQNfisAApTvMRsdM5FLB6vL02jeczoBAAMCAANtAAM2BA', caption='Siz user menyudasiz!', reply_markup=AdminSeeButton())
        else:
            await call.message.answer_photo(photo='AgACAgIAAxkBAANhZ3I9OPow2mySc-ahVi7srTQNfisAApTvMRsdM5FLB6vL02jeczoBAAMCAANtAAM2BA' ,caption=f"Ovqat zakaz qiladigan bot", reply_markup=UserButton())
        await state.set_state(Start.user)
    elif xabar == 'izoh yozish':
        await state.update_data(izohh=xabar)
        await call.message.answer(text="Bot haqidagi fikringizni yozib yuboring. Biz uchun har bir mijozning fikri muhim!")
        await state.set_state(User.izoh_yozish)
    else:
        for i in baza.read('product','*'):
            if i[0]==int(xabar.split('-')[-1]):
                await state.update_data(nomi=i[1], narxi=i[2], product_id=i[0])
                await call.message.answer_photo(photo=i[3], caption=f"Nomi: {i[1]}\nNarxi: {i[2]} so'm\n\n{i[1]} nechta olmoqchisiz?", reply_markup=MaxsulotSoni())
                await state.set_state(User.maxsulot_soni)
    await call.message.delete()

### Izoh qoldirish
@user_router.message(F.text, User.izoh_yozish)
async def IzohYozish(message:Message, state:FSMContext):
    xabar = message.text
    await state.update_data(matn=xabar)
    await message.answer(text=f"📝 Izoh:\n{xabar}\n\nBu izohni yuborishni hohlaysizmi?", reply_markup=sorash)
    await state.set_state(User.user_tasdiqlash)
    await message.delete()

#### User tasdiqlash knopkasi
@user_router.callback_query(F.data, User.user_tasdiqlash)
async def UserTasdiqlash(call:CallbackQuery, state:FSMContext):
    xabar = call.data
    data = await state.get_data()
    if xabar == 'ha':
        if data.get('izohh'):
            baza.insert('izohlar', telegram_id=call.from_user.id, name=call.from_user.first_name, izoh=data.get('matn'))
            if call.from_user.id in Adminlar():
                await call.message.answer_photo(photo='AgACAgIAAxkBAANhZ3I9OPow2mySc-ahVi7srTQNfisAApTvMRsdM5FLB6vL02jeczoBAAMCAANtAAM2BA', caption='Siz qoldirgan izoh adminga yuborildi!\nNima zakaz qilmoqchisiz?', reply_markup=AdminSeeButton())
            else:
                await call.message.answer_photo(photo='AgACAgIAAxkBAANhZ3I9OPow2mySc-ahVi7srTQNfisAApTvMRsdM5FLB6vL02jeczoBAAMCAANtAAM2BA' ,caption="Siz qoldirgan izoh adminga yuborildi!\nNima zakaz qilmoqchisiz?", reply_markup=UserButton())
            await state.set_state(Start.user)
    elif xabar == 'yoq':
        if data.get('izohh'):
            if call.from_user.id in Adminlar():
                await call.message.answer_photo(photo='AgACAgIAAxkBAANhZ3I9OPow2mySc-ahVi7srTQNfisAApTvMRsdM5FLB6vL02jeczoBAAMCAANtAAM2BA', caption='Siz qoldirgan izoh adminga yuborildi!\nNima zakaz qilmoqchisiz?', reply_markup=AdminSeeButton())
            else:
                await call.message.answer_photo(photo='AgACAgIAAxkBAANhZ3I9OPow2mySc-ahVi7srTQNfisAApTvMRsdM5FLB6vL02jeczoBAAMCAANtAAM2BA' ,caption="Siz qoldirgan izoh adminga yuborildi!\nNima zakaz qilmoqchisiz?", reply_markup=UserButton())
            await state.set_state(Start.user) 
    await call.message.delete()

#### Maxsulotni sonini kiritish knopkasi
@user_router.callback_query(F.data, User.maxsulot_soni)
async def MaxsulotSoniBot(call:CallbackQuery, state:FSMContext):
    xabar = call.data
    data = await state.get_data()
    if xabar == 'orqaga':
        a = baza.read('categorya','*',where_name=f"id = {int(data.get('categorya_id'))}")
        await call.message.answer_photo(photo=a[0][2], caption=f"Categorya: {a[0][1]}", reply_markup=ProductAddRemovReplay(id=int(data.get('categorya_id'))))
        await state.set_state(User.start)
    elif xabar.startswith('+'):
        for i in baza.read('product','*'):
            if i[0]==int(data.get('product_id')):
                await call.message.answer_photo(photo=i[3], caption=f"Nomi: {i[1]}\nNarxi: {i[2]} so'm\n\n{i[1]} x {xabar.split('+')[-1]} ta = {i[2] * int(xabar.split('+')[-1])} so'm", reply_markup=MaxsulotSoni(id=int(xabar.split('+')[-1])))
                await state.set_state(User.maxsulot_soni)
    elif xabar.startswith('-'):
        for i in baza.read('product','*'):
            if i[0]==int(data.get('product_id')):
                await call.message.answer_photo(photo=i[3], caption=f"Nomi: {i[1]}\nNarxi: {i[2]} so'm\n\n{i[1]} x {xabar.split('-')[-1]} ta = {i[2] * int(xabar.split('-')[-1])} so'm", reply_markup=MaxsulotSoni(id=int(xabar.split('-')[-1])))
                await state.set_state(User.maxsulot_soni)
    elif xabar.split('-')[0] == "savatga_add" or xabar.startswith('='):
        try:
            if call.from_user.id in [i[1] for i in baza.read('savat','*')]:
                if data.get('nomi') in [i[3] for i in baza.read('savat','*') if i[1]==call.from_user.id]:
                    a = int(xabar.split('-')[-1]) + int([i[-1] for i in baza.read("savat","*") if i[3]==data.get("nomi")][0])
                    baza.update('savat', yangi_name=f"soni = {a}", manzil_name=f"id = {int([i[0] for i in baza.read('savat','*') if i[1]==call.from_user.id and i[3]==data.get('nomi')][0])}")
                else:
                    baza.insert('savat', telegram_id=call.from_user.id, user=call.from_user.first_name, nomi=data.get('nomi'), narxi=int(data.get('narxi')), soni=int(xabar.split('-')[-1]))
            else:
                baza.insert('savat', telegram_id=call.from_user.id, user=call.from_user.first_name, nomi=data.get('nomi'), narxi=int(data.get('narxi')), soni=int(xabar.split('-')[-1]))
        except:
            print('Savatga q\'shishda xatolik')
            baza.insert('savat', telegram_id=call.from_user.id, user=call.from_user.first_name, nomi=data.get('nomi'), narxi=int(data.get('narxi')), soni=int(xabar.split('-')[-1]))
        if call.from_user.id in Adminlar():
            await call.message.answer_photo(photo='AgACAgIAAxkBAANhZ3I9OPow2mySc-ahVi7srTQNfisAApTvMRsdM5FLB6vL02jeczoBAAMCAANtAAM2BA', caption='Maxsulot savatga qo\'shildi! Yana maxsulot tanlaysizmi?', reply_markup=AdminSeeButton())
        else:
            await call.message.answer_photo(photo='AgACAgIAAxkBAANhZ3I9OPow2mySc-ahVi7srTQNfisAApTvMRsdM5FLB6vL02jeczoBAAMCAANtAAM2BA' ,caption=f"Maxsulot savatga qo'shildi! Yana maxsulot tanlaysizmi?", reply_markup=UserButton())
        await state.set_state(Start.user)
    await call.message.delete()

#####################################################################################################

#######  Admin Start 
@admin_router.callback_query(F.data, Start.admin)
async def AdminStart(call: CallbackQuery, state: FSMContext):
    xabar = call.data
    await call.answer('Iltimos kuting...')
    await asyncio.sleep(1)
    if xabar == 'button_add_remov_replay':
        await call.message.answer(text="Bu knopkalar orqali siz categorya va producta qo'shishingiz, o'chirishingiz va bor knopkalarni yangilashingiz mumkin", reply_markup=c_p_button)
        await state.set_state(Admin.button_add_remov_replay)
    elif xabar == 'admin_add_remov':
        await call.message.answer(text="Bu knopkalar orqali siz yangi admin qo'sholasiz yoki bor adminni o'chira olasiz", reply_markup=a_r_admin)
        await state.set_state(Admin.admin_add_remov)
    elif xabar == 'reklama_yuborish':
        await call.message.answer(text="Yubormoqchi bo'lgan reklamangizning vide yoki rasmini yuboring agar faqat matn yubormoqchi bo'lsangiz matining o'zini yozib yuboring")
        await state.set_state(Admin.reklama_yuborish)
    elif xabar == 'bot haqida izohlar':
        if UsersIzohlar() == True:
            a = baza.read('izohlar','*')
            await call.message.answer(text=f"{a[0][0]}.{a[0][2]} yozgan izoh\n{a[0][3]}", reply_markup=AdminIzohlar(id=int(a[0][0])))
            await state.set_state(Admin.izohlar_read)
        elif UsersIzohlar() == False:
            await call.message.answer(text="Hozircha botga qoldirilgan izohlar yo'q keyinroq qayta tekshiring", reply_markup=AdminButton)
            await state.set_state(Start.admin)
    elif xabar == 'biz bilan boglanish':
        try:
            for i in baza.read('malumotlar','*'):
                if i[0]==1:
                    await call.message.answer(text=f"🤖 Bizning bot: {i[1]}\n🙎‍♂️ Admin: {i[2]}\n🟥 Instagram kanal: instagram.com/{i[3]}\n📞 Telefon raqam: {i[4]}\n🚴‍♂️ Yetkazib berish masofasi: {i[7]} km\n\nQaysi malumotni o'zgartirmoqchisiz?", reply_markup=bot_malumotlari)
                    await state.set_state(Admin.boglanish)
        except:
            await call.message.answer(text="🤖 Bizning bot: \n🙎‍♂️ Admin: \n🟥 Instagram kanal: \n📞 Telefon raqam: ")
    elif xabar == 'knopka_tekshirish':
        await call.message.answer_photo(photo='AgACAgIAAxkBAANhZ3I9OPow2mySc-ahVi7srTQNfisAApTvMRsdM5FLB6vL02jeczoBAAMCAANtAAM2BA', caption='User menyuga xush kelibsiz!', reply_markup=AdminSeeButton())
        await state.set_state(Start.user)
    
    elif xabar == 'statistika':
        await call.message.answer(text='Hozircha statistika yo\'q', reply_markup=AdminButton)
        await state.set_state(Start.admin)
    await call.message.delete()









### Bot foydalanuvchilari knopkasi
# @admin_router.callback_query(F.data, Admin.foydalanuvchilar)
# async def BotFoydalanuchilari(call:CallbackQuery, state:FSMContext):
#     xabar = call.data
#     if xabar == 'orqaga':
#         await call.message.answer(text="Siz adminsiz\nNima qilmoqchisiz?", reply_markup=AdminButton)
#         await state.set_state(Start.admin)
#     if xabar == 'foydalanuvchilar_soni':
#         await call.message.answer(text=f"Bot foydalanuvchilar soni: 👤 {len(baza.read("users","*"))} ta\nAdminlar soni: 👨‍💼 {len(baza.read('admin','*'))} ta", reply_markup=ortga)
#         await state.set_state(Admin.izohlar_read)
#     if xabar == 'bot haqida izohlar':
#         if UsersIzohlar() == True:
#             a = baza.read('izohlar','*')
#             await call.message.answer(text=f"{a[0][0]}.{a[0][2]} yozgan izoh\n{a[0][3]}", reply_markup=AdminIzohlar(id=int(a[0][0])))
#             await state.set_state(Admin.izohlar_read)
#         elif UsersIzohlar() == False:
#             await call.message.answer(text="Hozircha botga qoldirilgan izohlar yo'q keyinroq qayta tekshiring", reply_markup=f_comment)
#             await state.set_state(Admin.foydalanuvchilar)
#     await call.message.delete()

### Izohlar paginatsiyasi
@admin_router.callback_query(F.data, Admin.izohlar_read)
async def IzohlarniOqish(call:CallbackQuery, state:FSMContext):
    xabar = call.data
    if xabar == 'orqaga':
        await call.message.answer(text="Siz adminsiz nima qilmoqchisiz?", reply_markup=AdminButton)
        await state.set_state(Start.admin)
    elif xabar.startswith('keyingi'):
        id = int(xabar.split('_')[-1])
        a = baza.read('izohlar','*', where_name=f"id = {id}")
        await call.message.answer(text=f"{a[0][0]}.{a[0][2]} yozgan izoh\n{a[0][3]}", reply_markup=AdminIzohlar(id=id))
        await state.set_state(Admin.izohlar_read)
    elif xabar.startswith('oldingi'):
        id = int(xabar.split('_')[-1])
        a = baza.read('izohlar','*', where_name=f"id = {id}")
        await call.message.answer(text=f"{a[0][0]}.{a[0][2]} yozgan izoh\n{a[0][3]}", reply_markup=AdminIzohlar(id=id))
        await state.set_state(Admin.izohlar_read)
    elif xabar.startswith('bekor'):
        idd = xabar.split('_')[-1]
        aa = baza.read('izohlar','*',where_name=f"id = {idd}")
        await call.bot.send_message(chat_id=aa[0][1], text=f"Siz qoldirigan izoh:\n{aa[0][3]}\n\nSiz qoldirgan izoh admin o'qidi va o'chirib tashladi!")
        baza.delete('izohlar',manzil_name=f"id = {idd}")
        if UsersIzohlar() == True:
            a = baza.read('izohlar','*')
            await call.message.answer(text=f"{a[0][0]}.{a[0][2]} yozgan izoh\n{a[0][3]}", reply_markup=AdminIzohlar(id=int(a[0][0])))
            await state.set_state(Admin.izohlar_read)
        elif UsersIzohlar() == False:
            await call.message.answer(text="Hozircha botga qoldirilgan izohlar yo'q keyinroq qayta tekshiring", reply_markup=AdminButton)
            await state.set_state(Start.admin)
    elif xabar.startswith('javob'):
        id = xabar.split('_')[-1]
        await state.update_data(iddd=id)
        aa = baza.read('izohlar','*',where_name=f'id = {id}')
        await call.message.answer(text=f"{aa[0][2]}ning qoldirgan izohi\n{aa[0][3]}\n\nJavobingizni yozib qoldiring!")
        await state.set_state(Admin.javob)
    await call.message.delete()

### Izoh yozish
@admin_router.message(F.text, Admin.javob)
async def JavobYozish(message:Message, state:FSMContext):
    xabar = message.text
    await state.update_data(javobb=xabar)
    await message.answer(text=f"Sizning yozgan javobingiz\n{xabar}\n\nYozganlaringizni rostanham yuborishni hohlaysizmi", reply_markup=sorash)
    await state.set_state(Admin.javob_tasdiqlash)

#### Izohga yozgan javobni tasdiqlash
@admin_router.callback_query(F.data, Admin.javob_tasdiqlash)
async def JavobniTasdiqlash(call:CallbackQuery, state:FSMContext):
    xabar =call.data
    data = await state.get_data()
    if xabar == 'ha':
        a = baza.read('izohlar','*',where_name=f'id = {int(data.get('iddd'))}')
        await call.bot.send_message(chat_id=int(a[0][1]), text=f"Siz qoldirgan izoh\n{a[0][3]}\n\nSizning izohingizga yozilgan javob\n{data.get('javobb')}")
        baza.delete('izohlar',manzil_name=f'id = {a[0][0]}')
        await call.message.answer(text="Siz yozgan javobingiz yuborildi!\nNima qilmoqchisiz", reply_markup=AdminButton)
        await state.set_state(Start.admin)
    elif xabar == 'yoq':
        a = baza.read('izohlar','*')
        await call.message.answer(text=f"{a[0][0]}.{a[0][2]} yozgan izoh\n{a[0][3]}", reply_markup=AdminIzohlar(id=int(a[0][0])))
        await state.set_state(Admin.izohlar_read)










#### Admin bilan bog'lanish knopkasi
@admin_router.callback_query(F.data, Admin.boglanish)
async def BoglanishAdmin(call:CallbackQuery, state:FSMContext):
    xabar = call.data
    if xabar == 'admin bosh menyuga qaytish':
        await call.message.answer(text=f"Siz adminsiz\nNima qilmoqchsiz?", reply_markup=AdminButton)
        await state.set_state(Start.admin)
    else:
        await state.update_data(yangi=xabar)
        if xabar == 'bot manzilini yangilash':
            await call.message.answer(text="Yangi bot usernameni yuboring\nMasalan: @username_bot")
            await state.set_state(Admin.yangi_malumot)
        if xabar == 'admin manzili yangilash':
            await call.message.answer(text="Yangi admin usernameni yuboring\nMasalan: @admin_name")
            await state.set_state(Admin.yangi_malumot)
        if xabar == 'instagram manzili yangilash':
            await call.message.answer(text="Yangi instagram nomini yuboring\nMasalan: fs_diyorbek")
            await state.set_state(Admin.yangi_malumot)
        if xabar == 'telefon raqamni yangilash':
            await call.message.answer(text="Yangi telefon raqamni yuboring\nMasalan: +998907142083")
            await state.set_state(Admin.yangi_malumot)
        if xabar == 'bizning manzil':
            await call.message.answer(text="Yangi manzilingizni kiritishingiz mumkin!", reply_markup=lacation)
            await state.set_state(Admin.admin_loc)
    await call.message.delete()

## Admin Locatsiyani yuborish joyi
@user_router.message((F.text|F.location), Admin.admin_loc)
async def LocatsiyaUlashish(message:Message, state:FSMContext):
    local = message.location if message.location else None
    text = message.text if message.text else None
    if text:
        await message.answer(text="Iltimos manzlingizni yuboring", reply_markup=lacation)
        await state.set_state(Admin.admin_loc)
    if local:
        la = message.location.latitude
        lo = message.location.longitude
        await state.update_data(la=la, lo=lo)
        await message.answer(text="Necha km ga yetkazib berishingizni kirting. Iltimos faqat raqam kirting!\nMasalan: 30")
        await state.set_state(Admin.yangi_malumot)
    await message.delete()

@admin_router.message(F.text, Admin.yangi_malumot)
async def YangiMalumotlarTutish(message:Message, state:FSMContext):
    xabar = message.text
    data = await state.get_data()
    a = baza.read('malumotlar','*',where_name='id=1')
    if data.get('yangi') == 'bizning manzil':
        if xabar.isdigit():
            await state.update_data(masofa=xabar)
            await message.answer_location(latitude=data.get('la'),longitude=data.get('lo'))
            await message.answer(text=f"Yetkazib berish masofasi: {xabar} km\n\nBu manzilni va yetkazib berish masofasini tasdiqlaysizmi?", reply_markup=sorash)
            await state.set_state(Admin.malumot_tasdiqlash)
        else:
            await message.answer(text="Iltimos yetkazib berish masofasini boshqatdan kirting!\nMasalan: 30")
            await state.set_state(Admin.yangi_malumot)
    if data.get('yangi')=='bot manzilini yangilash':
        if xabar.lower().endswith('bot'):
            await state.update_data(mal=xabar)
            await message.answer(text=f"Eski bot username: {a[0][1]}\nYangi bot username: {xabar}\n\nBu usernameni tasdiqlaysizmi?", reply_markup=sorash)
            await state.set_state(Admin.malumot_tasdiqlash)
        else:
            await message.answer(text="Iltimos botning yangi usernameni yuboring\nMasalan: @username_bot")
            await state.set_state(Admin.yangi_malumot)
    if data.get('yangi') == 'admin manzili yangilash':
        if xabar.startswith('@') and not (xabar.startswith('_') or xabar.endswith('_')):
            await state.update_data(mal=xabar)
            await message.answer(text=f"Eski bot username: {a[0][2]}\nYangi bot username: {xabar}\n\nBu usernameni tasdiqlaysizmi?", reply_markup=sorash)
            await state.set_state(Admin.malumot_tasdiqlash)
        else:
            await message.answer(text="Admin usernameni xato yubordingiz iltimos boshqatdan yuboring\nMasalan: @dima06_13")
            await state.set_state(Admin.yangi_malumot)
    if data.get('yangi') == 'instagram manzili yangilash':
        pattern = r'^[a-zA-Z0-9._]{1,30}$'
        if re.match(pattern, xabar):
            if not (xabar.endswith('.') or xabar.endswith('_')):
                await state.update_data(mal=xabar)
                await message.answer(text=f"Eski instagram nomi: {a[0][3]}\nYangi instagram nomi: {xabar}\nBu instagram nameni tasdiqlaysizmi?", reply_markup=sorash)
                await state.set_state(Admin.malumot_tasdiqlash)
        else:
            await message.answer(text='Iltimos instagramdagi nomingizni yozib yuboring\nMasalan: fs_diyorbek')
            await state.set_state(Admin.yangi_malumot)
    if data.get('yangi') == 'telefon raqamni yangilash':
        pattern = r'^\+998(33|90|91|93|94|95|97|98|99|88)[0-9]{7}$'
        if re.match(pattern, xabar):
            await state.update_data(mal=xabar)
            await message.answer(text=f"Eski telefon raqam: {a[0][4]}\nYangi telefon raqam: {xabar}\nYangi telefon raqamni tasdiqlaysizmi?", reply_markup=sorash)
            await state.set_state(Admin.malumot_tasdiqlash)
        else:
            await message.answer(text="Telefon raqam yuborishda xatolik iltimos boshqatdan yuboring\nMasalan: +998907142083")
            await state.set_state(Admin.yangi_malumot)
    await message.delete()

#### Bot manzillarini yangilashni tasdiqlash
@admin_router.callback_query(F.data, Admin.malumot_tasdiqlash)
async def YangiMalumotTasdiqlash(call:CallbackQuery, state:FSMContext):
    xabar = call.data
    data = await state.get_data()
    a = baza.read('malumotlar','*',where_name='id=1')
    if xabar == 'ha':
        if data.get('yangi')=='bot manzilini yangilash':
            await call.message.answer(f'🤖 Bizning bot: {data.get('mal')}\n🙎‍♂️ Admin: {a[0][2]}\n🟥 Instagram kanal: instagram.com/{a[0][3]}\n📞 Telefon raqam: {a[0][4]}\n🚴‍♂️ Yetkazib berish masofasi: {a[0][7]} km\n\nBot manzili yangilandi. Endi qaysi malumotlarni yangilamoqchisiz?', reply_markup=bot_malumotlari)
            baza.update('malumotlar',yangi_name=f'bot = "{data.get('mal')}"', manzil_name='id = 1')
        elif data.get('yangi')=='admin manzili yangilash':
            await call.message.answer(f'🤖 Bizning bot: {a[0][1]}\n🙎‍♂️ Admin: {data.get('mal')}\n🟥 Instagram kanal: instagram.com/{a[0][3]}\n📞 Telefon raqam: {a[0][4]}\n🚴‍♂️ Yetkazib berish masofasi: {a[0][7]} km\n\nAdmin manzili yangilandi. Endi qaysi malumotlarni yangilamoqchisiz?', reply_markup=bot_malumotlari)
            baza.update('malumotlar',yangi_name=f'admin = "{data.get('mal')}"', manzil_name='id = 1')
        elif data.get('yangi')=='instagram manzili yangilash':
            await call.message.answer(f'🤖 Bizning bot: {a[0][1]}\n🙎‍♂️ Admin: {a[0][2]}\n🟥 Instagram kanal: instagram.com/{data.get('mal')}\n📞 Telefon raqam: {a[0][4]}\n🚴‍♂️ Yetkazib berish masofasi: {a[0][7]} km\n\nInstagram manzili yangilandi. Endi qaysi malumotlarni yangilamoqchisiz?', reply_markup=bot_malumotlari)
            baza.update('malumotlar',yangi_name=f'insta = "{data.get('mal')}"', manzil_name='id = 1')
        elif data.get('yangi')=='telefon raqamni yangilash':
            await call.message.answer(f'🤖 Bizning bot: {a[0][1]}\n🙎‍♂️ Admin: {a[0][2]}\n🟥 Instagram kanal: instagram.com/{a[0][3]}\n📞 Telefon raqam: {data.get('mal')}\n🚴‍♂️ Yetkazib berish masofasi: {a[0][7]} km\n\nTelefon raqam yangilandi. Endi qaysi malumotlarni yangilamoqchisiz?', reply_markup=bot_malumotlari)
            baza.update('malumotlar',yangi_name=f'tel = "{data.get('mal')}"', manzil_name='id = 1')
        elif data.get('yangi')=='bizning manzil':
            await call.message.answer(f'🤖 Bizning bot: {a[0][1]}\n🙎‍♂️ Admin: {a[0][2]}\n🟥 Instagram kanal: instagram.com/{a[0][3]}\n📞 Telefon raqam: {a[0][4]}\n🚴‍♂️ Yetkazib berish masofasi: {data.get('masofa')} km\n\nTelefon raqam yangilandi. Endi qaysi malumotlarni yangilamoqchisiz?', reply_markup=bot_malumotlari)
            baza.update('malumotlar', yangi_name=f'masofa={int(data.get('masofa'))}', manzil_name='id = 1')
            baza.update('malumotlar', yangi_name=f'la={float(data.get('la'))}', manzil_name='id = 1')
            baza.update('malumotlar', yangi_name=f'lo={float(data.get('lo'))}', manzil_name='id = 1')
    elif xabar == 'yoq':
        if data.get('yangi')=='bot manzilini yangilash':
            await call.message.answer(f"🤖 Bizning bot: {a[0][1]}\n🙎‍♂️ Admin: {a[0][2]}\n🟥 Instagram kanal: instagram.com/{a[0][3]}\n📞 Telefon raqam: {a[0][4]}\n🚴‍♂️ Yetkazib berish masofasi: {a[0][7]} km\n\nBot manzilini yangilash bekor qilindi. Qaysi malumotlarni yangilamoqchisiz?", reply_markup=bot_malumotlari)
        elif data.get('yangi')=='admin manzili yangilash':
            await call.message.answer(f'🤖 Bizning bot: {a[0][1]}\n🙎‍♂️ Admin: {a[0][2]}\n🟥 Instagram kanal: instagram.com/{a[0][3]}\n📞 Telefon raqam: {a[0][4]}\n🚴‍♂️ Yetkazib berish masofasi: {a[0][7]} km\n\nAdmin manzilini yangilash bekor qilindi. Qaysi malumotlarni yangilamoqchisiz?', reply_markup=bot_malumotlari)
        elif data.get('yangi')=='instagram manzili yangilash':
            await call.message.answer(f'🤖 Bizning bot: {a[0][1]}\n🙎‍♂️ Admin: {a[0][2]}\n🟥 Instagram kanal: instagram.com/{a[0][3]}\n📞 Telefon raqam: {a[0][4]}\n🚴‍♂️ Yetkazib berish masofasi: {a[0][7]} km\n\nInstagram manzilini yangilash bekor qilindi. Qaysi malumotlarni yangilamoqchisiz?', reply_markup=bot_malumotlari)
        elif data.get('yangi')=='telefon raqamni yangilash':
            await call.message.answer(f'🤖 Bizning bot: {a[0][1]}\n🙎‍♂️ Admin: {a[0][2]}\n🟥 Instagram kanal: instagram.com/{a[0][3]}\n📞 Telefon raqam: {a[0][4]}\n🚴‍♂️ Yetkazib berish masofasi: {a[0][7]} km\n\nTelefon raqamni yangilash bekor qilindi. Qaysi malumotlarni yangilamoqchisiz?', reply_markup=bot_malumotlari)
        elif data.get('yangi')=='bizning manzil':
            await call.message.answer(f'🤖 Bizning bot: {a[0][1]}\n🙎‍♂️ Admin: {a[0][2]}\n🟥 Instagram kanal: instagram.com/{a[0][3]}\n📞 Telefon raqam: {a[0][4]}\n🚴‍♂️ Yetkazib berish masofasi: {a[0][7]} km\n\nTelefon raqamni yangilash bekor qilindi. Qaysi malumotlarni yangilamoqchisiz?', reply_markup=bot_malumotlari)
    await state.set_state(Admin.boglanish)
    await call.message.delete()

#####  Reklama yuborish knopkasi
@admin_router.message((F.photo | F.text | F.video), Admin.reklama_yuborish)
async def ReklamaYuborishBot(message: Message, state: FSMContext):
    xabar = message.text if message.text else None
    photo = message.photo[-1].file_id if message.photo else None
    video = message.video.file_id if message.video else None
    if xabar:
        await state.update_data(matn=xabar)
        await message.answer(text=f"Reklama ✈️\n{xabar}\n\nBu reklamani yubormoqchimisiz?", reply_markup=sorash)
        await state.set_state(Admin.reklama_tasdiqlash)
    elif photo:
        await state.update_data(photo=photo)
        await message.answer_photo(photo=photo, caption="Bu rasim tagida turadigan matinni yozib yuboring")
        await state.set_state(Admin.reklama_matn)
    elif video:
        await state.update_data(video=video)
        await message.answer_video(video=video, caption="Bu video tagida turadigan matinni yozib yuboring")
        await state.set_state(Admin.reklama_matn)
    else:
        await message.answer(text="Iltimos matin, rasim yoki video yuboring!")
        await state.set_state(Admin.reklama_yuborish)
    await message.delete()

### Rasim yoki video tagidagi
@admin_router.message(F.text, Admin.reklama_matn)
async def ReklamTagLavha(message:Message, state:FSMContext):
    xabar = message.text
    data = await state.get_data()
    if data.get('photo'):
        await state.update_data(tag=xabar)
        await message.bot.send_photo(chat_id=message.from_user.id, photo=data.get('photo'), caption=f"{xabar}\n\nBu reklamani yuborishni hohlaysizmi?", reply_markup=sorash)
        await state.set_state(Admin.reklama_tasdiqlash)
    elif data.get('video'):
        await state.update_data(tag=xabar)
        await message.bot.send_video(chat_id=message.from_user.id, video=data.get('video'), caption=f"{xabar}\n\nBu reklamani yuborishni hohlaysizmi?", reply_markup=sorash)
        await state.set_state(Admin.reklama_tasdiqlash)
    else:
        await message.answer(text="Iltimos rasim yoki video tagida turadigan matinni yuboring!")
        await state.set_state(Admin.reklama_matn)
    await message.delete()

### Reklamani yuborishni tasdiqlash
@admin_router.callback_query(F.data, Admin.reklama_tasdiqlash)
async def ReklamaniTasdiqlash(call:CallbackQuery, state:FSMContext):
    xabar = call.data
    data = await state.get_data()
    if xabar == 'ha':
        if data.get('matn'):
            for i in baza.read('users', "*"):
                if i[1] != call.from_user.id:
                    await call.bot.send_message(chat_id=i[1], text=data.get('matn'))
            await call.message.answer(text="Reklama yuborildi!\nEndi nima qilmoqchisiz?", reply_markup=AdminButton)
        elif data.get('photo'):
            for i in baza.read('users', "*"):
                if i[1] != call.from_user.id:
                    await call.bot.send_photo(chat_id=i[1], photo=data.get('photo'), caption=data.get('tag'))
            await call.message.answer(text="Reklama yuborildi!\nEndi nima qilmoqchisiz?", reply_markup=AdminButton)
        elif data.get('video'):
            for i in baza.read('users', "*"):
                if i[1] != call.from_user.id:
                    await call.bot.send_video(chat_id=i[1], video=data.get('video'), caption=data.get('tag'))
            await call.message.answer(text="Reklama yuborildi!\nEndi nima qilmoqchisiz?", reply_markup=AdminButton)
    if xabar == 'yoq':
        await call.message.answer(text="Reklama yuborish bekor qilindi\nNima qilmoqchisiz?", reply_markup=AdminButton)
    await state.set_state(Start.admin)
    await call.message.delete()

### Admin qo'shish o'chirish joyi
@admin_router.callback_query(F.data, Admin.admin_add_remov)
async def AdminAddRemov(call:CallbackQuery, state:FSMContext):
    xabar = call.data
    if xabar == 'admin bosh menyuga qaytish':
        await call.message.answer(text=f"Siz adminsiz", reply_markup=AdminButton)
        await state.set_state(Start.admin)
    if xabar == 'admin_add':
        await state.update_data(add_remov=xabar)
        await call.message.answer(text="Qo'shmoqchi bo'lgan adminingizning contactini yuboring.\nQo'shmoqchi bo'lgan adminingiz oldin botga start bosgan bo'lishi kerak!")
        await state.set_state(Admin.admin_add)
    if xabar == 'admin_remov':
        if AdminRemovButtons() == None:
            await call.message.answer(text="Bu knopkada xatolik qaytdi iltimos hozircha boshqa knopkani tanlang", reply_markup=a_r_admin)
            await state.set_state(Admin.admin_add_remov)
        else:
            await state.update_data(add_remov=xabar)
            await call.message.answer(text="Qaysi admini o'chirmoqchisiz?", reply_markup=AdminRemovButtons())
            await state.set_state(Admin.admin_remov)
    await call.message.delete()

### Admin o'chirish joyi
@admin_router.callback_query(F.data, Admin.admin_remov)
async def AdminRemovBot(call:CallbackQuery, state:FSMContext):
    xabar = call.data
    if xabar == 'admin remov':
        await call.message.answer(text="Bu knopkalar orqali siz yangi admin qo'sholasiz yoki bor adminni o'chira olasiz", reply_markup=a_r_admin)
        await state.set_state(Admin.admin_add_remov)
    else:
        tg_id = xabar.split('-')[1]
        if int(tg_id) != 6378609931:
            ism = xabar.split('-')[2]
            id = xabar.split('-')[0]
            raqam = xabar.split('-')[3]
            await state.update_data(admin_ism=ism)
            await state.update_data(admin_id=id)
            await state.update_data(admin_tg_id=tg_id)
            await state.update_data(admin_raqam=raqam)
            await call.message.answer(text=f"Admin\nIsmi: {ism}\nTelegram raqam: {raqam}\nTelegram id: {id}\n\nRostan ham bu adminni o'chirmoqchimisiz?", reply_markup=sorash)
            await state.set_state(Admin.admin_tasdiqlash)
        else:
            await call.message.answer(text="Bu bosh admin buni o'chirib bo'lmaydi. Boshqa adminni o'chirishga xarakat qilib ko'ring", reply_markup=AdminRemovButtons())
            await state.set_state(Admin.admin_remov)
    await call.message.delete()

### Admin qo'shish joyi
@admin_router.message((F.contact | F.text), Admin.admin_add)
async def AadminAdd(message:Message, state:FSMContext):
    if message.contact:
        tel = message.contact.phone_number
        name = message.contact.first_name
        id = message.contact.user_id
        await state.update_data(tel = tel)
        await state.update_data(name = name)
        await state.update_data(id = id)
        await message.answer(text=f"Siz qo'shmoqchi bo'lgan amdin malumotlari\nIsmi: {name}\nTel raqam: {tel}\nId raqam: {id}\n\nBu userni qo'shishni tasdiqlaysizmi?", reply_markup=sorash)
        await state.set_state(Admin.admin_tasdiqlash)
    else:
        await message.answer('Ilimos yangi admining contactini yuboring')
        await state.set_state(Admin.admin_add)
    await message.delete()

#### Admin qo'shishni tasdiqlash
@admin_router.callback_query(F.data, Admin.admin_tasdiqlash)
async def AdminTasdiqlash(call:CallbackQuery, state:FSMContext):
    xabar = call.data
    data = await state.update_data()
    if xabar == 'ha':
        if data.get('add_remov') == 'admin_add':
            baza.insert('admin', telegram_id=int(data.get('id')), user=data.get('name'), phone=f'{data.get('tel')}')
            await call.message.answer(text="Yangi admin qo'shildi!\nNima qilmoqchisiz?", reply_markup=a_r_admin)
        elif data.get('add_remov') == 'admin_remov':
            baza.delete('admin',manzil_name=f'id = {int(data.get('admin_id'))}')
            await call.message.answer(text="Siz tanlagan admin o'chirildi!\nEndi nima qilmoqchisiz?", reply_markup=a_r_admin)
        await state.set_state(Admin.admin_add_remov)
    elif xabar == 'yoq':
        if data.get('add_remov') == 'admin_add':
            await call.message.answer(text="Yangi admin qo'shish bekor qlindi!\nNima qilmoqchisiz?", reply_markup=a_r_admin)
        elif data.get('add_remov') == 'admin_remov':
            await call.message.answer(text="Admin o'chirish bekor qilindi!\nNima qiloqchisiz?", reply_markup=a_r_admin)
        await state.set_state(Admin.admin_add_remov)
    await call.message.delete()

### Knopka qo'shish, o'chirish va yangilashni bo'lib yuborish
@admin_router.callback_query(F.data, Admin.button_add_remov_replay)
async def CtegoryaAndProduct(call:CallbackQuery, state:FSMContext):
    xabar = call.data
    await call.answer('Iltimos kuting...')
    await asyncio.sleep(1)
    if xabar == 'knopka_add':
        await state.update_data(work=xabar)
        await call.message.answer(text='Qo\'shmoqchi bo\'lgan knopkangizning turini tanlang', reply_markup=categorya_product)
        await state.set_state(Admin.a_r_r_button)
    elif xabar == 'knopka_remov':
        await state.update_data(work=xabar)
        await call.message.answer(text="Qayerdagi knopkani o'chirmoqchisiz?", reply_markup=categorya_product)
        await state.set_state(Admin.a_r_r_button)
    elif xabar == 'knopka_replay':
        await state.update_data(work=xabar)
        await call.message.answer(text="Qayerdagi knopkani yangilamoqchisiz?", reply_markup=categorya_product)
        await state.set_state(Admin.a_r_r_button)
    elif xabar == 'admin bosh menyuga qaytish':
        await call.message.answer(text=f"Siz adminsiz", reply_markup=AdminButton)
        await state.set_state(Start.admin)
    await call.message.delete()

### Categorya yoki productaga bo'lib yuborish
@admin_router.callback_query(F.data, Admin.a_r_r_button)
async def CategoryaAdd(call:CallbackQuery, state:FSMContext):
    xabar = call.data
    await call.answer('Iltimos kuting...')
    await asyncio.sleep(1)
    data = await state.get_data()
    if xabar == 'categorya':
        await state.update_data(c_and_p=xabar)
        if data.get('work')=='knopka_add':
            await call.message.answer(text='Categorya nomini yozing')
            await state.set_state(Admin.catogorya_name)
        elif data.get('work')=='knopka_remov':
            if CategoryaAddRemovReplay() == None:
                await call.message.answer(text='Hali categoryada maxsulot yo\'q oldin cateogya qo\'shing!', reply_markup=c_p_button)
                await state.set_state(Admin.button_add_remov_replay)
            else:
                await call.message.answer(text="Qaysi categoryani o'chirmoqchisiz?", reply_markup=CategoryaAddRemovReplay())
                await state.set_state(Admin.categorya_remov)
        elif data.get('work')=='knopka_replay':
            if CategoryaAddRemovReplay() == None:
                await call.message.answer(text='Hali categoryada maxsulot yo\'q oldin cateogya qo\'shing!', reply_markup=c_p_button)
                await state.set_state(Admin.button_add_remov_replay)
            else:
                await call.message.answer(text="Qaysi categoryani malumotlarini o'zgartirmoqchisiz?", reply_markup=CategoryaAddRemovReplay())
                await state.set_state(Admin.categorya_reply)
    elif xabar == 'product':
        await state.update_data(c_and_p = xabar)
        if data.get('work')=='knopka_add':
            await call.message.answer(text='Qaysi categoryaga product qo\'shmoqchisiz?', reply_markup=CategoryaAddRemovReplay())
            await state.set_state(Admin.categorya_id)
        elif data.get('work')=='knopka_remov':
            if ProductAddRemovReplay(-1) == None:
                await call.message.answer(text='Hali productada maxsulot yo\'q oldin producta qo\'shing!', reply_markup=c_p_button)
                await state.set_state(Admin.button_add_remov_replay)
            else:
                await call.message.answer(text="Qaysi categoryadagi productani o'chirmoqchisiz?", reply_markup=CategoryaAddRemovReplay())
                await state.set_state(Admin.categorya_id)
        elif data.get('work')=='knopka_replay':
            if CategoryaAddRemovReplay() == None:
                await call.message.answer(text='Hali categorya maxsulot yo\'q oldin cateogya qo\'shing!', reply_markup=c_p_button)
                await state.set_state(Admin.button_add_remov_replay)
            if ProductAddRemovReplay() == None:
                await call.message.answer(text="Producta table bo'sh oldin poducta qo'shing", reply_markup=c_p_button)
                await state.set_state(Admin.button_add_remov_replay)
            else:
                await call.message.answer(text="Qaysi categoryadagi prducta malumotlarini o'zgartirmoqchisiz?", reply_markup=CategoryaAddRemovReplay())
                await state.set_state(Admin.categorya_id)
    elif xabar == 'knopka menyuga qaytish':
        await call.message.answer(text="Bu knopkalar orqali siz categorya va producta qo'shishingiz, o'chirishingiz va bor knopkalarni yangilashingiz mumkin", reply_markup=c_p_button)
        await state.set_state(Admin.button_add_remov_replay)
    await call.message.delete()

### Categoryani tanlash
@admin_router.callback_query(Admin.categorya_id)
async def CategoryaId(call:CallbackQuery, state:FSMContext):
    xabar = call.data
    data = await state.get_data()
    if xabar == 'admin bosh menyuga qaytish':
        if data.get('work') == 'knopka_add':
            await call.message.answer(text='Qo\'shmoqchi bo\'lgan knopkangizning turini tanlang', reply_markup=categorya_product)
        elif data.get('work') == 'knopka_remov':
            await call.message.answer(text="Qayerdagi knopkani o'chirmoqchisiz?", reply_markup=categorya_product)
        elif data.get('work') == 'knopka_replay':
            await call.message.answer(text="Qayerdagi knopkani yangilamoqchisiz?", reply_markup=categorya_product)
        await state.set_state(Admin.a_r_r_button)
    else:
        if data.get('work') == 'knopka_add':
            await state.update_data(categorya_id = int(xabar.split("-")[-1]))
            await state.update_data(categorya_nomi = xabar.split('-')[0])
            await call.message.answer(text='Endi qo\'shmoqchi bo\'lgan productangizni nomini yozing')
            await state.set_state(Admin.producta_name)
        elif data.get('work') == 'knopka_remov':
            try:
                if int(xabar.split('-')[-1]) in [i[-1] for i in baza.read('product','*')]:
                    await state.update_data(categorya_id = int(xabar.split("-")[-1]))
                    await state.update_data(categorya_nomi = xabar.split('-')[0])
                    await call.message.answer(text="Qaysi productani o'chirmoqchisiz?", reply_markup=ProductAddRemovReplay(id=int(xabar.split('-')[-1])))
                    await state.set_state(Admin.producta_remov)
                else:
                    await call.message.answer(text="Bu categoryada malumot yo'q\nQaysi categoryadagi productani o'chirmoqchisiz?", reply_markup=CategoryaAddRemovReplay())
            except Exception as e:
                print("Categoryaga keirishda xatolik!", e)
        elif data.get('work') == 'knopka_replay':
            try:
                if int(xabar.split('-')[-1]) in [i[-1] for i in baza.read('product','*')]:
                    await state.update_data(categorya_id = int(xabar.split("-")[-1]))
                    await state.update_data(categorya_nomi = xabar.split('-')[0])
                    await call.message.answer(text="Qaysi productaning malumotlarini o'zgartirmoqchisiz?", reply_markup=ProductAddRemovReplay(id=int(xabar.split("-")[-1])))
                    await state.set_state(Admin.producta_replay)
                else:
                    await call.message.answer(text="Bu categoryada hali producta yo'q!\nQaysi categoryadagi productaning malumotlarini yangilamoqchisiz?", reply_markup=CategoryaAddRemovReplay())
                    await state.set_state(Admin.categorya_id)
            except Exception as e:
                print("Producta malumotlarini o'zgartirishda xatolik! ", e)
    await call.message.delete()

### Categoryada qayerini yangilashni so'raydi
@admin_router.callback_query(F.data, Admin.producta_replay)
async def ProdductaReplay(call:CallbackQuery, state:FSMContext):
    xabar = call.data
    data = await state.get_data()
    if xabar == 'admin bosh menyuga qaytish':
        await call.message.answer(text="Qaysi categoryadagi prducta malumotlarini o'zgartirmoqchisiz?", reply_markup=CategoryaAddRemovReplay())
        await state.set_state(Admin.categorya_id)
    else:
        await state.update_data(praducta_id = int(xabar.split('-')[-1]))
        for i in baza.read('product','*', where_name=f'id = {int(xabar.split('-')[-1])}'):
            await state.update_data(e_pr_nomi = i[1])
            await state.update_data(e_pr_narxi = i[2])
            await state.update_data(e_pr_rasmi = i[3])
            await call.message.answer_photo(photo=i[3], caption=f"Categorya nomi: {data.get('categorya_nomi')}\nProducta nomi: {i[1]}\nProducta narxi: {i[2]} so'm\n\nBu productaning qaysi malumotini o'zgartirmoqchisiz?", reply_markup=replay_buttons_p)
            await state.set_state(Admin.replay_buttons)
    await call.message.delete()
            
### Replay buttons 
@admin_router.callback_query(F.data, Admin.replay_buttons)
async def ReplayButtons(call:CallbackQuery, state:FSMContext):
    xabar = call.data
    data = await state.get_data()
    if xabar == 'replay orqaga':
        await call.message.answer(text="Qaysi categoryani malumotlarini o'zgartirmoqchisiz?", reply_markup=CategoryaAddRemovReplay())
        await state.set_state(Admin.categorya_reply)
    if xabar == 'replay orqaga producta':
        await call.message.answer(text="Qaysi productaning malumotlarini o'zgartirmoqchisiz?", reply_markup=ProductAddRemovReplay(id=int(data.get('categorya_id'))))
        await state.set_state(Admin.producta_replay)
    else:
        await state.update_data(r_turi = xabar)
        if xabar == 'categorya':
            await call.message.answer(text=mesages[data.get('c_and_p')][xabar], reply_markup=CategoryaAddRemovReplay())
            await state.set_state(Admin.producta_replay_call)
        else:
            await call.message.answer(text=mesages[data.get('c_and_p')][xabar])
            await state.set_state(Admin.replay_tasdiqlash)
    await call.message.delete()

### Replay productaning categorya knopkasi
@admin_router.callback_query(F.data, Admin.producta_replay_call)
async def CategoryaOrBack(call:CallbackQuery, state:FSMContext):
    xabar = call.data
    data = await state.get_data()
    id = data.get('praducta_id')
    if xabar == 'admin bosh menyuga qaytish':
        for i in baza.read('product','*', where_name=f'id = {int(id)}'):
            await call.message.answer_photo(photo=i[3], caption=f"Categorya nomi: {data.get('categorya_nomi')}\nProducta nomi: {i[1]}\nProducta narxi: {i[2]} so'm\n\nBu productaning qaysi malumotini o'zgartirmoqchisiz?", reply_markup=replay_buttons_p)
            await state.set_state(Admin.replay_buttons)
    else:
        print(xabar.split('-'))
        await state.update_data(t_c_id = int(xabar.split('-')[-1]))
        for i in baza.read('product','*', where_name=f'id = {int(id)}'):
            await call.message.answer_photo(photo=i[3], caption=f"Eski categorya nomi: {data.get('categorya_nomi')}\nYangi categorya nomi: {xabar.split('-')[0]}\nProducta nomi: {i[1]}\nProducta narxi: {i[2]} so'm\n\nRostan ham bu productaning categoryasini o'zgartirmoqchimisiz?", reply_markup=sorash)
            await state.set_state(Admin.tasdiqlash)
    await call.message.delete()
 
### Replay textni tasdiqlashni so'rash
@admin_router.message((F.text | F.photo), Admin.replay_tasdiqlash)
async def ReplayTasdiqlashText(message:Message, state:FSMContext):
    xabar = message.text if message.text else None
    photo = message.photo[-1].file_id if message.photo else None
    data = await state.get_data()
    print(xabar)
    if data.get('c_and_p') == 'categorya':
        print(1)
        cat_mal = data.get('c_malumot')
        cat_nomi = cat_mal.split('_')[1]
        cat_rasmi = cat_mal.split('_')[2]
        print(cat_rasmi)
        if data.get('r_turi', None) == 'nomi':
            if xabar:
                await state.update_data(c_new_name = xabar)
                await message.answer_photo(photo=cat_rasmi, caption=f"Categorya\nEski nomi: {cat_nomi}\nYangi nomi: {xabar}\nO'zgartirishni xoxlaysizmi?", reply_markup=sorash)
                await state.set_state(Admin.tasdiqlash)
            else:
                await message.answer('Iltimos matn yuboring!')
                await state.set_state(Admin.replay_tasdiqlash)
        if data.get('r_turi') == 'rasmi':
            if photo:
                await state.update_data(c_new_photo = photo)
                img = [
                    InputMediaPhoto(media=f"{cat_rasmi}", caption='Eski rasmi'),
                    InputMediaPhoto(media=f"{photo}", caption='Yangi rasmi')
                ]
                await message.bot.send_media_group(chat_id=message.from_user.id, media=img)
                await message.answer(text=f'Eski rasmi va yangi rasmi\nTuri: Categotrya\nNomi: {cat_nomi}\n\nRostan ham rasmini o\'zgartirmoqchimisiz?', reply_markup=sorash)
                await state.set_state(Admin.tasdiqlash)
            else:
                await message.answer('Iltimos productaning yangi rasmini yuboring!')
                await state.set_state(Admin.replay_tasdiqlash)
    
    elif data.get('c_and_p') == 'producta':
        if data.get('r_turi', None) == 'nomi':
            if xabar:
                await state.update_data(p_new_name = xabar)
                await message.answer_photo(photo=data.get('e_pr_rasmi'), caption=f"Categorya nomi: {data.get('categorya_nomi')}\nProductaning eski nomi: {data.get('e_pr_nomi')}\nProductaning yangi nomi: {xabar}\nProducta narxi: {data.get('e_pr_narxi')} so'm\n\nO'zgartirishni xoxlaysizmi?", reply_markup=sorash)
                await state.set_state(Admin.tasdiqlash)
            else:
                await message.answer('Iltimos matn yuboring!')
                await state.set_state(Admin.replay_tasdiqlash)
        if data.get('r_turi') == 'narxi':
            if xabar.isdigit():
                await state.update_data(p_new_narxi = xabar)
                await message.answer_photo(photo=data.get('e_pr_rasmi'), caption=f"Categorya nomi: {data.get('categorya_nomi')}\nProducta nomi: {data.get('e_pr_nomi')}\nProductaning eski narxi: {data.get('e_pr_narxi')} so'm\nProductaning yangi narxi: {xabar} so'm\n\nO'zgartirishni xoxlaysizmi?", reply_markup=sorash)
                await state.set_state(Admin.tasdiqlash)
            else:
                await message.answer('Iltimos faqat summa raqamini kiriting\nMasalan: 25000')
                await state.set_state(Admin.replay_tasdiqlash)
        if data.get('r_turi') == 'rasmi':
            if photo:
                await state.update_data(p_new_rasmi = photo)
                img = [
                    InputMediaPhoto(media=f'{data.get('e_pr_rasmi')}', caption='Eski rasim'),
                    InputMediaPhoto(media=f'{photo}', caption='Yangi rasim')
                ]
                await message.bot.send_media_group(chat_id=message.from_user.id, media=img)
                await message.answer(text=f"Categorya nomi: {data.get('categorya_nomi')}\nProductaning nomi: {data.get('e_pr_nomi')}\nProducta narxi: {data.get('e_pr_narxi')} so'm\n\nO'zgartirishni xoxlaysizmi?", reply_markup=sorash)
                await state.set_state(Admin.tasdiqlash)
            else:
                await message.answer(text="Iltimos faqat rasim yuboring")
                await state.set_data(Admin.replay_tasdiqlash)
    await message.delete()

### Tasdiqlash funksiyasi
@admin_router.callback_query(F.data, Admin.tasdiqlash)
async def Tasdiqlash(call:CallbackQuery, state:FSMContext):
    xabar = call.data
    data = await state.get_data()
    if xabar == 'ha':                                                                           #### Ha
        if data.get('c_and_p') == 'categorya':
            if data.get('work') == 'knopka_add':
                AddCategorya(name=data.get('categorya_name'), photo=data.get('categorya_photo'))
                await call.message.answer(text='Categorya qo\'shildi!\nNima qilmoqchisiz?', reply_markup=c_p_button)
            elif data.get('work') == 'knopka_remov':
                RemoveCategorya(id=int(data.get('categorya_remov_id')))
                await call.message.answer(text="Categorya o'chirildi!\nNima qilmoqchisiz?", reply_markup=c_p_button)
            elif data.get('work') == 'knopka_replay':
                if data.get('r_turi') == 'nomi':
                    baza.update('categorya',yangi_name=f'name = "{data.get('c_new_name')}"', manzil_name=f'id = {int(data.get('c_malumot').split('_')[0])}')
                    await call.message.answer('Categorya nomi o\'zgartirildi!\nNima qilmoqchisiz?', reply_markup=c_p_button)
                if data.get('r_turi') == 'rasmi':
                    baza.update('categorya',yangi_name=f'rasm = "{data.get('c_new_photo')}"', manzil_name=f'id = {int(data.get('c_malumot').split('_')[0])}')
                    await call.message.answer('Categorya rasmi o\'zgartirildi!\nNima qilmoqchisiz?', reply_markup=c_p_button)
            await state.set_state(Admin.button_add_remov_replay)
        elif data.get('c_and_p') == 'product':
            if data.get('work') == 'knopka_add':
                AddProduct(nomi=data.get('producta_name'), narxi=int(data.get('producta_narx')), rasmi=data.get('producta_rasm'), categorya_id=int(data.get('categorya_id')))
                await call.message.answer(text='Producta qo\'shildi!\nNima qilmoqchisiz?', reply_markup=c_p_button)
            elif data.get('work') == 'knopka_remov':
                baza.delete('product', manzil_name=f'id = {int(data.get('c_id'))}')
                await call.message.answer(text='Producta o\'chirildi!\nNima qilmoqchisiz?', reply_markup=c_p_button)
            elif data.get('work') == 'knopka_replay':
                print('categorya replay')
                if data.get('r_turi') == 'categorya':
                    baza.update('product',yangi_name=f'categorya_id = {int(data.get('t_c_id'))}', manzil_name=f'id = {int(data.get('praducta_id'))}')
                    await call.message.answer(text="Producta boshqa categoryaga o'zgartirildi!\nNima qilmoqchisiz?", reply_markup=c_p_button)
                if data.get('r_turi') == 'nomi':
                    baza.update('product',yangi_name=f'name = "{data.get('p_new_name')}"', manzil_name=f'id = {int(data.get('praducta_id'))}')
                    await call.message.answer(text="Producta nomi o'zgartirildi!\nNima qilmoqchisiz?", reply_markup=c_p_button)
                if data.get('r_turi') == 'narxi':
                    baza.update('product', yangi_name=f'narxi = "{data.get('p_new_narxi')}"', manzil_name=f'id = {int(data.get('praducta_id'))}')
                    await call.message.answer(text="Producta narxi o'zgartirildi!\nNima qilmoqchisiz?", reply_markup=c_p_button)
                if data.get('r_turi') == 'rasmi':
                    baza.update('producta',yangi_name=f'rasmi = "{data.get('p_new_rasmi')}"', manzil_name=f'id = {int(data.get('praducta_id'))}')
                    await call.message.answer(text="Producta rasmi o'zgartirildi!\nNima qilmoqchisiz?", reply_markup=c_p_button)
            await state.set_state(Admin.button_add_remov_replay)
    if xabar == 'yoq':                                                                             #### Yo'q
        if data.get('c_and_p') == 'categorya':
            if data.get('work') == 'knopka_add':
                await call.message.answer(text='Categorya qo\'shilmadi!\nNima qilmoqchisiz?', reply_markup=c_p_button)
            elif data.get('work') == 'knopka_remov':
                await call.message.answer(text="Categorya o'chirilmadi!\nNima qilmoqchisiz?", reply_markup=c_p_button)
            elif data.get('work') == 'knopka_replay':
                if data.get('r_turi') == 'nomi':
                    await call.message.answer(text='Categorya nomini o\'zgartirish bekor qilindi!\nNima qilmoqchisiz?', reply_parameters=c_p_button)
                if data.get('r_turi') == 'rasmi':
                    await call.message.answer(text="Categorya rasmini o'zgartirish  bekor qilindi!\nNima qilmoqchisiz?", reply_markup=c_p_button)
            await state.set_state(Admin.button_add_remov_replay)
        elif data.get('c_and_p') == 'product':
            if data.get('work') == 'knopka_add':
                await call.message.answer(text='Producta qo\'shilmadi!\nNima qilmoqchisiz?', reply_markup=c_p_button)
            elif data.get('work') == 'knopka_remov':
                await call.message.answer(text='Producta o\'chirildi!\nNima qilmoqchisiz?', reply_markup=c_p_button)
            elif data.get('work') == 'knopka_replay':
                print('categorya replay')
                if data.get('r_turi') == 'categorya':
                    await call.message.answer(text="Productani boshqa categoryaga o'zgartirish bekor qilindi!\nNima qilmoqchisiz?", reply_markup=c_p_button)
                if data.get('r_turi') == 'nomi':
                    await call.message.answer(text="Producta nomini o'zgartirish bekor qilindi!\nNima qilmoqchisiz?", reply_markup=c_p_button)
                if data.get('r_turi') == 'narxi':
                    await call.message.answer(text="Producta narxini o'zgartirish bekor qilindi!\nNima qilmoqchisiz?", reply_markup=c_p_button)
                if data.get('r_turi') == 'rasmi':
                    await call.message.answer(text="Producta rasmini o'zgartirish bekor qilindi!\nNima qilmoqchisiz?", reply_markup=c_p_button)
            await state.set_state(Admin.button_add_remov_replay)          
    await call.message.delete()

### Categorya qo'shish 
@admin_router.message(F.text, Admin.catogorya_name)
async def CategoryaName(message:Message, state:FSMContext):
    xabar = message.text
    await state.update_data(categorya_name = xabar)
    await message.answer(text='Endi esa qo\'shmoqchi bo\'lgan categoryangizni rasmini yuboring')
    await state.set_state(Admin.categorya_photo)
    await message.delete()

@admin_router.message(F.photo, Admin.categorya_photo)
async def CategoryaPhoto(message:Message, state:FSMContext):
    photo = message.photo[-1].file_id
    data = await state.get_data()
    await state.update_data(categorya_photo = photo)
    await message.answer_photo(photo=photo, caption=f"Yangi categorya\nNomi: {data.get('categorya_name')}\n\nRostan ham bu categoryani qo'shmoqchimisiz?", reply_markup=sorash)
    await state.set_state(Admin.tasdiqlash)
    await message.delete()

### Producta qo'shish nomini
@admin_router.message(F.text, Admin.producta_name)
async def ProductaNomi(message:Message, state:FSMContext):
    xabar = message.text
    await state.update_data(producta_name = xabar)
    await message.answer(text="Enid esa producta narxini kirting\nMasaln: 20000")
    await state.set_state(Admin.producta_narxi)
    await message.delete()

### Producta narxi
@admin_router.message(F.text, Admin.producta_narxi)
async def ProductNarxi(message:Message, state:FSMContext):
    xabar = message.text
    if xabar.isdigit():
        await state.update_data(producta_narx=xabar)
        await message.answer(text='Endi producta rasmini kiriting')
        await state.set_state(Admin.producta_rasmi)
    else:
        await message.answer(text=f"{xabar} bu xato. Iltimos faqat raqam kiriting.")
        await state.set_state(Admin.producta_narxi)
    await message.delete()

### Producta rasmi
@admin_router.message(F.photo, Admin.producta_rasmi)
async def ProductaRasmi(message:Message, state:FSMContext):
    photo = message.photo[-1].file_id
    if photo:
        data = await state.get_data()
        await state.update_data(producta_rasm = photo)
        await message.answer_photo(photo=photo, caption=f"Yangi producta\nCategorya: {data.get('categorya_nomi')}\nNomi: {data.get('producta_name')}\nNarxi: {data.get('producta_narx')} so'm\n\nRostan ham bu productani qo'shmoqchisiz?", reply_markup=sorash)
        await state.set_state(Admin.tasdiqlash)
    else:
        await message.answer(text="Iltimos rasim yuboring")
        await state.set_state(Admin.producta_rasmi)
    await message.delete()

### Categorya o'chirish
@admin_router.callback_query(F.data, Admin.categorya_remov)
async def CategoryaRemov(call:CallbackQuery, state:FSMContext):
    xabar = call.data
    if xabar == 'admin bosh menyuga qaytish':
        await call.message.answer(text="Qayerdagi knopkani o'chirmoqchisiz?", reply_markup=categorya_product)
        await state.set_state(Admin.a_r_r_button)
    else:
        try:
            for i in baza.read('categorya', '*'):
                if int(xabar.split('-')[-1]) == i[0]:
                    await state.update_data(categorya_remov_id=i[0])
                    await call.message.answer_photo(photo=i[-1], caption=f"Nomi: {i[1]}\n\nRostan ham bu categoryani o'chirmoqchmisiz?", reply_markup=sorash)
                    await state.set_state(Admin.tasdiqlash)
        except Exception as e:
            print('Categoryani o\'chirishda xatolik: ', e)
    await call.message.delete()

### Productani o'chirish knopkasi
@admin_router.callback_query(F.data, Admin.producta_remov)
async def ProductaRemov(call:CallbackQuery, state:FSMContext):
    xabar = call.data
    data = await state.get_data()
    if xabar == "admin bosh menyuga qaytish":
        await call.message.answer(text="Qaysi categoryadagi productani o'chirmoqchisiz?", reply_markup=CategoryaAddRemovReplay())
        await state.set_state(Admin.categorya_id)
    else:
        try:
            for i in baza.read('product', "*"):
                if i[0]==int(xabar.split('-')[-1]):
                    await state.update_data(c_id = i[0])
                    await call.message.answer_photo(photo=i[-2], caption=f"Categorya nomi: {data.get('categorya_nomi')}\nProducta nomi: {i[1]}\nNarxi: {i[2]} so'm\n\nRostan ham bu productani o'chirmoqchimisiz?", reply_markup=sorash)
                    await state.set_state(Admin.tasdiqlash)
        except Exception as e:
            print('Producta o\'chirishda xatolik!', e)
    await call.message.delete()

### Categorya Replay
@admin_router.callback_query(F.data, Admin.categorya_reply)
async def ReplyaCategoryaBot(call:CallbackQuery, state:FSMContext):
    xabar = call.data
    if xabar == 'admin bosh menyuga qaytish':
        await call.message.answer(text="Qayerdagi knopkani yangilamoqchisiz?", reply_markup=categorya_product)
        await state.set_state(Admin.a_r_r_button)
    else:
        for i in baza.read('categorya',"*"):
            if i[0]==int(xabar.split('-')[-1]):
                await state.update_data(c_malumot = f'{i[0]}_{i[1]}_{i[2]}')
                await call.message.answer_photo(photo=i[2], caption=f"Nomi: {i[1]}\n\nBu categoryaning nimasini o'zgartirmoqchisiz?", reply_markup=replay_buttons)
                await state.set_state(Admin.replay_buttons)
    await call.message.delete()