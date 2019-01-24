from bokeh.io import output_notebook, show, output_file, curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider, Select
from bokeh.plotting import figure
from numpy.random import random, normal, lognormal
import pandas as pd

# bokeh app structure
# create plots and widgets

# add callbacks

# arrange plots and widgets into laiyouts

# call curdoc().add_root(layout)

# execute with
# bokeh serve --show myapp.py

# for more complex structure
# bokeh serve --show myappdir/


# curdoc().add_root(plot)

'''
# simple plot with slider
N = 300
src = ColumnDataSource(data={'x': random(N), 'y': random(N)})

plot = figure()
plot.circle(x='x', y='y', source=src)

slider = Slider(start=100, end=1000, value=N, step=10, 
                title="Number of Points")


def callback(attr, old, new):
    N = slider.value
    src.data={'x': random(N), 'y': random(N)}

slider.on_change('value', callback)

layout = column(slider, plot)

curdoc().add_root(layout)
'''

# drop down menu
df = pd.read_csv('data/harvard.csv').fillna(0, axis=1)
src = ColumnDataSource(data={'x': df['nevents'], 
                        'y': df['nplay_video']})
# src = ColumnDataSource(data={'x': random(N), 'y': random(N)})

plot = figure()
plot.circle('x', 'y', source=src)

# menu = Select(options=['nplay_video', 'nforum_posts'],
#                 value='nplay_video', title='Y Variable')


# def callback(attr, old, new):
#     if new == 'nplay_video': 
#         src.data = {'x': df['nevents'], 'y': df['nplay_video']}
#     # elif menu.value == 'normal': 
#     #     f = normal
#     else: 
#         src.data = {'x': df['nevents'], 'y': df['nforum_posts']}

# menu.on_change('value', callback)

layout = column(plot)

curdoc().add_root(plot)
