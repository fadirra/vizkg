from .chart import Chart
import plotly.express as px

class ScatterChart(Chart):
    def __init__(self, dataframe, kwargs):
        """
        Constructs all the necessary attributes for the ScatterChart object

        Parameters:
            dataframe (pandas.Dataframe): The dataframe
        """
        Chart.__init__(self, dataframe, kwargs)

    def _check_requirements(self):
        """
        Check the requirements for generating ScatterChart visualization

        Returns:
            (list) numerical_columns: list of numerical column
            (string) label_name: label name
        """
        numerical_columns = None
        label_name = None

        if self._is_numerical_column_exist(2):
            numerical_columns = self._numerical_column
            if len(self._label_column) > 0:
                label_name = self._label_column[0]
        
        return numerical_columns, label_name    

    def plot(self):
        """
        Generate ScatterChart visualization
        """
        numerical_columns, label_name = self._check_requirements()

        if numerical_columns is not None:
            x_label = numerical_columns[0]
            y_label = numerical_columns[1]
            if label_name is not None:
                fig = px.scatter(self.dataframe, x=x_label, y=y_label, color=label_name)
                fig.show()
            else:
                fig = px.scatter(self.dataframe, x=x_label, y=y_label)
                fig.show()                