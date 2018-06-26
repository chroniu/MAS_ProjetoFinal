# -*- coding: utf-8 -*-

years = 'SELECT distinct(YEAR(time_min_date)) as years FROM server_statistics ORDER BY years'

server_names = 'SELECT distinct(server) FROM server_statistics'

day_week = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado']

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


[]

filter_basic = ' '.join(['SELECT time_min_date as date, r_avg, r_max, r_p90,',
                         'us_avg, us_max, us_p90,',
                         'sy_avg, sy_max, sy_p90,',
                         'id_avg, id_max, id_p90',
                        'FROM server_statistics',
                        "WHERE server='{}'"])

filter_years = 'YEAR(time_min_date) in ({})'

filter_months = 'MONTH(time_min_date) in ({})'

filter_days = 'DAY(time_min_date) in ({})'

filter_week_day = 'DAYOFWEEK(time_min_date) in ({})'

filter_time_period = 'HOUR(time_min_date) >= {} AND HOUR(time_min_date) <= {}'

order = 'ORDER BY time_min_date ASC LIMIT 100000'