import pandas as pd
import matplotlib.pyplot as plt

output_folder = 'results/coverage_comparison_2019-12-12 20:49:02'

mcd = pd.read_csv(output_folder + '/mean_coverage_distance.csv')
coverage = mcd[list(filter(lambda c: 'coverage' in c, mcd.columns))]
stationary_coverage = coverage[-1000:].mean().reset_index()
stationary_coverage.columns = ['Title', 'CoverageDistance']
stationary_coverage['Eta'] = stationary_coverage['Title'].apply(lambda t: float(t[4:7]))
stationary_coverage.set_index('Eta')['CoverageDistance'].plot()
plt.ylabel('Stationary Coverage Distance (m)')
plt.xlabel('Eta squared')
plt.savefig(output_folder + '/eta_chart.pdf')
plt.savefig(output_folder + '/eta_chart.eps')
