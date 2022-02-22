import re
import pandas as pd
import importlib, inspect
from pandas import json_normalize
from SPARQLWrapper import SPARQLWrapper
from difflib import SequenceMatcher
import ssl

from .chartdict import chartdict as chart_dictionary

def set_chart(chart_input):
    """
    Setter of chart based on chart input

    :param (str) chart_input: The chart input

    :return: (str) chart: The available chart   
    """
    chart = chart_dictionary 
    charts = chart.keys()

    if chart_input is not None:
        lowercase_input = chart_input.lower()
        highest_prob = 0

        if lowercase_input in charts:
            chart = lowercase_input
        else:    
            for name in charts:
                prob_now = SequenceMatcher(None, lowercase_input, name).ratio()
                if prob_now > highest_prob and prob_now >= 0.5:
                    highest_prob = prob_now
                    chart = name
    else:
        chart = None

    return chart

def set_dataframe(sparql_query, sparql_endpoint, user, passwd):
    """
    Query the endpoint with the given query string and format the result table

    Parameters:
        (string) sparql_query: The sparql query.
        (string) sparql_endpoint: The sparql endpoint
        (string) user: The sparql endpoint basic authentication user
        (string) passwd: The sparql endpoint basic authentication password

    Returns:
        (pandas.Dataframe) result_table: The table of result    
    """

    sparql = SPARQLWrapper(sparql_endpoint)  

    sparql.setQuery(sparql_query)
    sparql.setReturnFormat('json')
    if user != None:
        ssl._create_default_https_context = ssl._create_unverified_context
        sparql.setCredentials(user, passwd)

    results = sparql.query().convert()
    table  = json_normalize(results["results"]["bindings"])

    data_table = table[[column_name for column_name in table.columns if column_name.endswith('.value')]]
    data_table.columns = data_table.columns.str.replace('.value$', '', regex=True)
    result_table = __convert_dtypes(data_table)
    
    return result_table

def __convert_dtypes(dataframe):
    """
    Convert data type each column of dataframe

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