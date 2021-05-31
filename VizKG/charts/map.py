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
    
    def _check_requirements(self):
        """
        Check the requirements for generating tree visualization

        Returns:
            (list) popup_data: list of label name
        """
        popup_data = None
        if hasattr(self.dataframe, 'coordinate'):
            new_data = self._add_point()
            if len(self._label_column) == 0:
                popup_data = new_data.coordinate_point
            else:
                popup_data = new_data[self._label_column[0]]
        else:
            print(f"Data has no attribute 'coordinate'")
            print(self._add_candidate_info)
        
        return popup_data

    def _add_point(self):
        """
        Add coordinate column for coordinate folium map

        Returns:
            (pandas.Dataframe): Dataframe with new coordinate column
        """
        data = self.dataframe.copy()    
        #Get coordinate data (latitude and longitude)
        data['coordinate_point'] = data['coordinate']
        dataframe_new = data.apply(lambda S:S.str.strip('Point()'))
        new = dataframe_new[dataframe_new.columns[-1]].str.split(" ", n = 1, expand = True)
        new = new.astype('float64')
        data['coordinate'] = new.apply(lambda x: list([x[1], x[0]]),axis=1)

        return data

    def plot(self):
        """
        Generate map visualization
        """
        popup_data = self._check_requirements()

        if popup_data is not None:
            new_data = self._add_point()
            #Initiate map folium object
            maps = folium.Map()

            #Marked the map folium object
            for i in range (len(new_data)):
                folium.Marker(
                    location=new_data.coordinate[i],
                    popup=popup_data[i]
                ).add_to(maps)

            display(maps)                