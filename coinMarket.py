import requests
import talib
import numpy as np
from telegram import Bot
from telegram.ext import Updater, CommandHandler

# دریافت داده‌های بازار از CoinMarketCap
def get_crypto_data(crypto_symbol='bitcoin'):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {
        "X-CMC_PRO_API_KEY": 'd93ab40b-3cd1-48d7-9a38-c3167387c01b',  # API Key شما
        "Accept": "application/json",
    }
    params = {
        "symbol": crypto_symbol.upper(),
        "convert": "USD",
        "limit": 1
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    return data['data'][0] if data['status']['error_code'] == 0 else None

# محاسبه RSI
def calculate_rsi(prices):
    rsi = talib.RSI(np.array(prices), timeperiod=14)
    return rsi[-1]  # آخرین مقدار RSI

# دستورات ربات
def start(update, context):
    update.message.reply_text('سلام! من ربات تحلیل کریپتو هستم.')

def get_crypto_signal(update, context):
    # ارز دیجیتال مورد نظر
    crypto_symbol = 'BTC'  # تغییر به نماد ارز مورد نظر
    data = get_crypto_data(crypto_symbol)
    
    if data is None:
        update.message.reply_text("خطا در دریافت داده‌ها.")
        return
    
    prices = [data['quote']['USD']['price']]  # قیمت فعلی ارز
    rsi_value = calculate_rsi(prices)
    
    # تحلیل بر اساس RSI
    if rsi_value < 30:
        signal = "سیگنال خرید: RSI پایین است."
    elif rsi_value > 70:
        signal = "سیگنال فروش: RSI بالا است."
    else:
        signal = "هیچ سیگنالی نداریم."
    
    update.message.reply_text(signal)

# راه‌اندازی ربات
def main():
    TOKEN = '7561510736:AAEZ4SkuRqkiq_N8HnWsmIc7OtO9JUhxP6g'  # توکن ربات تلگرام شما
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('signal', get_crypto_signal))
    updater.start_polling()
    updater.idle()

if name == '__main__':
    main()
