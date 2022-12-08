# usr/bin/env python

"""This is the data cleaner notebook from 10_code moved to a .py file for use CI/CD"""


# imports
import pandas as pd
import os


# make the empty dataframe with years and months from 1970 to 2022 as the index
df = pd.DataFrame(
    index=pd.MultiIndex.from_product(
        [range(1970, 2023), range(1, 13)], names=["year", "month"]
    )
)

# add a year_month column
df["date"] = df.index.to_series().apply(lambda x: str(x[0]) + "-" + str(x[1]).zfill(2))

# convert the year_month column to a datetime object
df["date"] = pd.to_datetime(df["date"], format="%Y-%m")

# reset the structure so the dataframe is only the date column
df = df.reset_index(drop=True)

df.head(10)

# ingest the census data
census_df = pd.read_excel(
    "../00_source_data/population-change-data-table.xlsx", skiprows=3
)
# keep only census columns
census_df = census_df[
    [
        "Area",
        "1910 Census",
        "1920 Census",
        "1930 Census",
        "1940 Census",
        "1950 Census",
        "1960 Census",
        "1970 Census",
        "1980 Census",
        "1990 Census",
        "2000 Census",
        "2010 Census",
        "2020 Census",
    ]
]

# rename the mispelled United States1 to US
census_df.loc[census_df["Area"] == "United States1", "Area"] = "US"

# Pull out only the US row
census_df = census_df[census_df["Area"] == "US"]

# pivot the census data
census_df = census_df.melt(id_vars=["Area"], var_name="Year", value_name="Population")

# convert the year column to a datetime
census_df["date"] = pd.to_datetime(census_df["Year"], format="%Y Census")

# convert the date column to a datetime object
census_df["date"] = pd.to_datetime(census_df["date"], format="%Y")

# drop the Area column
census_df = census_df.drop(columns=["Area", "Year"])

# convert the population column to an integer
census_df["Population"] = census_df["Population"].astype(int)

# filter for just the years after 1949
census_df = census_df[census_df["date"] > "1969-12-31"]

# round the population column to the nearest 1000
census_df["Population"] = census_df["Population"].round(-3)

# reset the index
census_df = census_df.reset_index(drop=True)

census_df.head(10)

elec_df = pd.read_csv("../00_source_data/MER_T07_02A.csv")

# split the YYYYMM column into a year and month column
elec_df["year"] = elec_df["YYYYMM"].apply(lambda x: int(str(x)[:4]))
elec_df["month"] = elec_df["YYYYMM"].apply(lambda x: int(str(x)[4:]))

# drop all rows where month equals 13
elec_df = elec_df[elec_df["month"] != 13]

# make a date column from the year and month columns
elec_df["date"] = pd.to_datetime(
    elec_df["year"].astype(str) + "-" + elec_df["month"].astype(str).str.zfill(2)
)

# makes sure the date is a datetime object
elec_df["date"] = pd.to_datetime(elec_df["date"])

# drop the where Value equals not available
elec_df = elec_df[elec_df["Value"] != "Not Available"]

# convert value to an integer
elec_df["Value"] = elec_df["Value"].astype(float)

# groupby date and sum the electricity generation
elec_df = elec_df.groupby("date").sum().reset_index()

# keep the date and value columns
elec_df = elec_df[["date", "Value"]]

# rename value to generation
elec_df = elec_df.rename(columns={"Value": "generation"})

# round the generation column to the nearest 100
elec_df["generation"] = elec_df["generation"].round(-2)

elec_df.head(10)

veh_df = pd.read_csv("../00_source_data/MER_T01_08.csv")

# subset for the rows where unit is Miles per Gallon
veh_df = veh_df[veh_df["Unit"] == "Miles per Gallon"]

# keep Descriptions where the value is All Motor Vehicles Fuel Economy
veh_df = veh_df[veh_df["Description"] == "All Motor Vehicles Fuel Economy"]

# split the YYYYMM column into two columns
veh_df["Year"] = veh_df["YYYYMM"].astype(str).str[:4]
veh_df["Month"] = veh_df["YYYYMM"].astype(str).str[4:]

# if the month column is 13 make it 1
veh_df.loc[veh_df["Month"] == "13", "Month"] = "1"

# make a date column from year and month columns and add the day as 01
veh_df["date"] = pd.to_datetime(
    veh_df["Year"].astype(str) + "-" + veh_df["Month"].astype(str) + "-01"
)

# keep the Value and Year columns
veh_df = veh_df[["Value", "date"]]

# Rename the value column to Veh_MPG
veh_df = veh_df.rename(columns={"Value": "Veh_MPG"})

# convert Veh_MPG to a float
veh_df["Veh_MPG"] = veh_df["Veh_MPG"].astype(float)

# groupby year and take the mean
veh_df = veh_df.groupby("date").mean()

# filter to only years after 1972
veh_df = veh_df[veh_df.index > "1972-12-31"]

# reset the index
veh_df = veh_df.reset_index()

veh_df.head(10)

# create a loop to read in all the csv files in the folder and merge them into one dataframe
# create a list of the files in the folder
files = os.listdir("../00_source_data/NOAA_data")

# create an empty list to hold the dataframes
dfs = []

# loop through the files
for file in files:
    # read in the csv file
    tempdf = pd.read_csv("../00_source_data/NOAA_data/" + file, skiprows=4)
    # append the dataframe to the list
    dfs.append(tempdf)

# merge the dataframes into one dataframe
noaa_df = pd.concat(dfs)

# convert the date column to a datetime object of month and year
noaa_df["date"] = pd.to_datetime(noaa_df["Date"], format="%Y%m")

# rename Value to AvgTemp
noaa_df = noaa_df.rename(columns={"Value": "AvgTemp"})

# drop the date and anomaly columns
noaa_df = noaa_df.drop(columns=["Date", "Anomaly"])

# drop years before 1973
noaa_df = noaa_df[noaa_df["date"] > "1972-12-31"].reset_index(drop=True)

# switch the column order
noaa_df = noaa_df[["date", "AvgTemp"]]

noaa_df.head(20)


ev_df = pd.read_excel("../00_source_data/afv_vehicle_data.xlsx")

# drop the first column
# ev_df = ev_df.drop(columns=["Unnamed: 0"])

# pivot the dataframe to put columns as rows and vice versa
ev_df = ev_df.melt(id_vars=["Unnamed: 0"], var_name="year", value_name="ev_sales")

# drop dows where sales is z
ev_df = ev_df[ev_df["ev_sales"] != "Z"]

# drop the unnamed column
ev_df = ev_df.drop(columns=["Unnamed: 0"])

# groupby year and sum the sales
ev_df = ev_df.groupby("year").sum().reset_index()

# rename the year column to date
ev_df = ev_df.rename(columns={"year": "date"})

# convert the date column to a datetime object
ev_df["date"] = pd.to_datetime(ev_df["date"], format="%Y")

ev_df.head(10)

gdp = pd.read_csv("../00_source_data/GDP.csv")

# rename Date to date
gdp = gdp.rename(columns={"DATE": "date"})

# make sure date is a datetime object
gdp["date"] = pd.to_datetime(gdp["date"])

gdp.head(10)

gnp = pd.read_csv("../00_source_data/GNP.csv")

# rename Date to date
gnp = gnp.rename(columns={"DATE": "date"})

# make sure date is a datetime object
gnp["date"] = pd.to_datetime(gnp["date"])

gnp.head(10)

# Merging

# merge the census data with the empty dataframe
merged_df = pd.merge(df, census_df, on="date", how="left")
# smooth the population column
merged_df["Population"] = merged_df["Population"].interpolate()
merged_df.plot(x="date", y="Population")

# # filter the data to include only the years after 1972
merged_df = merged_df[merged_df["date"] > "1972-12-31"]

merged_df.head()

# merge the energy data with the merged dataframe
merged_df2 = pd.merge(merged_df, elec_df, on="date", how="left").copy()
# smooth the energy column
merged_df2["generation"] = merged_df2["generation"].interpolate()
merged_df2.plot(x="date", y="generation")

merged_df2.head()

# merge vehicle data
merged_df3 = pd.merge(merged_df2, veh_df, on="date", how="left").copy()
# smooth the vehicle column
merged_df3["Veh_MPG"] = merged_df3["Veh_MPG"].interpolate()
merged_df3.plot(x="date", y="Veh_MPG")

merged_df3.head()

# merge the NOAA df on date
merged_df4 = pd.merge(merged_df3, noaa_df, on="date", how="left").copy()

# # smooth the temperature column
merged_df4["AvgTemp"] = merged_df4["AvgTemp"].interpolate()
merged_df4.plot(x="date", y="AvgTemp")

merged_df4.head()

# merge df4 and the ev_df on date
merged_df5 = pd.merge(merged_df4, ev_df, on="date", how="left").copy()

# # smooth the ev_sales column
merged_df5["ev_sales"] = merged_df5["ev_sales"].interpolate()
merged_df5.plot(x="date", y="ev_sales")

# replace the nan ev_sales with 0
merged_df5["ev_sales"] = merged_df5["ev_sales"].fillna(0)

merged_df5.head(10)

# add the GDP df
merged_df6 = pd.merge(merged_df5, gdp, on="date", how="left").copy()

# interpolate missing values for gdp
merged_df6["GDP"] = merged_df6["GDP"].interpolate()

merged_df6.head(10)

# add the GNP df
merged_df7 = pd.merge(merged_df6, gnp, on="date", how="left").copy()

# interpolate missing values for gdp
merged_df7["GNP"] = merged_df7["GNP"].interpolate()

merged_df7.head(10)

# save merged df4 to a csv in the 20_clean_data_directory
merged_df7.to_csv("../20_clean_data/merged_dataset.csv", index=False)
