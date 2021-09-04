import unittest
import VizKG.visualize as vkg
from VizKG.charts import Chart
from VizKG.utils import generate_charts_dictionary

class VizKGTestCase(unittest.TestCase):

    def setUp(self):
        query = """
            #entity of barack obama
            SELECT ?item ?linkTo ?prop ?itemLabel ?propLabel  ?linkToLabel ?img ?dob ?height ?point
            WHERE
            {
            BIND(wd:Q76 AS ?item)
            VALUES ?prop { wdt:P26 wdt:P40 }
            VALUES ?USA { wd:Q30 }
            ?item ?prop ?linkTo .
            ?item rdfs:label ?itemLabel .
            ?linkTo rdfs:label ?linkToLabel .
            ?propFull wikibase:directClaim ?prop .
            ?propFull rdfs:label ?propLabel .
            ?item wdt:P18 ?img;
                    wdt:P569 ?dob;
                    wdt:P2048 ?height.
            ?USA wdt:P625 ?point.
            FILTER(LANG(?itemLabel)="en")
            FILTER(LANG(?linkToLabel)="en")
            FILTER(LANG(?propLabel)="en")
            }
        """
        service_url = "https://query.wikidata.org/sparql"
        self.obj = vkg(sparql_query=query, sparql_service_url=service_url)
        # self.chart = DataIdentification(self.obj.dataframe)
        self.chart = Chart(self.obj.dataframe, self.obj.kwargs)
        

    def test_column_dataframe(self):
        obj_column_names = list(self.obj.dataframe.columns)
        column_names = ["item", "linkTo", "prop", "itemLabel", "propLabel", "linkToLabel", "img", "dob", "height", "point"]
        self.assertListEqual(obj_column_names, obj_column_names)

    def test_string_column_data_type(self):
        str_column_names = ["item", "linkTo", "prop", "itemLabel", "propLabel", "linkToLabel", "img", "point"]
        for name in str_column_names:
            self.assertEqual(True, (self.obj.dataframe[name].dtypes == 'string'))

    def test_date_column(self):
        date_column = self.chart._date_column
        for name in date_column:
            self.assertEqual(True, (self.obj.dataframe[name].dtypes == 'datetime64[ns]')) 

    def test_numeric_column(self):
        numeric_column = self.chart._numerical_column
        for name in numeric_column:
            self.assertEqual(True, (self.obj.dataframe[name].dtypes == 'float64'))        

    def test_uri_column(self):
        uri_column = self.chart._uri_column
        exp_uri_column = ["item",  "prop", "linkTo"]
        self.assertListEqual(uri_column, exp_uri_column)

    def test_label_column(self):
        label_column = self.chart._label_column
        exp_label_column = ["itemLabel", "linkToLabel", "propLabel"]
        self.assertListEqual(label_column, exp_label_column)

    def test_img_column(self):
        img_column = self.chart._img_column
        exp_img_column = ["img"]
        self.assertListEqual(img_column, exp_img_column)

    def test_coord_column(self):
        coord_column = self.chart._coordinate_column
        exp_coord_column = ["point"]
        self.assertListEqual(coord_column, exp_coord_column)

if __name__ == '__main__':

    unittest.main()