import pandas as pd
import matplotlib.pyplot as plt
import re

from coverageconfig import ITERATIONS
from coverage import LOWER_BOUND, INDEPENDENT_LB



def plot_eta_chart(output_folder):
    mcd = pd.read_csv(output_folder + '/mean_coverage_distance.csv')
    coverage = mcd[list(filter(lambda c: 'coverage' in c, mcd.columns))]
    stationary_coverage = coverage[-1000:].mean().reset_index()
    stationary_coverage.columns = ['Title', 'CoverageDistance']
    stationary_coverage['Eta'] = stationary_coverage['Title'].apply(lambda t: float(t[4:7]))
    stationary_coverage.set_index('Eta')['CoverageDistance'].plot()
    plt.ylabel('Stationary Coverage Distance (m)')
    plt.xlabel('η')
    plt.savefig(output_folder + '/eta_chart.pdf')
    plt.savefig(output_folder + '/eta_chart.eps')
    plt.show()

def plot_coverage_dynamics(output_folder, label_var, max_time=ITERATIONS * 0.25):
    mcd = pd.read_csv(output_folder + '/mean_coverage_distance.csv')
    mcd[label_var] = mcd['name'].apply(lambda name: float(re.compile(f'{label_var}=(.*)').findall(name)[0]))
    mcd.pivot_table(values='coverage', index='time', columns=label_var).plot()
    plt.ylabel('C(t)')
    plt.savefig(output_folder + '/coverage.eps')
    plt.savefig(output_folder + '/coverage.pdf')
    plt.show()
    mcd['dCoverage'] = mcd.groupby(['name', label_var]) \
        .apply(lambda x: (x.coverage - x.coverage.shift(1)) / (x.time - x.time.shift(1))) \
        .reset_index(name='dCoverage').set_index('level_2')['dCoverage']
    mcd[mcd.time < max_time].pivot_table(values='dCoverage', index='time', columns=label_var).ewm(com=6).mean().plot()
    plt.xlabel('t')
    plt.ylabel('dC(t)/dt')
    plt.savefig(output_folder + '/dcoverage.eps')
    plt.savefig(output_folder + '/dcoverage.pdf')
    plt.show()



def plot_coverage_time(output_folder, label_var, lower_bound):
    mcd = pd.read_csv(output_folder + '/mean_coverage_distance.csv')
    c_lim = mcd[mcd.time == mcd.time.max()][[label_var, 'coverage']]
    c_lim.set_index(label_var).plot()
    plt.savefig(output_folder + '/coverage_lower_bound.eps')
    plt.savefig(output_folder + '/coverage_lower_bound.pdf')
    plt.show()
    mcd = mcd.merge(c_lim.rename(columns={'coverage': 'minCoverage'}), on=label_var)
    x4 = mcd[mcd['coverage'] < (lower_bound + 4)].groupby(label_var)['time'].min() \
        .reset_index() \
        .rename(columns={'time': 'ε=4'})
    x2 = mcd[mcd['coverage'] < (lower_bound + 2)].groupby(label_var)['time'].min() \
        .reset_index() \
        .rename(columns={'time': 'ε=2'})
    x1 = mcd[mcd['coverage'] < (lower_bound + 1)].groupby(label_var)['time'].min() \
        .reset_index() \
        .rename(columns={'time': 'ε=1'})
    x0_5 = mcd[mcd['coverage'] < (lower_bound + 0.5)].groupby(label_var)['time'].min() \
        .reset_index() \
        .rename(columns={'time': 'ε=0.5'})
    x = x4.merge(x2, on=label_var, how='left')\
        .merge(x1, on=label_var, how='left')\
        .merge(x0_5, on=label_var, how='left')
    x.set_index(label_var).plot()
    plt.ylabel('Coverage time')
    plt.savefig(output_folder + '/coverage_time.eps')
    plt.savefig(output_folder + '/coverage_time.pdf')
    plt.show()


if __name__ == '__main__':
    output_folder_eta = 'results/coverage_comparison_2019-12-17 17:28:48'
    plot_eta_chart(output_folder_eta)

    output_folder_phi = 'results/coverage_comparison_2019-12-26 11:06:21'
    plot_coverage_dynamics(output_folder_phi, 'phi', max_time=30)
    plot_coverage_time(output_folder_phi, 'phi', LOWER_BOUND)
    
    output_folder_gamma = 'results/coverage_comparison_2019-12-25 01:12:58'
    plot_coverage_dynamics(output_folder_gamma, 'gamma', max_time=30)
    plot_coverage_time(output_folder_gamma, 'gamma', INDEPENDENT_LB)
