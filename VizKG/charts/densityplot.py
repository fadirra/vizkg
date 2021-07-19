from .chart import Chart
import seaborn as sns

class DensityPlot(Chart):
    def __init__(self, dataframe, kwargs):
        """
        Constructs all the necessary attributes for the DensityPlot object

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
        Check the requirements for generating DensityPlot visualization

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

    def filter_data(self):

        var_name = list(self.dataframe.columns)
        data = self.dataframe.copy()

        if len(self._date_column) > 0:
            filter_date_column = list(set(var_name) - set(self._date_column))
            data = data.filter(items=filter_date_column)
        else:
            pass

        return data

    def draw(self):

        numerical_label, label_name  = self._check_requirements()

        if label_name is not None:
            sns.displot(data=self.dataframe, x=numerical_label, hue=label_name, kind="kde")
            pass
        else:
            sns.displot(data=self.dataframe, x=numerical_label, kind="kde")
            pass
        




