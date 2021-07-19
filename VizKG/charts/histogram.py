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

    def promote_to_candidate(self):

        is_promote = self._is_var_exist(self._numerical_column, 1)

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
        Check the requirements for generating Histogram visualization

        Returns:
            (string) numerical_label: label of numerical column
            (string) label_name: label name
        """
        numerical_label = None
        label_name = None

        if self._is_var_exist(self._numerical_column, 1):
            numerical_label = self._numerical_column[0]
            self._item_var, self._categorical_column  = self._set_item_and_categorical()
            if len(self._categorical_column) > 0:
                label_name = self._categorical_column[0]

        return numerical_label, label_name      

    def draw(self):
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

