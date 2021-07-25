# VizKG
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/17caTzWK1-rPU44mYfn5v4YaEc7Y7eAZa?pli=1#scrollTo=gOM-o9o6twi4)
[![Python Versions](https://img.shields.io/pypi/pyversions/VizKG.svg)](https://pypi.org/project/VizKG)
[![PyPI Version](https://img.shields.io/pypi/v/VizKG.svg)](https://pypi.org/project/VizKG)
[![PyPI License](https://img.shields.io/pypi/l/VizKG.svg)](https://github.com/fadirra/vizkg/blob/main/LICENSE)

Visualization library for SPARQL query results

## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install VizKG.

```bash
pip install VizKG
```

## Usage

```python
# Import the library
import VizKG.visualize as vkg
```

### Wikidata: COVID-19 Vaccine Origins
```python
sparql_query = """
SELECT DISTINCT ?vaccineLabel ?originCountry  {
  ?vaccine wdt:P1924 wd:Q84263196 .
  ?vaccine wdt:P178 ?developer.
  ?vaccine rdfs:label ?vaccineLabel .
  ?developer wdt:P17 ?origin . 
  ?origin rdfs:label ?originCountry .
  FILTER (LANG(?vaccineLabel) = 'en').
  FILTER (LANG(?originCountry) = 'en').
}LIMIT 25
"""
#to query another endpoint, change the URL for the service and the query
sparql_service_url = "https://query.wikidata.org/sparql"
chart = vkg(sparql_query=sparql_query, sparql_service_url=sparql_service_url, chart='sunburst')
chart.plot()
```
![WD:COVID-19 Vaccine origins](https://raw.githubusercontent.com/fadirra/vizkg/main/images/VizKG-Wikidata_COVID-19%20Vaccine's%20origin.png)


### DBpedia: Map of Temples in Indonesia
```python
sparql_query = """
SELECT * WHERE {
  ?item dbo:wikiPageWikiLink dbr:Candi_of_Indonesia;
        geo:geometry ?geo .
  ?item rdfs:label ?itemLabel.
  FILTER((LANG(?itemLabel)) = "en")
}
"""
#to query another endpoint, change the URL for the service and the query
sparql_service_url = "https://dbpedia.org/sparql/"
chart = vkg(sparql_query=sparql_query, sparql_service_url=sparql_service_url, chart='map')
chart.plot()
```
![DBpedia:Map of Temples in Indonesia](https://raw.githubusercontent.com/fadirra/vizkg/main/images/VizKG-DBpedia-Map%20of%20Temple%20in%20Indonesia.png)


### OU_UK: Number of Employees by Job Title
```python
sparql_query = """
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX schema: <http://schema.org/jobTitle>

SELECT DISTINCT ?jobTitle (COUNT(?jobTitle) as ?count) WHERE {?s a foaf:Person .
  ?s <http://schema.org/jobTitle> ?jobTitle .
  FILTER (lang(?jobTitle) != 'en')
}
GROUP BY ?jobTitle
HAVING (?count > 10)
"""
#to query another endpoint, change the URL for the service and the query
sparql_service_url = "https://data.open.ac.uk/sparql"
chart = vkg(sparql_query=sparql_query, sparql_service_url=sparql_service_url, chart='TreeMap')
chart.plot()
```
![OU_UK:Number of Employees by Job Title](https://raw.githubusercontent.com/fadirra/vizkg/main/images/VizKG-OU_OU%20Number%20of%20employees%20based%20on%20job%20title.png)


### Budaya KB: Number of Temples by Indonesian Regencies
```python
sparql_query = """
prefix bkb: <https://budayakb.cs.ui.ac.id/ns#>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>


SELECT ?provLabel (COUNT(?temple) AS ?numTemple) WHERE {
  ?temple a bkb:Candi .
  ?temple bkb:locationInProvince ?prov .
  ?prov rdfs:label ?provLabel.
  FILTER (lang(?provLabel) = 'id')

} GROUP BY ?provLabel
ORDER BY DESC(?numTemple)
"""
#to query another endpoint, change the URL for the service and the query
sparql_service_url = "https://budayakb.cs.ui.ac.id/budaya/sparql"
chart = vkg(sparql_query=sparql_query, sparql_service_url=sparql_service_url, chart='bubble')
chart.plot()
```
![BudayaKB:Number of Temples by Indonesian Regencies](https://raw.githubusercontent.com/fadirra/vizkg/main/images/VizKG-Budaya%20KB_Number%20of%20temple%20in%20Indonesia.png)

## Supported Visualizations
- Table
- ImageGrid
- Map
- Tree
- Timeline
- Dimensions
- Graph
- WordCloud
- Tree Map
- SunBurst Chart
- Line Chart
- Bar Chart
- Area Chart
- StackedArea Chart
- Histogram
- Density Plot
- Box Plot
- Violin Plot
- Bubble Chart
- Scatter Chart
- HeatMap
- Radar Chart

