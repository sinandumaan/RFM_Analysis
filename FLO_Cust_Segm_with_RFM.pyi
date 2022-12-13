
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

df.columns
df.describe().T
df.isnull().sum()
df.info()


