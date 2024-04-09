#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from capybot import load_data
import sys

# Do not use automatic offsets for plot axis
import matplotlib as mpl
mpl.rcParams['axes.formatter.useoffset'] = False

if len(sys.argv) < 2:
    sys.exit("No path to Capybot log file given")

file = sys.argv[1]

data = load_data(file);
number_of_ramms = len(data['ramm_pool_states']);

POOL_STATE_PLOT_INDEX = 0
IMB_RATIO_PLOT_INDEX = 1
VOLUME_PLOT_INDEX = 2

PLOTS_PER_RAMM = 3

fig, ax = plt.subplots(nrows = number_of_ramms, ncols = PLOTS_PER_RAMM, figsize = (22, 5 * number_of_ramms));
fig.tight_layout(pad=4.0)

# Colors to use when plotting per-asset RAMM data.
# See https://xkcd.com/color/rgb/
colors = ["#dfff00", "#ca82e1", "#7aa0c4"]

def ramm_data_helper(*, category, subplot_matrix, subplot_row_index, subplot_col_index, xlabel, ylabel, subplot_label_suffix):
    """
    Helper function to plot RAMM data.

    Since plotting each RAMM's per-asset volume, imbalance ratios and pool state is almost the same,
    this function abstracts the common logic behind that.

    :param category: The category of data to plot - pool state, imbalance ratios or trading volumes.
    :param subplot_matrix: The matrix of subplots to plot on. Each of its rows is an individual RAMM, and each of its columns is a category's plot.
    :param subplot_row_index: The row index of the subplot matrix to plot on. Each index belongs to a different RAMM.
    :param subplot_col_index:
        The column index of the subplot matrix to plot on. Each index belongs to a different category's plot.
        See `POOL_STATE_PLOT_INDEX` and similar above.
    :param xlabel: The label for the label of that category's x-axis.
    :param ylabel: The label for the label of that category's y-axis.
    :param subplot_label_suffix:
        The suffix to append to each asset in the label of the plot.
        In the case of the legend for the RAMM imb. ratios' plot, it'll be " imb. ratio".
    """
    subplot_matrix[subplot_row_index][subplot_col_index].clear()

    subplot_matrix[subplot_row_index][subplot_col_index].set_xlabel(xlabel)
    subplot_matrix[subplot_row_index][subplot_col_index].set_ylabel(ylabel)

    timestamps = category['time']
    start_ts = timestamps[0]

    # Convert UNIX timestamps to seconds since the start of the simulation
    timestamps = [ts - start_ts for ts in timestamps]

    # No recorded states, skip
    if len(category['data']) == 0:
        return

    for col_idx, key in enumerate(category['data'][0]):
        asset_data = list(map(lambda x: x[key], category['data']))
        subplot_matrix[subplot_row_index][subplot_col_index].plot(timestamps, asset_data, label = key + subplot_label_suffix, color = colors[col_idx])

    # Reasoning for the legend placement:
    # https://stackoverflow.com/questions/4700614/how-to-put-the-legend-outside-the-plot
    subplot_matrix[subplot_row_index][subplot_col_index].legend(bbox_to_anchor=(0, 1.02, 1, 0.2), loc="lower left", mode="expand", borderaxespad=0, ncol=3);
    subplot_matrix[subplot_row_index][subplot_col_index].set_facecolor('xkcd:midnight blue')

def animate_ramm_data():
    # Recall that this is going to be done once a second - visualizing logs from long-running
    # instances should be done in a static manner, without animation
    data = load_data(file);

    if number_of_ramms == 1:
        subplot_matrix = [ax]
    else:
        subplot_matrix = ax

    for r, ramm_id in enumerate(data['ramm_pool_states']):
        # RAMM pool state plots
        pool_state = data['ramm_pool_states'][ramm_id]
        ramm_data_helper(
            category = pool_state,
            subplot_matrix = subplot_matrix,
            subplot_row_index = r,
            subplot_col_index = POOL_STATE_PLOT_INDEX,
            xlabel = 'Time (s)',
            ylabel = 'Pool state',
            subplot_label_suffix = ' pool state')

        # RAMM imbalance ratio plots
        imb_ratio = data['ramm_imb_ratios'][ramm_id]
        ramm_data_helper(
            category = imb_ratio,
            subplot_matrix = subplot_matrix,
            subplot_row_index = r,
            subplot_col_index = IMB_RATIO_PLOT_INDEX,
            xlabel = 'Time (s)',
            ylabel = 'Imbalance ratios',
            subplot_label_suffix = ' imb. ratio')

        # RAMM trading volume plots
        volume = data['ramm_volumes'][ramm_id]
        ramm_data_helper(
            category = volume,
            subplot_matrix = subplot_matrix,
            subplot_row_index = r,
            subplot_col_index = VOLUME_PLOT_INDEX,
            xlabel = 'Time (s)',
            ylabel = 'Trading volumes',
            subplot_label_suffix = ' volume')

# Check if the user wants a statically or dynamically rendered plot
switch = sys.argv[2]

plt.subplots_adjust(top=0.92)

if switch == '--static':
    animate_ramm_data()
    plt.show()
elif switch == '--dynamic':
    anim = animation.FuncAnimation(fig, func = animate_ramm_data, interval = 1000)
    plt.show()
else: 
    sys.exit("Invalid switch given: use either `--static` or `--dynamic`")
