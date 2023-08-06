import time
import telebot
from flask import abort, request
from flask_restful import Resource

from hiddifypanel.models import *

logger = telebot.logger


class ExceptionHandler(telebot.ExceptionHandler):
    def handle(self, exception):
        logger.error(exception)


bot = telebot.TeleBot("", parse_mode="HTML", threaded=False, exception_handler=ExceptionHandler())
bot.username=''

def register_bot():
    try:
        global bot
        token = hconfig(ConfigEnum.telegram_bot_token)
        if token:
            bot.token = hconfig(ConfigEnum.telegram_bot_token)
            try:
                bot.username=bot.get_me().username
            except:
                pass
            # bot.remove_webhook()
            time.sleep(0.1)
            domain = get_panel_domains()[0].domain
            proxy_path = hconfig(ConfigEnum.proxy_path)
            user_secret = hconfig(ConfigEnum.admin_secret)
            bot.set_webhook(url=f"https://{domain}/{proxy_path}/{user_secret}/api/v1/tgbot/")
    except Exception as e:
        print(e)
        import traceback
        traceback.print_stack()

    


class TGBotResource(Resource):
    def post(self):
        try:
            if request.headers.get('content-type') == 'application/json':
                json_string = request.get_data().decode('utf-8')
                update = telebot.types.Update.de_json(json_string)
                bot.process_new_updates([update])
                return ''
            else:
                abort(403)
        except Exception as e:
            print("Error", e)
            import traceback
            traceback.print_exc()
            return "", 500
#واقعا برای 5 دلار میخوای کرک میکنی؟ حاجی ارزش وقت خودت بیشتره
#Email hiddify@gmail.com for free permium version. Do not crack this cheap product
