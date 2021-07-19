from .chart import Chart
import plotly.express as px

class AreaChart(Chart):
    def __init__(self, dataframe, kwargs):
        """
        Constructs all the necessary attributes for the AreaChart object

        Parameters:
            dataframe (pandas.Dataframe): The dataframe
        """
        Chart.__init__(self, dataframe, kwargs)

    def promote_to_candidate(self):

        is_promote = self._is_var_exist(self._numerical_column, 1) and self._is_var_exist(self._date_column, 1)

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
        Check the requirements for generating AreaChart visualization

        Returns:
            (string) date_label: date label  for axis-x
            (string) int_label: numerical label for axis-y
            (string) label_name: label name
        """
        date_label = None
        int_label = None
        label_name = None

        if self._is_var_exist(self._date_column, 1):
            date_label = self._date_column[0]
            if self._is_var_exist(self._numerical_column, 1):
                int_label = self._numerical_column[0]
                if self._is_var_exist(self._label_column, 1):
                    label_name = self._label_column[0]
        
        return date_label, int_label, label_name          

    def draw(self):
        """
        Generate AreaChart visualization
        """
        date_label, numerical_label, label_name  = self._check_requirements()

        if label_name is not None:
            #plot
            fig = px.area(self.dataframe, x=date_label, y=numerical_label, color=label_name, line_group=label_name)
            fig.show()
        else:
            fig = px.area(self.dataframe, x=date_label, y=numerical_label)
            fig.show()

