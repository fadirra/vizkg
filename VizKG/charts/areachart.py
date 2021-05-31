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

        if self._is_date_column_exist(1):
            date_label = self._date_column[0]
            if self._is_numerical_column_exist(1):
                int_label = self._numerical_column[0]
                if self._is_label_column_exist(1):
                    label_name = self._label_column[0]
        
        return date_label, int_label, label_name          

    def plot(self):
        """
        Generate AreaChart visualization
        """
        date_label, numerical_label, label_name  = self._check_requirements()

        if date_label is not None and numerical_label is not None and label_name is not None:
            #plot
            fig = px.area(self.dataframe, x=date_label, y=numerical_label, color=label_name, line_group=label_name)
            fig.show()

