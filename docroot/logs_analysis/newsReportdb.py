#! python3

import psycopg2
from prettytable import PrettyTable, from_db_cursor

try:

    # connect to the database 
    DBNAME = "news"
    db = psycopg2.connect(database=DBNAME)
    # create a cursor to use with the database
    cursor = db.cursor()
    #----------------------------------------------------------------------------------------

    # check if view for problem1 exists
    cursor.execute("select * from information_schema.tables where table_name=%s", ('problem1',))
    problemOneViewExists = bool(cursor.rowcount)

    #  1. What are the most popular three articles of all time?
    #     Which articles have been accessed the most?
    #     Present this information as a sorted list with the most popular article at the top.
    if problemOneViewExists:
        with db:
            cur = db.cursor()
            cur.execute("""Select title, views from problem1;""")
            onerow = cur.fetchall()
    else:
        with db:
            cur = db.cursor()
            cur.execute( """Create view problem1 as
                            SELECT
                                articles.title,
                                articles.author,
                                count (articles.author) as views
                            FROM
                                public.articles,
                                public.log
                            WHERE
                                log.path != '/' AND
                                Concat('/article/',articles.slug) = log.path
                            GROUP BY
                                articles.title,
                                articles.author,
                                articles.slug,
                                log.path
                            ORDER BY
                                views desc;""")
            cur.execute("""Select title, views from problem1;""")
            onerow = cur.fetchall()

    problemOneTable = PrettyTable(['Title', 'views', ])
    # left justify the title
    problemOneTable.align['Title'] = "l"
    # left justify the views
    problemOneTable.align['views'] = "l"

    for record in onerow:
        problemOneTable.add_row(record)

    print(problemOneTable)
    print("")
    #----------------------------------------------------------------------------------------

    # 2. Who are the most popular article authors of all time?
    # That is, when you sum up all of the articles each author has written,
    # which authors get the most page views?
    # Present this as a sorted list with the most popular author at the top.

    cursor.execute("select * from information_schema.tables where table_name=%s", ('problem2',))
    problemTwoViewExists = bool(cursor.rowcount)

    if problemTwoViewExists:
        with db:
            cur = db.cursor()
            cur.execute("""Select Name, sum from problem2;""")
            oneRowProblemTwo = cur.fetchall()
    else:
        with db:
            cur = db.cursor()
            cur.execute( """Create view problem2 as
                            SELECT
                                authors.name,
                                sum(problem1.views)
                            FROM
                                authors,
                                problem1
                            WHERE
                                problem1.author = authors.id
                            Group By
                                authors.name
                            ORDER By
                                sum desc;""")
            cur.execute("""Select Name, sum from problem2;""")
            oneRowProblemTwo = cur.fetchall()


    problemTwoTable = PrettyTable(['Author', 'Total Views', ])
    # left justify the title
    problemTwoTable.align['Author'] = "l"
    # left justify the views
    problemTwoTable.align['views'] = "l"

    for record in oneRowProblemTwo:
        problemTwoTable.add_row(record)

    print(problemTwoTable)
    print("")
    #----------------------------------------------------------------------------------------


    # 3. On which days did more than 1% of requests lead to errors?
    #    The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser.
    #    (Refer to this lesson for more information about the idea of HTTP status codes.)

    cursor.execute("select * from information_schema.tables where table_name=%s", ('errorperday',))
    problemThreeOneViewExists = bool(cursor.rowcount)
    if problemThreeOneViewExists:
        with db:
            cur = db.cursor()
            cur.execute("""Select * from errorperday;""")
            Problem3_1 = cur.fetchall()
    else:
        with db:
            cur = db.cursor()
            cur.execute( """create view errorperday as
                            select
                                subq.time,
                                count(subq.time)
                            from
                            (
                                select
                                    id,
                                    cast ((log.time) as DATE),
                                    count(Date(log.time))
                                from
                                    log
                                where
                                    log.status = '404 NOT FOUND'
                                Group By
                                    log.id,
                                    log.time
                                order by
                                    log.time) as subq
                            group by
                                subq.time
                            order by
                                subq.time;""")
            cur.execute("""Select * from errorperday;""")
    #         Problem3_1 = cur.fetchall()

    # ErrorPerDayTable = PrettyTable(['Time', 'requests w/Errors'])

    # # left justify the Time
    # ErrorPerDayTable.align['Time'] = "l"
    # # left justify the requests w/Errors
    # ErrorPerDayTable.align['requests w/Errors'] = "l"

    # for record in Problem3_1:
    #     ErrorPerDayTable.add_row(record)

    # print(ErrorPerDayTable)
    # print("")


    cursor.execute("select * from information_schema.tables where table_name=%s", ('requestsperday',))
    problemThreeTwoViewExists = bool(cursor.rowcount)
    if problemThreeTwoViewExists:
        with db:
            cur = db.cursor()
            cur.execute("""Select * from requestsperday;""")
            Problem3_2 = cur.fetchall()
    else:
        with db:
            cur = db.cursor()
            cur.execute( """create view requestsperday as
                            select
                                subq.time,
                                count(subq.time)
                            from
                            (
                                select
                                    id,
                                    cast ((log.time) as DATE),
                                    count(Date(log.time))
                                from
                                    log
                                Group By
                                    log.id,
                                    log.time
                                order by
                                    log.time) as subq
                            group by
                                subq.time
                            order by
                                subq.time;""")
            cur.execute("""Select * from requestsperday;""")
    #         Problem3_2 = cur.fetchall()

    # RequestsPerDayTable = PrettyTable(['Time', 'requests'])

    # # left justify the Time
    # RequestsPerDayTable.align['Time'] = "l"
    # # left justify the requests w/Errors
    # RequestsPerDayTable.align['requests'] = "l"

    # for record in Problem3_2:
    #     RequestsPerDayTable.add_row(record)

    # print(RequestsPerDayTable)
    # print("")

    cur = db.cursor()
    cur.execute("""select
                        errorPerDay.Time,
                        errorPerDay.count,
                        RequestsPerDay.count,
                        (cast(errorPerDay.count AS DOUBLE PRECISION)/cast(RequestsPerDay.count AS DOUBLE PRECISION )*100)
                    from
                        errorperday,
                        requestsperday
                    where
                        errorPerDay.time = RequestsPerDay.time 
                    group by
                        errorPerDay.time,
                        errorPerDay.count,
                        RequestsPerDay.count
                    having
                        (cast(errorPerDay.count AS DOUBLE PRECISION)
                        /cast(RequestsPerDay.count AS DOUBLE PRECISION ))
                            >= cast(0.01 AS DOUBLE PRECISION) """)
    problem3_3 = cur.fetchall()

    ExceededErrorTable = PrettyTable(['date','Errors', 'requests', 'percent Error'])
    for record in problem3_3:
        ExceededErrorTable.add_row(record)

    print(ExceededErrorTable)
    print("")

    db.close()

except:
    db.close()