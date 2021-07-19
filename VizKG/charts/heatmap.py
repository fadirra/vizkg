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

        if self._is_var_exist(self._numerical_column, 2):

            self.figsize = self.__set_figsize(self.kwargs.get('figsize'))
            #check if param figsize exist
            if self.figsize is not None:
                plt.figure(figsize=self.figsize)
                sns.heatmap(self.dataframe.corr(), annot = True)
                plt.show(block=True)
            else:                 
                #plot HeatMap
                plt.figure(figsize=(13,8))
                sns.heatmap(self.dataframe.corr(), annot = True)
                plt.show(block=True)

    @staticmethod
    def __set_figsize(figsize_input):
        """
        Setter of figsize based on figsize input for matplotlib chart

        Parameters:
            (tuple) figsize_input: The figsize input

        Returns:
            (tuple) figsize: The result figsize  
        """
        figsize = None
        is_numeric_value = None

        try:
            if figsize_input is not None and len(figsize_input) == 2:
                is_numeric_value = all(isinstance(v, int) or isinstance(v, float) for v in figsize_input)
            else:
                is_numeric_value = False
        except:
            is_numeric_value = False
            
        if is_numeric_value:
            figsize = figsize_input
        else:
            figsize = None

        return figsize