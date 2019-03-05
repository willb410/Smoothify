from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask, jsonify,render_template
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from mysql_conn import password
import numpy as np
import pymysql
pymysql.install_as_MySQLdb()
import requests
import pandas as pd

import sys
sys.path.append("static/js")
sys.path.append("static/css")
sys.path.append("static/Images")

connection_string = (f"root:{password}@localhost/real_estate")
engine = create_engine(f"mysql://{connection_string}", pool_recycle=3600) #, pool_pre_ping=True)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the table
mean_sales_count = Base.classes.mean_sales_count
median_sales_count = Base.classes.median_sales_count
median_price_sqft = Base.classes.median_price_sqft
median_price_zip = Base.classes.median_price_zip
print(Base.classes.keys())

# Create our connection object
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/")
def apps():
    
    return render_template("index.html")

@app.route("/names")
def names():
    """Return list of available cities"""
    available_cities = ['Austin, TX', 
                'Dallas-Forth Worth, TX', 
                'Denver, CO', 
                'Detroit, MI', 
                'New York City, NY', 
                'Orlando, FL', 
                'Raleigh-Durham, NC', 
                'San Francisco, CA', 
                'Seattle, WA', 
                'Washington D.C']
    return jsonify(available_cities)

@app.route("/cities")
def cities():
    """Return stats for each city for all available years"""
    city_dict = {}
    results = (session.query(mean_sales_count.Metro).all())
    city_list = list(np.ravel(results))
    session.rollback()  
    city_list = ['Austin-Round Rock', 'Dallas-Fort Worth-Arlington', 'Denver-Aurora-Lakewood', 'Detroit-Warren-Dearborn', 'New York-Newark-Jersey City', 'Orlando-Kissimmee-Sanford', 'Raleigh-Durham-Chapel Hill', 'San Francisco-Oakland-Hayward', 'Seattle-Tacoma-Bellevue', 'Washington-Arlington-Alexandria']
    print(city_list)
    city_ST = {'Austin-Round Rock': 'Austin, TX', 
                'Dallas-Fort Worth-Arlington': 'Dallas-Forth Worth, TX', 
                'Denver-Aurora-Lakewood': 'Denver, CO', 
                'Detroit-Warren-Dearborn': 'Detroit, MI', 
                'New York-Newark-Jersey City': 'New York City, NY', 
                'Orlando-Kissimmee-Sanford': 'Orlando, FL', 
                'Raleigh-Durham-Chapel Hill': 'Raleigh-Durham, NC', 
                'San Francisco-Oakland-Hayward': 'San Francisco, CA', 
                'Seattle-Tacoma-Bellevue': 'Seattle, WA', 
                'Washington-Arlington-Alexandria': 'Washington D.C.'}
    for city in city_list:
        mean_results = ((session.query(
                        mean_sales_count._2008,
                        mean_sales_count._2009,
                        mean_sales_count._2010,
                        mean_sales_count._2011,
                        mean_sales_count._2012,
                        mean_sales_count._2013,
                        mean_sales_count._2014,
                        mean_sales_count._2015,
                        mean_sales_count._2016,
                        mean_sales_count._2017,
                        mean_sales_count._2018
                        )).
                        filter(mean_sales_count.Metro == city).all())
        mean_results_list = list(np.ravel(mean_results))  
        session.rollback()     
        median_results = ((session.query(
                        median_sales_count._2008,
                        median_sales_count._2009,
                        median_sales_count._2010,
                        median_sales_count._2011,
                        median_sales_count._2012,
                        median_sales_count._2013,
                        median_sales_count._2014,
                        median_sales_count._2015,
                        median_sales_count._2016,
                        median_sales_count._2017,
                        median_sales_count._2018
                        )).
                        filter(median_sales_count.Metro == city).all())
        median_results_list = list(np.ravel(median_results)) 
        session.rollback() 
        sqft_results = ((session.query(
                        median_price_sqft._1996,
                        median_price_sqft._1997,
                        median_price_sqft._1998,
                        median_price_sqft._1999,
                        median_price_sqft._2000,
                        median_price_sqft._2001,
                        median_price_sqft._2002,
                        median_price_sqft._2003,
                        median_price_sqft._2004,
                        median_price_sqft._2005,
                        median_price_sqft._2006,
                        median_price_sqft._2007,
                        median_price_sqft._2008,
                        median_price_sqft._2009,
                        median_price_sqft._2010,
                        median_price_sqft._2011,
                        median_price_sqft._2012,
                        median_price_sqft._2013,
                        median_price_sqft._2014,
                        median_price_sqft._2015,
                        median_price_sqft._2016,
                        median_price_sqft._2017,
                        median_price_sqft._2018
                        )).
                        filter(median_price_sqft.Metro == city).all())
        sqft_results_list = list(np.ravel(sqft_results))  
        session.rollback()

        price_results = ((session.query(median_price_zip._2013,
                        median_price_zip._2014,
                        median_price_zip._2015,
                        median_price_zip._2016,
                        median_price_zip._2017,
                        median_price_zip._2018,
                        median_price_zip.coordinates)).
                        filter(median_price_zip.Metro == city).all())
        price_results_list = list(np.ravel(price_results))
        session.rollback()

        coordinate_results = ((session.query(
                        median_price_zip.coordinates)).
                        filter(median_price_zip.Metro == city).all())
        city_coordinates = list(np.ravel(coordinate_results))
        session.rollback()

        city_dict[city_ST[city]] = {
            "Metro Area": city,
            "Coordinates" : str(city_coordinates[0]),
            "Average (Median) Sale Price Per Year": {
                "2013": str(price_results_list[0]),
                "2014": str(price_results_list[1]),
                "2015": str(price_results_list[2]),
                "2016": str(price_results_list[3]),
                "2017": str(price_results_list[4]),
                "2018": str(price_results_list[5]),
            },
            "Average (Mean) # Sales Per Year": {
                "2008": str(int(mean_results_list[0])),
                "2009": str(int(mean_results_list[1])),
                "2010": str(int(mean_results_list[2])),
                "2011": str(int(mean_results_list[3])),
                "2012": str(int(mean_results_list[4])),
                "2013": str(int(mean_results_list[5])),
                "2014": str(int(mean_results_list[6])),
                "2015": str(int(mean_results_list[7])),
                "2016": str(int(mean_results_list[8])),
                "2017": str(int(mean_results_list[9])),
                "2018": str(int(mean_results_list[10]))
            },
            "Average (Median) # Sales Per Year": {
                "2008": str(int(median_results_list[0])),
                "2009": str(int(median_results_list[1])),
                "2010": str(int(median_results_list[2])),
                "2011": str(int(median_results_list[3])),
                "2012": str(int(median_results_list[4])),
                "2013": str(int(median_results_list[5])),
                "2014": str(int(median_results_list[6])),
                "2015": str(int(median_results_list[7])),
                "2016": str(int(median_results_list[8])),
                "2017": str(int(median_results_list[9])),
                "2018": str(int(median_results_list[10]))
            },
            "Average (Median) Price Per Square Foot": {
                "1996": str(int(sqft_results_list[0])),
                "1997": str(int(sqft_results_list[1])),
                "1998": str(int(sqft_results_list[2])),
                "1999": str(int(sqft_results_list[3])),
                "2000": str(int(sqft_results_list[4])),
                "2001": str(int(sqft_results_list[5])),
                "2002": str(int(sqft_results_list[6])),
                "2003": str(int(sqft_results_list[7])),
                "2004": str(int(sqft_results_list[8])),
                "2005": str(int(sqft_results_list[9])),
                "2006": str(int(sqft_results_list[10])),
                "2007": str(int(sqft_results_list[11])),
                "2008": str(int(sqft_results_list[12])),
                "2009": str(int(sqft_results_list[13])),
                "2010": str(int(sqft_results_list[14])),
                "2011": str(int(sqft_results_list[15])),
                "2012": str(int(sqft_results_list[16])),
                "2013": str(int(sqft_results_list[17])),
                "2014": str(int(sqft_results_list[18])),
                "2015": str(int(sqft_results_list[19])),
                "2016": str(int(sqft_results_list[20])),
                "2017": str(int(sqft_results_list[21])),
                "2018": str(int(sqft_results_list[22]))
            }
        }
    return jsonify(city_dict)

""" @app.route("/ZipCodes")
def zip():
    metro_names = ['Seattle-Tacoma-Bellevue',
    'Washington-Arlington-Alexandria',
    'Detroit-Warren-Dearborn',
    'Denver-Aurora-Lakewood',
    'Austin-Round Rock',
    'Orlando-Kissimmee-Sanford',
    'Raleigh-Durham-Chapel Hill',
    'Dallas-Fort Worth-Arlington',
    'San Francisco-Oakland-Hayward',
    'New York-Newark-Jersey City']

    price_agg = pd.read_sql_table('median_price_zip', engine)

    metro_zipcodes = {}
    for metro in metro_names:
        metro_zipcodes[metro] = list(price_agg.loc[price_agg.Metro == metro].ZipCode)

    zip_geo = {'WA':'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/wa_washington_zip_codes_geo.min.json',
            'DC':'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/dc_district_of_columbia_zip_codes_geo.min.json', 
            'MD':'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/md_maryland_zip_codes_geo.min.json', 
            'VA':'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/va_virginia_zip_codes_geo.min.json', 
            'WV':'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/wv_west_virginia_zip_codes_geo.min.json', 
            'MI':'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/mi_michigan_zip_codes_geo.min.json', 
            'CO':'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/co_colorado_zip_codes_geo.min.json', 
            'TX':'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/tx_texas_zip_codes_geo.min.json', 
            'FL':'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/fl_florida_zip_codes_geo.min.json', 
            'NC':'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/nc_north_carolina_zip_codes_geo.min.json', 
            'CA':'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/ca_california_zip_codes_geo.min.json', 
            'NY':'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/ny_new_york_zip_codes_geo.min.json', 
            'NJ':'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/nj_new_jersey_zip_codes_geo.min.json'}
    
    metro_zips = []
    for key, url in zip_geo.items():
        r = requests.get(url)
        zips_json = r.json()
        
        sub_zips = {}
        for i in range(0, len(zips_json['features'])):
            for key, values in metro_zipcodes.items():
                for value in values:
                    if value == int(zips_json['features'][i]['properties']['ZCTA5CE10']):
                        sub_zips[value] = zips_json['features'][i]['geometry']['coordinates'][0]
        metro_zips.append(sub_zips)
   
    return jsonify(metro_zips) """


#  Define main behavior
if __name__ == "__main__":
    app.run(debug=True)
