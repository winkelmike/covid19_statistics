import subprocess

# EXTRACT raw data
print('Running pull_from_git')
subprocess.call("python pull_from_git.py", shell=True)

print('Running pull_government_measures_from_humdata')
subprocess.call("python data\\pull_government_measures_from_humdata.py", shell=True)

# UPDATE local data files
print('Running time_series_etl')
subprocess.call("python data\\time_series_etl.py", shell=True)

# UPDATE visualizations
print('Running line_plot_per_country')
subprocess.call("python visualizations\\line_plot_per_country.py", shell=True)
