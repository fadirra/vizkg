from .chart import Chart
import networkx as nx
import matplotlib.pyplot as plt

class Graph(Chart):
    def __init__(self, dataframe, kwargs):
        """
        Constructs all the necessary attributes for the Graph object

        Parameters:
            dataframe (pandas.Dataframe): The dataframe
            kwargs (dictionary): Arbitrary keyword arguments.
        """
        Chart.__init__(self, dataframe, kwargs)

    def promote_to_candidate(self):

        is_promote = self._is_var_exist(self._uri_column, 2)

        return is_promote

    def plot(self):
        """
        Generate visualization
        """
        if self.promote_to_candidate():
            self.draw()
        else:
            pass

    def _check_requirements(self):
        """
        Check the requirements for generating graph visualization

        Returns:
            (list) filter_column: list of filter label name
            (bool) is_label_column: if column not uri column
        """
        filter_column = None
        is_label_column = False

        if self._is_var_exist(self._uri_column, 2):
            if len(self._uri_column) > len(self._label_column):
                filter_column = self._uri_column
            else:
                filter_column = self._sort_label_column(self._label_column)
                is_label_column = True
        
        return filter_column, is_label_column      

    def _sort_label_column(self, label_column):
        #sort based on unique value (ASC)
        unique_dict = {name:len(self.dataframe[name].unique()) for name in (label_column)}
        sort_dict = {k: v for k, v in sorted(unique_dict.items(), key=lambda item: item[1])}

        sorted_label_column = list(sort_dict.keys())

        return sorted_label_column

    def draw(self):
        """
        Generate graph visualization
        """
        is_label_column = True
        filter_column = None
        keyword_column = None
        filter_column, is_label_column = self._check_requirements()

        #check mode keyword
        self.mode_keyword = set_mode(self.kwargs.get('mode_keyword'))
        if self.mode_keyword is not None:
            keyword_column = self._check_variable_mode_keyword()
            

        #plot
        if filter_column is not None:
            self.figsize = set_figsize(self.kwargs.get('figsize'))
            #check if param figsize exist
            if self.figsize is not None:
                plt.figure(figsize=self.figsize)
            else:
                plt.figure(figsize=(20,15))
            try:
                #check if edge label exist
                if len(filter_column) > 2:
                    #check if label exist (not uri)
                    if keyword_column is not None:
                        graph, positions, edge_labels = self.create_graph_nx('source_node', 'target_node', 'edge_label')
                    elif is_label_column:
                        graph, positions, edge_labels = self.create_graph_nx(filter_column[0], filter_column[2], filter_column[1])
                    else:
                        graph, positions, edge_labels = self.create_graph_nx(filter_column[0], filter_column[2], filter_column[1])
                    nx.draw_networkx(graph, positions, arrowsize=15, node_color='#f0f8ff')
                    nx.draw_networkx_edge_labels(graph, pos=positions, edge_labels=edge_labels, font_color='r')
                else:
                    graph, positions, edge_labels = self.create_graph_nx(filter_column[0], filter_column[1])
                    nx.draw_networkx(graph, positions, arrowsize=15, node_color='#f0f8ff')
            finally:
                plt.show()

    def create_graph_nx(self, source_column, target_column, edge_column=None):
        """
        Create graph networkx

        Paramaters:
            (list) node_list: list of node
            (list) filter_column: list of parent and child name column

        Returns:
            (networkx.DiGraph) Graph: Digraph graph
        """
        Graph = nx.DiGraph()
        
        #add edges and edge_label to graph
        edge_label = {}
        for key, node in self.dataframe.iterrows():
            Graph.add_edges_from([(node[source_column],node[target_column])])
            if edge_column is not None:
                edge_label[(node[source_column],node[target_column])] = node[edge_column]


        #Getting positions for each node.
        positions = nx.kamada_kawai_layout(Graph)

        return Graph, positions, edge_label

    def _check_variable_mode_keyword(self):
        """
        Check the required var for generating graph visualization

        Returns:
            (list) filter_column: list of filter label name        
        """
        filter_column = None
        required_var = ['source_node', 'target_node', 'edge_label']
        exist_var = [name for name in self.dataframe.columns if name.startswith(tuple(required_var)) and self.dataframe[name].dtypes == 'string']
        miss_var = list(set(required_var)-set(exist_var))

        if len(miss_var) > 0:
            raise Exception(f"Missing required variable: {miss_var}")
        else:
            filter_column = required_var

        return filter_column

def set_mode(mode_input):
    """
    Setter of mode of mapping based on mode input

    Parameters:
        (bool) mode_input: The mode input

    Returns:
        (bool) mode: The result mode  
    """
    mode = None
    if mode_input is not None and isinstance(mode_input, bool) and mode_input == True:
        mode = mode_input
    else:
        mode = None
    
    return mode

def set_figsize(figsize_input):
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