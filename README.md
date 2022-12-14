# Azure AutoML Energy Demand Forecaster
[![CI/CD Pipeline](https://github.com/andrewkroening/energy-predictions/actions/workflows/main.yml/badge.svg)](https://github.com/andrewkroening/energy-predictions/actions/workflows/main.yml)

### Introduction

This project uses Microsoft Azure Machine Learning resources to construct a forecast model for energy demand in the United States. It's not intended for serious use, so don't treat it as such. To construct the model, I cherry-picked a few data sources that seemed interesting:

* [U.S. Energy Net Electricty Production Data](https://www.eia.gov/totalenergy/data/browser/?tbl=T07.02A)

* [Fuel Economy of the average vehicle in the U.S.](https://www.eia.gov/totalenergy/data/browser/csv.php?tbl=T01.08)

* [Estimated and Real Population figures from the U.S. Census Bureau](https://www2.census.gov/programs-surveys/decennial/2020/data/apportionment/population-change-data-table.xlsx)

* [Climate and Temperature Data](https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/national/time-series/110/tavg/1/12/1940-2022?base_prd=true&begbaseyear=1901&endbaseyear=2000)

* [Sales of various Electric Vehicles (Hybrid, Plug-in Hybrid, Battery) in the U.S.](https://www.bts.gov/content/gasoline-hybrid-and-electric-vehicle-sales)

* [Quarterly US GDP Data](https://fred.stlouisfed.org/series/GDP)

* [Quarterly US GNP Data](https://fred.stlouisfed.org/series/GNP)

* Numbers of Data Centers operating in the U.S. - This ultimately was not added, because it was a pain to find a reliable source for this information.

### Phase III ([Demo Video](https://youtu.be/z0Jt5nhTZUc))

In the last phase of the project, we sought to put all of the tools together that we know so far. The concept would be to ingest data to a databse, use some of that data to train a ML model, deploy said model, and then consume that model and the rest of our data in a Power BI report. In the video, I talk through these steps, and give a few considerations for users of different types to think about before launching into the process. Spoiler: it doesn't totally work for my use case.

Here's a sketch of the idealized pipeline at completion:
<img src="https://github.com/andrewkroening/energy-predictions/blob/f0f5190336b1a03c45a69116363442c6df7406c0/30_intermediate_files/energy_predict_PHIII.png" alt="PhaseI" width="1000"/>

### Phase II ([Demo Video](https://youtu.be/Nh-wG2ZLLAs))

In Phase II, I made some changes to the base dataset. I removed energy consumption and changed the source of the energy generation statistics to a different EIA table. This improved readability and interpretability. I also added sales figures for vehicles with a big battery (battery electric, hybrid, plug-in hybrid). With these new figures, I re-ran our ML experiment using Azure AutoML. The results are captured below. In summary, it looks like the AutoML model (VotingEnsemble) performed very well:


<img src="https://github.com/andrewkroening/energy-predictions/blob/92fd42ca40d5324b1f52e867e34fe71e17b059b0/30_intermediate_files/forecast_perform.png" alt="PhaseI" width="1000"/>

<img src="https://github.com/andrewkroening/energy-predictions/blob/92fd42ca40d5324b1f52e867e34fe71e17b059b0/30_intermediate_files/feature_rank.png" alt="PhaseI" width="1000"/>

### Phase I ([Demo video](https://youtu.be/RkAp5NcK8c4))

In Phase I, I constructed a Machine Learning Workspace in Azure and a repository on GitHub to host the code I use to clean data and test API calls. I determined the API calls need some more work, so I use a [notebook](https://github.com/andrewkroening/energy-predictions/blob/6ef76311342997dc1e8e61baa563a4df174d471d/10_code/data_cleaner.ipynb) to clean data, transform it, and merge into a time series. That data is then uploaded to an Azure storage account and we construct a simple pipeline to test the resources and data. Big surprise: when you include Energy Production as a predictor of Energy Consumption the model is *really* accurate.

Here's a drawing to illustrate what Phase I accomplished:
<img src="https://github.com/andrewkroening/energy-predictions/blob/6ef76311342997dc1e8e61baa563a4df174d471d/30_intermediate_files/energy_predict_ph1.png" alt="PhaseI" width="1000"/>
