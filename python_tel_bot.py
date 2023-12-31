from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.dispatcher import run_async
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters


stock_url = ""
isAppRunning = True
localpath = 'C:/Users/pavan/Downloads/chromedriver_win32/chromedriver.exe'

def initialize_driver():
	print("Initializing driver....")
	options = webdriver.ChromeOptions()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	options.add_argument('--disable-notifications')
	options.add_argument('--headless')
	path = '/home/ubuntu/python/stock_tracker_python_telegram_bot/lib/chromedriver'
	driver = webdriver.Chrome(path,options = options)
	return driver


@run_async
def start(update: Update, context: CallbackContext):
	context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, Welcome to the Stock tracking bot. Please click on /start_tracking for starting the tracker")

@run_async
def start_tracking(update: Update, context: CallbackContext):
	global isAppRunning
	isAppRunning = True
	context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide valid stock url from Trading view.")

@run_async
def change_tracking(update: Update, context: CallbackContext):
	global isAppRunning, stock_url
	isAppRunning = True
	stock_url = update.message.text;
	context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide valid stock url from Trading view.");

@run_async
def stop_tracking(update: Update, context: CallbackContext):
	global isAppRunning
	isAppRunning = False
	print("Tracking stopped..")
	context.bot.send_message(chat_id=update.effective_chat.id, text="Tracking stopped. Thannk you! See you again. You can start tracking by clicking /start_tracking")

@run_async
def set_stock_url(update: Update, context: CallbackContext):
	global stock_url, isAppRunning
	isAppRunning = True
	stock_url = update.message.text;
	context.bot.send_message(chat_id=update.effective_chat.id, text="Tracking started. Stock url is {}".format(stock_url));

	count = 0
	current_price = "" 
	try:
		driver = initialize_driver();
		driver.get(stock_url)
		while isAppRunning:
			WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[6]/div/div[1]/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[2]/span[1]"))).click()
			page_source = driver.page_source
			soup = BeautifulSoup(page_source, 'html.parser')

			price = soup.find(class_ = "price-qWcO4bp9").get_text()
			title = soup.find(class_ = "title-ZJX9Rmzv").get_text()
			detail = soup.find(class_ = "text-eFCYpbUa").get_text()
			curr = soup.find(class_ = "currency-qWcO4bp9").get_text()
			change = soup.find(class_ = "change-SNvPvlJ3").get_text()
			if "−" in change:
				status = "🔴"
			else:
				status = "🟢"

			message = "{}\n{}\n{} {}\n{} {}".format(title,detail,price,curr,change,status)

			if price != current_price:
				current_price = price
				context.bot.send_message(chat_id=update.effective_chat.id, text=message);
			time.sleep(1)
			
			count = count + 1
			if count > 10:
				count = 0
				driver.refresh()
	except Exception as e:
		context.bot.send_message(chat_id=update.effective_chat.id, text="Error occured {}".format(e));





def main():
	updater = Updater("6228304338:AAF_Jwor2BQbIYUvPNo7ii55V3QU-V28lBE",use_context=True, workers=100)
	updater.dispatcher.add_handler(CommandHandler('start', start))
	updater.dispatcher.add_handler(CommandHandler('start_tracking', start_tracking))
	updater.dispatcher.add_handler(CommandHandler('stop_tracking', stop_tracking))
	updater.dispatcher.add_handler(CommandHandler('change_tracking', change_tracking))
	updater.dispatcher.add_handler(MessageHandler(Filters.text, set_stock_url))

	updater.start_polling()
	print("App started..")

	updater.idle()


if __name__ == '__main__':
    main()
