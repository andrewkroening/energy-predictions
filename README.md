# Azure AutoML Energy Demand Forecaster

### Introduction

This project uses Microsoft Azure Machine Learning resources to construct a forecast model for energy demand in the United States. It's not intended for serious use, so don't treat it as such. To construct the model, I cherry-picked a few data sources that seemed interesting:

* [U.S. Energy Net Electricty Production Data](https://www.eia.gov/totalenergy/data/browser/?tbl=T07.02A)

* [Fuel Economy of the average vehicle in the U.S.](https://www.eia.gov/totalenergy/data/browser/csv.php?tbl=T01.08)

* [Estimated and Real Population figures from the U.S. Census Bureau](https://www2.census.gov/programs-surveys/decennial/2020/data/apportionment/population-change-data-table.xlsx)

* [Climate and Temperature Data](https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/national/time-series/110/tavg/1/12/1940-2022?base_prd=true&begbaseyear=1901&endbaseyear=2000)

* [Sales of various Electric Vehicles (Hybrid, Plug-in Hybrid, Battery) in the U.S.](https://www.bts.gov/content/gasoline-hybrid-and-electric-vehicle-sales)

* Numbers of Data Centers operating in the U.S. (future)

### Phase III (In-progress)

For Phase III, I'll be seeking to accomplish a few tasks with the back end data:

* Add additional data sources

* Switch the data source to tabular from a csv file I uploaded using SQL

### Phase II ([Demo Video](https://youtu.be/Nh-wG2ZLLAs))

In Phase II, I made some changes to the base dataset. I removed energy consumption and changed the source of the energy generation statistics to a different EIA table. This improved readability and interpretability. I also added sales figures for vehicles with a big battery (battery electric, hybrid, plug-in hybrid). With these new figures, I re-ran our ML experiment using Azure AutoML. The results are captured below. In summary, it looks like the AutoML model (VotingEnsemble) performed very well:


<img src="https://github.com/andrewkroening/energy-predictions/blob/92fd42ca40d5324b1f52e867e34fe71e17b059b0/30_intermediate_files/forecast_perform.png" alt="PhaseI" width="1000"/>

<img src="https://github.com/andrewkroening/energy-predictions/blob/92fd42ca40d5324b1f52e867e34fe71e17b059b0/30_intermediate_files/feature_rank.png" alt="PhaseI" width="1000"/>

### Phase I ([Demo video](https://youtu.be/RkAp5NcK8c4))

In Phase I, I constructed a Machine Learning Workspace in Azure and a repository on GitHub to host the code I use to clean data and test API calls. I determined the API calls need some more work, so I use a [notebook](https://github.com/andrewkroening/energy-predictions/blob/6ef76311342997dc1e8e61baa563a4df174d471d/10_code/data_cleaner.ipynb) to clean data, transform it, and merge into a time series. That data is then uploaded to an Azure storage account and we construct a simple pipeline to test the resources and data. Big surprise: when you include Energy Production as a predictor of Energy Consumption the model is *really* accurate.

Here's a drawing to illustrate what Phase I accomplished:
<img src="https://github.com/andrewkroening/energy-predictions/blob/6ef76311342997dc1e8e61baa563a4df174d471d/30_intermediate_files/energy_predict_ph1.png" alt="PhaseI" width="1000"/>
