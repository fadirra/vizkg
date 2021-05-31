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

    def _check_requirements(self):
        """
        Check the requirements for generating DensityPlot visualization

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
        Generate DensityPlot visualization
        """
        numerical_label, label_name  = self._check_requirements()

        if numerical_label is not None:
            if label_name is not None:
                sns.displot(data=self.dataframe, x=numerical_label, hue=label_name, kind="kde")
                pass
            else:
                sns.displot(data=self.dataframe, x=numerical_label, kind="kde")
                pass               


