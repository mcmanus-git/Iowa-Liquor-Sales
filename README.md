# Iowa Liquor Sales
This repository is code for the 
[Plotly Dash Autumn App Challenge](https://community.plotly.com/t/autumn-community-app-challenge/66996) 
which ran from August 29, 2022 (date original dataset was altered), through October 2, 2022. 


## How the Winners of the App Challenge Were Decided:  

>  ***The winning apps will be judged according to the following categories:***  
> App creativity  
> App design  
> Data exploration  
> Data science or data analysis routines (eg numerical methods, machine learning, prediction, classification, optimization) [[1]](https://community.plotly.com/t/autumn-community-app-challenge/66996)  
> 


## Data
The raw dataset provided by the community can be
found [here](https://raw.githubusercontent.com/plotly/datasets/master/liquor_iowa_2021.csv).  
- [Iowa Liquor Sales | 2021 | 2.6 million rows](https://www.kaggle.com/datasets/tantable/iowa-liquor-sales-2021-v-interesting-26m-rows?sort=published)  
- [Iowa Liquor Sales | 2012-2017 | 12 Million Rows](https://www.kaggle.com/datasets/tantable/iowa-liquor-sales-2021-v-interesting-26m-rows?sort=published)  
- [Full Dataset Accessed via API](https://data.iowa.gov/Sales-Distribution/Iowa-Liquor-Sales/m3tr-qhgy)  

### Metadata from the Raw Data 

| name                               | dataTypeName  | description                                                                                                                                                                                                   | fieldName                   |
|------------------------------------|---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------|
| Invoice/Item Number                | text          | Concatenated invoice and line number   associated with the liquor order.  This   provides a unique identifier for the individual liquor products included in   the store order                                | invoice_line_no             |
| Date                               | calendar_date | Date of order                                                                                                                                                                                                 | date                        |
| Store Number                       | text          | Unique number assigned to the store who ordered the liquor.                                                                                                                                                   | store                       |
| Store Name                         | text          | Name of store who ordered the liquor.                                                                                                                                                                         | name                        |
| Address                            | text          | Address of store who ordered the liquor.                                                                                                                                                                      | address                     |
| City                               | text          | City where the store who ordered the liquor is located                                                                                                                                                        | city                        |
| Zip Code                           | text          | Zip code where the store who ordered the liquor is located                                                                                                                                                    | zipcode                     |
| Store Location                     | point         | Location of store who ordered the liquor.    The Address, City, State and Zip Code are geocoded to provide   geographic coordinates.  Accuracy of   geocoding is dependent on how well the address is inte... | store_location              |
| County Number                      | text          | Iowa county number for the county where store who ordered the liquor is   located\n                                                                                                                           | county_number               |
| County                             | text          | County where the store who ordered the liquor is located\n                                                                                                                                                    | county                      |
| Category                           | text          | Category code associated with the liquor ordered                                                                                                                                                              | category                    |
| Category Name                      | text          | Category of the liquor ordered.                                                                                                                                                                               | category_name               |
| Vendor Number                      | text          | The vendor number of the company for the brand of liquor ordered                                                                                                                                              | vendor_no                   |
| Vendor Name                        | text          | The vendor name of the company for the brand of liquor ordered                                                                                                                                                | vendor_name                 |
| Item Number                        | text          | Item number for the individual liquor product ordered.                                                                                                                                                        | itemno                      |
| Item Description                   | text          | Description of the individual liquor product ordered.                                                                                                                                                         | im_desc                     |
| Pack                               | number        | The number of bottles in a case for the liquor ordered                                                                                                                                                        | pack                        |
| Bottle Volume (ml)                 | number        | Volume of each liquor bottle ordered in milliliters.                                                                                                                                                          | bottle_volume_ml            |
| State Bottle Cost                  | number        | The amount that Alcoholic Beverages Division paid for each bottle of   liquor ordered                                                                                                                         | state_bottle_cost           |
| State Bottle Retail                | number        | The amount the store paid for each bottle of liquor ordered                                                                                                                                                   | state_bottle_retail         |
| Bottles Sold                       | number        | The number of bottles of liquor ordered by the store                                                                                                                                                          | sale_bottles                |
| Sale (Dollars)                     | number        | Total cost of liquor order (number of bottles multiplied by the state   bottle retail)                                                                                                                        | sale_dollars                |
| Volume Sold (Liters)               | number        | Total volume of liquor ordered in liters.    (i.e. (Bottle Volume (ml) x Bottles Sold)/1,000)                                                                                                                 | sale_liters                 |
| Volume Sold (Gallons)              | number        | Total volume of liquor ordered in gallons. (i.e. (Bottle Volume (ml) x   Bottles Sold)/3785.411784)                                                                                                           | sale_gallons                |


If you haven't heard of it, try out 
[tablesgenerator.com/markdown_tables](https://www.tablesgenerator.com/markdown_tables) that allows you to copy and 
paste tables, from Excel for example, into the tool which generates a markdown version of your table. Great time saver!




