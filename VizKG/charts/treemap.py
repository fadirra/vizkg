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
            (list) numerical_var: numerical variable
        """
        label_column = None
        numerical_var = None
        
        if self._is_var_exist(self._label_column, 1):
            label_column = self._label_column
            if self._is_var_exist(self._numerical_column):
                numerical_var = self._numerical_column[0]

        
        return label_column, numerical_var    

    def draw(self):
        """
        Generate TreeMap visualization
        """
        label_column, numerical_var  = self._check_requirements()

        if numerical_var is not None:
            fig = px.treemap(self.dataframe, values=numerical_var, path=label_column)
            fig.show()
        else:
            fig = px.treemap(self.dataframe, path=label_column)
            fig.show()                                
