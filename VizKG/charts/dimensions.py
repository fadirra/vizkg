from .chart import Chart
import plotly.graph_objects as go

class Dimensions(Chart):
    def __init__(self, dataframe, kwargs):
        """
        Constructs all the necessary attributes for the Dimensions object

        Parameters:
            dataframe (pandas.Dataframe): The dataframe
        """
        Chart.__init__(self, dataframe, kwargs)

    def promote_to_candidate(self):

        is_promote = self._is_var_exist(self._label_column, 2)

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
        Check the requirements for generating dimension visualization

        Returns:
            (list) dataframe_to_list: list of dataframe
        """
        dataframe_to_list = None
        if self._is_var_exist(self._label_column, 2):
            dataframe_to_list = []
            for column in self._label_column:
                dataframe_to_list += self.dataframe[column].tolist()
        
        return dataframe_to_list    

    def draw(self):
        """
        Generate Dimensions visualization
        """
        dataframe_to_list = self._check_requirements()

        if dataframe_to_list is not None:
            #plot
            figure = go.Figure(data=[go.Sankey(
                node = dict(
                    label = dataframe_to_list,
                ),
                link = dict(
                    source = self._index_data(dataframe_to_list), # indices correspond to labels, eg A1, A2, A1, B1, ...
                    target = self._index_data(dataframe_to_list, type_link='target'),
                    value = [1 for i in range(len(dataframe_to_list)-self.dataframe.shape[0])]
                ))])

            figure.show()

    def _index_data(self, dataframe_to_list, type_link='source'):
        """
        Return indices correspond to type_link labels

        Parameters:
            (string) type_link: Type of link {'source' or target}
                                DEFAULT: 'source'
        Returns:
            (list) indices: index list of Type of link                        
        """
        curr_key = 0
        indices = [0]
        curr_value = dataframe_to_list[0]
        first_row = [dataframe_to_list[0]] 
        data = dataframe_to_list[:-self.dataframe.shape[0]]

        if type_link == 'target':
          curr_value = dataframe_to_list[self.dataframe.shape[0]]
          first_row = [dataframe_to_list[self.dataframe.shape[0]]]
          data = dataframe_to_list[self.dataframe.shape[0]:]

        for key,value in enumerate(data):
          if value != curr_value :
            if value in first_row:
              curr_key = first_row.index(value)
              curr_value = value
              indices.append(curr_key)
              first_row.append(curr_value)
            else:
              indices.append(key)
              first_row.append(value)
              curr_value = value
              curr_key = key
          elif value == curr_value:
            if key != 0:
              indices.append(curr_key)
              first_row.append(curr_value)
              
        if type_link == 'target':
          indices = [i+self.dataframe.shape[0] for i in indices]

        return indices