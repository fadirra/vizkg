from .chart import Chart
import matplotlib.pyplot as plt
import seaborn as sns

class HeatMap(Chart):
    def __init__(self, dataframe, kwargs):
        """
        Constructs all the necessary attributes for the HeatMap object

        Parameters:
            dataframe (pandas.Dataframe): The dataframe
        """
        Chart.__init__(self, dataframe, kwargs)

    def plot(self):
        """
        Generate HeatMap visualization
        """

        if self._is_numerical_column_exist(3):
            #plot HeatMap
            plt.figure(figsize=(13,8))
            sns.heatmap(self.dataframe.corr(), annot = True)
            plt.show(block=True)