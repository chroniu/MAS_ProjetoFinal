# -*- coding: utf-8 -*-

years = 'SELECT distinct(YEAR(time_min_date)) as years FROM server_statistics ORDER BY years'

server_names = 'SELECT distinct(server) FROM server_statistics'

day_week = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado']

scale = ['mês', 'dia', 'hora']
scale_str = ['%Y-%m', '%Y-%m-%d', '%Y-%m-%d %H']
month = [
    ('0', 'All'),
    ('1', 'Janeiro'),
    ('2', 'Fevereiro'),
    ('3', 'Março'),
    ('4', 'Abril'),
    ('5', 'Maio'),
    ('6', 'Junho'),
    ('7', 'Julho'),
    ('8', 'Agosto'),
    ('9', 'Setembro'),
    ('10','Outubro'),
    ('11','Novembro'),
    ('12','Dezembro')]

filter_basic = ' '.join(["SELECT  date_format(time_min_date, '{}') as date,",
                         'AVG(r_avg)  as r_avg , MAX(r_max)  as r_max,  AVG(r_p90)  as r_p90,',
                         'AVG(us_avg) as us_avg, MAX(us_max) as us_max, AVG(us_p90) as us_p90,',
                         'AVG(sy_avg) as sy_avg, MAX(sy_max) as sy_max, AVG(sy_p90) as sy_p90,',
                         'AVG(id_avg) as id_avg, MAX(id_max) as id_max, AVG(id_p90) as id_p90',
                        'FROM server_statistics',
                        "WHERE server='{}'"])

filter_years = 'YEAR(time_min_date) in ({})'

filter_months = 'MONTH(time_min_date) in ({})'

filter_days = 'DAY(time_min_date) in ({})'

filter_week_day = 'DAYOFWEEK(time_min_date) in ({})'

filter_time_period = 'HOUR(time_min_date) >= {} AND HOUR(time_min_date) <= {}'

order = 'GROUP BY date ORDER BY date ASC LIMIT 100000'