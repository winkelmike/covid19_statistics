import pandas as pd
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource

FILE_PATH_NAME = "data/all_countries/covid_observations_all.csv"
data = pd.read_csv(FILE_PATH_NAME, parse_dates=['date'], index_col='date')

print(data.tail())
print(data.columns)

source = ColumnDataSource(data={
    'x'       : data.loc['2020-03-21'].confirmed,
    'y'       : data.loc['2020-03-21'].deaths,
    'country' : data.loc['2020-03-21'].country
})

# Create the figure: p
p = figure(title='time', x_axis_label='confirmed', y_axis_label='deaths',
           plot_height=400, plot_width=700,
           tools=[HoverTool(tooltips='@country')])

# Add a circle glyph to the figure p
p.circle(x='x', y='y', source=source)

# Output the file and show the figure
output_file('confirmed.html')
show(p)
# TODO, this is a first draft, requires a lot more reworking and data enrichment