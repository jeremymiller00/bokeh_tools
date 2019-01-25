# Perform necessary imports
import pandas as pd
from bokeh.io import output_file, show, curdoc
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool

df = pd.read_csv('data/gapminder_tidy.csv')


# make basic plot
# Make the ColumnDataSource: source
# src = ColumnDataSource(data={
#     'x'       : df[df['Year'] == 1970]['fertility'],
#     'y'       : df[df['Year'] == 1970]['life'],
#     'country' : df[df['Year'] == 1970]['Country']
# })

# Create the figure: p
# p = figure(title='1970', x_axis_label='Fertility (children per woman)', y_axis_label='Life Expectancy (years)',
#            plot_height=400, plot_width=700,
#            tools=[HoverTool(tooltips='@country')])

# Add a circle glyph to the figure p
# p.circle(x='x', y='y', source=src)

# Output the file and show the figure
# output_file('gapminder.html')
# show(p)

#################################################################
# starting the app
# Import the necessary modules

# Make the ColumnDataSource: source
src = ColumnDataSource(data={
    'x'       : df[df['Year'] == 1970]['fertility'],
    'y'       : df[df['Year'] == 1970]['life'],
    'country' : df[df['Year'] == 1970]['Country'],
    'pop'     : (df[df['Year'] == 1970]['population'] / 20000000) + 2,
    'region'  : df[df['Year'] == 1970]['region'].values,
})

# Save the minimum and maximum values of the fertility column: xmin, xmax
xmin = min(df['fertility'])
xmax = max(df['fertility'])

# Save the minimum and maximum values of the life expectancy column: ymin, ymax
ymin = min(df['fertility'])
ymax = max(df['fertility'])

# Create the figure: plot
plot = figure(title='Gapminder Data for 1970', plot_height=400,                   plot_width=700, tools=[HoverTool(tooltips='@country')])

# Add circle glyphs to the plot
plot.circle(x='x', y='y', fill_alpha=0.8, source=src)

# Set the x-axis label
# plot.xaxis.axis_label ='Fertility (children per woman)'

# Set the y-axis label
# plot.yaxis.axis_label = 'Life Expectancy (years)'

# Add the plot to the current document and add a title
curdoc().add_root(plot)
curdoc().title = 'Gapminder'

# Output the file and show the figure
# show(plot)
