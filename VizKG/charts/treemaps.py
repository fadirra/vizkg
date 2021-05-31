from .chart import Chart
import plotly.express as px

class TreeMap(Chart):
    def __init__(self, dataframe, kwargs):
        """
        Constructs all the necessary attributes for the TreeMap object

        Parameters:
            dataframe (pandas.Dataframe): The dataframe
        """
        Chart.__init__(self, dataframe, kwargs)

    def _check_requirements(self):
        """
        Check the requirements for generating TreeMap visualization

        Returns:
            (list) label_column: label name
            (list) numerical_column: list of numerical column
        """
        label_column = None
        numerical_column = None
        
        if self._is_label_column_exist(1):
            label_column = self._label_column
            if self._is_numerical_column_exist(1):
                numerical_column = self._numerical_column

        
        return label_column, numerical_column    

    def plot(self):
        """
        Generate TreeMap visualization
        """
        label_column, numerical_column  = self._check_requirements()

        if label_column is not None and numerical_column is not None:
            values_label,hover_label = self._check_numerical_columns()
            if hover_label is not None:
                #plot
                fig = px.treemap(self.dataframe, values=values_label, path=label_column, hover_data=[hover_label], labels={hover_label:hover_label})
                fig.show()
            else:
                fig = px.treemap(self.dataframe, values=values_label, path=label_column)
                fig.show()                


