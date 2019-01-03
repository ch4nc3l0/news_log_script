#! /usr/bin/python3.7.1
import psycopg2


# q1: What are the most popular three articles of all time?
def top_three_posts():
    conn = psycopg2.connect('dbname=news')
    print('Querying database for top three posts')
    cur = conn.cursor()
    sql = ('''
        select title, views
        from (select right(path, length(path) - 9) as slug,
        count(path) as views from log
        where status like %s
        and path != %s
        group by slug) as sub
        inner join articles using (slug)
        group by title, views
        order by views desc
        limit 3
        ''')
    sql_variables = ('%200%', '/', )
    cur.execute(sql, sql_variables)
    result = ('Top Three Posts:', cur.fetchall())
    for row in result:
        print(row)
    conn.close()
    print('Connection closed - query complete')


top_three_posts()


# q2: Who are the most popular article authors of all time?
def top_three_authors():
    conn = psycopg2.connect('dbname=news')
    print('Querying database for top three authors')
    cur = conn.cursor()
    sql = ('''
        select name, sum(count) as views
        from (select right(path, length(path) - 9) as slug,
        count(path) as count from log
        where status like %s
        and path != %s
        group by slug) as sub
        inner join articles using (slug)
        inner join authors on (authors.id = author)
        group by name
        order by views desc
        limit 3
        ''')
    sql_variables = ('%200%', '/', )
    cur.execute(sql, sql_variables)
    result = ('Top Three Authors:', cur.fetchall())
    for row in result:
        print(row)
    conn.close()
    print('Connection closed - query complete')


top_three_authors()


# q3: On which days did more than 1% of requests lead to errors?
def error_days():
    conn = psycopg2.connect('dbname=news')
    print('Querying database for days with errors over 1%')
    cur = conn.cursor()
    sql = ('''
        select day, error_percent from(
            select  to_char(date(time), 'Month DD, YYYY') as day,
            cast((cast(count(case when status not like %s then 1 else null end)
            as float) / count(status) * 100)as decimal(5,2)) as error_percent
            from log group by day) as sub
        group by day, error_percent
        having error_percent > 1
        order by day;
        ''')
    sql_variables = ('%200%', )
    cur.execute(sql, sql_variables)
    result = ('Days with errors over 1% :', cur.fetchall())
    for row in result:
        print(row)
    conn.close()
    print('Connection closed - query complete')


error_days()
