import logging
import numpy as np
import pandas as pd
import plotly.express as px

from abc import ABC, abstractmethod

LOGGER = logging.getLogger(__name__)


class Data(ABC):
    """Interface"""
    def load(self):
        pass


class _ColumnDataFromCSV(Data):
    """Get column from CSV and return pandas data frame"""

    def load(self, path: str, column_name: str, sep=',') -> pd.DataFrame:
        df = pd.read_csv(path, sep=sep)
        self.data_frame = pd.DataFrame(df.get(column_name))

        if self.data_frame is None:
            print("none")
            return None

        return self.data_frame


class Factory(ABC):

    @abstractmethod
    def create(self):
        pass

    def produce_result(self, configuration: dict, data) -> px:
        c = configuration
        d = data
        producer = self.create(d, c)
        result = producer.produce()
        return result


class Producer():
    """Interface"""
    def new(self):
        pass

    def produce(self):
        pass


class _FactoryManager():
    """Manage data init and processing."""
    def __init__(self, data_loader: Data, path_to_data: str, cname: str) -> None:
        self.dframe = data_loader().load(path=path_to_data, column_name=cname, sep=',')

        return None

    def job(self, data_process_factory: Factory, configuration: dict) -> px:
        figure = data_process_factory.produce_result(configuration, self.dframe)

        return figure


class _UniqValues(Factory):
    def create(self, data, *args):
        c = args
        d = data
        uniq_values_producer = _UniqValuesProducer().new(d, c)

        return uniq_values_producer


class _UniqValuesProducer(Producer):
    """
    Report repeated lines and it's number of occurrences, Eq. GNU command uniq -c
    """

    def new(self, data, *args):
        """Init and configure uniq_values method"""

        self.data_frame = data
        print(type(self.data_frame))
        self.desc = False
        self.limit = 10
        self.column_label = "Value"

        conf = args[0][0]
        conf_dict = dict(conf)

        if 'desc' in conf_dict:
            desc = conf_dict['desc']
            self.desc = desc

        if 'limit' in conf_dict:
            limit = conf_dict['limit']
            self.limit = limit

        if 'column_label' in conf_dict:
            self.column_label = conf_dict["column_label"]

        return self

    def produce(self) -> pd.DataFrame:
        column_names = []
        number_of_occurrences = []

        self.column_names_number_of_occurrences = {}

        # Uniq and count. Data in frame are converted to string to avoid comparison of non-matching types
        column_names, number_of_occurrences = np.unique(self.data_frame.astype(str),
                                                        return_counts=True)

        # Reverse the order of lists for descending result
        if self.desc:
            reversed(column_names)
            reversed(number_of_occurrences)

        self.values_and_number_of_occurrences = list(zip(column_names, number_of_occurrences))

        self.data_frame = pd.DataFrame(self.values_and_number_of_occurrences,
                                       columns=[self.column_label, "Number of occurrences"])

        self.sorted_data_frame = self.data_frame.sort_values(by=['Number of occurrences'], ascending=False)

        data = self.sorted_data_frame
        data_limited = data[:self.limit]

        data_count = data_limited.count(0).to_list()

        x_vals = [x for x in range(0, data_count[0])]

        fig = px.bar(data_limited,
                     x=x_vals,
                     y="Number of occurrences",
                     hover_data=["Value"]
                     )

        return fig


class _FrequencyOfOccurrences(Factory):
    def create(self, data, *args):
        cfg = args
        foop = _FrequencyOfOccurrencesProducer().new(data, cfg)

        return foop


class _FrequencyOfOccurrencesProducer(Producer):
    """
    Suppose you want to know how often you will meet the value when reading list of values line by line expressed as histogram.
    For example in the following set:
        a,b,a,b,a,b,a,b
    We have 8 items and we want to know the frequency of occurrences of letter b.
    X axe value = number of items - sequence
    Y axe value = for each x - y is either 0 b is not present or 1 b is present

    Outputs x,y coordinates 0:0,1:1,2:0,3:1,4:0:5:1... each 1 is bar on plot, 0 is empty space
    """

    def new(self, data, *args):

        self.column_label = ["Unknown"]
        self.value = str

        conf = args[0][0]
        conf_dict = dict(conf)

        if 'column_label' in conf_dict:
            self.column_label = conf_dict['column_label']

        searched_value = conf_dict['value']

        self.value = str(searched_value)
        self.data = data

        return self

    def produce(self) -> pd.DataFrame:
        self.x = "Slice sequence"
        self.y = "Value presence"
        binary_records = []

        # Create tuple of 0 and 1, 1 for match and vice versa
        for _, item in self.data.iterrows():
            if self.value in str(item):
                binary_records.append(1)
            else:
                binary_records.append(0)

        sequence = [x for x in range(len(binary_records))]
        coordinates = list(zip(sequence, binary_records))

        self.data_frame = pd.DataFrame(coordinates, columns=[self.x, self.y])

        print(self.data_frame)

        fig = px.bar(self.data_frame, x=self.x, y=self.y)

        return fig
