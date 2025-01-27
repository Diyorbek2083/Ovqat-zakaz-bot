from .sqliteClas import SQLiteBaza


baza = SQLiteBaza('databaza.db')

###  Admin Tabel yaratish
# baza.create_table('admin',{
#     'id':"INTEGER PRIMARY KEY NOT NULL",
#     'telegram_id':'INTEGER',
#     'name':'VARCHAR(255)',
#     'user':'VARCHAR(30)',
#     'phone':'VARCHAR(30)'
# })

### Categoriya Table yaratish
# baza.create_table('categorya',{
#     'id':'INTEGER PRIMARY KEY NOT NULL',
#     'name':'VARCHAR(40)',
#     'rasm':'VARCHAR(255)'
# })

### User table yaratish
# baza.create_table('users',{
#     'id':'INTEGER PRIMARY KEY NOT NULL',
#     'telegram_id':'INTEGER NOT NULL',
#     'name':'VARCHAR(255) NOT NULL',
#     'user_name':'VARCHAR(40)'
# })

### Producta Table yaratish
# baza.create_table('product',{
#     'id':'INTEGER PRIMARY KEY NOT NULL',
#     'name':'VARCHAR(50)',
#     'narxi':'INTEGER',
#     'rasmi':'VARCHAR(255)',
#     'categorya_id':'INTEGER'
# })

### Izohlar table
# baza.create_table('izohlar',{
#     'id':'INTEGER PRIMARY KEY NOT NULL',
#     'telegram_id':'INTEGER',
#     'name':'VARCHAR(255)',
#     'izoh':'TEXT NOT NULL'
# })

### Bot malumotlari
# baza.create_table('malumotlar', {
#     'id':'INTEGER PRIMARY KEY NOT NULL',
#     'bot':'VARCHAR(30)',
#     'admin':'VARCHAR(30)',
#     'insta':'VARCHAR(30)',
#     'tel':'VARCHAR(30)'
# })

### Zakazlar tabli
# baza.create_table("savat",{
#     "id":"INTEGER PRIMARY KEY NOT NULL",
#     "telegram_id":"INTEGER",
#     "user":"VARCHAR(255)",
#     "nomi":"VARCHAR(35)",
#     "narxi":"INTEGER",
#     "soni":"INTEGER"
# })

### Admin Tableni o'qish
def Adminlar():
    try:
        admin_list = []
        records = baza.read('admin', "*")
        if not records:
            print("Admin table bo'sh!")
            return admin_list
        for record in records:
            if len(record) > 1:
                admin_list.append(record[1])
        return admin_list
    except Exception as e:
        print(f"Admin tableni o'qishda xatolik: {e}")
        return []

### Admin qo'shish
def AdminQoshish(tel_id, name, phone):
    try:
        if not isinstance(tel_id, int) or not name or not phone:
            raise ValueError("Ma'lumotlar noto'g'ri formatda!")
        baza.insert('admin', telegram_id=tel_id, name=name, phone=phone)
    except Exception as e:
        print(f"Admin bazaga qo'shilmadi: {e}")

### Userlarni o'qish
def Userlar():
    try:
        user_list = []
        records = baza.read('users', "*")
        if not records:
            print("User table bo'sh!")
            return user_list
        for record in records:
            if len(record) > 1:
                user_list.append(record[1])
        return user_list
    except Exception as e:
        print(f"User tableni o'qishda xatolik: {e}")
        return []

### User qo'shish
def UserQoshish(tg_id, name, user):
    try:
        if not isinstance(tg_id, int) or not name or not user:
            raise ValueError("Ma'lumotlar noto'g'ri formatda!")
        baza.insert('users', telegram_id=tg_id, name=name, user_name=user)
    except Exception as e:
        print(f"User tablega qo'shishda xatolik: {e}")

### Categorya qo'shish
def AddCategorya(name, photo):
    try:
        if not name or not photo:
            raise ValueError("Ma'lumotlar noto'g'ri formatda!")
        baza.insert('categorya',name=name, rasm=photo)
    except Exception as e:
        print(f"Categorya tablega qo'shishda xatolik: {e}")

### Producta qo'shish
def AddProduct(nomi, narxi, rasmi, categorya_id):
    try:
        if not isinstance(categorya_id, int) or not isinstance(narxi, int) or not nomi or not rasmi:
            raise ValueError("Ma'lumotlar noto'g'ri formatda!")
        baza.insert('product', name=nomi, narxi=narxi, rasmi=rasmi, categorya_id=categorya_id)
    except Exception as e:
        print(f"Praducta tablega qo'shishda xatolik: {e}")

### Categorya o'chirish
def RemoveCategorya(id):
    try:
        baza.delete('categorya', manzil_name=f"id = {id}")
        baza.delete('product',manzil_name=f'categorya_id = {id}')
    except Exception as e:
        print('Tabledan malumot o\'chirishda xatolik: ', e)

### Izohlarni o'qish
def UsersIzohlar():
    try:
        a = baza.read('izohlar','*')
        if len(a)>0:
            return True
        else:
            return False
    except:
        print("Izohlar tablni o'qishda xatolik")
        return False
    
### Savatni o'qish funksiyasi
def SavatRead(id):
    try:
        if id in [id[1] for id in baza.read('savat','*')]:
            return True
        else:
            return False
    except:
        print("Savat tableni o'qishda xatolik qaytdi")
        return False

