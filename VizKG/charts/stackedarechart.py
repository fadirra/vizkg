from .chart import Chart
import matplotlib.pyplot as plt
import plotly.express as px

class StackedAreaChart(Chart):
    def __init__(self, dataframe, kwargs):
        """
        Constructs all the necessary attributes for the StackedAreaChart object

        Parameters:
            dataframe (pandas.Dataframe): The dataframe
        """
        Chart.__init__(self, dataframe, kwargs)

    def _check_requirements(self):
        """
        Check the requirements for generating StackedAreaChart visualization

        Returns:
            (string) date_label: date label  for axis-x
            (list) numerical_columns: numerical list
        """
        date_label = None
        numerical_column = None

        if self._is_date_column_exist(1):
            date_label = self._date_column[0]
            if self._is_numerical_column_exist(1):
                numerical_column = self._numerical_column
        
        return date_label, numerical_column          
  

    def plot(self):
        """
        Generate StackedAreaChart visualization
        """
        date_label, numerical_column  = self._check_requirements()

        if date_label is not None and numerical_column is not None:
            #set index by date label
            dataframe = self.dataframe.copy()
            dataframe = dataframe.set_index(date_label)
            #plot
            ax = dataframe.plot.area(stacked=True, figsize=(15,10))
            plt.show(block=True)

