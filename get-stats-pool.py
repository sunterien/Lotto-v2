import random
import argparse, os, time
from urllib import parse
import urllib.request
from urllib.request import urlopen
from urllib import request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from bs4 import BeautifulSoup
import sys
import os.path
import datetime
# import requests
import re
# import string
from collections import Counter


time = datetime.datetime.now().strftime("%Y-%m-%d")
time_day_week = datetime.datetime.now().strftime("%Y.%m.%d # %W # %A")

pool = ['02', '03', '04', '05', '06', '07', '08', '12', '14', '15', '16', '17', '18', \
'21', '23', '24', '25', '26', '27', '28', '31', '32', '34', '35', '36', '37', \
'38', '41', '42', '43', '45', '46', '47', '48', '51', '52', '53', '54', '56', '57', '58']

fullpool = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', \
'11', '12', '13', '14', '15', '16', '17', '18', '19', '20', \
'21', '22', '23', '24', '25', '26', '27', '28', '29', '30', \
'31', '32', '33', '34', '35', '36', '37', '38', '39', '40', \
'41', '42', '43', '44', '45', '46', '47', '48', '49', '50', \
'51', '52', '53', '54', '55', '56', '57', '58', '59']

pool_1 = ['02', '03', '04', '05', '06', '07', '08', '09', \
'12', '14', '15', '16', '17', '18', '19', \
'21', '23', '24', '25', '26', '27', '28', '29', \
'31', '32', '34', '35', '36', '37', '38', '39', \
'41', '42', '43', '45', '46', '47', '48', '49', \
'51', '52', '53', '54', '56', '57', '58']

temp_pool_2 = ['08', '16', '33', '36', '45', '51', '10', '17', \
'35', '41', '54', '19', '29', '46', '58', '02', '11', '18', '32', \
'40', '26', '31', '37', '42', '48', '49', '05', '47', '52', '13', \
'22', '03', '07', '09', '27', '44']

occur_numbers = []
	

def getlinestats():
	s_draw = []
	s_pool = []
	c1 = 0
	ind = 0
	c_numb = 1
	s_range = 1
	aver_pool = []
	for x in range(1):
		with open(time + "_draws.txt", "r", encoding='utf-8') as myfile:
			lines = myfile.readlines()
			l_draw = lines[c1]
			draw = l_draw.replace("\n", '')
			draw = draw.split(' ')
			for i in draw:
				s_draw.append(i)
			# print(s_draw)
			while ind == 0:
				n_line = lines[c1+1]
				line = n_line.replace("\n", '')
				line = line.split(' ')
				for i in line:
					if i not in s_pool:
						s_pool.append(i)
				if all(x in s_pool for x in s_draw):
					ind = 1
					c1 = 0
					c1 += s_range
				else:
					c1 +=1
					c_numb +=1
			
			count_pool = 0
			for i in s_pool:
				if i not in s_draw:
					count_pool += 1
			aver_pool.append(count_pool)

			print(str(c_numb) + ' - ' + str(count_pool))
			s_range +=1
			s_draw = []
			#s_pool = []
			ind = 0
			c_numb = 0
	print("Average: " + str(sum(aver_pool)/len(aver_pool)))
	print(s_pool)



def getjackpot():

	jackpot = []
	jackpotfile_list = []
	least_common_temp = []
	least_common = []
	drawing_pool = []

	with open(time + "_draws.txt", "r", encoding='utf-8') as myfile:
		lines = myfile.readlines()
		lastdraw = lines[0]
		previousdraw = lines[1]

	#print(lastdraw)
	#print(previousdraw)
	
	lastdraw = lastdraw.replace("\n", '')
	lastdraw = lastdraw.split(' ')

	previousdraw = previousdraw.replace("\n", '')
	previousdraw = previousdraw.split(' ')

	#----------- CONV to INTEGERS ------------
	lastdraw_int = [int(i) for i in lastdraw]
	fullpool_int = [int(i) for i in fullpool]
	#-----------------------------------------

	neighbours_temp = []
	for i in lastdraw_int:
		if i + 1 not in neighbours_temp and i + 1 < 60:
			neighbours_temp.append(i + 1)
		if i - 1 not in neighbours_temp and i - 1 > 0:
			neighbours_temp.append(i - 1)
	
	neighbours_str = [str(i) for i in neighbours_temp]

	neighbours = []
	for i in neighbours_str:
		neighbours.append(i.zfill(2))


	with open(time + "_draws.txt", "r", encoding='utf-8') as myfile:
		for line in myfile:
			line = line.rstrip('\n')
			line = line.split(" ")
			for i in line:
				occur_numbers.append(i)

	a = -1
	# print(occur_numbers)
	for i in range(10):
		least_common_temp.append(Counter(occur_numbers).most_common()[a])
		a = a - 1

	for i in dict(least_common_temp).keys():
		least_common.append(i)

	# --------- Drawing pool -------------

	count_pool = 0
	for i in fullpool:
		if i.zfill(2) not in lastdraw and i in temp_pool_2:
			count_pool +=1
			drawing_pool.append(i)
	#-------------------------------------

	while len(jackpot) < 6:
		i = random.choice(drawing_pool)
		if i.zfill(2) not in jackpot:
			jackpot.append(i.zfill(2))

	jackpot = ' '.join(jackpot)
	drawing_pool = ' '.join(drawing_pool)

	with open('jackpot.txt', 'r', encoding='utf-8') as jackpotfile:
		jackpotfile_list.append(time_day_week + ' # ' + jackpot + ' # ' + drawing_pool + '\n')
		for line in jackpotfile:
			jackpotfile_list.append(line)

	with open('jackpot.txt', 'w', encoding='utf-8') as jackpotfile:
		for i in jackpotfile_list:
			jackpotfile.write(i)

	with open('draws_complete.txt', 'r', encoding='utf-8') as myfile:
		firstline = myfile.readline()
		# print(firstline.encode('utf-8'))
		firstline = firstline.replace("\n", '')
		firstline = firstline.split(' - ')
		# print(firstline[2].replace('£', ''))

	print('-------------------------------')
	print('--- Pool: ' + str(count_pool) + ' --- ' + firstline[2].replace('£', '') + ' ---')
	print('Jackpot: ' + str(jackpot))
	print('Our numbers: 08 11 13 19 24 29')
	print('-------------------------------')

def getmyresluts():
	week_counter = 0
	sat_jackpots = []
	wed_jackpots = []
	pool = []
	with open('draws_complete.txt') as myresults:
		firstline = myresults.readline()
		if "Sat" in firstline:
			firstline = firstline.replace("\n", '')
			splitresult = firstline.split(' - ')
			lastresult = splitresult[1]
			lastresult = lastresult.split(' ')

			with open('jackpot.txt') as myjackpot:
				for line in myjackpot:
					if 'Thursday' in line or 'Friday' in line or 'Saturday' in line:
						split_jackpot_result = line.split(' # ')
						nr_week = split_jackpot_result[1]
						if week_counter == 0:
							master_week = nr_week
						mylastjackpots = split_jackpot_result[3]
						pool_raw = split_jackpot_result[4]  #-----------------------
						week_counter +=1

						if nr_week == master_week:
							sat_jackpots.append(mylastjackpots)
							pool.append(pool_raw) #-------------------

			win_list = []
			pool_list = []
			for item in sat_jackpots:
				ind_result = 0
				check_i = item.split(' ')
				for i in check_i:
					if i in lastresult:
						ind_result +=1
				win_list.append(ind_result)

			for item in pool:		#--------------------
				ind_result = 0
				check_i = item.split(' ')
				for i in check_i:
					if i in lastresult:
						ind_result +=1
				pool_list.append(ind_result)

			n = 0
			print()
			print('-----------------------------')
			print('|     My numbers    | W | P |')
			print('-----------------------------')
			for i in sat_jackpots:
				print('| ' + i + ' | ' + str(win_list[n]) + ' | ' + str(pool_list[n]) + ' | ')
				n +=1

		if "Wed" in firstline:
			firstline = firstline.replace("\n", '')
			splitresult = firstline.split(' - ')
			lastresult = splitresult[1]
			lastresult = lastresult.split(' ')

			with open('jackpot.txt') as myjackpot:
				for line in myjackpot:
					if 'Sunday' in line or 'Monday' in line or 'Tuesday' in line or 'Wednesday' in line:
						split_jackpot_result = line.split(' # ')
						nr_week = split_jackpot_result[1]
						if week_counter == 0:
							master_week = nr_week
						mylastjackpots = split_jackpot_result[3]
						pool_raw = split_jackpot_result[4]  #-----------------------
						week_counter +=1

						if nr_week == master_week:
							wed_jackpots.append(mylastjackpots)
							pool.append(pool_raw) #-------------------

			win_list = []
			pool_list = []
			for item in wed_jackpots:
				ind_result = 0
				check_i = item.split(' ')
				for i in check_i:
					if i in lastresult:
						ind_result +=1
				win_list.append(ind_result)

			for item in pool:		#--------------------
				ind_result = 0
				check_i = item.split(' ')
				for i in check_i:
					if i in lastresult:
						ind_result +=1
				pool_list.append(ind_result)

			n = 0
			print()
			print('-----------------------------')
			print('|     My numbers    | W | P |')
			print('-----------------------------')
			for i in wed_jackpots:
				print('| ' + i + ' | ' + str(win_list[n]) + ' | ' + str(pool_list[n]) + ' | ')
				n +=1
	


if os.path.isfile(str(time) + "_draws.txt"):
	os.system('cls')
	print("File exists")
	getlinestats()
else:
	os.system('cls')
	print("Please wait, I'm getting numbers...")
	# getnumbers()
	getlinestats()
