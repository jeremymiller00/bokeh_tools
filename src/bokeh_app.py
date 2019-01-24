from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider, Select
from bokeh.plotting import figure
from numpy.random import random, normal, lognormal

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
N = 300
src = ColumnDataSource(data={'x': random(N), 'y': random(N)})

plot = figure()
plot.circle(x='x', y='y', source=src)

menu = Select(options=['uniform', 'normal', 'lognormal'],
                value='uniform', title='Distribution')


def callback(attr, old, new):
    if menu.value == 'uniform': 
        f = random
    elif menu.value == 'normal': 
        f = normal
    else: 
        f = lognormal
    src.data={'x':f(size=N), 'y':f(size=N)}

menu.on_change('value', callback)

layout = column(menu, plot)

curdoc().add_root(layout)
