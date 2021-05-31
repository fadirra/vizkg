from .chart import Chart
import matplotlib.pyplot as plt
from imageio import imread
import time

class ImageGrid(Chart):
    def __init__(self, dataframe, kwargs):
        """
        Constructs all the necessary attributes for the Image Grid visualization

        Parameters:
            dataframe (pandas.Dataframe): The dataframe
        """
        Chart.__init__(self, dataframe, kwargs)

    def _check_requirements(self):
        """
        Check the requirements for Image Grid visualization

        Returns:
            (list) label_name: list of image label
        """
        label_name = None
        if hasattr(self.dataframe, 'picture'):
            if len(self._label_column) > 0:
                label_name = self._label_column[0]
            else:
                pass
        else:
            print(f"Data has no attribute 'picture'")
            print(self._add_candidate_info)
        
        return label_name

    def plot(self):
        """
        Generate Image Grid visualization
        """
        label_name = self._check_requirements()
        pic = [i for i in self.dataframe.picture]
        num_pic = len(pic)
        columns = 4
        width = 20
        height = max(20, int(num_pic/columns) * 20)

        if label_name is not None:
            item_label = [i for i in self.dataframe[label_name]]
            plt.figure(figsize=(20,20))
            for i, url in enumerate(pic):
                plt.subplot(int(num_pic / columns + 1), columns, i + 1)
                try:
                    image = imread(url)
                    plt.title(item_label[i])
                    plt.imshow(image) #, plt.xticks([]), plt.yticks([])
                    plt.axis('off')
                except:
                    time.sleep(5)
                    image = imread(url)
                    plt.title(item_label[i])
                    plt.imshow(image) #, plt.xticks([]), plt.yticks([])
                    plt.axis('off')  
        else:     
            plt.figure(figsize=(20,20))
            for i, url in enumerate(pic):
                plt.subplot(int(num_pic / columns + 1), columns, i + 1)
                try:
                    image = imread(url)
                    plt.imshow(image) #, plt.xticks([]), plt.yticks([])
                    plt.axis('off')
                except:
                    time.sleep(5)
                    image = imread(url)
                    plt.imshow(image) #, plt.xticks([]), plt.yticks([])
                    plt.axis('off')