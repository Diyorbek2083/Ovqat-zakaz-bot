from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from data.databaza import baza

### Locatsiyani ulashish
lacation = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📍 Manzilni yuborish", request_location=True)
        ]
    ], resize_keyboard=True
)

### Telefon ulashish knopkasi
telephone = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="☎️ Cantact ulashish", request_contact=True)
        ]
    ], resize_keyboard=True
)

### Izohlarni o'qish dagi konpkalar
def AdminIzohlar(id:int):
    button = InlineKeyboardBuilder()
    indx = [i[0] for i in baza.read('izohlar','*')]
    a = baza.read('izohlar','*',where_name=f'id = {id}')
    button.button(text="Javob yozish ✍️", callback_data=f'javob_{id}')
    button.button(text="O'chirib tashlash", callback_data=f"bekor_{id}")
    if len(baza.read('izohlar','*'))==1:
        button.button(text='⬅️ Orqaga qaytish', callback_data='orqaga')       
    elif min(indx)==id:
        button.button(text='⬅️ Orqaga qaytish', callback_data='orqaga')
        button.button(text="▶️ Keyingi izoh", callback_data=f"keyingi_{indx[indx.index(id)+1]}")
    elif max(indx)==id:
        button.button(text='⬅️ Orqaga qaytish', callback_data='orqaga')
        button.button(text="◀️ Oldingi izoh", callback_data=f"oldingi_{indx[indx.index(id)-1]}")
    else:
        button.button(text="◀️ Oldingi izoh", callback_data=f"oldingi_{indx[indx.index(id)-1]}")
        button.button(text="▶️ Keyingi izoh", callback_data=f"keyingi_{indx[indx.index(id)+1]}")
        button.button(text='⬅️ Orqaga qaytish', callback_data='orqaga')
    button.adjust(2)
    return button.as_markup()

### Orqaga knopka
ortga = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='◀️ Orqaga', callback_data='orqaga')
        ]
    ]
)

### Replay button producta
replay_buttons_p = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Nomi', callback_data='nomi'),
            InlineKeyboardButton(text='Narxi', callback_data='narxi')
        ],
        [
            InlineKeyboardButton(text='Rasmi', callback_data='rasmi'),
            InlineKeyboardButton(text='Categoryasi', callback_data='categorya')
        ],
        [
            InlineKeyboardButton(text='◀️ Orqaga', callback_data='replay orqaga producta')
        ]
    ]
)

### Replay button categorya
replay_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Nomi', callback_data='nomi'),
            InlineKeyboardButton(text='Rasmi', callback_data='rasmi')
        ],
        [
            InlineKeyboardButton(text='◀️ Orqaga', callback_data='replay orqaga')
        ]
    ]
)

### Admin Start bosganda chiqadigan knopkalar
AdminButton = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Knopka ➕➖🔄', callback_data='button_add_remov_replay'),
            InlineKeyboardButton(text='Admin ➕➖', callback_data='admin_add_remov')
        ],
        [
            InlineKeyboardButton(text='Reklama yuborish ✈️', callback_data='reklama_yuborish'),
            InlineKeyboardButton(text="Bot haqidagi izohlar 💬", callback_data="bot haqida izohlar")
        ],
        [
            InlineKeyboardButton(text="Biz bilan bog'lanish ", callback_data='biz bilan boglanish'),
            InlineKeyboardButton(text='Knopkalarni tekshirish 👀', callback_data='knopka_tekshirish')
        ],
        [
            InlineKeyboardButton(text="Statistika 📊", callback_data='statistika')
        ]
    ]
)

### User Start bosganda chiqadigan knopkalar
def UserButton():
    try:
        buton = InlineKeyboardBuilder()
        categories = baza.read('categorya', '*')
        if not categories:
            print("Kategoriya table bo'sh!")
        for i in categories:
            if len(i) < 2:
                continue
            buton.button(text=i[1], callback_data=f'{i[1]}-{i[0]}')
        buton.button(text="Bog'lanish 📞", callback_data='boglanish')
        buton.button(text='Zakaz berish 🛒', callback_data='zakaz_berish')
        buton.adjust(2)
        return buton.as_markup()
    except Exception as e:
        print(f"User menyuga knopka yaratishda xatolik: {e}")
        return None
    
### Qo'shish, o'chirish va yangilash knopkalari
c_p_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Knopka ➕',callback_data='knopka_add'),
            InlineKeyboardButton(text='Knopka ➖',callback_data='knopka_remov'),
            InlineKeyboardButton(text='Knopka 🔄', callback_data='knopka_replay')
        ],
        [
            InlineKeyboardButton(text='◀️ Orqaga', callback_data='admin bosh menyuga qaytish')
        ]
    ]
)

a_r_admin = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Admin ➕',callback_data='admin_add'),
            InlineKeyboardButton(text='Admin ➖',callback_data='admin_remov')
        ],
        [
            InlineKeyboardButton(text='◀️ Orqaga', callback_data='admin bosh menyuga qaytish')
        ]
    ]
)

bot_malumotlari = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Bot manzili 🤖',callback_data='bot manzilini yangilash'),
            InlineKeyboardButton(text='Admin manzili 🙎‍♂️', callback_data='admin manzili yangilash')
        ],
        [
            InlineKeyboardButton(text='Instagram manzil 🟥', callback_data='instagram manzili yangilash'),
            InlineKeyboardButton(text='Telefon raqam 📞',callback_data='telefon raqamni yangilash')
        ],
        [
            InlineKeyboardButton(text='📍 Bizning manzil', callback_data='bizning manzil')
        ],
        [
            InlineKeyboardButton(text='◀️ Orqaga', callback_data='admin bosh menyuga qaytish')
        ]
    ]
)

###  Admin button tekshirish
def AdminSeeButton():
    try:
        buton = InlineKeyboardBuilder()
        categories = baza.read('categorya', '*')
        if not categories:
            print("Kategoriya table bo'sh!")
        for i in categories:
            if len(i) < 2:
                continue
            buton.button(text=i[1], callback_data=f'{i[1]}-{i[0]}')
        buton.button(text="Bog'lanish 📞", callback_data='boglanish')
        buton.button(text='Zakaz berish 🛒', callback_data='zakaz_berish')
        buton.button(text='◀️ Orqaga', callback_data='ortga')
        buton.adjust(2)
        return buton.as_markup()
    except Exception as e:
        print(f"Admin tekshirish funksiyasida xato qaytdi: {e}")
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Bog'lanish 📞", callback_data='boglanish'),
                    InlineKeyboardButton(text='Zakaz berish 🛒', callback_data='zakaz_berish'),
                ],
                [
                    InlineKeyboardButton(text='◀️ Orqaga', callback_data='ortga') 
                ]
            ]
        )
    
### Ctegorya And Product Button
categorya_product = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Categorya',callback_data='categorya'),
            InlineKeyboardButton(text='Product', callback_data='product')
        ],
        [
            InlineKeyboardButton(text='◀️ Orqaga', callback_data='knopka menyuga qaytish') 
        ]
    ]
)

### Categorya add, remov and replay
def CategoryaAddRemovReplay():
    try:
        buton = InlineKeyboardBuilder()
        categories = baza.read('categorya', '*')
        if not categories:
            print("Kategoriya table bo'sh!")
        for i in categories:
            if len(i) < 2:
                continue
            buton.button(text=i[1], callback_data=f'{i[1]}-{i[0]}')
        buton.button(text='◀️ Orqaga', callback_data='admin bosh menyuga qaytish')
        buton.adjust(2)
        return buton.as_markup()
    except Exception as e:
        print(f"Qatogrya add, remov and reply da xato qaytdi: {e}")
        return None

### Product add, remov and reply
def ProductAddRemovReplay(id=00):
    try:
        if id==-1:
            if len(baza.read('product','*'))>0:
                return True
            else:
                return None
        if id in [i[-1] for i in baza.read('product','*')]:
            buton = InlineKeyboardBuilder()
            categories = baza.read('product', '*')
            if not categories:
                print("Kategoriya table bo'sh!")
            for i in categories:
                if len(i) < 2:
                    continue
                if int(id)==i[-1]:
                    buton.button(text=f"{i[1]}-{i[2]}so'm", callback_data=f'{i[1]}-{i[2]}-{i[0]}')
            buton.button(text='◀️ Orqaga', callback_data='admin bosh menyuga qaytish')
            buton.adjust(2)
            return buton.as_markup()
        else:
            return None
    except Exception as e:
        print(f"Qatogrya add, remov and reply da xato qaytdi: {e}")
        return None

### So'rash knopkasi ha yoki yo'q
sorash = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='✅ Ha', callback_data='ha'),
            InlineKeyboardButton(text='❌ Yoq', callback_data='yoq')
        ]
    ]
)

### Adminlarni chiqaruvchi knopkalar
def AdminRemovButtons():
    try:
        buton = InlineKeyboardBuilder()
        for i in baza.read('admin',"*"):
            buton.button(text=f'{i[2]}', callback_data=f"{i[0]}-{i[1]}-{i[2]}-{i[4]}")
        buton.button(text='◀️ Orqaga', callback_data='admin remov')
        buton.adjust(2)
        return buton.as_markup()
    except Exception as e:
        print("Admin knopka yaratishda xatolik! ", e)
        return None
    
### User bog'lanish knopkasi
user_bog = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='◀️ Orqaga', callback_data='admin bosh menyuga qaytish'),
            InlineKeyboardButton(text="Izoh yozish ✍️", callback_data="izoh yozish")
        ]
    ]
)

###### Savat ichidagi ovqat o'chirish knopkalari
def Zakazlar(id):
    karzinka = InlineKeyboardBuilder()
    a = 1
    for i in baza.read("savat","*"):
        if i[1]==id:
            karzinka.button(text=f"🗑{a}",callback_data=f"{i[0]}")
            a += 1
    karzinka.add(InlineKeyboardButton(text="✔️ Zakaz berish", callback_data="✔️ Zakaz berish"))
    karzinka.add(InlineKeyboardButton(text="🛒 Savatni tozalash",callback_data='🛒 Savatni tozalash'))
    karzinka.add(InlineKeyboardButton(text="◀️ Orqaga", callback_data="admin bosh menyuga qaytish"))
    karzinka.adjust(3)
    return karzinka.as_markup()

def MaxsulotSoni(id=0):
    son = InlineKeyboardBuilder()
    if id == 0:
        # son.button(text=f"{0}", callback_data=f"{0}")
        son.button(text="➕", callback_data=f"+{id+1}")
        son.button(text="◀️ Orqaga", callback_data="orqaga")
        son.adjust(1)
        return son.as_markup()
    if id > 0:
        son.button(text="➖", callback_data=f"-{id-1}")
        son.button(text=f"{id}", callback_data=f"=-{id}")
        son.button(text="➕", callback_data=f"+{id+1}")
        son.button(text="◀️ Orqaga", callback_data="orqaga")
        son.button(text="Savatga qo'shish", callback_data=f"savatga_add-{id}")
        son.adjust(3)
        return son.as_markup()
    
def ZakazSoni(telegram_id: int):
    son = InlineKeyboardBuilder()
    for i in baza.read('savat','*'):
        if telegram_id == i[1]:
            son.button(text="➖", callback_data=f"-{i[0]}_{int(i[-1])-1}")
            son.button(text=f"{i[3]}-{i[-1]} ta", callback_data=f"={i[3]}_{i[0]}_{i[-1]}")
            son.button(text="➕", callback_data=f"+{i[0]}_{int(i[-1])+1}")
    son.add(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="admin bosh menyuga qaytish"))
    son.add(InlineKeyboardButton(text="🗑 Savatni tozalash",callback_data='🛒 Savatni tozalash'))
    son.add(InlineKeyboardButton(text="✅ Zakaz berish", callback_data="✔️ Zakaz berish"))
    son.adjust(3)
    return son.as_markup()

def ProductIN(telegram_id:int ,id:int, soni:int):
    buton = InlineKeyboardBuilder()
    idd = [i[0] for i in baza.read('savat','*') if telegram_id==i[1]]
    if len(idd)==1:
        buton.button(text="➖", callback_data=f"-{id}_{int(soni)-1}")
        buton.button(text="➕", callback_data=f"+{id}_{int(soni)+1}")
        buton.button(text="⬅️ Orqaga", callback_data="ortga")
        buton.button(text="❌ O'chirish", callback_data=f"{id}_o'chirish")
    elif min(idd)==id and len(idd)>1:
        buton.button(text="➖", callback_data=f"-{id}_{int(soni)-1}")
        buton.button(text="➕", callback_data=f"+{id}_{int(soni)+1}")
        buton.button(text="⬅️ Orqaga", callback_data="ortga")
        buton.button(text="❌ O'chirish", callback_data=f"{id}_o'chirish")
        buton.button(text="▶️ Keyingi", callback_data=f"keyingi_{idd[idd.index(id)+1]}")
    elif max(idd)==id:
        buton.button(text="➖", callback_data=f"-{id}_{int(soni)-1}")
        buton.button(text="➕", callback_data=f"+{id}_{int(soni)+1}")
        buton.button(text="⬅️ Orqaga", callback_data="ortga")
        buton.button(text="❌ O'chirish", callback_data=f"{id}_o'chirish")
        buton.button(text="◀️ Oldingi", callback_data=f"oldingi_{idd[idd.index(id)-1]}")
    else:
        buton.button(text="➖", callback_data=f"-{id}_{int(soni)-1}")
        buton.button(text="➕", callback_data=f"+{id}_{int(soni)+1}")
        buton.button(text="⬅️ Orqaga", callback_data="ortga")
        buton.button(text="❌ O'chirish", callback_data=f"{id}_o'chirish")
        buton.button(text="◀️ Oldingi", callback_data=f"oldingi_{idd[idd.index(id)-1]}")
        buton.button(text="▶️ Keyingi", callback_data=f"keyingi_{idd[idd.index(id)+1]}")
    buton.adjust(2)
    return buton.as_markup()
