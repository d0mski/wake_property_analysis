# Packages

import pandas as pd
import datetime
import xlrd
import os
import sqlalchemy as db
import sqlite3
import matplotlib.pyplot as plt 

# SQL Connection

conn = sqlite3.connect('properties.sqlite')
cur=conn.cursor()

# Import Data

try:
    cur.execute('SELECT * FROM new_realinfo')
except:
    print("Table does not exist! Please wait as it is created...")
    df = pd.read_excel('Real_Est_Data_Final_Nov2019.xlsx')
    df.to_sql(name='new_realinfo', con=conn)

engine = db.create_engine('sqlite:///properties.sqlite', echo = True)
conn = engine.connect()

# Cleaning Data
cur.execute('CREATE TABLE IF NOT EXISTS new_realinfo AS SELECT * ORDER BY "YEAR"')
df = pd.read_sql_table('new_realinfo', conn)

df['Total_Assessed_Valuation'] = df['Assessed_Building_Value'] + df['Assessed_Land_Value']
df['Year'] = df['Total_Sale_Date'].dt.year
df = df[df["Land_classification"]=='R']
year = df.groupby(['Year'])
# print(year['Total_Assessed_Valuation'].mean())

# # Chart of initial data
y = year['Total_Sale_Date'].count()
z = year['Total_sale_Price'].mean()

# y.plot()
# plt.ylabel('Price in Dollars')
# plt.title('Number of Residential Home Sales per Year')
# plt.legend()
# plt.show()

# z.plot()
# plt.ylabel('Price in Dollars')
# plt.title('Average Price of Residential Homes per Year')
# plt.legend()
# plt.show()

# X-Coordinates for Graphs
def x_coor():
    xcoords = df['Year'].tolist()
    xcoords = set(xcoords)
    cleaned_x = [x for x in xcoords if str(x) != 'nan']
    return cleaned_x

# Function to analyze data by zipcode

def zipFunc(zip):
        input_zip = int(zip)
        filtered_data_zip_pre = df[df['PHYSICAL_ZIP_CODE']==input_zip]
        filtered_data_zip_pre = filtered_data_zip_pre.groupby('Year')
        filtered_data_zip = filtered_data_zip_pre['Total_sale_Price'].mean()
        filtered_data_zip.plot(label='Price by Zip Code')
        z.plot(label = 'Price by County')
        plt.ylabel('Price in Dollars')
        plt.title('Average Price of Residential Homes per Year in ' + str(input_zip))
        plt.legend()
        plt.show()
        zipcoords = filtered_data_zip.tolist()
        zipcoords = set(zipcoords)
        cleaned_zip = [x for x in zipcoords if str(x) != 'nan']
        return cleaned_zip

# Function to analyze data by street

def streetFunc(street, prefix=' '):
    input_street = street.upper()
    if prefix == ' ':
        filtered_data_pre = df[df["Street_Name"]==input_street]
        filtered_data_pre = filtered_data_pre.groupby('Year')
        filtered_data = filtered_data_pre['Total_sale_Price'].mean()
        filtered_data.plot()
        z.plot(label='Price by Street')
        plt.ylabel('Price in Dollars')
        plt.title('Average Price of Residential Homes per Year in ' + input_street.title())
        plt.legend()
        plt.show()
        streetcoords = filtered_data.tolist()
        streetcoords = set(streetcoords)
        cleaned_street = [x for x in streetcoords if str(x) != 'nan']
        return cleaned_street
    else:
        filtered_data_prefix = df[df["Street_Prefix"]==prefix.upper()]
        filtered_data_pre = filtered_data_prefix[filtered_data_prefix["Street_Name"]==input_street]
        filtered_data_pre = filtered_data_pre.groupby('Year')
        filtered_data = filtered_data_pre['Total_sale_Price'].mean()
        filtered_data.plot(label='Price by Street')
        z.plot(label = 'Price by County')
        plt.ylabel('Price in Dollars')
        plt.title('Average Price of Residential Homes per Year in ' + prefix.upper() + ' ' + input_street.title())
        plt.legend()
        plt.show()
        prefixcoords = filtered_data.tolist()
        prefixcoords = set(prefixcoords)
        cleaned_prefix = [x for x in prefixcoords if str(x) != 'nan']
        return cleaned_prefix

# Function to analyze data by city

def cityFunc(city):
        input_city = city.upper()
        filtered_data_city_pre = df[df['PHYSICAL_CITY']==input_city]
        filtered_data_city_pre = filtered_data_city_pre.groupby('Year')
        filtered_data_city = filtered_data_city_pre['Total_sale_Price'].mean()
        filtered_data_city.plot(label="City Price")
        z.plot(label = 'Price by County')
        plt.ylabel('Price in Dollars')
        plt.title('Average Price of Residential Homes per Year in ' + input_city.title())
        plt.legend()
        plt.show()
        citycoords = filtered_data_city.tolist()
        citycoords = set(citycoords)
        cleaned_city = [x for x in citycoords if str(x) != 'nan']
        return cleaned_city