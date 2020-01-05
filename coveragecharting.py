import pandas as pd
import matplotlib.pyplot as plt
import re
import os

from coverageconfig import ITERATIONS
from coverage import LOWER_BOUND, INDEPENDENT_LB, LOWER_BOUND_BC


LABEL_VAR_MAP = {'phi': 'φ', 'gamma': 'γ', 'epsilon': 'ε'}

plt.rcParams['legend.title_fontsize'] = 'xx-large'


def plot_eta_chart(output_folder):
    mcd = pd.read_csv(output_folder + '/mean_coverage_distance.csv')
    coverage = mcd[list(filter(lambda c: 'coverage' in c, mcd.columns))]
    stationary_coverage = coverage[-1000:].mean().reset_index()
    stationary_coverage.columns = ['Title', 'CoverageDistance']
    stationary_coverage['Eta'] = stationary_coverage['Title'].apply(lambda t: float(t[4:7]))
    stationary_coverage.set_index('Eta')['CoverageDistance'].plot()
    plt.ylabel('Stationary Coverage Distance (m)')
    plt.xlabel('η')
    plt.savefig(output_folder + '/eta_chart.eps')
    plt.show()

def plot_coverage_distance(output_folder, label_var, max_time=ITERATIONS * 0.25):
    mcd = pd.read_csv(output_folder + '/mean_coverage_distance.csv')
    mcd[label_var] = mcd['name'].apply(lambda name: float(re.compile(f'{label_var}=(.*)').findall(name)[0]))
    label_var_pretty = LABEL_VAR_MAP[label_var]
    mcd[mcd.time < max_time].rename(columns={label_var: label_var_pretty})\
        .pivot_table(values='coverage', index='time', columns=label_var_pretty).plot()
    plt.xlabel('t', fontsize=16)
    plt.ylabel('C(t)', fontsize=16)
    plt.savefig(output_folder + f'/coverage_{label_var}.eps')
    plt.show()


def plot_coverage_dynamics(output_folder, label_var, max_time=ITERATIONS * 0.25):
    mcd = pd.read_csv(output_folder + '/mean_coverage_distance.csv')
    mcd[label_var] = mcd['name'].apply(lambda name: float(re.compile(f'{label_var}=(.*)').findall(name)[0]))
    label_var_pretty = LABEL_VAR_MAP[label_var]
    mcd['dCoverage'] = mcd.groupby(['name', label_var]) \
        .apply(lambda x: (x.coverage - x.coverage.shift(1)) / (x.time - x.time.shift(1))) \
        .reset_index(name='dCoverage').set_index('level_2')['dCoverage']
    mcd[mcd.time < max_time].rename(columns={label_var: label_var_pretty})\
        .pivot_table(values='dCoverage', index='time', columns=label_var_pretty).ewm(com=6).mean().plot()
    plt.xlabel('t', fontsize=16)
    plt.ylabel('dC(t)/dt', fontsize=16)
    plt.savefig(output_folder + f'/dcoverage_{label_var}.eps')
    plt.show()


def plot_coverage_time(output_folder, label_var, lower_bound):
    trial_files = list(filter(lambda x: x[:5] == 'trial', os.listdir(output_folder))) 
    mcd = pd.concat(list(map(lambda f: pd.read_csv(output_folder + '/' + f), trial_files)))
    mcd[label_var] = mcd['name'].apply(lambda name: float(re.compile(f'{label_var}=(.*)').findall(name)[0]))
    epsilons = [0.5, 0.25, 0.125, 0.0625, 0.03125]
    hits = []
    for epsilon in epsilons:
        hit = mcd[mcd.coverage < lower_bound + epsilon].groupby([label_var, 'trialNumber'])['time'].min().reset_index()
        hit['epsilon'] = epsilon
        hits.append(hit)
    label_var_pretty = LABEL_VAR_MAP[label_var]
    epsilon_pretty = LABEL_VAR_MAP['epsilon']
    pd.concat(hits).rename(columns={label_var: label_var_pretty, 'epsilon': epsilon_pretty})\
        .pivot_table(values='time', columns=epsilon_pretty, index=label_var_pretty)\
        .plot()
    plt.xlabel(label_var_pretty, fontsize=16)
    plt.ylabel('Coverage time', fontsize=16)
    plt.savefig(output_folder + f'/coverage_time_{label_var}.eps')
    plt.show()


if __name__ == '__main__':
    # output_folder_eta = 'results/coverage_comparison_2019-12-17 17:28:48'
    # plot_eta_chart(output_folder_eta)

    output_folder_phi = 'results/coverage_comparison_2020-01-02 08:30:40'
    plot_coverage_distance(output_folder_phi, 'phi', max_time=100)
    plot_coverage_dynamics(output_folder_phi, 'phi', max_time=40)
    plot_coverage_time(output_folder_phi, 'phi', LOWER_BOUND_BC)

    output_folder_gamma = 'results/coverage_comparison_2020-01-04 18:08:30'
    plot_coverage_distance(output_folder_gamma, 'gamma', max_time=100)
    plot_coverage_dynamics(output_folder_gamma, 'gamma', max_time=40)
    plot_coverage_time(output_folder_gamma, 'gamma', INDEPENDENT_LB)
