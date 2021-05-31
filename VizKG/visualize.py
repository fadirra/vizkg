import sys

from .utils import set_chart, set_dataframe
from .charts import Chart
from .chartdict import chartdict

class vizKG:
  """
  Instantiate vizKG object.
  
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
                                'StackedAreaChart', 'ScatterChart', 'BubbleChart'}.
      **mode_keyword (boolean): Mode of mapping variable                           
      **figsize (float, float): Width, height in inches of plot
                
  """

  def __init__(self, sparql_query, sparql_service_url, chart=None, **kwargs):
      """
      Constructs all the necessary attributes for the vizKG object

      Parameters:
          sparql_query (string): The SPARQL query to retrieve.
          sparql_service_url (string): The SPARQL endpoint URL.
          chart (string): Type of visualization
          **mode_keyword (boolean): Mode of mapping variable 
          **figsize (float, float): Width, height in inches of plot

      """

      self.sparql_query = sparql_query
      self.sparql_service_url = sparql_service_url
      self.chart = set_chart(chart)
      self.kwargs = kwargs

      self.dataframe = set_dataframe(sparql_query, sparql_service_url)

  def plot(self):
      """
      Plot visualization with suitable corresponding chart

      """
      chart_list = chartdict.keys()
      chart = Chart(self.dataframe, self.kwargs)
      candidate_visualization = chart.candidate_form()
      figure = None
      if len(self.dataframe) != 0:
        if self.chart not in chart_list:
          print(f"No matching chart found instead use one of the available chart: {candidate_visualization}")
        else:
          try:
            if self.chart in chartdict:
              figure = chartdict[self.chart](self.dataframe, self.kwargs)
          finally:
            figure.plot()
      else:
        print("No matching records found")

sys.modules[__name__] = vizKG