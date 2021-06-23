import sys
import random
from .utils import set_chart, set_dataframe, generate_charts_dictionary
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
      chartdict = generate_charts_dictionary()
      chart_list = chartdict.keys()
      chart = Chart(self.dataframe, self.kwargs)
      candidate_visualization = list(chart.candidate_form())
      figure = None
      if len(self.dataframe) != 0:
        if self.chart not in chart_list:
          print(f"According to VizKG analysis, the following visualizations can be displayed: {candidate_visualization}")
          list_of_random_items = random.sample(candidate_visualization, 2)
          print(f"We show below two of them {tuple(list_of_random_items)} as illustrations: ")
          for idx,name in enumerate(list_of_random_items):
            figure = chartdict[name.lower()](self.dataframe, self.kwargs)
            figure.plot()         
        else:
          try:
            if self.chart in chartdict:
              figure = chartdict[self.chart](self.dataframe, self.kwargs)
          finally:
            figure.plot()
      else:
        print("No matching records found")

sys.modules[__name__] = VizKG