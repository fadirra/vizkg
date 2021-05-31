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
        self._words = self._word_result()

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

    def plot(self):
        """
        Display WordCloud visualizations

        Parameters:
            (string) words: the visualized words
        """
        if self._is_label_column_exist(1):
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
            plt.figure(figsize = (8, 8), facecolor = None) 
            plt.imshow(wordcloud) 
            plt.axis("off") 
            plt.tight_layout(pad = 0)
        else:
            print(self._add_candidate_info)  