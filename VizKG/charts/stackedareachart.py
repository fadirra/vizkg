from .chart import Chart
import matplotlib.pyplot as plt

class StackedAreaChart(Chart):
    def __init__(self, dataframe, kwargs):
        """
        Constructs all the necessary attributes for the StackedAreaChart object

        Parameters:
            dataframe (pandas.Dataframe): The dataframe
        """
        Chart.__init__(self, dataframe, kwargs)

    def promote_to_candidate(self):

        is_promote = False
        check_var = self._is_var_exist(self._numerical_column, 1) and self._is_var_exist(self._date_column, 1)
        if check_var:
            if (len(self._numerical_column) == 1):
                if len(self.dataframe[self._date_column[0]].unique()) == len(self.dataframe):
                    is_promote = True
                else:
                    is_promote = False
            else:
                is_promote = True

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
  

    def draw(self):
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

