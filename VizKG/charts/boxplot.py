from .chart import Chart
import plotly.express as px

class BoxPlot(Chart):
    def __init__(self, dataframe, kwargs):
        """
        Constructs all the necessary attributes for the BoxPlot object

        Parameters:
            dataframe (pandas.Dataframe): The dataframe
        """
        Chart.__init__(self, dataframe, kwargs)

    def _check_requirements(self):
        """
        Check the requirements for generating BoxPlot visualization

        Returns:
            (string) numerical_label: label of numerical column
            (list) label_column: label column
        """
        numerical_label = None
        label_column = None

        if self._is_numerical_column_exist(1):
            numerical_label = self._numerical_column[0]
            if self._is_label_column_exist(1):
                label_column=self._label_column
                
        return numerical_label, label_column      

    def plot(self):
        """
        Generate BoxPlot visualization
        """
        numerical_label, label_column  = self._check_requirements()

        if numerical_label is not None and label_column is not None:
            axis_label,group_label,make_axis_label = None,None, None
            if len(label_column) >= 3:
                axis_label,group_label,make_axis_label = self._check_labels()
            else:
                axis_label,group_label = self._check_labels()
                
            orientation = self._check_orientation(axis_label,group_label)

            if make_axis_label is not None:
                axis_label = make_axis_label
            else:
                pass

            if group_label is not None:
                if orientation is not None:
                    fig = px.box(self.dataframe, x=numerical_label, y=axis_label, color=group_label)
                    fig.show()
                else:
                    fig = px.box(self.dataframe, x=axis_label, y=numerical_label, color=group_label)
                    fig.show()
            else:
                if orientation is not None:
                    fig = px.box(self.dataframe, x=numerical_label, y=axis_label)
                    fig.show()
                else:
                    fig = px.box(self.dataframe, x=axis_label, y=numerical_label)
                    fig.show()                     