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

def ramm_data_helper(*, datum, subplot_matrix, subplot_row_index, datum_id, datum_index, subplot_col_index, xlabel, ylabel, subplot_label_suffix):
    subplot_matrix[subplot_row_index][subplot_col_index].clear()

    subplot_matrix[subplot_row_index][subplot_col_index].set_xlabel(xlabel)
    subplot_matrix[subplot_row_index][subplot_col_index].set_ylabel(ylabel)

    timestamps = datum['time']
    start_ts = timestamps[0]

    # Convert UNIX timestamps to seconds since the start of the simulation
    timestamps = [ts - start_ts for ts in timestamps]

    # No recorded states, skip
    if len(datum['data']) == 0:
        return

    for col_idx, key in enumerate(datum['data'][0]):
        asset_data = list(map(lambda x: x[key], datum['data']))
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
        subplot_matrix[r][POOL_STATE_PLOT_INDEX].clear()

        subplot_matrix[r][POOL_STATE_PLOT_INDEX].set_xlabel('Time (s)')
        subplot_matrix[r][POOL_STATE_PLOT_INDEX].set_ylabel('Asset balances')

        timestamps = pool_state['time']
        start_ts = timestamps[0]

        # Convert UNIX timestamps to seconds since the start of the simulation
        timestamps = [ts - start_ts for ts in timestamps]

        # No recorded states, skip
        if len(pool_state['data']) == 0:
            break

        for col_idx, key in enumerate(pool_state['data'][0]):
            asset_balances = list(map(lambda x: x[key], pool_state['data']))
            subplot_matrix[r][POOL_STATE_PLOT_INDEX].plot(timestamps, asset_balances, label = key + ' balance', color = colors[col_idx])

        # Reasoning for the legend placement:
        # https://stackoverflow.com/questions/4700614/how-to-put-the-legend-outside-the-plot
        subplot_matrix[r][POOL_STATE_PLOT_INDEX].legend(bbox_to_anchor=(0, 1.02, 1, 0.2), loc="lower left", mode="expand", borderaxespad=0, ncol=3);
        subplot_matrix[r][POOL_STATE_PLOT_INDEX].set_facecolor('xkcd:midnight blue')

        # RAMM imbalance ratio plots
        imb_ratio = data['ramm_imb_ratios'][ramm_id]
        subplot_matrix[r][IMB_RATIO_PLOT_INDEX].clear()

        subplot_matrix[r][IMB_RATIO_PLOT_INDEX].set_xlabel('Time (s)')
        subplot_matrix[r][IMB_RATIO_PLOT_INDEX].set_ylabel('Imbalance ratios')

        timestamps = imb_ratio['time']
        start_ts = timestamps[0]

        # Convert UNIX timestamps to seconds since the start of the simulation
        timestamps = [ts - start_ts for ts in timestamps]

        # No recorded states, skip
        if len(imb_ratio['data']) == 0:
            break

        for col_idx, key in enumerate(imb_ratio['data'][0]):
            imb_ratios = list(map(lambda x: x[key], imb_ratio['data']))
            subplot_matrix[r][IMB_RATIO_PLOT_INDEX].plot(timestamps, imb_ratios, label = key + ' imb. ratio', color = colors[col_idx])

        subplot_matrix[r][IMB_RATIO_PLOT_INDEX].legend(bbox_to_anchor=(0, 1.02, 1, 0.2), loc="lower left", mode="expand", borderaxespad=0, ncol=3);
        subplot_matrix[r][IMB_RATIO_PLOT_INDEX].set_facecolor('xkcd:navy blue')

        # RAMM trading volume plots
        volume = data['ramm_volumes'][ramm_id]
        subplot_matrix[r][VOLUME_PLOT_INDEX].clear()

        subplot_matrix[r][VOLUME_PLOT_INDEX].set_xlabel('Time (s)')
        subplot_matrix[r][VOLUME_PLOT_INDEX].set_ylabel('Trading volumes')

        timestamps = volume['time']
        start_ts = timestamps[0]

        # Convert UNIX timestamps to seconds since the start of the simulation
        timestamps = [ts - start_ts for ts in timestamps]

        # No recorded states, skip
        if len(volume['data']) == 0:
            break

        for col_idx, key in enumerate(imb_ratio['data'][0]):
            volumes = list(map(lambda x: x[key], volume['data']))
            subplot_matrix[r][VOLUME_PLOT_INDEX].plot(timestamps, volumes, label = key + ' volume', color = colors[col_idx])

        subplot_matrix[r][VOLUME_PLOT_INDEX].legend(bbox_to_anchor=(0, 1.02, 1, 0.2), loc="lower left", mode="expand", borderaxespad=0, ncol=3);
        subplot_matrix[r][VOLUME_PLOT_INDEX].set_facecolor('xkcd:navy blue')

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
