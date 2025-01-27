from aiogram.fsm.state import State, StatesGroup

class Start(StatesGroup):
    admin = State()
    user = State()


mesages = {
    'categorya':{
        'nomi':'Categoryaning yangi nomini yozing',
        'rasmi':'Categoryaning yangi rasmini yuboring'
    },
    'product':{
        'nomi':'Productaning yangi nomini yozing',
        'rasmi':'Productaning yangi rasmini yuboring',
        'narxi':'Productaning yangi narxini yozing iltimos faqat raqam bo\'lsin\nMasalan: 20000',
        'categorya':'Qaysi qategoryaga o\'tirmoqchisiz?'
    }
}