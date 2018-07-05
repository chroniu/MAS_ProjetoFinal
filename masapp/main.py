# -*- coding: utf-8 -*-
from os.path import dirname, join
import numpy as np
import pandas.io.sql as psql
import filters
from bokeh.plotting import figure
from bokeh.palettes import Spectral6, YlOrRd6, Spectral3
from bokeh.layouts import layout, widgetbox, column, row
from bokeh.models import ColumnDataSource, Div, RangeTool, HoverTool
from bokeh.models.ranges import Range1d
from bokeh.models.widgets import Slider, Select, TextInput, RadioButtonGroup, MultiSelect, RangeSlider, CheckboxButtonGroup, Button, DataTable, TableColumn, NumberFormatter, DateFormatter
from bokeh.io import curdoc
from bokeh.sampledata.movies_data import movie_path

def update():
    def update_range(range_, min_, max_):
        range_.start = min_
        range_.end = max_
        range_.reset_start = None
        range_.reset_end = None

    df = select_data()
    print("len(df)", len(df))
    #print(df.head())
    df['date'] = df['date'].astype(np.datetime64)

    if not (len(df) == 0):
        x_start = min(df['date'])
        x_end   = max(df['date'])

        #xs
        update_range(plot_sys.x_range, x_start, x_end)
        #ys
        #update_range(plot_sys.y_range, min(df['sy_max']), max(df['sy_max']))
        #update_range(plot_queue.y_range, min(df['r_max']), max(df['r_max']))



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


def add_plot_lines(plot_figure, source, plot_sources, pallet):
    for val, color in zip(plot_sources, pallet):
        plot_figure.line('date', val, source=source, color=color, line_width=2, alpha=0.7, legend=val)
        plot_figure.circle('date', val, source=source, color=color, line_width=2, alpha=0.7, legend=val)

    plot_figure.legend.location = "bottom_left"
    plot_figure.legend.click_policy="hide"


plot_sources = ['sy_max', 'sy_p90', 'sy_avg', 'r_max', 'r_p90', 'r_avg']

tooltips=[
        ("data", "@date{%F}"),
        ("(sy_max, sy_avg, sy_90)", "(@sy_max, @sy_avg, @sy_p90)"),
        ("(r_max, r_avg, r_p90)", "(@r_max, @r_avg, @r_p90)")
    ]

tools = ['save']#, 'wheel_zoom', 'box_zoom', 'reset']

print("loaded")
controls, select_data = filters.build_filter_controls(filters.read_default_filter())
for control in controls:
    if type(control) in [RadioButtonGroup, CheckboxButtonGroup]:
        control.on_change('active', lambda attr, old, new: update())
    else:
        control.on_change('value', lambda attr, old, new: update())


source = ColumnDataSource(data=dict(date=[], us_max=[] ))

#plots  sys
plot_sys = figure(plot_height=300, toolbar_location="right", #name="line",
           x_axis_type="datetime", x_range= Range1d(), y_range=Range1d(start=0, end=1.1), sizing_mode="scale_width",
           tools=tools, title="Sys")
plot_sys.add_tools(HoverTool(show_arrow=False, line_policy='next', tooltips=tooltips, formatters={'date':'datetime'}))
add_plot_lines(plot_sys, source, plot_sources[0:4], Spectral3)
plot_sys.yaxis.axis_label = 'sys'
plot_sys.background_fill_color="#f5f5f5"
plot_sys.grid.grid_line_color="white"

#plot fila
plot_queue = figure(plot_height=300,  toolbar_location="right", #name="line",
           x_axis_type="datetime", x_range=plot_sys.x_range, sizing_mode="scale_width",
           tools=tools, title="Queue")
plot_queue.add_tools(HoverTool(show_arrow=False, line_policy='next', tooltips=tooltips, formatters={'date':'datetime'}))
add_plot_lines(plot_queue, source, plot_sources[3:], Spectral3)
plot_queue.yaxis.axis_label = 'r'
plot_queue.background_fill_color="#f5f5f5"
plot_queue.grid.grid_line_color="white"


# plot seletor
select = figure(plot_height=320, y_range=plot_queue.y_range, sizing_mode="scale_width",
                x_axis_type="datetime", y_axis_type=None,
                toolbar_location="right", tools=tools)
select
range_rool = RangeTool(x_range=plot_sys.x_range)
range_rool.overlay.fill_color = "navy"
range_rool.overlay.fill_alpha = 0.2

#select.line('date', 'sy_max', source=source)
add_plot_lines(select, source, plot_sources, Spectral6)
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
data_table = DataTable(source=source, columns=columns, sizing_mode="stretch_both")
table = widgetbox(data_table)

inputs = widgetbox(*controls, sizing_mode='scale_width')
inputs.name="inputs"
plots = row(plot_sys, plot_queue,  sizing_mode='scale_width')
plots.name = "plots"

#input_row = row(inputs,  sizing_mode='scale_both')
#input_row.name = "inputs"

selector = select
selector.name = "selector"
data_table.name = "table"

update()  # initial load of the data
curdoc().title = "MAS Dashboard"
curdoc().add_root(selector)
curdoc().add_root(inputs)
curdoc().add_root(plots)
curdoc().add_root(data_table)
curdoc().title = "MAS"
