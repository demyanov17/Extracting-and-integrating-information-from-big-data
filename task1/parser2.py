import re
import csv
import json
import requests
from bs4 import BeautifulSoup


class HTML_2_Parser():

	def __init__(self):
	    """
	    Constructor.

	    :param speed: скорость отряда
	    """
	    self.atribute_dict = dict()

	def file_parser(self, file_path):

		HTMLFile = open(file_path, "r")
		# Reading the file 
		index = HTMLFile.read()
		soup = BeautifulSoup(index, 'lxml')
		name = soup.find("meta", property="og:description")["content"]#.find('content')
		name = str(name).split(' в')[0].split("ноутбук ")[-1]
		print(name)
		if self.atribute_dict.get("Модель") is None:
			self.atribute_dict["Модель"] = [name]
		else:
			self.atribute_dict["Модель"].append(name)
		self.extract_data(soup)
		#print(self.atribute_dict)


	def write_csv(self):
		import pandas as pd

		# Создание DataFrame
		df = pd.DataFrame(self.atribute_dict)

		# Запись DataFrame в CSV с сохранением индекса
		df.to_csv('file.csv', index=True)


	def extract_data(self, soup):

		key = None
		for atibute in soup.find_all("tr"):
		#Тип экрана, <td>Диагональ экрана</td>

			if "Диагональ экрана" in atibute.text:
				key, value = atibute.text.split('<td>')[0].split("\n")[1:-1]
				print(atibute)

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

			if key is not None:
				if self.atribute_dict.get(key) is None:
					self.atribute_dict[key] = [value]
				else:
					self.atribute_dict[key].append(value)
			key = None


parser = HTML_2_Parser()
parser.file_parser("source2/source3.html")
parser.file_parser("source2/source4.html")
parser.write_csv()
