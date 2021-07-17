import re
import statistics

class Chart():
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
        self._coordinate_column = self._set_coordinate_column()
        self._img_column = self._set_image_column()
        self._label_column = self._set_label_column()
        
    def promote_to_candidate(self):
        pass

    def _set_label_column(self):
        """
        Get label column name of dataframe based on 'string' dtypes 
            with excluded uri, image url and coordinate column
            and sort based on unique value

        :return: (list) label_column: list of label column        
        """
        str_column = list(self.dataframe.columns)
        
        #exclude uri, image url, coordinate column
        excluded_column = self._uri_column + self._img_column + self._coordinate_column + self._numerical_column + self._date_column
        label_column = list(set(str_column) - set(excluded_column))

        #sort based on unique value (ASC)
        unique_dict = {name:len(self.dataframe[name].unique()) for name in (label_column)}
        sort_dict = {k: v for k, v in sorted(unique_dict.items(), key=lambda item: item[1])}

        sorted_label_column = list(sort_dict.keys())
        return sorted_label_column

    def _set_item_and_categorical(self):
        """
        Set item and categorical var from label or uri column

        :return: (list,list) list_item_col, list_of_categorical_variable: list of name        
        """
        item_col = []
        categorical_col = []

        filter_col = []
        if len(self._label_column) > 0:
            filter_col = self._label_column
        elif len(self._uri_column) > 0:
            filter_col = self._uri_column
        else:
            pass

        unique_dict = {name:len(self.dataframe[name].unique()) for name in (filter_col)}
        sort_dict = {k: v for k, v in sorted(unique_dict.items(), key=lambda item: item[1])}
        for name, value in sort_dict.items():
            if value <= (len(self.dataframe) / 2):
                categorical_col.append(name)
            else:
                item_col.append(name)
        return item_col, categorical_col

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
        """
        Get uri column name of dataframe based on regex pattern

        :return: (list) uri_column: list of uri variable
        """
        #Regex pattern
        pattern_url = r"^(?:http(s)?:\/\/)[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$(?<!.[jpg|gif|png|JPG|PNG])" 
        uri_column = self.set_column_based_on_regex(pattern_url)

        return uri_column

    def _set_image_column(self):
        """
        Get image column name of dataframe based on regex pattern

        :return: (list) image_column: list of image variable
        """
        #Regex pattern
        pattern_img = r"^http(s)?://(?:[a-z0-9\-]+\.)+[a-z]{2,6}(?:/[^/#?]+)+\.(?:jpg|jpeg|gif|png|JPG|JPEG|Jpeg)$"        
        image_column = self.set_column_based_on_regex(pattern_img)

        return image_column

    def _set_coordinate_column(self):
        """
        Get coordinate column name of dataframe based on regex pattern

        :return: (list) coordinate_column: list of coordinate variable
        """
        #Regex pattern
        pattern_coordinate1 = r"^Point"
        pattern_coordinate2 = r"^POINT"
        coordinate_column1 = self.set_column_based_on_regex(pattern_coordinate1)
        coordinate_column2 = self.set_column_based_on_regex(pattern_coordinate2)
        
        coordinate_column = coordinate_column1 + coordinate_column2
        return coordinate_column

    def set_column_based_on_regex(self, pattern):
        """
        Set list of column name based on regex matching

        :return: (list) column: list of name
        """
        list_column = []

        for i in range (len(self.dataframe.columns)):
            column_name = self.dataframe.columns[i]
            column = self.dataframe[self.dataframe.columns[i]]
            is_matched_column = self.check_data_per_column(column, pattern)
            if is_matched_column:
                list_column.append(column_name)
        
        return list_column

    def check_data_per_column(self, column, pattern):
        """
        Check entire data per column of dataframe if matched with regex pattern

        Parameters:
            (pandas.Dataframe) column: column of dataframe
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

    def _is_var_exist(self, column, request=1):
        """
        Check if list exist return True if exist

        Parameters:
            (int) request:number of required column
        
        Returns:
            (boolena) is_exist: True if list exist
        """
        is_exist = False
        if len(column) >= request:
            is_exist = True
        else:
            is_exist = False
        
        return is_exist

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
            print(f"Missing {str(miss)} required label variable")

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
            print(f"Missing {str(miss)} required date variable")
        
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
        if len(self._numerical_column) >= request:
            is_exist = True
        else:
            miss = request - len(self._numerical_column)
            print(f"Missing {str(miss)} required numerical variable")
        
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
        if len(self._uri_column) >= request:
            is_exist = True
        else:
            miss = request - len(self._uri_column)
            print(f"Missing {str(miss)} required uri variable as identifiers")
        
        return is_exist

    def _is_img_uri_column_exist(self, request=1):
        """
        Check if list exist return True if exist

        Parameters:
            (int) request:number of required column
        
        Returns:
            (boolena) is_exist: True if list exist
        """
        is_exist = False
        miss = request
        if len(self._img_column) >= request:
            is_exist = True
        else:
            print(f"Missing {str(miss)} required image variable")
        
        return is_exist  

    def _is_coordinate_exist(self, request=1):
        """
        Check if list exist return True if exist

        Parameters:
            (int) request:number of required column
        
        Returns:
            (boolena) is_exist: True if list exist
        """
        is_exist = False
        miss = request
        if len(self._coordinate_column) >= request:
            is_exist = True
        else:
            print(f"Missing {str(miss)} required coordinate variable")
        
        return is_exist  

    def _get_label_from_uri(self, uri_column):
        """
        Add and get label column (name) from uri (extract name from the last slash in uri)

        Parameters:
            (string) uri_column: Name of uri column
        
        Returns:
            (string) column_name: Name of label column 
        """
        column_name = (f"{uri_column}Label")
        self.dataframe[column_name] = self.dataframe[uri_column].apply(lambda x: x.split("/")[-1])

        return column_name

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