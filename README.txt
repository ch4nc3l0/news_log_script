# Logs
Logs is a simple script for testing against the news database. It answers three statistics:
-What are the three most popular articles
-What are the three most popular authors
-What days had a request error percent over 1%.

# Installation
The file should be in the same directory as the news database. Logs is dependent on psycopg2 to connect to the database.
```$ pip install psycopg2```

# Usage
Their is no configuration for logs, the following example will get the intended output from the command line.
```$ python logs.py```