from .chart import Chart
import matplotlib.pyplot as plt
from imageio import imread
import time
import warnings

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
        if self._is_img_uri_column_exist(1):
            if len(self._label_column) > 0:
                label_name = self._label_column[0]
            else:
                pass
        else:
            label_name = None
        
        return label_name

    def plot(self):
        """
        Generate Image Grid visualization
        """
        if self._is_img_uri_column_exist(1):
            self.draw_imagegrid()
        else:
            pass

    def draw_imagegrid(self):

        label_name = self._check_requirements()
        columns = 4
        width = 20

        data_to_pic = self.truncate_data()

        pic = [i for i in data_to_pic.picture]
        num_pic = len(pic)
        height = max(20, int(num_pic/columns) * 20)

        if label_name is not None:
            item_label = [i for i in data_to_pic[label_name]]
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

    def truncate_data(self):

        data = self.dataframe
        if len(self.dataframe) > 200 :
            data = data.dataframe[:100]
            print(f"Time limit exceed. Showing only top of 200 pictures")
        else:
            pass

        return data
        
