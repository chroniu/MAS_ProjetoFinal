# -*- coding: utf-8 -*-

from os.path import dirname, join

import numpy as np
import pandas.io.sql as psql
import filters
from bokeh.plotting import figure
from bokeh.layouts import layout, widgetbox
from bokeh.models import ColumnDataSource, Div
from bokeh.models.widgets import Slider, Select, TextInput, RadioButtonGroup, MultiSelect, RangeSlider, CheckboxButtonGroup
from bokeh.io import curdoc
from bokeh.sampledata.movies_data import movie_path

#conn = sql.connect(movie_path)
#query = open(join(dirname(__file__), 'query.sql')).read()
#movies = psql.read_sql(query, conn)

axis_map = {
#    "Tomato Meter": "Meter",
#    "Numeric Rating": "numericRating",
#    "Number of Reviews": "Reviews",
#    "Box Office (dollars)": "BoxOffice",
#    "Length (minutes)": "Runtime",
#    "Year": "Year",
}

desc = Div(text=open(join(dirname(__file__), "description.html")).read(), width=800)


source = ColumnDataSource(data=dict(date=dates, close=AAPL['adj_close']))

x = np.linspace(0, 10, 500)
y = np.sin(x)

source = ColumnDataSource(data=dict(x=x, y=y))

plot = figure(y_range=(-10, 10), plot_width=400, plot_height=400)

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

source = ColumnDataSource(data=dict(date=[], us_max=[]))


controls, select_data = filters.build_filter_controls(filters.read_default_filter())

def update():
    df = select_data()
    print("len(df)", len(df))
    print(df.head())

#    x_name = axis_map[x_axis.value]
#    y_name = axis_map[y_axis.value]#

#    p.xaxis.axis_label = x_axis.value
#    p.yaxis.axis_label = y_axis.value
#    p.title.text = "%d movies selected" % len(df)
#    source.data = dict(
#        x=df[x_name],
#        y=df[y_name],
#        color=df["color"],
#        title=df["Title"],
#        year=df["Year"],
#        revenue=df["revenue"],
#        alpha=df["alpha"],
#   )

for control in controls:
    if type(control) in [RadioButtonGroup, CheckboxButtonGroup]:
        control.on_change('active', lambda attr, old, new: update())
    else:
        control.on_change('value', lambda attr, old, new: update())

sizing_mode = 'fixed'  # 'scale_width' also looks nice with this example

inputs = widgetbox(*controls, sizing_mode=sizing_mode)
l = layout([
    [desc],
    [p, inputs],#[inputs, p],
], sizing_mode=sizing_mode)

update()  # initial load of the data

curdoc().add_root(l)
curdoc().title = "MAS"
