#!/usr/bin/env python
# coding: utf-8

import json

# Load all data from the output of a Capybot. Each line is a log message in JSON format.
def load_data(file):
    prices = {}
    strategies = {}
    orders = {}
    # RAMM data
    ramm_pool_states = {}
    ramm_imb_ratios = {}

    with open(file) as f:
        for line in f.read().splitlines():
            try:
                line_data = json.loads(line)

                if 'msg' not in line_data:
                    continue

                match line_data['msg']:
                    # A price message for a swap pool
                    case "price":
                        entry = line_data['price']
                        price = entry['price'];
                        source = entry['source_uri'];

                        # The first price is used as the relative offset
                        if source not in prices:
                            prices[source] = {
                                'offset': entry['price'],
                                'price': [],
                                'time': [],
                            }
                        prices[source]['price'].append(price)
                        prices[source]['time'].append(line_data['time'] / 1000)

                    # When starting, Capybot outputs all used strategies. But note that this is only done once.
                    case "strategies":
                        for strategy in line_data['strategies']:
                            strategies[strategy] = {};
                            strategies[strategy]['parameters'] = line_data['strategies'][strategy];
                            strategies[strategy]['statuses'] = {
                                'value': [],
                                'time': []
                            }

                    # Status from a strategy. This may contain arbitrary values decided by the strategy, so we just store everything.
                    case "strategy status":
                        strategy = line_data['uri']
                        entry = line_data['data'];
                        strategies[strategy]['statuses']['value'].append(entry)
                        strategies[strategy]['statuses']['time'].append(line_data['time'] / 1000)

                    # A strategy returned a trade order. Store the time-stamp.
                    case "order":
                        strategy = line_data['strategy']
                        if strategy not in orders:
                            orders[strategy] = {
                                'time':  [],
                            }
                        orders[strategy]['time'].append(line_data['time'] / 1000);

                    # The data below pertains *only* to `capybot`'s RAMMs
                    case "ramm pool state":
                        ramm_id = line_data['ramm_id']
                        if ramm_id not in ramm_pool_states:
                            ramm_pool_states[ramm_id] = {
                                'time': [],
                                'data': []
                            }
                        pool_state = line_data['data']
                        timestamp = line_data['time'] / 1000

                        ramm_pool_states[ramm_id]['time'].append(timestamp)
                        ramm_pool_states[ramm_id]['data'].append(pool_state)

                    case "imb ratios":
                        ramm_id = line_data['ramm_id']
                        if ramm_id not in ramm_imb_ratios:
                            ramm_imb_ratios[ramm_id] = {
                                'time': [],
                                'data': []
                            }
                        imb_ratios = line_data['data']
                        timestamp = line_data['time'] / 1000

                        ramm_imb_ratios[ramm_id]['time'].append(timestamp)
                        ramm_imb_ratios[ramm_id]['data'].append(imb_ratios)

                    case "ramm volumes":
                        continue

                    case _:
                        continue
                     
            except: 
                continue
                
    return {
        'prices': prices, 
        'strategies': strategies,
        'orders': orders,
        'ramm_pool_states': ramm_pool_states,
        'ramm_imb_ratios': ramm_imb_ratios
    }