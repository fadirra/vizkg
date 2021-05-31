from .chart import Chart
import plotly.express as px

class Histogram(Chart):
    def __init__(self, dataframe, kwargs):
        """
        Constructs all the necessary attributes for the Histogram object

        Parameters:
            dataframe (pandas.Dataframe): The dataframe
        """
        Chart.__init__(self, dataframe, kwargs)

    def _check_requirements(self):
        """
        Check the requirements for generating Histogram visualization

        Returns:
            (string) numerical_label: label of numerical column
            (string) label_name: label name
        """
        numerical_label = None
        label_name = None

        if self._is_numerical_column_exist(1):
            numerical_label = self._numerical_column[0]
            if len(self._label_column) > 0:
                unique_list = [len(self.dataframe[name].unique()) for name in self._label_column]
                min_unique = min(unique_list)
                idx_min_unique = unique_list.index(min(unique_list))
                if min_unique <= 5 and min_unique < len(self.dataframe):
                    label_name=self._label_column[idx_min_unique]

        return numerical_label, label_name      

    def plot(self):
        """
        Generate Histogram visualization
        """
        numerical_label, label_name  = self._check_requirements()

        if numerical_label is not None:
            if label_name is not None:
                #plot
                fig = px.histogram(self.dataframe, x=numerical_label, color=label_name, marginal="rug", hover_data=self.dataframe.columns)
                fig.show()
            else:
                #plot
                fig = px.histogram(self.dataframe, x=numerical_label, marginal="rug", hover_data=self.dataframe.columns)
                fig.show()  

