from .chart import Chart
import plotly.express as px
import datetime

class Timeline(Chart):
    def __init__(self, dataframe, kwargs):
        """
        Constructs all the necessary attributes for the Timeline object

        Parameters:
            dataframe (pandas.Dataframe): The dataframe
        """
        Chart.__init__(self, dataframe, kwargs)

    def _check_requirements(self):
        """
        Check the requirements for Timeline visualization

        Returns:
            (list) date_column: label for axis-x
            (list) label_name: label for axis-y
        """
        date_column = None
        label_name = None

        if self._is_date_column_exist(1):
            date_column = self._date_column
            if len(self._label_column) == 0:
                if len(self._uri_column) > 0:
                    label_name = self._uri_column[0]
                elif hasattr(self.dataframe, 'coordinate'):
                    label_name = [name for name in self.dataframe.columns if name.startswith(tuple(['coordinate']))][0]
                else:
                    self._is_label_column_exist()
                    label_name = None
            else:
                label_name = self._label_column[0]
        
        return date_column, label_name


    def plot(self):
        """
        Generate Timeline visualization
        """
        date_column, label_name = self._check_requirements()

        if date_column is not None and label_name is not None:
            if len(date_column) >= 2:
                if self.dataframe[date_column[0]][0] > self.dataframe[date_column[1]][0]:
                    date_column[1],date_column[0] = date_column[0],date_column[1]
                fig = px.timeline(self.dataframe, x_start=date_column[0], x_end=date_column[1], 
                                y=label_name, color=label_name)
                fig.update_yaxes(autorange="reversed")
                fig.show()
            else:
                add_column = self.dataframe.copy()
                add_column['Y+1'] = [add_column[date_column[0]][i] + datetime.timedelta(days=365) for i in range (len(add_column))]
                fig = px.timeline(add_column, x_start=date_column[0], x_end='Y+1', 
                                    y=label_name, color=label_name, hover_data={'Y+1':False})
                fig.update_yaxes(autorange="reversed")
                fig.show()
