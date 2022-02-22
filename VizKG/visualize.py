import sys
import random
from .utils import set_chart, set_dataframe, chartdict
from .charts import Chart
class VizKG:
  """
  Instantiate VizKG object.
  
  Attributes:
      sparql_query (string): The SPARQL query to retrieve.
      sparql_service_url (string): The SPARQL endpoint URL.
      chart (string): Type of visualization
        Options = {'Table', 'ImageGrid', 'Timeline' 'Graph' 
                  'Map', 'Tree','WordCloud', 'Dimensions',
                  'LineChart', 'BarChart', 'Histogram',
                  'DensityPlot', 'TreeMap' ,'SunBurstChart', 
                  'HeatMap' ,'PieChart', 'DonutChart',
                  'BoxPlot' ,'ViolinPlot', 'AreaChart',
                  'StackedAreaChart', 'ScatterChart', 
                  'BubbleChart', 'RadarChart'}.
      **figsize (float, float): Width, height in inches of matplotlib plot 
  """

  def __init__(self, sparql_query, sparql_service_url, user=None, passwd=None, chart=None, **kwargs):
      """
      Constructs all the necessary attributes for the vizKG object

      Parameters:
          sparql_query (string): The SPARQL query to retrieve.
          sparql_service_url (string): The SPARQL endpoint URL.
          user (string): The sparql endpoint basic authentication user
          passwd (string): The sparql endpoint basic authentication password
          chart (string): Type of visualization
      """

      self.sparql_query = sparql_query
      self.sparql_service_url = sparql_service_url
      self.user = user
      self.passwd = passwd
      self.chart = set_chart(chart)
      self.kwargs = kwargs

      self.__data = set_dataframe(sparql_query, sparql_service_url, user, passwd)
      self.__candidate_visualization = self.__find_candidate()
      self.dataframe = self.__data
      self.candidate_visualization = self.__candidate_visualization     

  def plot(self):
      """
      Plot visualization with suitable corresponding chart

      """
      chart_list = chartdict.keys()
      figure = None
      if len(self.__data) != 0:
        if self.chart not in chart_list:
          if len(self.__candidate_visualization) > 1:
            print(f"You haven’t selected the chart type for your query result visualization.")
            print(f"Based on your query result data, we suggest to choose one of the following chart type: {self.__candidate_visualization}\n")
            self.__plot_randomize(self.__candidate_visualization)
          else:
            figure = chartdict["table"](self.__data, self.kwargs)
            figure.plot()      
        else:
          if self.chart in self.__candidate_visualization:
            figure = chartdict[self.chart](self.__data, self.kwargs)
            figure.plot()
          else:
            print(f"Based on your query result data, we suggest to choose one of the following chart type: {self.__candidate_visualization}\n")
      else:
        print("No matching records found")

  def __find_candidate(self):
      """
      Find candidate of visualization

      Returns:
          (list) candidate: List of recommendation chart name      
      """
      chart_list = list(chartdict.keys())
      candidate = []
      for idx,name in enumerate(chart_list):
          check = chartdict[name.lower()](self.__data, self.kwargs)
          if check.promote_to_candidate():
            candidate.append(name)
      return candidate

  def __plot_randomize(self, candidate_visualization):
      """
      Plot two of recommendation chart chart

      Returns:
          (list) candidate: List of recommendation chart name      
      """
      list_of_random_items = random.sample(candidate_visualization, 2)
      print(f"We show below two of them {tuple(list_of_random_items)} as illustrations: ")
      for idx,name in enumerate(list_of_random_items):
        figure = chartdict[name.lower()](self.__data, self.kwargs)
        figure.plot()

sys.modules[__name__] = VizKG