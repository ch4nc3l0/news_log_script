#! /usr/bin/python3.7.1
import psycopg2


def connect_to_db():
    try:
        conn = psycopg2.connect('dbname=news')
        cur = conn.cursor()
        return conn, cur
    except psycopg2.DatabaseError as error:
        print(error)


def run_query(sql, sql_var, query_name, col_descriptor):
    conn, cur = connect_to_db()
    query = sql
    query_variables = sql_var
    cur.execute(query, query_variables)
    print(query_name)
    result = cur.fetchall()
    for (column1, column2) in result:
        print('{} - {} {}'.format(column1, column2, col_descriptor))
    print('-' * 70)
    conn.close()


# q1: What are the most popular three articles of all time?
def top_three_posts():
    connect_to_db()
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
    query_name = ('Most popular posts:')
    run_query(sql, sql_variables, query_name, 'Views')


# q2: Who are the most popular article authors of all time?
def top_three_authors():
    connect_to_db()
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
    query_name = ('Most popular authors:')
    run_query(sql, sql_variables, query_name, 'Views')


# q3: On which days did more than 1% of requests lead to errors?
def error_days():
    connect_to_db()
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
    query_name = ('Day(s) with error percent over 1%:')
    run_query(sql, sql_variables, query_name, 'Percent')


if __name__ == '__main__':
    top_three_posts()
    top_three_authors()
    error_days()
