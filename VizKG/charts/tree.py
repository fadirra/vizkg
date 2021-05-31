from .chart import Chart
from anytree import Node, RenderTree

class Tree(Chart):
    def __init__(self, dataframe, kwargs):
        """
        Constructs all the necessary attributes for the Tree object

        Parameters:
            dataframe (pandas.Dataframe): The dataframe
        """
        Chart.__init__(self, dataframe, kwargs)

    def _check_requirements(self):
        """
        Check the requirements for generating tree visualization

        Returns:
            (list) filter_column: list of filter label name
        """
        filter_column = None
        if self._is_uri_column_exist(2):
            filter_column = self._label_column
            if len(self._label_column) < 2:
                filter_column = self._uri_column
        
        return filter_column
    
    def plot(self):
        """
        Generate tree visualization
        """
        #filter_column
        filter_column = self._check_requirements()

        if filter_column is not None:
            #Extract selected column as new dataframe
            data = self.dataframe[filter_column].copy()

            nodes = {}
            for parent, child in zip(data.iloc[:, 0],data.iloc[:, 1]):
                self.add_nodes(nodes, parent, child)

            roots = list(data[~data.iloc[:, 0].isin(data.iloc[:, 1])][data.columns[0]].unique())
            for root in roots:         # you can skip this for roots[0], if there is no forest and just 1 tree
                for pre, _, node in RenderTree(nodes[root]):
                    print("%s%s" % (pre, node.name))

    @staticmethod    
    def add_nodes(nodes, parent, child):
        """
        Set parent nodes with corresponding child nodes
        """
        if parent not in nodes:
            nodes[parent] = Node(parent)  
        if child not in nodes:
            nodes[child] = Node(child)
            nodes[child].parent = nodes[parent]