import re
import csv
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup


class HTML_1_Parser():

	def __init__(self):

	    self.atribute_dict = dict()

	def file_parser(self, file_path):

		HTMLFile = open(file_path, "r")
		# Reading the file 
		index = HTMLFile.read()
		soup = BeautifulSoup(index, 'lxml')
		name = name = soup.find("meta", property="og:title")["content"]
		name = str(name).split(' - купить')[0]
		if self.atribute_dict.get("Модель") is None:
			self.atribute_dict["Модель"] = [name]
		else:
			self.atribute_dict["Модель"].append(name)
		self.extract_data(soup)


	def write_csv(self):

		df = pd.DataFrame(self.atribute_dict)
		df.to_csv('source1.csv', index=True)


	def extract_data(self, soup):

		key = None

		for atibute in soup.find_all("tr"):
			if "Год выпуска" in atibute.text:
				key, value = atibute.text.split('<td>')[0].split("\n")[1:-1]

			if "Дисплей" in atibute.text:
				key, value = atibute.text.split('<td>')[0].split("\n")[1:-1]

			if "Разрешение экрана" in atibute.text:
				key, value = atibute.text.split('<td>')[0].split("\n")[1:-1]

			if "Оперативная память" in atibute.text:
				key, value = atibute.text.split('<td>')[0].split("\n")[1:-1]

			if "Объём памяти" in atibute.text:
				key, value = atibute.text.split('<td>')[0].split("\n")[1:-1]

			if "Оперативная память" in atibute.text:
				key, value = atibute.text.split('<td>')[0].split("\n")[1:-1]

			if "Количество ядер" in atibute.text:
				key, value = atibute.text.split('<td>')[0].split("\n")[1:-1]

			if "Процессор" in atibute.text:
				key, value = atibute.text.split('<td>')[0].split("\n")[1:-2]

			if "Разъёмы" in atibute.text:
				key, value = atibute.text.split('<td>')[0].split("\n")[1:-1]

			if "Цвет" in atibute.text:
				key, value = atibute.text.split('<td>')[0].split("\n")[1:-1]

			if "В комплекте" in atibute.text:
				key, value = atibute.text.split('<td>')[0].split("\n")[1:-1]

			if key is not None:
				if self.atribute_dict.get(key) is None:
					self.atribute_dict[key] = [value]
				else:
					self.atribute_dict[key].append(value)
			key = None


class HTML_2_Parser():

	def __init__(self):

	    self.atribute_dict = dict()

	def file_parser(self, file_path):

		HTMLFile = open(file_path, "r")
		# Reading the file 
		index = HTMLFile.read()
		soup = BeautifulSoup(index, 'lxml')
		name = soup.find("meta", property="og:description")["content"]#.find('content')
		name = str(name).split(' в')[0].split("ноутбук ")[-1]
		if self.atribute_dict.get("Модель") is None:
			self.atribute_dict["Модель"] = [name]
		else:
			self.atribute_dict["Модель"].append(name)
		self.extract_data(soup)


	def write_csv(self):

		df = pd.DataFrame(self.atribute_dict)
		df.to_csv('source2.csv', index=True)


	def extract_data(self, soup):

		columns_list = ["Диагональ экрана", "Процессор", "Серия"]
		key = None
		for atibute in soup.find_all("tr"):

			if "Диагональ экрана" in atibute.text:
				key, value = atibute.text.split('<td>')[0].split("\n")[1:-1]

			if "Процессор" in atibute.text:
				key, value = atibute.text.split('<td>')[0].split("\n")[1:-1]

			if "Серия" in atibute.text:
				key, value = atibute.text.split('<td>')[0].split("\n")[1:-1]

			if "Цвет" in atibute.text:
				key, value = atibute.text.split('<td>')[0].split("\n")[1:-1]

			if "Тип экрана" in atibute.text:
				key, value = atibute.text.split('<td>')[0].split("\n")[1:-1]

			if "Диагональ экрана" in atibute.text:
				key, value = atibute.text.split('<td>')[0].split("\n")[1:-1]

			if "Разрешение экрана" in atibute.text:
				key, value = atibute.text.split('<td>')[0].split("\n")[1:-1]

			if "Яркость" in atibute.text:
				key, value = atibute.text.split('<td>')[0].split("\n")[1:-1]

			if "Количество ядер процессора" in atibute.text:
				key, value = atibute.text.split('<td>')[0].split("\n")[1:-1]

			if "Видеопроцессор" in atibute.text:
				key, value = atibute.text.split('<td>')[0].split("\n")[1:-1]

			if "Количество ядер процессора" in atibute.text:
				key, value = atibute.text.split('<td>')[0].split("\n")[1:-1]

			if "Тип накопителя" in atibute.text:
				key, value = atibute.text.split('<td>')[0].split("\n")[1:-1]

			if "Bluetooth" in atibute.text:
				key, value = atibute.text.split('<td>')[0].split("\n")[1:-1]

			if "Интерфейсы" in atibute.text:
				key, value = atibute.text.split('<td>')[0].split("\n")[1:-1]

			if "Емкость аккумулятора" in atibute.text:
				key, value = atibute.text.split('<td>')[0].split("\n")[1:-1]

			if "Время работы" in atibute.text:
				key, value = atibute.text.split('<td>')[0].split("\n")[1:-1]

			if "Микрофон" in atibute.text:
				key, value = atibute.text.split('<td>')[0].split("\n")[1:-1]

			if "Сканер отпечатка пальца" in atibute.text:
				key, value = atibute.text.split('<td>')[0].split("\n")[1:-1]

			if "Год" in atibute.text:
				key, value = atibute.text.split('<td>')[0].split("\n")[1:-1]

			if "Вес" in atibute.text:
				key, value = atibute.text.split('<td>')[0].split("\n")[1:-1]

			# if any(column in atibute.text for column in columns_list):
			# 	key, value = atibute.text.split('<td>')[0].split("\n")[1:-1]

			if key is not None:
				if self.atribute_dict.get(key) is None:
					self.atribute_dict[key] = [value]
				else:
					self.atribute_dict[key].append(value)
			key = None


parser = HTML_1_Parser()
import os
for file in os.listdir("source1"):
	if file.endswith(".html"):
		parser.file_parser(f"source1/{file}")
parser.write_csv()


parser = HTML_2_Parser()
import os
for file in os.listdir("source2"):
	if file.endswith(".html"):
		parser.file_parser(f"source2/{file}")
parser.write_csv()
