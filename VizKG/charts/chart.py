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
        self.kwargs = kwargs
                
        self._uri_column = self._set_uri_column()
        self._date_column = self._set_date_column()
        self._numerical_column = self._set_numerical_column()
        self._coordinate_column = self._set_coordinate_column()
        self._img_column = self._set_image_column()
        self._label_column = self._set_label_column()
        
    def promote_to_candidate(self):
        "Check required variable to generate chart"
        pass

    def plot(self):
        "Generate visualization"
        pass

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

    def _set_label_column(self):
        """
        Get label column name of dataframe based on 'string' dtypes 
            with excluded uri, image url and coordinate column

        :return: (list) label_column: list of label column        
        """
        str_column = list(self.dataframe.columns)
        
        #exclude uri, image url, coordinate column
        excluded_column = self._uri_column + self._img_column + self._coordinate_column + self._numerical_column + self._date_column
        label_column = [i for i in str_column + excluded_column if i not in str_column or i not in excluded_column]

        return label_column

    def _set_item_and_categorical(self):
        """
        Set item and categorical var from label column
        set categorical var if unique value <= (len(self.dataframe) / 2)

        :return: (list,list) list_item_col, list_of_categorical_variable: list of name        
        """
        item_col = []
        categorical_col = []

        filter_col = []
        if len(self._label_column) > 0:
            filter_col = self._label_column

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

