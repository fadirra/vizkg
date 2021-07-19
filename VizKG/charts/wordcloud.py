from .chart import Chart
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import STOPWORDS, WordCloud as wrdcld

class WordCloud(Chart):
    def __init__(self, dataframe, kwargs):
        """
        Constructs all the necessary attributes for the WordCloud object

        Parameters:
            dataframe (pandas.Dataframe): The dataframe
        """
        Chart.__init__(self, dataframe, kwargs)

    def promote_to_candidate(self):

        is_promote = self._is_var_exist(self._label_column, 1)

        return is_promote

    def plot(self):
        """
        Generate visualization
        """
        if self.promote_to_candidate():
            self.draw()
        else:
            pass

    def _word_result(self):
        """
        Compile dataframe to one variable

        Parameters:
            (pandas.Dataframe) dataframe: The dataframe

        Returns:
            (string) words: The word result
        """
        #Merge into one column
        new_data = self.dataframe[self._label_column]
        new_data_flat = list(pd.Series(new_data.values.ravel('F')))

        #Merge into one variable
        words = " ".join([str(element) for element in new_data_flat])

        return words

    def draw(self):
        """
        Display WordCloud visualizations

        Parameters:
            (string) words: the visualized words
        """
        if self._is_var_exist(self._label_column, 1):
            #initiate words
            words = self._word_result()
            #initiate wordcloud object
            stopwords = set(STOPWORDS) 
            wordcloud = wrdcld(
                            width = 800, height = 800, 
                            background_color ='white', 
                            stopwords = stopwords, 
                            min_font_size = 10
                            ).generate(words) 
            
            # plot the WordCloud image
            self.figsize = self.__set_figsize(self.kwargs.get('figsize'))
            #check if param figsize exist
            if self.figsize is not None:
                plt.figure(figsize = self.figsize, facecolor = None) 
                plt.imshow(wordcloud) 
                plt.axis("off") 
                plt.tight_layout(pad = 0)
            else:                 
                plt.figure(figsize = (8, 8), facecolor = None) 
                plt.imshow(wordcloud) 
                plt.axis("off") 
                plt.tight_layout(pad = 0)

    @staticmethod
    def __set_figsize(figsize_input):
        """
        Setter of figsize based on figsize input for matplotlib chart

        Parameters:
            (tuple) figsize_input: The figsize input

        Returns:
            (tuple) figsize: The result figsize  
        """
        figsize = None
        is_numeric_value = None

        try:
            if figsize_input is not None and len(figsize_input) == 2:
                is_numeric_value = all(isinstance(v, int) or isinstance(v, float) for v in figsize_input)
            else:
                is_numeric_value = False
        except:
            is_numeric_value = False
            
        if is_numeric_value:
            figsize = figsize_input
        else:
            figsize = None

        return figsize