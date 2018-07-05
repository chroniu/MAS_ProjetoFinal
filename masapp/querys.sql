years = 'SELECT distinct(YEAR(time_min_date)) as years FROM server_statistics ORDER BY years'

server_names = 'SELECT distinct(server) FROM server_statistics'

day_week = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']

month = [
    (0, 'All'),
    (1, 'Janeiro'),
    (2, 'Fevereiro'),
    (3, 'Março'),
    (4, 'Abril'),
    (5, 'Maio'),
    (6, 'Junho'),
    (7, 'Julho'),
    (8, 'Agosto'),
    (9, 'Setembro'),
    (10,'Outubro'),
    (11,'Novembro'),
    (12,'Dezembro')]


filter_basic = 'SELECT r, r_std, r_max, r_p90,
       st, st_std, st_max, st_p90,
       us, us_std, us_max, us_p90,
       sys, sys_std, sys_max, sys_p90,
       id, id_std, id_max, id_p90
FROM server_statistics
WHERE server={}'

filter_years = 'YEAR(time_min_date) in {}'

filter_months = 'MONTH(time_min_date) in {}'

filter_days = 'DAY(time_min_date) in {}'

filter_week_day = 'DAYOFWEEK(time_min_date) in {}'

filter_time_period = 'HOUR(time_min_date) >= {} AND HOUR(time_min_date) <= {}'
