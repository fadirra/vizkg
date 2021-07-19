from .chart import Chart
import folium
from IPython.display import display

class Map(Chart):
    def __init__(self, dataframe, kwargs):
        """
        Constructs all the necessary attributes for the Map object

        Parameters:
            dataframe (pandas.Dataframe): The dataframe
        """
        Chart.__init__(self, dataframe, kwargs)

    def promote_to_candidate(self):

        is_promote = self._is_var_exist(self._coordinate_column, 1)

        return is_promote
    
    def _check_requirements(self):
        """
        Check the requirements for generating tree visualization

        Returns:
            (list) popup_data: list of label name
        """
        popup_data = None
        if self._is_var_exist(self._coordinate_column, 1):
            new_data = self._add_point()
            if len(self._label_column) == 0:
                popup_data = new_data.coordinate_point
            else:
                popup_data = new_data[self._label_column[0]]
        else:
            popup_data = None
        
        return popup_data


    def plot(self):
        """
        Generate Image Grid visualization
        """
        if self._is_var_exist(self._coordinate_column, 1):
            self.draw_map()
        else:
            pass


    def draw_map(self):
        """
        Generate map visualization
        """
        popup_data = self._check_requirements()

        if popup_data is not None:
            data_point = self._add_point()
            #Initiate map folium object
            new_data = self.truncate_data(data_point)
            maps = folium.Map()

            #Marked the map folium object
            for i in range (len(new_data)):
                folium.Marker(
                    location=new_data.coordinate[i],
                    popup=popup_data[i]
                ).add_to(maps)

            display(maps)                

    def _add_point(self):
        """
        Add coordinate column for coordinate folium map

        Returns:
            (pandas.Dataframe): Dataframe with new coordinate column
        """
        copy_data = self.dataframe.copy()

        coor_var = self._coordinate_column[0]    
        #Get coordinate data (latitude and longitude)
        char_delete = 'Point()OINT'
        copy_data['coordinate_point'] = copy_data[coor_var]
        dataframe_new = copy_data.coordinate_point.astype(str).apply(lambda S:S.strip(char_delete))
        dataframe_new = dataframe_new.to_frame()
        new = dataframe_new[dataframe_new.columns[-1]].str.split(" ", n = 1, expand = True)
        new = new.astype('float64')
        copy_data['coordinate'] = new.apply(lambda x: list([x[1], x[0]]),axis=1)

        return copy_data

    def truncate_data(self, data):

        if len(data) > 2000 :
            truncate_data = data.head(2000)
            data = truncate_data
            print(f"Time limit exceed... Showing only 2000 coordinates")
        else:
            pass

        return data