import sys
import random
from .utils import set_chart, set_dataframe, info_chart_not_selected, chartdict, info_candidate
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
      **figsize (float, float): Width, height in inches of plot
  """

  def __init__(self, sparql_query, sparql_service_url, chart=None, **kwargs):
      """
      Constructs all the necessary attributes for the vizKG object

      Parameters:
          sparql_query (string): The SPARQL query to retrieve.
          sparql_service_url (string): The SPARQL endpoint URL.
          chart (string): Type of visualization
      """

      self.sparql_query = sparql_query
      self.sparql_service_url = sparql_service_url
      self.chart = set_chart(chart)
      self.kwargs = kwargs

      self.__data = set_dataframe(sparql_query, sparql_service_url)
      self.__candidate_visualization = self.__find_candidate()
      self.candidate_visualization = self.__candidate_visualization
      self.dataframe = self.__data

  def plot(self):
      """
      Plot visualization with suitable corresponding chart

      """
      chart_list = chartdict.keys()
      figure = None
      if len(self.__data) != 0:
        if self.chart not in chart_list:
          if len(self.__candidate_visualization) > 1:
            info_chart_not_selected(self.__candidate_visualization)
            self.__plot_randomize(self.__candidate_visualization)
          else:
            figure = chartdict["table"](self.__data, self.kwargs)
            figure.plot()      
        else:
          if self.chart in self.__candidate_visualization:
            figure = chartdict[self.chart](self.__data, self.kwargs)
            figure.plot()
          else:
            info_candidate(self.__candidate_visualization)
      else:
        print("No matching records found")

  def __find_candidate(self):
      chart_list = list(chartdict.keys())
      candidate = []
      for idx,name in enumerate(chart_list):
        check = chartdict[name.lower()](self.__data, self.kwargs)
        is_promoted = check.promote_to_candidate()
        if is_promoted:
          candidate.append(name)
      return candidate

  def __find_candidate_form(self):

      chart_list = chartdict.keys()
      chart = Chart(self.__data, self.kwargs)
      candidate_visualization = list(chart.candidate_form())

      return candidate_visualization

  def __plot_randomize(self, candidate_visualization):

      list_of_random_items = random.sample(candidate_visualization, 2)
      print(f"We show below two of them {tuple(list_of_random_items)} as illustrations: ")
      for idx,name in enumerate(list_of_random_items):
        figure = chartdict[name.lower()](self.__data, self.kwargs)
        figure.plot()

sys.modules[__name__] = VizKG