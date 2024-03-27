#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib.animation as animation
from capybot import load_data
import sys
from matplotlib.widgets import Slider

ARBITRAGE_RELATIVE_LIMIT = 1.0005

# Do not use automatic offsets for plot axis
import matplotlib as mpl
mpl.rcParams['axes.formatter.useoffset'] = False

if len(sys.argv) != 2:
    sys.exit("No path to Capybot log file given")

file = sys.argv[1]

data = load_data(file);
number_of_strategies = len(data['strategies']);

fig, ax = plt.subplots(nrows = number_of_strategies, ncols = 1, figsize = (6, 10));
fig.tight_layout(pad=2.0)

def animate_strategies(j):
    data = load_data(file);

    # if only one arbitrage strategy is being used, the ax object is not iterable,
    # and will not be subscriptable - thus the checked
    if number_of_strategies > 1:
        ax_object = ax[i]
    else:
        ax_object = ax

    for i, uri in enumerate(data['strategies']):
        strategy = data['strategies'][uri]
        ax_object.clear()
        ax_object.set_title(strategy['parameters']['name'] + "")

        ax_object.set_xlabel('Time (s)')
        ax_object.set_ylabel('Arbitrage potential')

        # A horizontal line is drawn at the relative limit at which arbitrage is considered
        ax_object.axhline(y = ARBITRAGE_RELATIVE_LIMIT, color = 'black', linestyle = '--', label = 'Arbitrage threshold')

        timestamps = strategy['statuses']['time']
        start_ts = timestamps[0]

        timestamps = [ts - start_ts for ts in timestamps]

        if len(strategy['statuses']['value']) == 0:
            break

        for key in strategy['statuses']['value'][0]:
            y = list(map(lambda x: x[key], strategy['statuses']['value']))
            ax_object.plot(timestamps, y, label = key)

        # A trade order is indicated by a vertical red line
        if uri in data['orders']:
            order_ts = [ts - start_ts for ts in data['orders'][uri]['time']];
            ax_object.axvline(color = 'r', label = 'Trade order')
            for order_t in order_ts:
                ax_object.axvline(x = order_t, color = 'r', linestyle = '-.', alpha = 0.05)

        ax_object.legend();

""" def animate_strategies(j):
    if number_of_strategies > 1:
        return "More than 1 strat, currently not implemented"

    data = load_data(file);

    for i, uri in enumerate(data['strategies']):

        # the entirety of the strategies' collected data
        strategy = data['strategies'][uri]

        ax.clear()
        ax.set_title(strategy['parameters']['name'] + "")

        print("strat name: ", strategy['parameters']['name'])

        timestamps = strategy['statuses']['time']
        min_timestamp = timestamps[0]

        timestamps = [ts - min_timestamp for ts in timestamps]
        print(timestamps)

        if len(strategy['statuses']['value']) == 0:
            break

        arbitrage_vals = list(map(lambda x: x['arbitrage'], strategy['statuses']['value']))
        print(arbitrage_vals)
        rev_arbitrage_vals = list(map(lambda x: x['reverse'], strategy['statuses']['value']))
        print(rev_arbitrage_vals)

        ax.plot(timestamps, arbitrage_vals, label = "arbitrage", color = 'b')
        ax.plot(timestamps, rev_arbitrage_vals, label = "reverse arbitrage", color = 'g')

#        # A trade order is indicated by a vertical red line
#        if uri in data['orders']:
#            min_order_ts = min(data['orders'][uri]['time'])
#
#            order_t = [ts - min_order_ts for ts in data['orders'][uri]['time']];
#            for oi in order_t:
#                #print("order at: ", xi)
#                ax.axvline(x = oi, color = 'r')

        ax.legend(); """


anim = animation.FuncAnimation(fig, func = animate_strategies, interval = 1000)
plt.show()
