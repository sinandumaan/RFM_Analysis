
# Customer Segmentation with RFM

# FLO aims to segment its distributions and target marketing according to these segments.
# For this purpose, the behaviors of the customers will be defined and groups will be formed according to these behavior clusters.

# Data Preparation and Data Understanding

import pandas as pd
import datetime as dt
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.2f' % x)
pd.set_option('display.width',1000)

df_ = pd.read_csv("flo_data_20k.csv")
df = df_.copy()

# Variables summary

df.columns
df.describe().T
df.isnull().sum()
df.info()

# The number of total orders and total customer values are defined

df["order_num_total"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
df["customer_value_total"] = df["customer_value_total_ever_offline"] + df["customer_value_total_ever_online"]

# Variable which contains "date" is converted to datetime datatype

date_columns = df.columns[df.columns.str.contains("date")]
df[date_columns] = df[date_columns].apply(pd.to_datetime)

# The distribution of the number of customers in the shopping channels, the total number of products purchased and the total expenditures.

df.groupby("order_channel").agg({"master_id":"count",
                                 "order_num_total":"sum",
                                 "customer_value_total":"sum"})

# The top 10 customers with the highest customer value

df.sort_values("customer_value_total", ascending=False)[:10]

# The top 10 customers with the most orders.

df.sort_values("order_num_total", ascending=False)[:10]

# Functionalize the Data Preparation section
def data_prep(dataframe):
    dataframe["order_num_total"] = dataframe["order_num_total_ever_online"] + dataframe["order_num_total_ever_offline"]
    dataframe["customer_value_total"] = dataframe["customer_value_total_ever_offline"] + dataframe["customer_value_total_ever_online"]
    date_columns = dataframe.columns[dataframe.columns.str.contains("date")]
    dataframe[date_columns] = dataframe[date_columns].apply(pd.to_datetime)
    return df






