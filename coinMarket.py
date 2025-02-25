import requests
# دریافت داده‌های بازار از CoinGecko
def get_crypto_data(crypto_symbol='bitcoin'):
    url = f'https://api.coingecko.com/api/v3/coins/{crypto_symbol}/market_chart?vs_currency=usd&days=1'
    response = requests.get(url)
    data = response.json()
    return data
import talib
import numpy as np

# محاسبه RSI
def calculate_rsi(prices):
    rsi = talib.RSI(np.array(prices), timeperiod=14)
    return rsi[-1]  # آخرین مقدار RSI
from telegram import Bot
from telegram.ext import Updater, CommandHandler

TOKEN = '7561510736:AAEZ4SkuRqkiq_N8HnWsmIc7OtO9JUhxP6g' 
# دستورات ربات
def start(update, context):
    update.message.reply_text('سلام! من ربات تحلیل کریپتو هستم.')

def get_crypto_signal(update, context):
    # ارز دیجیتال مورد نظر
    crypto_symbol = 'bitcoin'  # اینجا می‌تونی ارز رو تغییر بدی
    data = get_crypto_data(crypto_symbol)
    prices = [price[1] for price in data['prices']]  # قیمت‌ها
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
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('signal', get_crypto_signal))
    updater.start_polling()
    updater.idle()

if __name__== '__main__':
    main()