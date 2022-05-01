import logging, requests, json
from thefuzz import fuzz
from thefuzz import process
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = 'telegrambotapi'
HYPIXELAPI = 'https://api.hypixel.net/skyblock/bazaar?key=INSERT HYPIXEL API KEY HERE'
#to get the hypixel api key do /api new

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help']) 
async def welcome(message: types.Message):
    await message.reply("type /list to get all available items")

@dp.message_handler(commands=['list'])
async def list(message: types.Message):
    json = requests.get(HYPIXELAPI).json()
    chese = json["products"]["CHEESE_FUEL"]["quick_status"]
    await message.answer(f'🧀 items list: https://telegra.ph/Hypixel-Skyblock-Item-ID-List-04-24')
    
@dp.message_handler()
async def cheese(message: types.Message):
    try:
        json = requests.get(HYPIXELAPI).json()
        
        item = message.text.upper().replace(' ', '_')
        items = json["products"].keys()
        st, nd = process.extract(item, items, limit=2)
        item1, perc1 = st
        item2, perc2 = nd
        qstat = json["products"][item1]["quick_status"]
        qsell = round(qstat["sellPrice"], 2)
        qbuy = round(qstat["buyPrice"], 2)
        
        sellpricePer = json["products"][item1]["sell_summary"][0]["pricePerUnit"]
        buypricePer = json["products"][item1]["buy_summary"][0]["pricePerUnit"]
        sellAmount = json["products"][item1]["sell_summary"][0]["amount"]
        buyAmount = json["products"][item1]["buy_summary"][0]["amount"]
        sellOrders = json["products"][item1]["sell_summary"][0]["orders"]
        buyOrders = json["products"][item1]["buy_summary"][0]["orders"]
        
        await message.answer(f'📈 {item1} bz stats: \n' + 
            f'💰 [SELL] {sellpricePer} coins / [AMOUNT] {sellAmount} / [ORDERS] {sellOrders}\n'
            f'💰 [BUY] {buypricePer} coins / [AMOUNT] {buyOrders} / [ORDERS] {buyOrders}\n'
            f'💰 [QUICK SELL] {qsell} coins\n' + 
            f'💰 [QUICK BUY] {qbuy} coins')
        
    except KeyError:
        await message.answer(f'no cheese?')
    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
