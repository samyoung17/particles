import pandas as pd
import matplotlib.pyplot as plt
import re



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


def plot_dynamics(x_axis_label, output_folder):
    mcd = pd.read_csv(output_folder + '/mean_coverage_distance.csv')
    distance = mcd[list(filter(lambda c: 'distance' in c, mcd.columns)) + ['time']]
    distance_stack = distance.set_index('time').stack().reset_index()
    distance_stack.columns = ['time', 'name', 'distance']
    distance_stack[x_axis_label] = distance_stack['name'].apply(lambda name: float(re.compile(f'{x_axis_label}=(.*)\.distance').findall(name)[0]))
    distance_stack['speed'] = distance_stack.groupby(['name', x_axis_label])\
        .apply(lambda x: (x.distance - x.distance.shift(1)) / (x.time - x.time.shift(1)))\
        .reset_index(name='speed').set_index('level_2')['speed']
    distance_stack.pivot_table(values='speed', index='time', columns=x_axis_label).plot()
    plt.show()
    # distance_stack.pivot_table(values='distance', index='time', columns=x_axis_label).plot()
    # plt.show()


if __name__ == '__main__':
    output_folder = 'results/coverage_comparison_2019-12-17 17:28:48'
    plot_eta_chart(output_folder)
    x_axis_label = 'phi'
    output_folder = 'results/coverage_comparison_2019-12-24 17:33:44'
    plot_dynamics(x_axis_label, output_folder)