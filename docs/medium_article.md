# Building Interactive Histograms with Bokeh

## Getting Started with Bokeh in Python

You are probably familiar with Matplotlib and Seaborn, two excellent (and highly related) Python plotting libraries. The purpose of this article is to get you started with Bokeh if you are not yet familiar with it. You will learn how to write a custom Python class to simplify plotting interactive histograms with Bokeh.

NB: please use this code as a template / baseline and experiment on your own! My intention is to provide instructions for building a functional Python class that can be expanded and customized based on individual need.

First we will write three plotting functions which will help us to get familiar with Bokeh syntax and conventions. Then we will wrap these three functions is a class to make creating various plots quicker and easier. As with any Python script we begin with the necessary imports:  

```python
import pandas as pd
import numpy as np
from bokeh.plotting import figure
from bokeh.io import output_notebook, show, output_file
from bokeh.models import ColumnDataSource, HoverTool, Panel
from bokeh.models.widgets import Tabs
```

## Function One: Hist Hover  
This is a function for creating a single histogram with cursor-hover interactivity. When the user hovers of the bars of the histogram the upper and lower bounds, as well as the count, of the bar are displayed. The color is also changed to highlight that particular bar.

The first step is to create the data for the histogram with the Numpy function `np.histogram`. Here we pass is the source dataframe, the column we want to plot, and the number of bins:

`hist, edges = np.histogram(dataframe[column], bins = bins)`

I'm leaving the arguments generic here because we are going to build this out into a function which will take these argument when it is called. We then turn this histogram data into a dataframe:

```python
hist_df = pd.DataFrame({column: hist,
                        "left": edges[:-1],
                        "right": edges[1:]})
hist_df["interval"] = ["%d to %d" % (left, right) for left, 
                        right in zip(hist_df["left"], hist_df["right"])]
```

The first part here creates a dataframe from the histogram data with the target variable counts, and left and rights edges of the bins. The second part creates a new column describing the bins interval. This will be useful when we call the HoverTool in Bokeh.

Next we create a ColumnDataSource object in Bokeh. This is the object that Bokeh uses for much of its plotting capabilities.

```python
src = ColumnDataSource(hist_df)
```

Then we actually create the plot with two separate calls:

```python
plot = figure(plot_height = 600, plot_width = 600,
      title = "Histogram of {}".format(column.capitalize()),
      x_axis_label = column.capitalize(),
      y_axis_label = "Count")  

plot.quad(bottom = 0, top = column,left = "left", 
    right = "right", source = src, fill_color = colors[0], 
    line_color = "black", fill_alpha = 0.7,
    hover_fill_alpha = 1.0, hover_fill_color = colors[1])
```

This first call creates a Bokeh figure object where we specify the size (this will later be an attribute of the class), title, and labels. The second call creates a "glyph" on top of the figure. This is Bokeh's way of actually putting data on the canvas. Here we tell to Bokeh to plot rectangles with the height and edges specified in our ColumnDataSource object (remember the data comes from our Numpy histogram dataframe). It might seem a little verbose right now (especially compared to Seaborn) but the results will be worth it!

Then we add the hover tool:

```python
hover = HoverTool(tooltips = [('Interval', '@interval'),
                          ('Count', str("@" + column))])
plot.add_tools(hover)
```

Here we are referencing the 'Interval" column we created above and as well as the count. These will be displayed when the user hovers over a bin.

Lastly we ask Bokeh to show us the plot:

```python
        if show_plot == True:
            show(plot)
        else:
            return plot
```

We need the option of returning the plot so that this function can be called as a helper is the next two functions. And voila! We have our function for creating a histogram with hover tool interactivity! The last bit we will add here is an option for plotting on a log scale, which will require an `if, else` break. Note that if `log_scale=True` then we add another column to the histogram dataframe.

```python
def hist_hover(dataframe, column, colors=["SteelBlue", "Tan"], bins=30, log_scale=False, show_plot=True):

    # build histogram data with Numpy
    hist, edges = np.histogram(dataframe[column], bins = bins)
    hist_df = pd.DataFrame({column: hist,
                             "left": edges[:-1],
                             "right": edges[1:]})
    hist_df["interval"] = ["%d to %d" % (left, right) for left, 
                           right in zip(hist_df["left"], hist_df["right"])]

    # bokeh histogram with hover tool
    if log_scale == True:
        hist_df["log"] = np.log(hist_df[column])
        src = ColumnDataSource(hist_df)
        plot = figure(plot_height = 600, plot_width = 600,
              title = "Histogram of {}".format(column.capitalize()),
              x_axis_label = column.capitalize(),
              y_axis_label = "Log Count")    
        plot.quad(bottom = 0, top = "log",left = "left", 
            right = "right", source = src, fill_color = colors[0], 
            line_color = "black", fill_alpha = 0.7,
            hover_fill_alpha = 1.0, hover_fill_color = colors[1])
    else:
        src = ColumnDataSource(hist_df)
        plot = figure(plot_height = 600, plot_width = 600,
              title = "Histogram of {}".format(column.capitalize()),
              x_axis_label = column.capitalize(),
              y_axis_label = "Count")    
        plot.quad(bottom = 0, top = column,left = "left", 
            right = "right", source = src, fill_color = colors[0], 
            line_color = "black", fill_alpha = 0.7,
            hover_fill_alpha = 1.0, hover_fill_color = colors[1])
    # hover tool
    hover = HoverTool(tooltips = [('Interval', '@interval'),
                              ('Count', str("@" + column))])
    plot.add_tools(hover)
    # output
    if show_plot == True:
        show(plot)
    else:
        return plot
```

I have deliberately left the docstring blank and encourage you to write it on your own. This will help you build your understanding of the code and explain any additional functionality you may have written.

## Function Two: Histotabs for PLotting a Group of Numeric Variables

The basic `hist_hover` function above is the most complex, and will actually be called as the basis for the two types of tabbed interfaces we will create next. Here is the function to create a tabbed interface of a set of continuous variable. When you call the function the tabbed interface will appear in a new browser window or Jupyter notebook cell (if specified).

```python
def histotabs(dataframe, features, log_scale=False, show_plot=False):
    hists = []
    for f in features:
        h = hist_hover(dataframe, f, log_scale=log_scale, show_plot=show_plot)
        p = Panel(child=h, title=f.capitalize())
        hists.append(p)
    t = Tabs(tabs=hists)
    show(t)
```

Here we create an empty list to store our individual histograms (one for each variable). Then we the histograms one by one by calling `hist_hover` with the appropriate column. Each histogram is stored in its own Panel object, which is added to our list of histograms. We then create a Bokeh Tabs object assigning the content to our list of histograms, and ask Bokeh to show the Tabs object. 

## Function Three: Filtered Histotabs for Looking at a Single Numeric Variable Filtered by a Catergorical Variable  

Here's our final function:

```python
def filtered_histotabs(dataframe, feature, filter_feature, log_scale=False,show_plot=False):
    hists = []
    for col in dataframe[filter_feature].unique():
        sub_df = dataframe[dataframe[filter_feature] == col]
        histo = hist_hover(sub_df, feature, log_scale=log_scale, show_plot=show_plot)
        p = Panel(child = histo, title=col)
        hists.append(p)
    t = Tabs(tabs=hists)
    show(t)
```

This function is straightforward as well. First we filter the dataframe by the unique values in the `filter_feature`. Then we call `hist_hover` with this filtered dataframe and our target feature. Again we create a unique Panel object for each histogram, add them to our list, and use that list as the content for our Tabs object. And voila! We have a nice interactive set of histograms.

## Putting it all together

Now we take these three functions and wrap them up in a Bokeh Histogram class where they will become methods. Core visual attributes can be defined when we instantiate the class. Then it's easy to call the methods and create any histograms you need.

```python

class BokehHistogram():

    def __init__(self, colors=["SteelBlue", "Tan"], height=600, width=600):
        self.colors = colors
        self.height = height
        self.width = width

    def hist_hover(self, dataframe, column, bins=30, log_scale=False, show_plot=True):
        hist, edges = np.histogram(dataframe[column], bins = bins)
        hist_df = pd.DataFrame({column: hist,
                                 "left": edges[:-1],
                                 "right": edges[1:]})
        hist_df["interval"] = ["%d to %d" % (left, right) for left, 
                               right in zip(hist_df["left"], hist_df["right"])]

        if log_scale == True:
            hist_df["log"] = np.log(hist_df[column])
            src = ColumnDataSource(hist_df)
            plot = figure(plot_height = self.height, plot_width = self.width,
                  title = "Histogram of {}".format(column.capitalize()),
                  x_axis_label = column.capitalize(),
                  y_axis_label = "Log Count")    
            plot.quad(bottom = 0, top = "log",left = "left", 
                right = "right", source = src, fill_color = self.colors[0], 
                line_color = "black", fill_alpha = 0.7,
                hover_fill_alpha = 1.0, hover_fill_color = self.colors[1])
        else:
            src = ColumnDataSource(hist_df)
            plot = figure(plot_height = self.height, plot_width = self.width,
                  title = "Histogram of {}".format(column.capitalize()),
                  x_axis_label = column.capitalize(),
                  y_axis_label = "Count")    
            plot.quad(bottom = 0, top = column,left = "left", 
                right = "right", source = src, fill_color = self.colors[0], 
                line_color = "black", fill_alpha = 0.7,
                hover_fill_alpha = 1.0, hover_fill_color = self.colors[1])

        hover = HoverTool(tooltips = [('Interval', '@interval'),
                                  ('Count', str("@" + column))])
        plot.add_tools(hover)

        if show_plot == True:
            show(plot)
        else:
            return plot

    def histotabs(self, dataframe, features, log_scale=False, show_plot=False):
        hists = []
        for f in features:
            h = self.hist_hover(dataframe, f, log_scale=log_scale, show_plot=show_plot)
            p = Panel(child=h, title=f.capitalize())
            hists.append(p)
        t = Tabs(tabs=hists)
        show(t)

    def filtered_histotabs(self, dataframe, feature, filter_feature, log_scale=False, show_plot=False):
        hists = []
        for col in dataframe[filter_feature].unique():
            sub_df = dataframe[dataframe[filter_feature] == col]
            histo = self.hist_hover(sub_df, feature, log_scale=log_scale, show_plot=show_plot)
            p = Panel(child = histo, title=col)
            hists.append(p)
        t = Tabs(tabs=hists)
        show(t)
``` 

Here is an example of how you can use this class. First load some data into a Pandas dataframe. For demonstration I will use the Harvard Ed X data set which you can download [here](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/26147). 

```python
df = pd.read_csv('path_to_your_data_file')
```

Create an instance of the Bokeh Histogram object. Custom colors and sizes can be declared here, but I'm sticking with the defaults for now:

```python
h = BokehHistogram()
```

Then simply call methods off of your object with the appropriate parameters specified.

```python
h.hist_hover(df.fillna(0, axis=1), 'nevents', log_scale=True)

h.histotabs(df.fillna(0, axis=1), ['nevents', 'ndays_act', 'nchapters'], log_scale=True)

h.filtered_histotabs(df.fillna(0, axis=1), 'nevents', 'final_cc_cname_DI', log_scale=True)
```

I chose to plot on a log scale because the data approach an exponential distribution. I also simply filled null values with zero for demonstration purposes (not always a good idea!)

And now you should have some nifty tabbed histograms to share! Please modify the code as you see fit, customize it to your needs, and write some docstrings and comments! My fully commented code can be found [here](https://github.com/jeremymiller00/bokeh_tools)

Thanks for reading!

