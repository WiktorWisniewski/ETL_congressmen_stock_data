# ETL_congressmen_stock_data

This is the project for ETL process of congressmen stock data. It includes architecture design and report created with Dash.

## Architecture

AWS lambda function retrieves daily data from https://housestockwatcher.com/api. The data consists of stock transactions made by us congress members. These transactions are transformed from json file into csv table and loaded into s3 bucket and then with use of copy command is loaded into redshift serverless data warehouse. To create a report data is extrated from redshift to local instance and with Dash is created analytics report.

<img width="653" alt="Zrzut ekranu 2023-12-9 o 13 19 19" src="https://github.com/WiktorWisniewski/ETL_congressmen_stock_data/assets/73825405/7d905712-1b93-4a43-be98-1bb180c63d80">

Table in redshift was created by table_redshift.sql code in redshift serverless query window. 

Follow these aws documentiantion steps of setting up cloud infrastructure to run this code: https://repost.aws/knowledge-center/redshift-lambda-function-queries.



## Report

With the help of dash an analytics report can be created. Before accessing data you need to make your cluster available, see official aws documentation https://repost.aws/knowledge-center/redshift-cluster-private-public. Analyzing and ma

<img width="1726" alt="Zrzut ekranu 2023-12-9 o 13 23 04" src="https://github.com/WiktorWisniewski/ETL_congressmen_stock_data/assets/73825405/8b31318a-ed62-4d4d-9359-a0570b889b84">

