import pandas as pd
import numpy as np
import matplotlib as mlt
import seaborn as srn
print("hello")
df=pd.read_csv("dirty_cafe_sales.csv")
print(df.head())
print(df.shape)

## show columns ##

print(df.columns)

## check data type##
print(df.info())
## find missing values##
print(df.isnull().sum())

## % of missing values##
print((df.isnull().sum()/len(df))*100)

## find no of duplicates##
print(df.duplicated().sum())

## 
print(df['Transaction ID'].duplicated(keep=False).sum())

## duplicates in Transaction ID##

print(df.loc[df['Transaction ID'].duplicated(),'Transaction ID'])
 ## suplicates in Item ##

print(df.loc[df['Item'].duplicated(),'Item'])

## 

print(df['Item'].unique())

print(df.loc[df['Item'].duplicated(),'Item'].unique())

## Replace Error and Unknown with NaN in Item column ##

df['Item']=df['Item'].replace(['ERROR','UNKNOWN'],np.nan)

print(df['Item'].unique())

## identify Invalied values in Price Per UNit column ##

print(df['Price Per Unit'].unique())
## replacing them

df['Price Per Unit']=df['Price Per Unit'].replace(['ERROR','UNKNOWN'],np.nan)
print(df['Price Per Unit'].unique())

## I will fill missing values of the help of Price of item column##
print(df[['Item','Price Per Unit']].drop_duplicates())

## maping b/w item and price## two or more item have same price  

price_maping=df.dropna(subset=['Price Per Unit','Item']).drop_duplicates(subset='Item').set_index('Item')['Price Per Unit']
print(price_maping)

## filling missing value of price column##

df['Price Per Unit']=df['Price Per Unit'].fillna(df['Item'].map(price_maping))

print(df.isnull().sum())
print(df['Price Per Unit'].isna().sum())
print(df) 


##
print(df["Total Spent"].unique())
df["Total Spent"]=df["Total Spent"].replace(["ERROR","UNKNOWN"],np.nan)
print(df) 

## 
print(df["Quantity"].unique())

df["Quantity"]=df["Quantity"].replace(["ERROR","UNKNOWN"],np.nan)
print(df["Quantity"].unique())
df["Total Spent"]=df["Total Spent"].astype('float')
print(df.info())
df["Quantity"]=df["Quantity"].astype('Int64')
df["backup_price"]=df["Total Spent"]/df["Quantity"]

print(df["backup_price"].isnull().sum())
print(df.loc[df["Price Per Unit"].isna() ,["backup_price"]].sample(20))

## updating again left null values in price 

df["Price Per Unit"]=df["Price Per Unit"].fillna(df['backup_price'])
df=df.drop("backup_price", axis=1)
## changes Transaction column data type str to datetime

df['Transaction Date']=pd.to_datetime(df['Transaction Date'],errors='coerce')
## filling missing values in Item column 

print(df[["Item","Price Per Unit"]])
print(df.loc[:, ["Price Per Unit",'Item']].drop_duplicates())
for value in df["Item"].unique():
    print("value:",value ,"| data type:",type(value))


for value in df["Price Per Unit"].unique():
    print("value:",value ,"| data type:",type(value))

print(df[["Item","Location"]].drop_duplicates())
df["Price Per Unit"]=pd.to_numeric(df['Price Per Unit'])

df1=df.loc[df["Price Per Unit"].isin([1.0,1.5,2.0,4.0,5.0])].dropna(subset=["Item"]).drop_duplicates(["Price Per Unit"]).set_index("Price Per Unit")["Item"]
print(df1)
df['Item']=df['Item'].fillna(df["Price Per Unit"].map(df1))

## Filling missing value in Total spend column
df["backup_spend"]=df["Price Per Unit"]*df["Quantity"]
df["Total Spent"]=df["Total Spent"].combine_first(df["backup_spend"])
print(df["Total Spent"].unique())

## Filling remaining missing values in Item column ## (not working)
df.set_index("Total Spent",inplace=True)
df["bkp_item"]=df.loc[:,"Item"]
df["Item"]=df["Item"].combine_first(df["bkp_item"])
print(df["bkp_item"].isna().sum())
df=df.reset_index()

col=df.pop("Total Spent")
df.insert(4,"Total Spent",col)
##
##

## Filling missing values in Quantity column
df['bkp_qty']=df["Total Spent"]/df["Price Per Unit"]
df["Quantity"]=df['Quantity'].combine_first(df["bkp_qty"])
df=df.drop(columns=["backup_spend","bkp_item","bkp_qty"])
## filling missing value in coluns location payment mode
df[["Payment Method","Location"]]=df[["Payment Method","Location"]].replace(["ERROR","UNKNOWN"],np.nan)
df[["Payment Method","Location"]]=df[["Payment Method","Location"]].apply(lambda x:x.fillna(x.mode()[0]))
print(df["Location"].unique())
print(df["Payment Method"].unique())
## filling missing values in item column with "Juice"=is mode in juice and cake having same price#

df1=df.loc[df["Item"].isin(["Cake","Juice"]),"Item"].mode()
print(df1)
df["Item"]=df["Item"].fillna("Juice")

## handling missing value in Transaction Date column
print(df["Transaction Date"].dt.day_name().drop_duplicates())
print(df.head(20))
##removing duplicates
df=df.drop_duplicates()
print(df.info())
## saving cleaned data#
df.to_csv(r"C:\Users\manoj\OneDrive\Desktop\DA\cleaned_cafe_data.csv", index=False)