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

fig, ax = plt.subplots(nrows = number_of_ramms, ncols = 2, figsize = (16, 9));
fig.tight_layout(pad=2.0)

colors = ["#7aa0c4", "#ca82e1", "#8bcd50"]

def animate_ramm_data():
    # Recall that this is going to be done once a second - visualizing logs from long-running
    # instances should be done in a static manner, without animation
    data = load_data(file);

    for i, ramm_id in enumerate(data['ramm_pool_states']):
        pool_state = data['ramm_pool_states'][ramm_id]
        ax[POOL_STATE_PLOT_INDEX].clear()

        ax[POOL_STATE_PLOT_INDEX].set_xlabel('Time (s)')
        ax[POOL_STATE_PLOT_INDEX].set_ylabel('Asset balances')

        timestamps = pool_state['time']
        start_ts = timestamps[0]

        # Convert UNIX timestamps to seconds since the start of the simulation
        timestamps = [ts - start_ts for ts in timestamps]

        # No recorded states, skip
        if len(pool_state['data']) == 0:
            break

        #print(data['ramm_pool_states'])

        for col_idx, key in enumerate(pool_state['data'][0]):
            asset_balances = list(map(lambda x: x[key], pool_state['data']))
            ax[POOL_STATE_PLOT_INDEX].plot(timestamps, asset_balances, label = 'Balance for ' + key, color = colors[col_idx])

        ax[POOL_STATE_PLOT_INDEX].legend(bbox_to_anchor=(0, 1.02, 1, 0.2), loc="lower left", mode="expand", borderaxespad=0, ncol=3);

    for i, ramm_id in enumerate(data['ramm_imb_ratios']):
        imb_ratio = data['ramm_imb_ratios'][ramm_id]
        ax[IMB_RATIO_PLOT_INDEX].clear()

        ax[IMB_RATIO_PLOT_INDEX].set_xlabel('Time (s)')
        ax[IMB_RATIO_PLOT_INDEX].set_ylabel('Imbalance ratios')

        timestamps = imb_ratio['time']
        start_ts = timestamps[0]

        # Convert UNIX timestamps to seconds since the start of the simulation
        timestamps = [ts - start_ts for ts in timestamps]

        # No recorded states, skip
        if len(imb_ratio['data']) == 0:
            break

        for col_idx, key in enumerate(imb_ratio['data'][0]):
            imb_ratios = list(map(lambda x: x[key], imb_ratio['data']))
            ax[IMB_RATIO_PLOT_INDEX].plot(timestamps, imb_ratios, label = 'Imbalance ratio for ' + key, color = colors[col_idx])

        ax[IMB_RATIO_PLOT_INDEX].legend(bbox_to_anchor=(0, 1.02, 1, 0.2), loc="lower left", mode="expand", borderaxespad=0, ncol=3);

# Check if the user wants a statically or dynamically rendered plot
switch = sys.argv[2]

plt.subplots_adjust(top=0.9)

if switch == '--static':
    animate_ramm_data()
    plt.show()
elif switch == '--dynamic':
    anim = animation.FuncAnimation(fig, func = animate_ramm_data, interval = 1000)
    plt.show()
else: 
    sys.exit("Invalid switch given: use either `--static` or `--dynamic`")
