# News Reporting information for Udacity course

- [News Reporting information for Udacity course](#news-reporting-information-for-udacity-course)
  - [objectives](#objectives)
  - [how to login to psql](#how-to-login-to-psql)
  - [dependencies](#dependencies)
  - [List of relations between tables](#list-of-relations-between-tables)
  - [Articles Table](#articles-table)
  - [Authors Table](#authors-table)
  - [Log Table](#log-table)
  - [example table data](#example-table-data)
    - [Articles table data](#articles-table-data)
    - [Authors Table data](#authors-table-data)
    - [Log Table Snippet of data](#log-table-snippet-of-data)

## objectives

    1. What are the most popular three articles of all time?
    Which articles have been accessed the most?
    Present this information as a sorted list with the most popular article at the top.

    Example:

    "Princess Shellfish Marries Prince Handsome" — 1201 views
    "Baltimore Ravens Defeat Rhode Island Shoggoths" — 915 views
    "Political Scandal Ends In Political Scandal" — 553 views

    2. Who are the most popular article authors of all time?
    That is, when you sum up all of the articles each author has written, which authors get the most page views?
    Present this as a sorted list with the most popular author at the top.

    Example:

    Ursula La Multa — 2304 views
    Rudolf von Treppenwitz — 1985 views
    Markoff Chaney — 1723 views
    Anonymous Contributor — 1023 views

    3. On which days did more than 1% of requests lead to errors?
    The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser.
    (Refer to this lesson for more information about the idea of HTTP status codes.)

    Example:

    July 29, 2016 — 2.5% errors

## how to login to psql

    psql -U vagrant -W news
    password: vagrant

## dependencies

    1. psycopg2 - install using:     `pip install psycopg2 --user`
    2. prettytable - install using:  `pip install prettytable --user`

## List of relations between tables

|Schema  |   Name   | Type  |  Owner
|:-------|:---------|:------|:----------
| public | articles | table | vagrant
| public | authors  | table | vagrant
| public | log      | table | vagrant

## Articles Table

| Column |           Type           | Nullable |               Default
|--------|:-------------------------|---------:|:--------------------------------------
| author | integer                  | not null |
| title  | text                     | not null |
| slug   | text                     | not null |
| lead   | text                     |          |
| body   | text                     |          |
| time   | timestamp with time zone |          | now()
| id     | integer                  | not null | nextval('articles_id_seq'::regclass)

|Indexes
|:------
|    "articles_pkey" PRIMARY KEY, btree (id)
|    "articles_slug_key" UNIQUE CONSTRAINT, btree (slug)
|Foreign-key constraints:
|    "articles_author_fkey" FOREIGN KEY (author) REFERENCES authors(id)

## Authors Table

| Column |  Type   | Nullable |               Default
|--------|:--------|:---------|:-------------------------------------
| name   | text    | not null |
| bio    | text    |          |
| id     | integer | not null | nextval('authors_id_seq'::regclass)

|Indexes:
|:------
|    "authors_pkey" PRIMARY KEY, btree (id)
|Referenced by:
|    TABLE "articles" CONSTRAINT "articles_author_fkey" FOREIGN KEY (author) REFERENCES authors(id)

## Log Table

| Column |           Type           |  Nullable |             Default
|--------|--------------------------|----------|---------------------------------
| path   | text                     |          |
| ip     | inet                     |          |
| method | text                     |          |
| status | text                     |          |
| time   | timestamp with time zone |          | now()
| id     | integer                  | not null | nextval('log_id_seq'::regclass)

|Indexes:
|:-------
|    "log_pkey" PRIMARY KEY, btree (id)

## example table data

### Articles table data

  | author |               title                |            slug           |               time               | id |
  |--------|------------------------------------|---------------------------|----------------------------------|----|
  |   3    |  Bad things gone, say good people  |      bad-things-gone      | 2016-08-15 11:55:10.814316-07:00 | 23 |
  |   4    |        Balloon goons doomed        |    balloon-goons-doomed   | 2016-08-15 11:55:10.814316-07:00 | 24 |
  |   1    |  Bears love berries, alleges bear  |     bears-love-berries    | 2016-08-15 11:55:10.814316-07:00 | 25 |
  |   2    |  Candidate is jerk, alleges rival  |     candidate-is-jerk     | 2016-08-15 11:55:10.814316-07:00 | 26 |
  |   1    |      Goats eat Google's lawn       |     goats-eat-googles     | 2016-08-15 11:55:10.814316-07:00 | 27 |
  |   1    |     Media obsessed with bears      | media-obsessed-with-bears | 2016-08-15 11:55:10.814316-07:00 | 28 |
  |   2    | Trouble for troubled troublemakers |    trouble-for-troubled   | 2016-08-15 11:55:10.814316-07:00 | 30 |
  |   1    |      There are a lot of bears      |       so-many-bears       | 2016-08-15 11:55:10.814316-07:00 | 29 |

### Authors Table data

|          name          |                                                bio                                                 | id |
|------------------------|----------------------------------------------------------------------------------------------------|----|
|    Ursula La Multa     |            Ursula La Multa is an expert on bears, bear abundance, and bear accessories.            | 1  |
| Rudolf von Treppenwitz | Rudolf von Treppenwitz is a nonprofitable disorganizer specializing in procrastinatory operations. | 2  |
| Anonymous Contributor  |                    Anonymous Contributor's parents had unusual taste in names.                     | 3  |
|     Markoff Chaney     |                         Markoff Chaney is the product of random genetics.                          | 4  |

### Log Table Snippet of data

|                 path                |       ip       | method |     status    |            time           |    id   |
|-------------------------------------|----------------|--------|---------------|---------------------------|---------|
|                  /                  | 198.51.100.195 |  GET   |     200 OK    | 2016-07-01 01:00:00-06:00 | 1678923 |
|      /article/candidate-is-jerk     | 198.51.100.195 |  GET   |     200 OK    | 2016-07-01 01:00:47-06:00 | 1678924 |
|      /article/goats-eat-googles     | 198.51.100.195 |  GET   |     200 OK    | 2016-07-01 01:00:34-06:00 | 1678925 |
|      /article/goats-eat-googles     | 198.51.100.195 |  GET   |     200 OK    | 2016-07-01 01:00:52-06:00 | 1678926 |
|    /article/balloon-goons-doomed    | 198.51.100.195 |  GET   |     200 OK    | 2016-07-01 01:00:23-06:00 | 1678927 |
|                  /                  |  192.0.2.194   |  GET   |     200 OK    | 2016-07-01 01:00:05-06:00 | 1678928 |
|      /article/candidate-is-jerk     |  192.0.2.194   |  GET   |     200 OK    | 2016-07-01 01:00:54-06:00 | 1678929 |
|       /article/so-many-bearsb       | 198.51.100.194 |  GET   | 404 NOT FOUND | 2016-07-01 01:07:54-06:00 | 1679180 |
|                  /                  |   192.0.2.80   |  GET   |     200 OK    | 2016-07-01 01:00:15-06:00 | 1678930 |