# Logs
Logs is a simple script for testing against the news database. It answers three common questions:
- What are the three most popular articles?
- What are the three most popular authors?
- What days had a request error percent over 1%?


# Installation
Logs was made to query against the news database, it can be setup in a few steps.
The data in the news database can be [downloaded here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). 
The news database was setup using PostgreSQL:
```
psql -d news -f newsdata.sql
```
Clone the GitHub repository into the same directory as the news database. Logs is dependent on psycopg2 to connect to the database.
```
git clone https://github.com/ch4nc3l0/news_log_script.git
pip install psycopg2
```


# Usage
Their is no configuration for logs, the following example will get the intended output from the command line.
```
python logs.py
```
