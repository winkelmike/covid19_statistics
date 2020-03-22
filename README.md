# covid19_statistics

A data-pipeline set up from the JHU CSSE data repo (https://github.com/CSSEGISandData/COVID-19)
Build to make visualizations and analyses

pull_from_git.py: pulls latest data from JHU CSSE data repo in the /source_data/ 
  (requires active connection from JHU CSSE repo  to /source_data/ folder)
  
time_series_etl.py: parses source data files to observation based CSV's

line_plot_per_country: creates a set of static visualizations per country based on observations
