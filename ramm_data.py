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

fig, ax = plt.subplots(nrows = number_of_ramms, ncols = 1, figsize = (6, 10));
fig.tight_layout(pad=2.0)

def animate_ramm_data(j):
    # Recall that this is going to be done once a second - visualizing logs from long-running
    # instances should be done in a static manner, without animation
    data = load_data(file);

    # if only one RAMM's data is being plotted, only its pool states will be plotted, and so the ax
    # object is not iterable, thus not subscriptable - thus the check
    if number_of_ramms > 1:
        ax_object = ax[i]
    else:
        ax_object = ax

    for i, ramm_id in enumerate(data['ramm_pool_states']):
        pool_state = data['ramm_pool_states'][ramm_id]
        ax_object.clear()
        ax_object.set_title("Pool State of RAMM" + ramm_id)

        ax_object.set_xlabel('Time (s)')
        ax_object.set_ylabel('Asset balances')

        timestamps = pool_state['time']
        start_ts = timestamps[0]

        # Convert UNIX timestamps to seconds since the start of the simulation
        timestamps = [ts - start_ts for ts in timestamps]

        # No recorded states, skip
        if len(pool_state['data']) == 0:
            break

        #print(data['ramm_pool_states'])

        for key in pool_state['data'][0]:
            asset_balances = list(map(lambda x: x[key], pool_state['data']))
            ax_object.plot(timestamps, asset_balances, label = 'Balance for ' + key)

        ax_object.legend();

        return

        # A trade order is indicated by a vertical red line
        if ramm_id in data['orders']:
            order_ts = [ts - start_ts for ts in data['orders'][ramm_id]['time']];
            # Set the label for all trade orders once
            ax_object.axvline(color = 'r', label = 'Trade order')
            for order_t in order_ts:
                ax_object.axvline(x = order_t, color = 'r', linestyle = '-.', alpha = 0.05)

        

switch = sys.argv[2]

if switch == '--static':
    animate_ramm_data(0)
    plt.show()
elif switch == '--dynamic':
    anim = animation.FuncAnimation(fig, func = animate_ramm_data, interval = 1000)
    plt.show()
else: 
    sys.exit("Invalid switch given: use either `--static` or `--dynamic`")
