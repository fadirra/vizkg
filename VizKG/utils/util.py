import re
import pandas as pd
import importlib, inspect
from pandas import json_normalize
from SPARQLWrapper import SPARQLWrapper
from difflib import SequenceMatcher

def generate_charts_dictionary():
    """
        Get dictionary of chart type

        Returns:
            (dict) chartdict: dictionary of visualization chart type
    """
    keys = []
    values = []
    for name, mod in inspect.getmembers(importlib.import_module("VizKG.charts"), inspect.ismodule):
            keys.append(name)

    for name, cls in inspect.getmembers(importlib.import_module("VizKG.charts"), inspect.isclass):
            values.append(cls)

    chartdict = {keys[i]: values[i] for i in range(len(values))}
    chartdict.pop("chart")

    return chartdict    

def set_chart(chart_input):
    """
    Setter of chart based on chart input

    Parameters:
        (string) chart_input: The chart input

    Returns:
        (list) chart: The available chart   
    """
    chart = generate_charts_dictionary()
    charts = chart.keys()

    if chart_input is not None:
        lowercase_input = chart_input.lower()
        
        highest_prob = 0
        for name in charts:
            prob_now = SequenceMatcher(None, lowercase_input, name).ratio()
            if prob_now > highest_prob and prob_now >= 0.5:
                highest_prob = prob_now
                chart = name

        if lowercase_input in charts:
            chart = lowercase_input

        if chart is None:
            raise Exception("No available chart")

    else:
        chart = None

    return chart


def set_dataframe(sparql_query, sparql_endpoint):
    """
    Query the endpoint with the given query string and format the result table

    Parameters:
        (string) sparql_query: The sparql query.
        (string) sparql_endpoint: The sparql endpoint

    Returns:
        (pandas.Dataframe) result_table: The table of result    
    """

    sparql = SPARQLWrapper(sparql_endpoint)  

    sparql.setQuery(sparql_query)
    sparql.setReturnFormat('json')

    results = sparql.query().convert()
    table  = json_normalize(results["results"]["bindings"])

    data_table = table[[column_name for column_name in table.columns if column_name.endswith('.value')]]
    data_table.columns = data_table.columns.str.replace('.value$', '', regex=True)
    rename_column_table = __rename_column_table(data_table)
    change_dtype_table = __change_dtypes(rename_column_table)
    result_table = change_dtype_table
    
    return result_table


def __rename_column_table(dataframe):
    """
    Rename column of dataframe based on regex validity check

    Parameters:
        (pandas.Dataframe) dataframe: The table

    Returns:
        (pandas.Dataframe) dataframe: The result table             
    """

    #Regex pattern
    pattern_url = r"^(?:http(s)?:\/\/)[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$(?<!.[jpg|gif|png|JPG|PNG])" 
    pattern_img = r"^http(s)?://(?:[a-z0-9\-]+\.)+[a-z]{2,6}(?:/[^/#?]+)+\.(?:jpg|jpeg|gif|png|JPG|JPEG|Jpeg)$"        
    pattern_coordinate = r"^Point"

    for i in range (len(dataframe.columns)):
        column = dataframe[dataframe.columns[i]]
        is_picture_column = __check_data_per_column(column, pattern_img)
        is_coordinate_column = __check_data_per_column(column, pattern_coordinate)
        if is_picture_column:
            dataframe =  dataframe.rename(columns={dataframe.columns[i]: "picture"}, errors="raise")
        elif is_coordinate_column:
            dataframe =  dataframe.rename(columns={dataframe.columns[i]: "coordinate"}, errors="raise")
        else:
            pass

    return dataframe

def __check_data_per_column(column, pattern):
    """
    Check entire data per column of dataframe if matched with regex pattern

    Parameters:
        (pandas.Dataframe) column: column name of dataframe
        (string) pattern: regex pattern

    Returns:
        (boolen) boolean_check: The result table             
    """
    boolean_check = False
    for datapoint in range(len(column)):
        data = column.iloc[datapoint]
        try:
            if re.match(pattern, data):
                boolean_check = True
        except TypeError:
            pass
            
    return boolean_check

def __change_dtypes(dataframe):
    """
    Change data type column of dataframe

    Parameters:
        (pandas.Dataframe) dataframe: The table

    Returns:
        (pandas.Dataframe) table: The result table             
    """

    for column in dataframe:
        try:
            dataframe[column] = dataframe[column].astype('string')
        except ValueError:
            pass

    for column in dataframe:
        try:
            dataframe[column] = dataframe[column].astype('datetime64')
        except ValueError:
            pass

    for column in dataframe:
        try:
            dataframe[column] = dataframe[column].astype('float64')
        except (ValueError, TypeError):
            pass

    return dataframe