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

    def promote_to_candidate(self):

        is_promote = self._is_var_exist(self._date_column, 1) and (self._is_var_exist(self._label_column, 1) or self._is_var_exist(self._uri_column, 1))

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
        Check the requirements for Timeline visualization

        Returns:
            (list) date_column: label for axis-x
            (list) label_name: label for axis-y
        """
        date_column = None
        label_name = None

        if self._is_var_exist(self._date_column, 1):
            date_column = self._date_column
            if len(self._label_column) == 0:
                if len(self._uri_column) > 0:
                    label_name = self._uri_column[0]
                else:
                    label_name = None
            else:
                label_name = self._label_column[0]
        
        return date_column, label_name


    def draw(self):
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
                data = self.dataframe.sort_values(by=[date_column[0]])
                range_time = data[date_column[0]][0] - data[date_column[0]][len(self.dataframe)-1]
                add_column = self.dataframe.copy()

                if range_time <= datetime.timedelta(days=30):
                    add_column['T+1'] = [add_column[date_column[0]][i] + datetime.timedelta(days=1) for i in range (len(add_column))]
                elif range_time > datetime.timedelta(days=30) and range_time <= datetime.timedelta(days=365):
                    add_column['T+1'] = [add_column[date_column[0]][i] + datetime.timedelta(days=15) for i in range (len(add_column))]
                else:
                    add_column['T+1'] = [add_column[date_column[0]][i] + datetime.timedelta(days=365) for i in range (len(add_column))]

                fig = px.timeline(add_column, x_start=date_column[0], x_end='T+1', 
                                    y=label_name, color=label_name, hover_data={'T+1':False})
                fig.update_yaxes(autorange="reversed")
                fig.show()
