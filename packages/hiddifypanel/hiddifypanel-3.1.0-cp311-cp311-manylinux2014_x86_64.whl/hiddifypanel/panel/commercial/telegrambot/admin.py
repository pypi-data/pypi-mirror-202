from . import bot

from telebot import types
from hiddifypanel.models import *
import datetime
from hiddifypanel.panel.database import db

@bot.message_handler(commands=['start'],func=lambda message: "admin" in message.text)
def send_welcome(message):
    text = message.text
    #print("dddd",text)
    uuid = text.split()[1].split("_")[1] if len(text.split()) > 1 else None
    if uuid:
        if uuid==hconfig(ConfigEnum.admin_secret):
            start_admin(message)
            return
    bot.reply_to(message, "error")




def start_admin(message):

    bot.reply_to(message,"Welcome to admin bot. Choose your action",reply_markup=admin_keyboard_main())

def admin_hash():
    return hash(hconfig(ConfigEnum.admin_secret))%100000
    

def admin_keyboard_main():

    return types.InlineKeyboardMarkup(keyboard=[[
                types.InlineKeyboardButton(
                    text="Create Package",
                    callback_data=f'{admin_hash()}create_package'
                )
            ]
        ]
    )

def admin_keyboard_gig(old_action):
    def keyboard(gig):
        return types.InlineKeyboardButton(
                    text=f"{gig} GB",
                    callback_data=f"{old_action} {gig}"
                )
    return types.InlineKeyboardMarkup(keyboard=[
        [keyboard(i) for i in range(1,5)] ,
        [keyboard(5*i) for i in range(1,5)],
        [keyboard(50*i) for i in range(1,5)]
        ]
    )
def admin_keyboard_days(old_action):
    def keyboard(days):
        return types.InlineKeyboardButton(
                    text=f"{days}",
                    callback_data=f"{old_action} {days}"
                )
    return types.InlineKeyboardMarkup(keyboard=[
        [keyboard(i) for i in range(1,16,3)] ,
        [keyboard(30*i) for i in range(1,5)]
        ]
    )    
def admin_keyboard_count(old_action):
    def keyboard(count):
        return types.InlineKeyboardButton(
                    text=f"{count}",
                    callback_data=f"{old_action} {count}"
                )
    return types.InlineKeyboardMarkup(keyboard=[
        [keyboard(i) for i in range(1,5)] ,
        [keyboard(i*5) for i in range(1,5)],
        [keyboard(i*50) for i in range(1,5)]
        ]
    )        
@bot.callback_query_handler(func=lambda call: call.data.startswith(f'{admin_hash()}create_package'))
def create_package(call): # <- passes a CallbackQuery type object to your function
    from . import Usage
    try:
        splt=call.data.split(" ")
        if len(splt)==1:    
            new_text="package size? حجم بسته؟"
            bot.edit_message_text(new_text, call.message.chat.id, call.message.message_id,reply_markup=admin_keyboard_gig(call.data))
            bot.answer_callback_query(call.id, text="Ok", show_alert=False,cache_time =1)
        elif len(splt)==2:    
            new_text="package days? چند روز؟"
            bot.edit_message_text(new_text, call.message.chat.id, call.message.message_id,reply_markup=admin_keyboard_days(call.data))
            bot.answer_callback_query(call.id, text="Ok", show_alert=False,cache_time =1)
        elif len(splt)==3:
            new_text="How many? چه تعداد؟"
            bot.edit_message_text(new_text, call.message.chat.id, call.message.message_id,reply_markup=admin_keyboard_count(call.data))
            bot.answer_callback_query(call.id, text="Ok", show_alert=False,cache_time =1)
        elif len(splt)==4:
            gig=int(splt[1])
            days=int(splt[2])
            count=int(splt[3])
            new_text="Wait... لطفا صبر کنید"
            bot.edit_message_text(new_text, call.message.chat.id, call.message.message_id,reply_markup=None)
            domain=(ParentDomain if hconfig(ConfigEnum.is_parent) else Domain).query.first()
            for i in range(1,count+1):
                user=User(package_days=days,usage_limit_GB=gig,name=f"auto {i} {datetime.date.today()}")
                db.session.add(user)
                db.session.commit()    
                # bot.send_message(call.message.chat.id,f"Days: {days}     Limit: {gig}GB     #{i}\n\n https://{domain.domain}/{hconfig(ConfigEnum.proxy_path)}/{user.uuid}/",reply_markup=Usage.user_keyboard(user.uuid))
                bot.send_message(call.message.chat.id,Usage.get_usage_msg(user.uuid),reply_markup=Usage.user_keyboard(user.uuid))

            # db.session.commit()
            new_text="Finished..."
            bot.edit_message_text(new_text, call.message.chat.id, call.message.message_id,reply_markup=admin_keyboard_main())
            bot.answer_callback_query(call.id, text="Ok", show_alert=False,cache_time =1)
            hiddify.quick_apply_users()
        
    except Exception as e:
        print (e)
        # import traceback
        # traceback.print_stack()
        # new_text=f"Error {e}"
        # bot.edit_message_text(new_text, call.message.chat.id, call.message.message_id,reply_markup=admin_keyboard_main())
        # bot.answer_callback_query(call.id,cache_time =1)

#واقعا برای 5 دلار میخوای کرک میکنی؟ حاجی ارزش وقت خودت بیشتره
#Email hiddify@gmail.com for free permium version. Do not crack this cheap product
