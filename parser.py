import os
import re
import requests
import pandas as pd
import json, yaml, csv
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod


class HTML_Parser(ABC):

    def __init__(self, source_name):
        self.atribute_dict = dict()
        self.source_name = source_name
        with open("parser.yaml", "r") as stream:
            self.config = yaml.safe_load(stream)[self.source_name]

    def parse_source(self):
        path = "../task0/"
        for file in os.listdir(path + self.source_name):
            if file.endswith(".html"):
                self.file_parser(path + self.source_name + "/" + file)
        self.write_csv()

    @abstractmethod
    def file_parser(self, file_path):
        pass

    @abstractmethod
    def extract_data(self, soup):
        pass

    def add_attribute_dict(self, key, value):
        if self.atribute_dict.get(key) is None:
            self.atribute_dict[key] = [value]
        else:
            self.atribute_dict[key].append(value)

    def write_csv(self):
        df = pd.DataFrame(self.atribute_dict)
        df.to_csv(f"{self.source_name}.csv", index=True)


class HTML_1_Parser(HTML_Parser):

    def file_parser(self, file_path):

        HTMLFile = open(file_path, "r")
        index = HTMLFile.read()
        soup = BeautifulSoup(index, "lxml")
        name = name = soup.find("meta", property="og:title")["content"]
        name = str(name).split(" - купить")[0]
        name = name.replace(",", "")
        self.add_attribute_dict("Модель", name)
        self.extract_data(soup)

    def extract_data(self, soup):

        key = None

        for atibute in soup.find_all("tr"):
            for column in self.config["columns_list"]:
                if column in atibute.text:
                    key, value = atibute.text.split("<td>")[0].split("\n")[1:-1]

            if "Процессор" in atibute.text:
                key, value = atibute.text.split("<td>")[0].split("\n")[1:-2]

            if key is not None:
                self.add_attribute_dict(key, value)
            key = None

        notebook_price = soup.find("span", class_="update_price").text
        self.add_attribute_dict("Цена", notebook_price)

        notebook_weight = soup.find("span", class_="pr_weight").text
        self.add_attribute_dict("Вес", notebook_weight)


class HTML_2_Parser(HTML_Parser):

    def file_parser(self, file_path):

        HTMLFile = open(file_path, "r")
        index = HTMLFile.read()
        soup = BeautifulSoup(index, "lxml")
        name = soup.find("meta", property="og:description")["content"]
        name = str(name).split(" в")[0].split("ноутбук ")[-1]
        self.add_attribute_dict("Модель", name)
        self.extract_data(soup)

    def extract_data(self, soup):

        key = None

        for atibute in soup.find_all("tr"):
            for column in self.config["columns_list"]:
                if column in atibute.text:
                    key, value = atibute.text.split("<td>")[0].split("\n")[1:-1]

            if "Комплектация" in atibute.text:
                key, value = atibute.text.split("<td>")[0].split("\n")[1:-1]
                value = value.replace(",", ";")

            if key is not None:
                self.add_attribute_dict(key, value)
            key = None

        notebook_price = soup.find("p", class_="price").text
        self.add_attribute_dict("Цена", notebook_price)


HTML_1_Parser("source1").parse_source(), HTML_2_Parser("source2").parse_source()
