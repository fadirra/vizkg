import re
import pandas as pd
import matplotlib.pyplot as plt
import statistics

class Chart:
    def __init__(self, dataframe, kwargs):
        """
        Constructs all the necessary attributes for the Chart object

        Parameters:
            dataframe (pandas.Dataframe): The dataframe
            kwargs: Arbitrary keyword arguments.
        """
        self.dataframe = dataframe
        self.mode_keyword = self.__set_mode(kwargs.get('mode_keyword'))
        self.figsize = self.__set_figsize(kwargs.get('figsize'))
        
        self._uri_column = self._set_uri_column()
        self._date_column = self._set_date_column()
        self._numerical_column = self._set_numerical_column()
        self._label_column = self._set_label_column()
        self.candidate_viz = self.candidate_form()

    def _set_label_column(self):
        """
        Get object or label column name of dataframe based on regex and object data type
        """
        #Regex pattern
        pattern_url = r"^(?:http(s)?:\/\/)[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$(?<!.[jpg|gif|png|JPG|PNG])" 
        label_column = []

        for i in range (len(self.dataframe.columns)):
            column_name = self.dataframe.columns[i]
            column = self.dataframe[column_name]
            is_uri_column = self.__check_data_per_column(column, pattern_url)
            try:
                if not column_name.startswith(tuple(['coordinate', 'picture'])) and is_uri_column == False and column.dtypes == 'string':
                    label_column.append(column_name)
            except TypeError:
                pass

        return label_column

    def _set_date_column(self):
        """
        Get date column name of dataframe based on date data type
        """
        date_column = [name for name in self.dataframe.columns if self.dataframe[name].dtypes == 'datetime64[ns]']

        return date_column

    def _set_numerical_column(self):
        """
        Get date column name of dataframe based on date data type
        """
        numerical_column = [name for name in self.dataframe.columns if self.dataframe[name].dtypes == 'float64']

        return numerical_column 

    def _set_uri_column(self):
        """
        Get date column name of dataframe based on date data type
        """
        #Regex pattern
        pattern_url = r"^(?:http(s)?:\/\/)[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$(?<!.[jpg|gif|png|JPG|PNG])" 
        uri_column = []

        for i in range (len(self.dataframe.columns)):
            column_name = self.dataframe.columns[i]
            column = self.dataframe[self.dataframe.columns[i]]
            is_uri_column = self.__check_data_per_column(column, pattern_url)
            if is_uri_column:
                uri_column.append(column_name)

        return uri_column

    def candidate_form(self):
        """
        Find candidate form for visualization

        Parameter:
            dataframe (pandas.Dataframe): The data table

        Returns:
            candidate_visualization (list): List of candidate visualization
        """

        candidate_visualization = []
        dimension_column = [name for name in self.dataframe.columns if not name.startswith(tuple(['picture', 'coordinate']))]

        #Add to candidate visualization
        if 'picture' in self.dataframe.columns:
            candidate_visualization.append('ImageGrid')
        if 'coordinate' in self.dataframe.columns:
            candidate_visualization.append('Map')
        if len(self._date_column) >= 1 and len(self._label_column) >= 1:
            candidate_visualization.append('Timeline')
        if len(self._label_column) >= 2 and len(self._uri_column) >= 2:
            candidate_visualization.append('Graph')
            candidate_visualization.append('Tree')
        if len(dimension_column) > 2 :
            candidate_visualization.append('Dimensions')
        if len(self._numerical_column) >= 3:
            candidate_visualization.append('HeatMap')
        if len(self._label_column) >= 1:
            candidate_visualization.append('WordCloud')
        if len(self._label_column) >= 1 and len(self._date_column) >= 1 and len(self._numerical_column) >= 1:
            candidate_visualization.append('AreaChart')
        if len(self._date_column) >= 1 and len(self._numerical_column) >= 2:
            candidate_visualization.append('StackedAreaChart')
        if len(self._numerical_column) >= 2:
            candidate_visualization.append('ScatterChart')
        if len(self._date_column) >= 1 and len(self._numerical_column) >= 1:
            candidate_visualization.append('LineChart')
        if len(self._label_column) <= 2 and len(self._numerical_column) == 1:
            candidate_visualization.append('BarChart')
        if len(self._label_column) >= 2 and len(self._numerical_column) >= 1:
            candidate_visualization.append('TreeMap')
            candidate_visualization.append('SunBurstChart')
        if len(self._numerical_column) >= 1:
            candidate_visualization.append('Histogram')
            candidate_visualization.append('DensityPlot')
        if len(self._label_column) >= 1 and len(self._numerical_column) >= 1:
            candidate_visualization.append('PieChart')
            candidate_visualization.append('DonutChart')
            candidate_visualization.append('BoxPlot')
            candidate_visualization.append('ViolinPlot')
            candidate_visualization.append('BubbleChart')
            candidate_visualization.append('TreeMap')
            candidate_visualization.append('SunBurstChart')
        candidate_visualization.append('Table')

        return set(candidate_visualization)

    def _is_label_column_exist(self, request=1):
        """
        Check if list exist return True if exist

        Parameters:
            (int) request:number of required column
        
        Returns:
            (boolena) is_exist: True if list exist
        """
        is_exist = False
        if len(self._label_column) >= request:
            is_exist = True
        else:
            miss = request - len(self._label_column)
            print(f"Missing {str(miss)} required label column, instead use one of this available chart: {self.candidate_viz}")

        return is_exist

    def _is_date_column_exist(self, request=1):
        """
        Check if list exist return True if exist

        Parameters:
            (int) request:number of required column
        
        Returns:
            (boolena) is_exist: True if list exist
        """
        is_exist = False
        if len(self._date_column) >= request:
            is_exist = True
        else:
            miss = request - len(self._date_column)
            print(f"Missing {str(miss)} required date column, instead use one of this available chart: {self.candidate_viz}")
        
        return is_exist
    
    def _is_numerical_column_exist(self, request=1):
        """
        Check if list exist return True if exist

        Parameters:
            (int) request:number of required column
        
        Returns:
            (boolena) is_exist: True if list exist
        """
        is_exist = False
        candidate_form = self.candidate_viz
        if len(self._numerical_column) >= request:
            is_exist = True
        else:
            miss = request - len(self._numerical_column)
            print(f"Missing {str(miss)} required numerical column, instead use one of this available chart: {self.candidate_viz}")
        
        return is_exist

    def _is_uri_column_exist(self, request=1):
        """
        Check if list exist return True if exist

        Parameters:
            (int) request:number of required column
        
        Returns:
            (boolena) is_exist: True if list exist
        """
        is_exist = False
        candidate_form = self.candidate_viz
        if len(self._uri_column) >= request:
            is_exist = True
        else:
            miss = request - len(self._uri_column)
            print(f"Missing {str(miss)} required uri column as identifiers, instead use one of this available chart: {self.candidate_viz}")
        
        return is_exist

    def _add_candidate_info(self):
        """
        add information of candidate visualization
        """
        candidate_text = "Instead use of this available chart" + self.candidate_viz

        return candidate_text

    def _check_labels(self):
        """
        Check the requirements for label

        Returns:
            (string) axis_label: label for axis
            (string) group_label: label for group_label
            (string) make_axis_label: label for make group_label
        """
        axis_label = None
        group_label = None
        make_axis_label = None

        if len(self._label_column) > 1:
            unique_dict = {name:len(self.dataframe[name].unique()) for name in (self._label_column)}
            sort_dict = {k: v for k, v in sorted(unique_dict.items(), key=lambda item: item[1])}
            fltr_dict = {name:value for name, value in sort_dict.items() if value <= (len(self.dataframe))}
            key_fltr_dict = list(fltr_dict.keys())
            if len(fltr_dict) < 3:
                axis_label = key_fltr_dict[1]
                make_axis_label = key_fltr_dict[0]
            elif len(fltr_dict) >= 3:
                axis_label = key_fltr_dict[2]
                make_axis_label = key_fltr_dict[1]
                group_label = key_fltr_dict[0]
            else:
                axis_label = key_fltr_dict[0]
        else:
            axis_label = self._label_column[0]
        
        if group_label is not None:
            return axis_label,group_label,make_axis_label
        else:
            return axis_label,make_axis_label

    def _check_orientation(self, axis_label, group_label=None, max_number=6):
        """
        Check the requirements for orientation, returns None if horizontal

        Returns:
            (string) orientation: label for axis
        """
        orientation = None
        num_box = 0
        num_axis = len(self.dataframe[axis_label].unique())
        num_box = 0

        if group_label is not None:
            num_group = len(self.dataframe[group_label].unique())
            num_box = num_axis + num_group
        else:
            num_box = num_axis

        if num_box > max_number:
            orientation = 'Horizontal'

        return orientation

    def _check_numerical_columns(self):
        """
        Check the requirements for numerical label

        Returns:
            (string) values_label: label for values
            (string) hover_label: label for hover text
        """
        values_label = None
        hover_label = None

        min_dict = {name:statistics.median(list(self.dataframe[name])) for name in (self._numerical_column)}
        sort_dict = {k: v for k, v in sorted(min_dict.items(), key=lambda item: item[1])}
        if len(sort_dict) > 1:
            values_label = list(sort_dict.keys())[1]
            hover_label = list(sort_dict.keys())[0]
        else:
            values_label = list(sort_dict.keys())[0]
        
        return values_label,hover_label

    def __check_data_per_column(self,column, pattern):
        """
        Check entire data per column of dataframe if matched with regex pattern

        Parameters:
            (pandas.Dataframe) column: column name of dataframe
            (string) pattern: regex pattern

        Returns:
            (boolen) boolean_check: The result table             
        """
        boolean_check = False
        for datapoint in range(len(column)):
            data = column.iloc[datapoint]
            try:
                if re.match(pattern, data):
                    boolean_check = True
            except TypeError:
                pass
                
        return boolean_check

    @staticmethod
    def __set_mode(mode_input):
        """
        Setter of mode based on mode input

        Parameters:
            (bool) mode_input: The mode input

        Returns:
            (bool) mode: The result mode  
        """
        mode = None
        if mode_input is not None and isinstance(mode_input, bool):
            mode = mode_input
        else:
            mode = None
        
        return mode

    @staticmethod
    def __set_figsize(figsize_input):
        """
        Setter of figsize based on figsize input

        Parameters:
            (tuple) figsize_input: The figsize input

        Returns:
            (tuple) figsize: The result figsize  
        """
        figsize = None
        is_numeric_value = None

        if figsize_input is not None and len(figsize_input) == 2:
            is_numeric_value = all(isinstance(v, int) or isinstance(v, float) for v in figsize_input)
        else:
            is_numeric_value = False
            
        if is_numeric_value:
            figsize = figsize_input
        else:
            figsize = None

        return figsize