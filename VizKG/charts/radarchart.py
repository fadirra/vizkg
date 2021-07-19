from .chart import Chart
import plotly.graph_objects as go


class RadarChart(Chart):
    def __init__(self, dataframe, kwargs):
        """
        Constructs all the necessary attributes for the Radar Chart object

        Parameters:
            dataframe (pandas.Dataframe): The dataframe
        """
        Chart.__init__(self, dataframe, kwargs)

    def promote_to_candidate(self):

        is_promote = self._is_var_exist(self._label_column, 1) and self._is_var_exist(self._numerical_column, 3)

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
        Check the requirements for generating Radar Chart visualization

        Returns:
            (string) label_name: label name
            (list) numerical_column: list of numerical column
        """
        label_name = None
        numerical_column = None
        
        if self._is_var_exist(self._numerical_column, 3):
            numerical_column = self._numerical_column
            if self._is_var_exist(self._label_column, 1):
                label_name = self._label_column[0]
        
        return label_name, numerical_column    

    def draw(self):
        """
        Generate Radar Chart visualization
        """
        label_name, numerical_column  = self._check_requirements()

        if label_name is not None and numerical_column is not None:
            categories = numerical_column
            data_label = self.dataframe[label_name]
            data_numeric = self.dataframe[numerical_column]

            list_number = []

            fig = go.Figure()

            for i in range (len(data_numeric)):
                idx_data_numeric = (list(data_numeric.iloc[i]))
                fig.add_trace(go.Scatterpolar(
                    r=idx_data_numeric,
                    theta=categories,
                    fill='toself',
                    name=data_label[i]
                ))
                list_number.append(idx_data_numeric)

            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                    visible=True,
                    range=[0, max(list_number)]
                    )),
                showlegend=False
            )

            fig.show()



