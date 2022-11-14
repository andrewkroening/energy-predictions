# Azure AutoML Energy Demand Forecaster

### Introduction

This project uses Microsoft Azure Machine Learning resources to construct a forecast model for energy demand in the United States. It's not intended for serious use, so don't treat it as such. To construct the model, I cherry-picked a few data sources that seemed interesting:

* [U.S. Energy Consumption and Production Data](https://www.eia.gov/totalenergy/data/browser/csv.php?tbl=T01.01)

* [Fuel Economy of the average vehicle in the U.S.](https://www.eia.gov/totalenergy/data/browser/csv.php?tbl=T01.08)

* [Estimated and Real Population figures from the U.S. Census Bureau](https://www2.census.gov/programs-surveys/decennial/2020/data/apportionment/population-change-data-table.xlsx)

* [Climate and Temperature Data](https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/national/time-series/110/tavg/1/12/1940-2022?base_prd=true&begbaseyear=1901&endbaseyear=2000)

* Registration figures for Battery Electric and Plug-in Hybrid Electric Vehicles in the U.S. (future)

* Numbers of Data Centers operating in the U.S. (future)

### Phase II (In-progress)

For Phase II, I'll be seeking to accomplish a few tasks with the back end data:

* Add energy data via an API call instead of static

* Add additional data sources

* Switch the data source to tabular from a csv file I uploaded

* Use AutoML to select the ideal model and push to a deployment resource

### Phase I ([Demo video](https://youtu.be/RkAp5NcK8c4))

In Phase I, I constructed a Machine Learning Workspace in Azure and a repository on GitHub to host the code I use to clean data and test API calls. I determined the API calls need some more work, so I use a [notebook](https://github.com/andrewkroening/energy-predictions/blob/6ef76311342997dc1e8e61baa563a4df174d471d/10_code/data_cleaner.ipynb) to clean data, transform it, and merge into a time series. That data is then uploaded to an Azure storage account and we construct a simple pipeline to test the resources and data. Big surprise: when you include Energy Production as a predictor of Energy Consumption the model is *really* accurate.

Here's a drawing to illustrate what Phase I accomplished:
<img src="https://github.com/andrewkroening/energy-predictions/blob/6ef76311342997dc1e8e61baa563a4df174d471d/30_intermediate_files/energy_predict_ph1.png" alt="PhaseI" width="1000"/>

