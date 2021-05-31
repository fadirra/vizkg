from .chart import Chart
import plotly.express as px

class DonutChart(Chart):
    def __init__(self, dataframe, kwargs):
        """
        Constructs all the necessary attributes for the DonutChart object

        Parameters:
            dataframe (pandas.Dataframe): The dataframe
        """
        Chart.__init__(self, dataframe, kwargs)

    def _check_requirements(self):
        """
        Check the requirements for generating DonutChart visualization

        Returns:
            (string) label_name: label name
            (list) numerical_column: list of numerical column
        """
        label_name = None
        numerical_column = None
        
        if self._is_numerical_column_exist(1):
            numerical_column = self._numerical_column
            if self._is_label_column_exist(1):
                if len(self._label_column) > 1:
                    axis_label, group_label = self._check_labels()
                    if group_label is not None:
                        label_name = group_label
                    else:
                        label_name = axis_label
                else:    
                    label_name = self._label_column[0]

        
        return label_name, numerical_column    

    def plot(self):
        """
        Generate DonutChart visualization
        """
        label_name, numerical_column  = self._check_requirements()

        if label_name is not None and numerical_column is not None:
            values_label,hover_label = self._check_numerical_columns()
            if hover_label is not None:
                #plot
                fig = px.pie(self.dataframe, values=values_label, names=label_name, hole=0.3,
                                hover_data=[hover_label])
                fig.show()
            else:
                fig = px.pie(self.dataframe, values=values_label, names=label_name, hole=0.3)
                fig.show()                



