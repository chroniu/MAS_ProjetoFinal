# -*- coding: utf-8 -*-

from os.path import dirname, join

import numpy as np
import pandas.io.sql as psql
import filters
from bokeh.plotting import figure
from bokeh.layouts import layout, widgetbox, column
from bokeh.models import ColumnDataSource, Div, RangeTool
from bokeh.models.ranges import Range1d
from bokeh.models.widgets import Slider, Select, TextInput, RadioButtonGroup, MultiSelect, RangeSlider, CheckboxButtonGroup, Button, DataTable, TableColumn, NumberFormatter, DateFormatter
from bokeh.io import curdoc
from bokeh.sampledata.movies_data import movie_path

#conn = sql.connect(movie_path)
#query = open(join(dirname(__file__), 'query.sql')).read()
#movies = psql.read_sql(query, conn)

def update():
    df = select_data()
    print("len(df)", len(df))
    #print(df.head())
    df['date'] = df['date'].astype(np.datetime64)

    if not (len(df) == 0):
        x_start = min(df['date'])
        x_end   = max(df['date'])
        y_start = min(df['r_max'])
        y_end   = max(df['r_max'])
        
        p.x_range.start = x_start
        p.x_range.end   = x_end
        p.x_range.reset_start = None
        p.x_range.reset_end = None

    source.data = dict(
        date=df['date'],
        r_max=df['r_max'],
        r_avg=df['r_avg'],
        r_p90=df['r_p90'],
        us_max=df['us_max'],
        us_avg=df['us_avg'],
        us_p90=df['us_p90'],
        sy_max=df['sy_max'],
        sy_avg=df['sy_avg'],
        sy_p90=df['sy_p90'],
        id_max=df['id_max'],
        id_avg=df['id_avg'],
        id_p90=df['id_p90'],
    )

    
print("loaded")

desc = Div(text=open(join(dirname(__file__), "description.html")).read(), width=800)

controls, select_data = filters.build_filter_controls(filters.read_default_filter())
for control in controls:
    if type(control) in [RadioButtonGroup, CheckboxButtonGroup]:
        control.on_change('active', lambda attr, old, new: update())
    else:
        control.on_change('value', lambda attr, old, new: update())


source = ColumnDataSource(data=dict(date=[], us_max=[] ))

#plots 
p = figure(plot_height=110, tools="", toolbar_location=None, #name="line",
           x_axis_type="datetime", x_range= Range1d(), sizing_mode="scale_width")

p.line('date', 'sy_max', source=source, line_width=2, alpha=0.7)
p.yaxis.axis_label = 'sy_max'
p.background_fill_color="#f5f5f5"
p.grid.grid_line_color="white"

select = figure(plot_height=110, y_range=p.y_range,
                x_axis_type="datetime", y_axis_type=None,
                tools="", toolbar_location=None, sizing_mode="scale_width")

range_rool = RangeTool(x_range=p.x_range)
range_rool.overlay.fill_color = "navy"
range_rool.overlay.fill_alpha = 0.2

select.line('date', 'sy_max', source=source)
select.ygrid.grid_line_color = None
select.add_tools(range_rool)
select.toolbar.active_multi = range_rool
select.background_fill_color="#f5f5f5"
select.grid.grid_line_color="white"
select.x_range.range_padding = 0.01

# define a tabela
columns = [
    TableColumn(field="date", title="Data" , formatter=DateFormatter()),#format="%%Y/%m/%d %H")
    TableColumn(field="r_max", title="r_max", formatter=NumberFormatter(format="0.000")),
    TableColumn(field="r_avg", title="r_avg", formatter=NumberFormatter(format="0.000")),
    TableColumn(field="r_p90", title="r_p90", formatter=NumberFormatter(format="0.000")),
    TableColumn(field="us_max", title="us_max", formatter=NumberFormatter(format="0.000")),
    TableColumn(field="us_avg", title="us_avg", formatter=NumberFormatter(format="0.000")),
    TableColumn(field="us_p90", title="us_p90", formatter=NumberFormatter(format="0.000")),
    TableColumn(field="sy_max", title="sy_max", formatter=NumberFormatter(format="0.000")),
    TableColumn(field="sy_avg", title="sy_avg", formatter=NumberFormatter(format="0.000")),
    TableColumn(field="sy_p90", title="sy_p90", formatter=NumberFormatter(format="0.000")),
    TableColumn(field="id_max", title="id_max", formatter=NumberFormatter(format="0.000")),
    TableColumn(field="id_avg", title="id_avg", formatter=NumberFormatter(format="0.000")),
    TableColumn(field="id_p90", title="id_p90", formatter=NumberFormatter(format="0.000"))
]
data_table = DataTable(source=source, columns=columns)#, width=800)
table = widgetbox(data_table)


sizing_mode = 'fixed'  # 'scale_width' also looks nice with this example

inputs = widgetbox(*controls, sizing_mode=sizing_mode)
l = layout([
    [desc],
    [column(select, p), inputs],
    [table]
], sizing_mode=sizing_mode)

update()  # initial load of the data
curdoc().add_root(l)
curdoc().title = "MAS"
