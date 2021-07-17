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

    def promote_to_candidate(self):

        is_promote = self._is_var_exist(self._numerical_column, 2)

        return is_promote

    def plot(self):
        """
        Generate visualization
        """
        if self.promote_to_candidate():
            self.draw()
        else:
            pass

    def draw(self):
        """
        Generate HeatMap visualization
        """

        if self._is_numerical_column_exist(2):
            #plot HeatMap
            plt.figure(figsize=(13,8))
            sns.heatmap(self.dataframe.corr(), annot = True)
            plt.show(block=True)