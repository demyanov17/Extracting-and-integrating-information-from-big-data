import os
import ast
import json
import numpy as np
from mrjob.job import MRJob
from typing import List, Tuple, Dict
from strings_similarity_metrics import jaro_similarity, jaro_winkler_similarity


class MR_Duplicate_Finder(MRJob):

    ##############################
    #                            #
    #     Disjoint Blocking      #
    #                            #
    ##############################

    #####################################################
    #                 |               |                 #
    #    ###########  |  ###########  |  ###########    #
    #    #         #  |  #         #  |  #         #    #
    #    #         #  |  #         #  |  #         #    #
    #    #         #  |  #         #  |  #         #    #
    #    ###########  |  ###########  |  ###########    #
    #                 |               |                 #
    #####################################################

    data_table_color = {
        "Серебристый": "Silver",
        "Серый космос": "Space Gray",
        "Чёрный космос": "Space Black",
    }

    def mapper(self, _: None, line: str) -> Tuple[str, Dict]:
        """Creating a key for each entity included
        in the sources
        Args:
            line(str): string with a feature
            representation of the entity
        Returns:
            key(str): RAM + SSD
            value(dict): dict with a description of the entity
        """

        entity_dict = ast.literal_eval(line[:-1])
        yield f"RAM: {entity_dict['Оперативная память']} GB, SSD: {entity_dict['Объём памяти']} GB", entity_dict

    def reducer(self, block_key: str, entities: List[Dict]) -> Tuple[str, List[Dict]]:
        """Finding duplicates in the disjoint block
        Args:
            block_key(str): created key(RAM + SSD) which
            describes this block
            entities(list): contains list of dicts with a
            description of entities satisfying this block
        Returns:
            key(str): key(RAM + SSD) that
            describes this block
            value(list): a list containing lists consisting
            of duplicate dictionaries
        """

        entities = list(entities)
        lenght = len(entities)
        duplicates = [[entities[i]] for i in range(lenght)]
        for i in range(lenght - 1):
            for j in range(i + 1, lenght):
                if self.similarity_checker(entities[i], entities[j]):
                    duplicates[i].append(entities[j])

        yield (block_key, duplicates)

    def similarity_checker(self, entity_1: Dict, entity_2: Dict, threshold=0.92) -> bool:
        """Calculate entity similarity and
        comparing it with a threshold value
        Returns:
            bool: duplicate indicator
            between two entities
        """

        attribute_similarity_scores = np.asarray(
            [
                jaro_similarity(entity_1["Модель"], entity_2["Модель"]),
                entity_1["Год выпуска"] == entity_2["Год выпуска"],
                entity_1["Разрешение экрана"] == entity_2["Разрешение экрана"],
                entity_1["Процессор"] == entity_2["Процессор"],
                entity_1["Количество ядер"] == entity_2["Количество ядер"],
                (
                    self.data_table_color[entity_1["Цвет"]]
                    if entity_1["Цвет"] in self.data_table_color.keys()
                    else entity_1["Цвет"]
                )
                == (
                    self.data_table_color[entity_2["Цвет"]]
                    if entity_2["Цвет"] in self.data_table_color.keys()
                    else entity_2["Цвет"]
                ),
                jaro_winkler_similarity(
                    "".join(entity_1["Комплектация"]), "".join(entity_2["Комплектация"])
                ),
                abs(entity_1["Вес"] - entity_2["Вес"]) < 0.1,
                abs(entity_1["Цена"] - entity_2["Цена"]) < 40000,
            ]
        )

        attribute_weights = np.ones(attribute_similarity_scores.shape[0])
        attribute_weights[1:6] *= 10
        attribute_weights /= attribute_weights.sum()

        return (attribute_similarity_scores * attribute_weights).sum() > threshold


if __name__ == "__main__":

    json_data = []

    with open("../task1/source1.json") as json_file:
        json_data = json.load(json_file)
    with open("../task1/source2.json") as json_file:
        json_data.extend(json.load(json_file))

    with open("raw_data.json", "w", encoding="utf8") as json_file:
        for item in json_data:
            json.dump(item, json_file, ensure_ascii=False)
            json_file.write(",\n")

    data = []
    Duplicate_Finder = MR_Duplicate_Finder(["raw_data.json"])
    with Duplicate_Finder.make_runner() as runner:
        runner.run()
        for _, duplicate_lists_of_dicts in Duplicate_Finder.parse_output(
            runner.cat_output()
        ):
            for duplicate_list_of_dicts in duplicate_lists_of_dicts:
                data.append({"duplicates": duplicate_list_of_dicts})
    
    os.remove("raw_data.json")

    with open("duplicates.json", "w", encoding="utf8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
