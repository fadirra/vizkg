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

    def promote_to_candidate(self):

        is_promote = self._is_var_exist(self._label_column, 1)

        return is_promote

    def plot(self):
        """
        Generate visualization
        """
        if self.promote_to_candidate():
            self.draw()
        else:
            pass

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
            if self._is_var_exist(self._numerical_column):
                numerical_column = self._numerical_column

        
        return label_column, numerical_column    

    def draw(self):
        """
        Generate TreeMap visualization
        """
        label_column, numerical_column  = self._check_requirements()
        values_label,hover_label = None,None
        if self._is_var_exist(self._numerical_column):
            values_label,hover_label = self._check_numerical_columns()
        else:
            pass

        if hover_label is not None:
            #plot
            fig = px.treemap(self.dataframe, values=values_label, path=label_column, hover_data=[hover_label], labels={hover_label:hover_label})
            fig.show()
        elif numerical_column is not None:
            fig = px.treemap(self.dataframe, values=values_label, path=label_column)
            fig.show()
        else:
            fig = px.treemap(self.dataframe, path=label_column)
            fig.show()                                


