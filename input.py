import pywinauto
from pywinauto import application
import time
import win32gui
import re
import argparse, os, time
from urllib import parse
import urllib.request
from urllib.request import urlopen
from urllib import request
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import sys
import os.path
import datetime
import pyperclip
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains


def ViewBot(browser):
	draws = []

	with open("bigwin.txt") as mydraws:
		for line in mydraws:
			draw = []
			listsplit = line.split()
			for i in listsplit:
				draw.append(i)
			draws.append(draw)

	print(draws)
	number_of_lines = len(draws)
	print("Number of lines: " + str(number_of_lines))
	line = 0
	col = 0

	for i in range(number_of_lines * 6):
		field = browser.find_element_by_id('lotto_playslip_line_' + str(line) + '_pool_0_' + 'col_' + str(col))
		field.send_keys(draws[line][col])

		if col == 5:
			col = 0
			line +=1
		else:
			col +=1
		
		
def main():

	profile = webdriver.FirefoxProfile()
	profile.set_preference("browser.cache.disk.enable", False)
	profile.set_preference("browser.cache.memory.enable", False)
	profile.set_preference("browser.cache.offline.enable", False)
	profile.set_preference("network.http.use-cache", False)
	browser = webdriver.Firefox(profile)
	browser.get("https://www.national-lottery.co.uk/sign-in")
	
	time.sleep(2)
	
	emailElement = browser.find_element_by_id('form_username')
	emailElement.send_keys("sunterien")
	passElement = browser.find_element_by_id('form_password')
	passElement.send_keys("bobJ@B0478_LOTTOUK4466")
	passElement.submit()
	time.sleep(2)
	browser.get("https://www.national-lottery.co.uk/games/lotto")
	os.system('cls')  # cls windows clear Linux
	print('Success!')
	input("Enter to continue...")
	ViewBot(browser)
	#browser.close()


if __name__ == '__main__': main()
