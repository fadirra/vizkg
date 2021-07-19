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

        if self._is_var_exist(self._date_column, 1):
            date_label = self._date_column[0]
            if self._is_var_exist(self._numerical_column, 1):
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
            self.figsize = self.__set_figsize(self.kwargs.get('figsize'))
            #check if param figsize exist
            if self.figsize is not None:
                ax = dataframe.plot.area(stacked=True, figsize=self.figsize)
                plt.show(block=True)
            else:
                ax = dataframe.plot.area(stacked=True, figsize=(15,10))
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