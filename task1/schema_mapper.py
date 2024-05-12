import re
import yaml, json
from mrjob.job import MRJob
from typing import List, Tuple
from operator import itemgetter


class Source_Mapper:

    columns = None
    with open("schema_mapper.yaml", "r") as stream:
        config = yaml.safe_load(stream)

    def reducer(self, model: str, model_attributes: List) -> Tuple[str, List]:
        yield (model, list(model_attributes))


class Source1_Mapper(Source_Mapper, MRJob):

    def __init__(self, data):
        Source_Mapper.__init__(self)
        MRJob.__init__(self, data)

    def mapper(self, _: None, line: str) -> Tuple[str, List]:
        """Converts strings from csv to single schema format
        Args:
            line(str): string with a feature
            representation of the entity
        Returns:
            key(str): laptop model name
            value(List): list of converted attributes
            whose values ​​satisfy the target schema
        """
        config = Source_Mapper.config["source1"]
        ids = config["ids"]
        column_values = line.split(",")
        if column_values[config["model_name_id"]] == "Модель":
            Source1_Mapper.columns = itemgetter(*([config["model_name_id"]] + ids))(column_values)
        else:
            process_name = column_values[config["process_name_id"]].split(" (")[0][1:]
            cores_number = int(config["cores_id"])
            ssd_memory_capacity, type_ = column_values[config["ssd_id"]].split()[1:]
            ssd_memory_capacity = int(ssd_memory_capacity)
            if type_ == "ТБ":
                ssd_memory_capacity *= 1024
            ram_capacity = int(column_values[config["ram_id"]].split()[0])
            screen = column_values[config["screen_id"]].split()[0][1:]
            equipment = column_values[config["equipment_id"]].split(" / ")
            year = int(column_values[config["year_id"]])
            color = column_values[config["color_id"]]
            weight = float(column_values[config["weight_id"]])
            price = int(column_values[config["price_id"]].replace(" ", "").split("р")[0])
            yield (
                column_values[config["model_name_id"]],
                [
                    year,
                    ssd_memory_capacity,
                    ram_capacity,
                    screen,
                    process_name,
                    cores_number,
                    color,
                    equipment,
                    weight,
                    price,
                ],
            )


class Source2_Mapper(Source_Mapper, MRJob):

    def __init__(self, data):
        Source_Mapper.__init__(self)
        MRJob.__init__(self, data)

    def mapper(self, _: None, line: str) -> Tuple[str, List]:
        """csv -> [key, value]
        Converts strings from csv to single schema format
        Args:
            line(str): string with a feature
            representation of the entity
        Returns:
            key(str): laptop model name
            value(List): list of converted attributes
            whose values ​​satisfy the target schema
        """
        config = Source_Mapper.config["source2"]
        ids = config["ids"]
        column_values = line.split(",")
        if column_values[config["model_name_id"]] == "Модель":
            Source2_Mapper.columns = itemgetter(*([config["model_name_id"]] + ids))(column_values)
        else:
            process_name = column_values[config["process_name_id"]]
            cores_number = int(column_values[config["cores_id"]])
            ssd_memory_capacity = int(column_values[config["ssd_id"]].split()[0])
            ram_capacity = int(column_values[config["ram_id"]].split()[0])
            equipment = column_values[config["equipment_id"]].split("; ")
            year = int(column_values[config["year_id"]])
            weight = float(column_values[config["weight_id"]].split()[0])
            price = int(column_values[config["price_id"]].split("р")[0].replace(" ", ""))
            yield (
                column_values[config["model_name_id"]],
                [
                    year,
                    ssd_memory_capacity,
                    ram_capacity,
                    column_values[config["screen_id"]].replace("×", "x"),
                    process_name,
                    cores_number,
                    column_values[config["color_id"]],
                    equipment,
                    weight,
                    price,
                ],
            )


class Schema_Mapper():

    def __init__(self, source_name):
        self.source_name = source_name
        with open("schema_mapper.yaml", "r") as stream:
            self.config = yaml.safe_load(stream)

    def map_source(self):

        data = []
        source_mappers_dict = {"source1": Source1_Mapper, "source2": Source2_Mapper}
        Source_Mapper = source_mappers_dict[self.source_name]([f"{self.source_name}.csv"])
        with Source_Mapper.make_runner() as runner:
            runner.run()
            Source_Mapper.columns = self.config["schema_columns"]
            for model, atributes in Source_Mapper.parse_output(runner.cat_output()):
                new_dict = dict(zip(Source_Mapper.columns, [model] + next(iter(atributes))))
                data.append(new_dict)
        with open(f"{self.source_name}.json", "w", encoding="utf8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

Schema_Mapper("source1").map_source(), Schema_Mapper("source2").map_source()
