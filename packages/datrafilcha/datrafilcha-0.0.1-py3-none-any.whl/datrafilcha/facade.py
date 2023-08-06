from os import path

from . import graph_functions
from .graph_functions import _FactoryManager, _ColumnDataFromCSV


class DataFiltersFacade:
    def __init__(self):
        self.factory_manager = _FactoryManager

    def csv_column(self, function_cfg: dict, data_source_file: str, column: str):
        """
        Process column based data from CSV based on configuration
        """

        # Setup
        function_type = function_cfg['id']

        # Check method existence - avoid unnecessary data processing
        if not hasattr(graph_functions, function_type):
            raise NameError("Graphing function doesn't exists! ")

        # Check data exists
        if not path.exists(data_source_file):
            raise NameError("Data source doesn't exists")

        # Factory - loads data, filter/process data
        factory = self.factory_manager(_ColumnDataFromCSV, data_source_file, column)

        data_processing_function = getattr(graph_functions, function_type)

        cfg_of_function = {}
        if len(function_cfg) > 1:
            cfg_of_function = {k: v for k, v in function_cfg.items() if k != 'id'}

        # Generate data with desired function
        figure = factory.job(data_process_factory=data_processing_function(),
                             configuration=cfg_of_function)

        html_data = figure.to_html(full_html=False)

        return html_data
