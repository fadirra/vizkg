from .chart import Chart
import plotly.figure_factory as ff

class Table(Chart):
    def __init__(self, dataframe, kwargs):
        """
        Constructs all the necessary attributes for the Table object

        Parameters:
            dataframe (pandas.Dataframe): The dataframe
        """
        Chart.__init__(self, dataframe, kwargs)

    def plot(self):
        """
        Generate table visualization
        """
        fig = ff.create_table(self.dataframe)
        fig.show()    