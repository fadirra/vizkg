from .chart import Chart
import seaborn as sns
import plotly.express as px

class BarChart(Chart):
    def __init__(self, dataframe, kwargs):
        """
        Constructs all the necessary attributes for the BarChart object

        Parameters:
            dataframe (pandas.Dataframe): The dataframe
        """
        Chart.__init__(self, dataframe, kwargs)

    def promote_to_candidate(self):

        item_column, categorical_column = self._set_item_and_categorical()
        is_promote = self._is_var_exist(self._numerical_column, 1) and self._is_var_exist(item_column, 1)

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
        Check the requirements for generating BarChart visualization

        Returns:
            (string) int_label: numerical label 
            (list) item_column: item_column
            (list) categorical_column: categorical_column
        """
        int_label = None
        item_column = None
        categorical_column = None

        if self._is_var_exist(self._numerical_column, 1):
            int_label = self._numerical_column[0]
            if self._is_var_exist(self._label_column, 1):
                item_column, categorical_column = self._set_item_and_categorical()
        
        return int_label, item_column, categorical_column    

    def draw(self):
        """
        Generate BarChart visualization
        """
        numerical_label, item_column, categorical_column  = self._check_requirements()
        
        #check orientation
        orientation = None
        if len(categorical_column) > 0:
            orientation = self._check_orientation(item_column[0],categorical_column[0])
        else:
            orientation = self._check_orientation(item_column[0])

        if len(categorical_column) > 0:
            if orientation is not None:
                fig = px.bar(self.dataframe, x=numerical_label, y=item_column[0], color=categorical_column[0])
                fig.show()
            else:
                fig = px.bar(self.dataframe, x=item_column[0], y=numerical_label, color=categorical_column[0])
                fig.show()
        else:
            if orientation is not None:
                data = self.dataframe.sort_values(by=[numerical_label])
                fig = px.bar(data, x=numerical_label, y=item_column[0])
                fig.show()
            else:
                data = self.dataframe.sort_values(by=[numerical_label], ascending=False)
                fig = px.bar(data, x=item_column[0], y=numerical_label)
                fig.show()             


    def _check_orientation(self, axis_label, group_label=None, max_number=6):
        """
        Check the requirements for changing orientation, returns None if horizontal

        Returns:
            (string) orientation: label for axis
        """
        orientation = None
        num_box = 0
        num_axis = len(self.dataframe[axis_label].unique())
        num_box = 0

        if group_label is not None:
            num_group = len(self.dataframe[group_label].unique())
            num_box = num_axis + num_group
        else:
            num_box = num_axis

        if num_box > max_number:
            orientation = 'Horizontal'

        return orientation