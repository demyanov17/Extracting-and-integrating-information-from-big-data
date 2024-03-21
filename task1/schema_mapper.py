import re
from mrjob.job import MRJob


class MR_Gender_Analyzer2(MRJob):

    columns = None

    def mapper(self, _, line):

        """ csv -> [key, value]
        Args:
            line(str):
        Returns:
            key(str):
            value(List):
        """

        from operator import itemgetter

        ids = [2,5,6]
        column_values = line.split(",")
        if column_values[1] == "Модель":
            MR_Gender_Analyzer2.columns = itemgetter(*([1] + ids))(column_values)
        else:
            yield (column_values[1], itemgetter(*ids)(column_values)) 
 

    def reducer(self, combi, line):
        line = next(iter(line))
        float(line[1])
        line = list(line)

        yield (combi, line)

if __name__ == '__main__':
    data = []
    Gender_Analyzer = MR_Gender_Analyzer2(["source2.csv"])
    with Gender_Analyzer.make_runner() as runner:
        runner.run()
        for i, (model, atributes) in enumerate(Gender_Analyzer.parse_output(runner.cat_output())):
            new_dict = dict(zip(Gender_Analyzer.columns, [model] + next(iter(atributes))))
            data.append(new_dict)
    import json
    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    with open('source2.json', 'w', encoding='utf8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)
    print(json_data)
