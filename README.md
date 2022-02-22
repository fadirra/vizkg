# VizKG
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/17caTzWK1-rPU44mYfn5v4YaEc7Y7eAZa?pli=1#scrollTo=gOM-o9o6twi4)
[![Python Versions](https://img.shields.io/pypi/pyversions/VizKG.svg)](https://pypi.org/project/VizKG)
[![PyPI Version](https://img.shields.io/pypi/v/VizKG.svg)](https://pypi.org/project/VizKG)
[![PyPI License](https://img.shields.io/pypi/l/VizKG.svg)](https://github.com/fadirra/vizkg/blob/main/LICENSE)

VizKG, a visualization library for SPARQL query results over KGs. VizKG links SPARQL query results and external visualization libraries by [mapping](https://bit.ly/VizKG-MappingRules) query variables to the visualization components needed, currently allowing for 24 types of visualizations. Not only that, VizKG also provides visualization recommendations for arbitrary SPARQL query result. 

### Update feature v.1.0.9
VizKG now features SPARQL endpoint access with basic authentication where users can use the feature at their own risk. The purpose of VizKG is for **educational only**.

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

### Visualization Recommendation 

VizKG returns the automated visualization when there is no chart type preference given.

```python
#Wikidata: Covid-19 Recoveries, Cases, and Death Growth
sparql_query = """
SELECT ?time ?Recoveries ?Cases ?Deaths WHERE {
  {
    SELECT ?time ?Recoveries WHERE {
      wd:Q84263196 p:P8010 ?countRes .
      FILTER NOT EXISTS { ?countRes pq:P276 ?loc }
      ?countRes ps:P8010 ?Recoveries ;
                   pq:P585 ?time .
    }
  } 
  {
    SELECT ?time ?Cases WHERE {
      wd:Q84263196 p:P1603 ?countRes .
      FILTER NOT EXISTS { ?countRes pq:P276 ?loc }
       ?countRes ps:P1603 ?Cases ;
                   pq:P585 ?time .
    }
  } 
  {
    SELECT ?time ?Deaths WHERE {
      wd:Q84263196 p:P1120 ?countRes .
      FILTER NOT EXISTS { ?countRes pq:P276 ?loc }
       ?countRes ps:P1120 ?Deaths ;
                   pq:P585 ?time .
    }
  }
}
"""
sparql_service_url = "https://query.wikidata.org/sparql"
chart = vkg(sparql_query=sparql_query, sparql_service_url=sparql_service_url)
chart.plot()
```
![WD:COVID-19 Growth](https://raw.githubusercontent.com/fadirra/vizkg/main/images/VizKG-Wikidata_%20Covid19%20Recoveries%2C%20Cases%2C%20and%20Death%20Growth.png)

## Use Case Examples

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
- Graph
- Tree
- Dimensions
- Timeline
- WordCloud
- Histogram
- Density Plot
- Box Plot
- Violin Plot
- Line Chart
- Bar Chart
- Area Chart
- Stacked Area Chart
- Bubble Chart
- Scatter Chart
- HeatMap
- Radar Chart
- Tree Map
- SunBurst Chart
- Pie Chart
- Donut Chart

## Related Work

| Tool                                                                    | Framework      | Data Source      | Input Type                          | Number of Chart Types   |
| :---                                                                    |     :---:      |     :---:        |     :---:                           |     :---:     |
|[Wikidata Query Service](https://query.wikidata.org/)                    | Web-based      | Wikidata only    |  SPARQL SELECT                      | 14    |
|[Dataviz](https://dataviz.toolforge.org/)                                | Web-based      | Wikidata only    |  SPARQL SELECT                      | 23    |
|[YASGUI](https://yasgui.triply.cc/)                                      | Web-based      | Generic          |  SPARQL SELECT and SPARQL CONSTRUCT | 11    |
|[LDVizWiz](http://semantics.eurecom.fr/datalift/rdfViz/apps/)            | Web-based      | Generic          |  SPARQL SELECT/ASK and RDF Data     | 27    |
|[Sparklis](http://www.irisa.fr/LIS/ferre/sparklis/)                      | Web-based      | Generic          |  Text                               | 4    |
|[Quedi](https://link.springer.com/chapter/10.1007%2F978-3-030-59833-4_5) | Web-based      | Generic          |  Text                               | 16    |
|[Voyager](https://vega.github.io/voyager/)                               | Web-based      | Generic          |  Tabular Data                       | 5    |
|[S-Paths](http://s-paths.lri.fr/)                                        | Web-based      | Generic          |  RDF Data                           | 10    |
|[Gastrodon](https://github.com/paulhoule/gastrodon)                      | Python Library | Generic          |  RDF Data                           | -    |
|[kglab](https://github.com/DerwenAI/kglab)                               | Python Library | Generic          |  RDF Data                           | 1    |
|[Autoviz](https://pypi.org/project/autoviz/)                             | Python Library | Generic          |  Tabular Data                       | 5    |
|[Visualizer](https://pypi.org/project/visualizer/)                       | Python Library | Generic          |  Tabular Data                       | 20    |

## Code Contributors

This project exists thanks to all the people who contribute.