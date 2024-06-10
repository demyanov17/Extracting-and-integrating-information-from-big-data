import os
import ast
import json
from mrjob.job import MRJob
from typing import List, Tuple, Dict


class Data_Fusion(MRJob):

    duplicates_number = 0

    color_data_table = {
        "Серебристый": "Silver",
        "Серый космос": "Space Gray",
        "Чёрный космос": "Space Black",
    }

    def mapper(self, _: None, line: str) -> Tuple[str, List]:
        """Counting the number of duplicates and
        generating all variations of the entity for each of them
        Args:
            line(str):
        Returns:
            key(str): duplicate_number
            value(List): dicts with a description of the entity
        """
        Data_Fusion.duplicates_number += 1
        yield "duplicate_" + str(self.duplicates_number), line

    def reducer(self, duplicates_number: str, duplicates: str) -> Tuple[str, Dict]:
        """Resolves conflict among controversial attributes
        in different versions of a duplicate
        Args:
            duplicates_number(str): string with duplicate number
            duplicates(str): contains list of dicts with a
            description of the entity
        Returns:
            key(str): duplicate_number
            value(dict): description of the entity
            over which conflicts resolved
        """

        atributes_resolving_strategy = {
            "Модель": lambda atribute_values: min(atribute_values, key=lambda i: len(i)),
            "Цвет": lambda atribute_values: self.color_data_table[atribute_values[0]] if atribute_values[0] in self.color_data_table.keys() else atribute_values[0],
            "Комплектация": self.choose_longest,
            "Вес": self.float_avg,
            "Цена": lambda atribute_values: sum(atribute_values) // len(atribute_values),
        }

        duplicates_dict = ast.literal_eval(next(duplicates)[:-1])
        entity_versions = duplicates_dict["duplicates"]

        if len(entity_versions) == 1:
            yield (duplicates_number, entity_versions[0])

        fused_entity = dict()
        for key in entity_versions[0].keys():
            if key in atributes_resolving_strategy.keys():
                fused_entity[key] = atributes_resolving_strategy[key]([entity_version[key] for entity_version in entity_versions])
            else:
                fused_entity[key] = entity_versions[0][key]

        yield (duplicates_number, fused_entity)


    def float_avg(self, atribute_values):
        def toFixed(numObj, digits=2):
            return f"{numObj:.{digits}f}"

        return float(toFixed(sum(atribute_values) / len(atribute_values)))


    def choose_longest(self, atribute_values):

        fused_list = []
        find_longest_value = lambda atribute_values: max(atribute_values, key=lambda i: len(i))
        for i in range(len(atribute_values[0])):
            curr_value_list = [list_value[i] for list_value in atribute_values]
            fused_list.append(find_longest_value(curr_value_list))
        return fused_list


if __name__ == "__main__":

    json_data = []

    with open("../task2/duplicates.json") as json_file:
        json_data = json.load(json_file)

    with open("raw_data.json", "w", encoding="utf8") as json_file:
        for item in json_data:
            json.dump(item, json_file, ensure_ascii=False)
            json_file.write(",\n")

    data = []
    Fusy = Data_Fusion(["raw_data.json"])
    with Fusy.make_runner() as runner:
        runner.run()
        for _, resolved_entity in Fusy.parse_output(runner.cat_output()):
            data.append(resolved_entity)

    os.remove("raw_data.json")

    with open("enteties.json", "w", encoding="utf8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
