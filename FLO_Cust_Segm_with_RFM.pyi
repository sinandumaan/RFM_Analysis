
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


# Calculating RFM(Recency, Frequency, Monetary) Metrics

# Specify the analysis date with parameter "last_order_date"
df["last_order_date"].max() # 2021-05-30
analysis_date = dt.datetime(2021,6,1)

# New Dataframe is created as named "rfm" and columns are ["customer_id","recency","frequency","monetary"]

rfm = pd.DataFrame()
rfm["customer_id"] = df["master_id"]
rfm["recency"] = (analysis_date - df["last_order_date"]).astype('timedelta64[D]')
rfm["frequency"] = df["order_num_total"]
rfm["monetary"] = df["customer_value_total"]

# Calculating RF and RFM Scores with qcut

rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

rfm["RF_SCORE"] = (rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str))

rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str) + rfm['monetary_score'].astype(str))

# Identifying RF Scores as Segment with Regular Expression(Regex)

seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

rfm['segment'] = rfm['RF_SCORE'].replace(seg_map, regex=True)

rfm.head()


# ANALYZE

rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])

#                    recency       frequency       monetary
#                       mean count      mean count     mean count
# segment
# about_to_sleep       113.79  1629      2.40  1629   359.01  1629
# at_Risk              241.61  3131      4.47  3131   646.61  3131
# cant_loose           235.44  1200     10.70  1200  1474.47  1200
# champions             17.11  1932      8.93  1932  1406.63  1932
# hibernating          247.95  3604      2.39  3604   366.27  3604
# loyal_customers       82.59  3361      8.37  3361  1216.82  3361
# need_attention       113.83   823      3.73   823   562.14   823
# new_customers         17.92   680      2.00   680   339.96   680
# potential_loyalists   37.16  2938      3.30  2938   533.18  2938
# promising             58.92   647      2.00   647   335.67   647


# Two Cases

# FLO includes a new women's shoe brand. Product prices of the included brand
# on your preferences. For this reason, it is specially designed with customers in the profile that will be interested in the promotion of the brand and product sales.
# you want to contact. Shopping from loyal customers (champions, loyal_customers) and female category
# customers to be contacted specifically. Save the id numbers of these customers to the csv file.

target_segments_customer_ids = rfm[rfm["segment"].isin(["champions","loyal_customers"])]["customer_id"]
customer_ids = df[(df["master_id"].isin(target_segments_customer_ids)) &(df["interested_in_categories_12"].str.contains("KADIN"))]["master_id"]
customer_ids.to_csv("shoe_brand_customer_id.csv", index=False)




