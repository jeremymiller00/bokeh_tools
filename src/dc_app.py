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
plot.xaxis.axis_label ='Fertility (children per woman)'

# Set the y-axis label
plot.yaxis.axis_label = 'Life Expectancy (years)'

# Add the plot to the current document and add a title
curdoc().add_root(plot)
curdoc().title = 'Gapminder'

# Output the file and show the figure
# show(plot)



'''
from website
'''

'''
combine bokeh models into layouts

# Create ColumnDataSource: source
source = ColumnDataSource(data={'x':x,'y':y})

# Add a line to the plot
plot.line('x', 'y', source=source)

# Create a column layout: layout
layout = column(widgetbox(slider), plot)

# Add the layout to the current document
curdoc().add_root(layout)
'''

'''
widget callbacks
# Define a callback function: callback
def callback(attr, old, new):

    # Read the current value of the slider: scale
    scale = slider.value

    # Compute the updated y using np.sin(scale/x): new_y
    new_y = np.sin(scale/x)

    # Update source with the new data values
    source.data = {'x': x, 'y': new_y}

# Attach the callback to the 'value' property of slider
slider.on_change('value', callback)

# Create layout and add to current document
layout = column(widgetbox(slider), plot)
curdoc().add_root(layout)
'''

'''
dropdown callbacks
# Perform necessary imports
from bokeh.models import ColumnDataSource, Select

# Create ColumnDataSource: source
source = ColumnDataSource(data={
    'x' : fertility,
    'y' : female_literacy
})

# Create a new plot: plot
plot = figure()

# Add circles to the plot
plot.circle('x', 'y', source=source)

# Define a callback function: update_plot
def update_plot(attr, old, new):
    # If the new Selection is 'female_literacy', update 'y' to female_literacy
    if new == 'female_literacy': 
        source.data = {
            'x' : fertility,
            'y' : female_literacy
        }
    # Else, update 'y' to population
    else:
        source.data = {
            'x' : fertility,
            'y' : population
        }

# Create a dropdown Select widget: select    
select = Select(title="distribution", options=['female_literacy', 'population'], value='female_literacy')

# Attach the update_plot callback to the 'value' property of select
select.on_change('value', update_plot)

# Create layout and add to current document
layout = row(select, plot)
curdoc().add_root(layout)
'''

'''
synchronize two dropdowns
# Create two dropdown Select widgets: select1, select2
select1 = Select(title='First', options=['A', 'B'], value='A')
select2 = Select(title='Second', options=['1', '2', '3'], value='1')

# Define a callback function: callback
def callback(attr, old, new):
    # If select1 is 'A' 
    if select1.value == 'A':
        # Set select2 options to ['1', '2', '3']
        select2.options = ['1','2','3']

        # Set select2 value to '1'
        select2.value = '1'
    else:
        # Set select2 options to ['100', '200', '300']
        select2.options = ['100','200','300']

        # Set select2 value to '100'
        select2.value = '100'

# Attach the callback to the 'value' property of select1
select1.on_change('value', callback)

# Create layout and add to current document
layout = widgetbox(select1, select2)
curdoc().add_root(layout)
'''
'''
button widgets
# Create a Button with label 'Update Data'
button = Button(label="Update Data")

# Define an update callback with no arguments: update
def update():

    # Compute new y values: y
    y = np.sin(x) + np.random.random(N)

    # Update the ColumnDataSource data dictionary
    source.data = {'x':x, 'y':y}

# Add the update callback to the button
button.on_click(update)

# Create layout and add to current document
layout = column(widgetbox(button), plot)
curdoc().add_root(layout)
'''

'''
button styles
# Import CheckboxGroup, RadioGroup, Toggle from bokeh.models
from bokeh.models import CheckboxGroup, RadioGroup, Toggle

# Add a Toggle: toggle
toggle = Toggle(button_type='success', label="Toggle button")

# Add a CheckboxGroup: checkbox
checkbox = CheckboxGroup(labels=['Option1', 'Option2', 'Option3'])

# Add a RadioGroup: radio
radio = RadioGroup(labels=['Option1', 'Option2', 'Option3'])

# Add widgetbox(toggle, checkbox, radio) to the current document
curdoc().add_root(widgetbox(toggle, checkbox, radio))
'''
 