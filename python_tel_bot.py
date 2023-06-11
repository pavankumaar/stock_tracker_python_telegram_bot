from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from Stocktracking import TrackStock

updater = Updater("6199264921:AAEFgyo3ro6ceg0zslLvSysI62ObONm2vQg",
				use_context=True)

stock_url = ""
isAppRunning = True

def initialize_driver():
	options = webdriver.ChromeOptions()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	options.add_argument('--disable-notifications')
	path = 'C:/Users/pavan/Downloads/chromedriver_win32/chromedriver.exe'
	driver = webdriver.Chrome(path,options = options)
	# update.message.reply_text("Intializing web driver...");
	return driver

def start_scrapper(driver, update):
	driver.get(stock_url)
	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[6]/div/div[1]/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[2]/span[1]"))).click()
	count = 0
	while True:
		page_source = driver.page_source
		soup = BeautifulSoup(page_source, 'html.parser')

		price = soup.find(class_ = "priceWrapper-qWcO4bp9").get_text()
		update.message.reply_text("Current price {}".format(price));
		time.sleep(1)
		
		count = count + 1
		if count > 10:
			start_scrapper(driver, update);


def start(update: Update, context: CallbackContext):
	update.message.reply_text("Hello, Welcome to the Stock tracking bot. Please click on /start_tracking for starting the tracker")

def start_tracking(update: Update, context: CallbackContext):
	isAppRunning = True
	update.message.reply_text("Please provide valid stock url from Trading view.")

def change_tracking(update: Update, context: CallbackContext):
	stock_url = update.message.text;
	update.message.reply_text("Please provide valid stock url from Trading view.");

def stop_tracking(update: Update, context: CallbackContext):
	isAppRunning = False
	update.message.reply_text("Tracking stopped. Thannk you! See you again.")

def set_stock_url(update: Update, context: CallbackContext):
	stock_url = update.message.text;
	update.message.reply_text("Tracking started. Stock url is {}".format(stock_url));
	driver = initialize_driver();
	driver.get(stock_url)
	count = 0
	while True:
		WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[6]/div/div[1]/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[2]/span[1]"))).click()
		page_source = driver.page_source
		soup = BeautifulSoup(page_source, 'html.parser')

		price = soup.find(class_ = "priceWrapper-qWcO4bp9").get_text()
		update.message.reply_text("Current price {}".format(price));
		time.sleep(1)
		
		count = count + 1
		if count > 10:
			count = 0
			driver.refresh()


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('start_tracking', start_tracking))
updater.dispatcher.add_handler(CommandHandler('stop_tracking', stop_tracking))
updater.dispatcher.add_handler(CommandHandler('change_tracking', change_tracking))
updater.dispatcher.add_handler(MessageHandler(Filters.text, set_stock_url))

updater.start_polling()
