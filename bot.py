from telegram.ext import Updater, CommandHandler, InlineQueryHandler, CallbackContext, MessageHandler, Filters
from telegram import InlineQueryResultArticle, InputTextMessageContent
import logging, datetime, pytz
import random
import requests
import re
import json
import giphy_client
from giphy_client.rest import ApiException
from pprint import pprint

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

apiKey = ""
with open('apiKey.txt', 'r') as file:
    apiKey = file.read().replace('\n', '')
updater = Updater(apiKey)
dp = updater.dispatcher

def search(keywords, max_results=None):
    url = 'https://duckduckgo.com/'
    params = {
    	'q': keywords
    }
    print(keywords)
    logger.debug("Hitting DuckDuckGo for Token")

    #   First make a request to above URL, and parse out the 'vqd'
    #   This is a special token, which should be used in the subsequent request
    res = requests.post(url, data=params)
    searchObj = re.search(r'vqd=([\d-]+)\&', res.text, re.M|re.I)

    if not searchObj:
        logger.error("Token Parsing Failed !")
        return -1

    logger.debug("Obtained Token")

    headers = {
        'authority': 'duckduckgo.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'sec-fetch-dest': 'empty',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'referer': 'https://duckduckgo.com/',
        'accept-language': 'en-US,en;q=0.9',
    }

    params = (
        ('l', 'us-en'),
        ('o', 'json'),
        ('q', keywords),
        ('vqd', searchObj.group(1)),
        ('f', ',,,'),
        ('p', '1'),
        ('v7exp', 'a'),
    )

    requestUrl = url + "i.js"

    logger.debug("Hitting Url : %s", requestUrl)

    while True:
        while True:
            try:
                res = requests.get(requestUrl, headers=headers, params=params)
                data = json.loads(res.text)
                break
            except ValueError as e:
                logger.debug("Hitting Url Failure - Sleep and Retry: %s", requestUrl)
                time.sleep(5)
                continue

        logger.debug("Hitting Url Success : %s", requestUrl)
        results = data["results"]
        if len(results) > 0:
            return results[random.randint(0,len(results)-1)]


def start(update, context):
    print(datetime.time(hour=22, minute= 41))
    context.job_queue.run_daily(msg,
                                datetime.time(hour=22, minute=39),
                                days=(0, 1, 2, 3, 4, 5, 6), context=update.message.chat_id)

def msg(context):
    context.bot.send_message(chat_id=context.job.context, text='text')

def error(update, context):
    """Log Errors caused by Updates."""
    #logger.warning('Update "%s" caused error "%s"', update, context.error)

def daily_job(bot, update, job_queue):
    """ Running on Mon, Tue, Wed, Thu, Fri = tuple(range(5)) """
    bot.send_message(chat_id='-573689659', text='Setting a daily notifications!')
    t = datetime.time(10, 00, 00, 000000)
    job_queue.run_daily(notify_assignees, t, days=tuple(range(5)), context=update)

def notify_assignees(bot, job):
    bot.send_message(chat_id='-573689659', text="Some text!")

def inlinequery(update, context):
    print("in inlinequery")
    query = update.inline_query.query
    if not query:
        return
    print(query)

def get_random_evgeny_message():
    a = ["יבגני יא תחת", "התחברת לאני הפנימי שלך?", "אלגרי לחתולים אלעק", "y r u gay?", "Confucius say: אתה מכוער"]
    return a[random.randint(0,len(a)-1)]


def get_url():
    contents = requests.get('https://random.dog/woof.json').json()    
    url = contents['url']
    return url

def get_cat_url():
    contents = requests.get('http://aws.random.cat//meow').json()
    file = contents['file']
    return file

def get_joke(update, context):
    contents = requests.get('https://us-central1-dadsofunny.cloudfunctions.net/DadJokes/random/jokes').json()
    context.bot.send_message(chat_id=update.message.chat_id, text=contents['setup'])
    context.bot.send_message(chat_id=update.message.chat_id, text=contents['punchline'])


def get_dog(update, context):
    url = get_url()
    chat_id = update.message.chat_id
    if url.endswith('.gif'):
        context.bot.send_animation(chat_id=chat_id, animation=url)
    else:
        context.bot.send_photo(chat_id=chat_id, photo=url)
    print(update.message.from_user.id)

def get_cat(update, context):
    url = get_cat_url()
    chat_id = update.message.chat_id
    if url.endswith('.gif'):
        context.bot.send_animation(chat_id=chat_id, animation=url)
    else:
        context.bot.send_photo(chat_id=chat_id, photo=url)
        

def evgeny(update, context):
    msg = get_random_evgeny_message()
    context.bot.send_message(chat_id=update.message.chat_id, text=msg)


def get_is_wednsday(update, context):
    api_instance = giphy_client.DefaultApi()
    api_key = 'uGK7Z8xvPGPRJcnl42NuhoZHNG6QYUPE' # str | Giphy API Key.
    q = 'wednesday' # str | Search query term or prhase.
    offset = 0 # int | An optional results offset. Defaults to 0. (optional) (default to 0)
    lang = 'en' # str | Specify default country for regional content; use a 2-letter ISO 639-1 country code. See list of supported languages <a href = \"../language-support\">here</a>. (optional)
    fmt = 'json' # str | Used to indicate the expected response format. Default is Json. (optional) (default to json)

    try: 
        # Search Endpoint
        api_response = api_instance.gifs_search_get(api_key, q, offset=offset, lang=lang, fmt=fmt)
        # pprint(api_response)
        # print(api_response.data)
        url = api_response.data[random.randint(0,len(api_response.data)-1)].images.downsized.url
        if datetime.datetime.today().weekday() == 2:
            context.bot.send_message(chat_id=update.message.chat_id, text="It's wednesday, my dudes!")
            context.bot.send_animation(chat_id=update.message.chat_id, animation=url)
        else:
            context.bot.send_message(chat_id=update.message.chat_id, text="It's not wednesday :(")
    except ApiException as e:
        print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)


def callback_timer(context: CallbackContext):
    print("callback")

    cid = -450717105
    user_id = 1120173890
    mention = "[Aviv Metz](tg://user?id="+str(user_id)+")"

    context.bot.send_message(chat_id=-450717105, text="Hi, " + mention,parse_mode="Markdown")

def get_wildcard(update, context):
    if re.search("[getGET]{3}|([a-z]|\d)", update.message.text, re.IGNORECASE | re.DOTALL):
        query = update.message.text[4:len(update.message.text)]
        res = search(query)
        context.bot.send_photo(chat_id=update.message.chat_id, photo=res['image'])

def inline_caps(update, context):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='GetDog',
            input_message_content=InputTextMessageContent("Get picture of a dog!")
        )
    )
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='GetCat',
            input_message_content=InputTextMessageContent("Get picture of a cat!")
        )
    )
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Get<AnyThing>',
            input_message_content=InputTextMessageContent("Get picture of anything! for example \GetBanana")
        )
    )
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='GetDadJoke',
            input_message_content=InputTextMessageContent("Get a joke from a dad!")
        )
    )
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='IsItwednesday',
            input_message_content=InputTextMessageContent("Check whether it's wednesday or not")
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)

def main():

    while True:
        try:
            print("while")
            dp.add_handler(CommandHandler("PersonolizedEvgenyMessage", evgeny, pass_job_queue=True))
            dp.add_handler(CommandHandler("GetDog", get_dog))
            dp.add_handler(CommandHandler("GetCat", get_cat))
            dp.add_handler(CommandHandler("GetDadJoke", get_joke))
            dp.add_handler(CommandHandler("IsItwednesday", get_is_wednsday))
            dp.add_handler(MessageHandler(Filters.text, get_wildcard))

            # dp.add_handler(CommandHandler("timer", callback_timer, pass_job_queue=True))
            job = updater.job_queue
            # print(datetime.datetime.now())
            # print(datetime.time(10, 0, 0))

            # job.run_once(callback_timer, 10)
            # job.run_repeating(callback_timer, 86400)

            dp.add_handler(InlineQueryHandler(inline_caps))
            # dp.add_error_handler(error)

            updater.start_polling()
            updater.idle()
        except:
            print("error, restarting...")

if __name__ == '__main__':
    main()


# https://api.telegram.org/bot1624402630:AAF87KMwneXXMNA77B2_XIEgmzcoyiWxz8I/getUpdates