# -*- coding: utf-8 -*-

from collections import Counter
from math import pi
import numpy as np
import pandas as pd
import querys
import database
from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, DataTable, RangeTool, TableColumn
from bokeh.palettes import Spectral11
from bokeh.plotting import figure
from bokeh.transform import cumsum
from bokeh.models.widgets import Slider, Select, TextInput, RadioButtonGroup, MultiSelect, RangeSlider, CheckboxButtonGroup
from bokeh.sampledata.autompg2 import autompg2 as mpg
from bokeh.sampledata.stocks import AAPL
from bokeh.models.widgets import Slider, Select, TextInput


def my_text_input_handler(attr, old, new):
    print("Previous label: " + old)
    print("Updated label: " + new)


def read_default_filter():
    db = database.db.cursor()

    db.execute(querys.server_names)
    server_names = [x[0] for x in db.fetchall()]

    db.execute(querys.years)
    year_select = [x[0] for x in db.fetchall()]

    month_select = querys.month
    day_week_select = querys.day_week

    db.close()
    return {
        'server_names': server_names,
        'year-start': year_select[0],
        'year-end': year_select[-1],
        'month': month_select,
        'day_week': day_week_select
        }


"""
Cria os filtros

options{
    server_names: list of strings,
    year-start: int,
    year-end: int,
    month: list of strings,
    day_week: list of strings
}
"""
def build_filter_controls(options):
    server_names = options['server_names']
    server_select = RadioButtonGroup(
        labels=server_names, active=0)

    year_select = RangeSlider(
        start=options['year-start'],
        end=options['year-end'],
        value=(options['year-start'], options['year-end']),
        step=1)#, title="Year")

    month_select = MultiSelect(
        title="Month:",
        value=['0'],
        options=options['month'])

    day_select = RangeSlider(
        start=1,
        end=31,
        value=(1, 31),
        step=1)###, title="Day")

    day_week_select = CheckboxButtonGroup(#title='Dia da semana',
        labels=options['day_week'])#,
        #active=[i for i in range(len(options['day_week']))])

    time_select = RangeSlider(start=0, end=24, value=(0,24), step=1, title="Period")

    scale_select =  RadioButtonGroup(labels=querys.scale, active=0)


    def select_data():
        print('data select')
        server_name = server_names[server_select.active]
        months = month_select.value
        days = day_select.value
        day_week = day_week_select.active
        years = year_select.value
        time = time_select.value
        scale = querys.scale_str[scale_select.active]
        
        db = database.db
        
        sql = build_query(server_name, scale, years, months, days, day_week, time)
        print(sql)
        #

        return pd.io.sql.read_sql(sql, db)


    return [server_select, scale_select, year_select, month_select, day_select,
            day_week_select, time_select], select_data



def build_query(server_name, scale, years, months, days, week_day, time_period):
    if('0' in months):
        months = [str(x) for x in range(1, 13)]

    if(days[0] == days[1]):
        days = [str(days[0])]
    else:
        days = [str(day) for day in range(days[0], days[1]+1)]
        
    if(years[0] == years[1]):
        years = [str(years[0])]
    else:
        years = [str(year) for year in range(years[0], years[1]+1)]    
        
#    import pdb; pdb.set_trace()
    if(week_day == []):
        week_day = [str(day) for day in range(1,8)]
    else:
        week_day = [str(day) for day in week_day]

    return ' AND '.join([querys.filter_basic.format(scale, server_name),
                         querys.filter_years.format(','.join([str(x) for x in years])),
                         querys.filter_months.format(','.join(months)),
                         querys.filter_days.format(','.join(days)),
                         querys.filter_week_day.format(','.join(
                             week_day)),#[str(querys.day_week.index(x)) for x in week_day])),
                         querys.filter_time_period.format(time_period[0], time_period[1])]) + ' ' +  querys.order
