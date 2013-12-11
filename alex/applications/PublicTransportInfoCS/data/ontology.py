#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from database import database
import codecs
import os

# tab-separated file containing city + stop in that city, one per line
CITIES_STOPS_FNAME = 'cities_stops.tsv'

ontology = {
    'slots': {
        'silence': set([]),
        'ludait': set([]),
        'task': set(['find_connection', 'find_platform', 'weather']),
        'from_stop': set(['Zličín', 'Anděl', ]),
        'to_stop': set(['Zličín', 'Anděl', ]),
        'via_stop': set(['Zličín', 'Anděl', ]),
        'from_city': set([]),
        'to_city': set([]),
        'via_city': set([]),
        'in_city': set([]),
        'departure_time': set([]),
        'departure_time_rel': set([]),
        'arrival_time': set([]),
        'arrival_time_rel': set([]),
        'time': set([]),
        'time_rel': set([]),
        'duration': set([]),
        'ampm': set(['morning', 'am', 'pm', 'evening', 'night']),
        'date': set([]),
        'date_rel': set(['today', 'tomorrow', 'day_after_tomorrow', ]),
        'centre_direction': set(['dontcare', 'dontknow', 'to', 'from', '*', ]),
        'num_transfers': set([]),
        'vehicle': set(["bus", "tram", "metro", "train", "cable_car", "ferry", ]),
        'alternative': set(['dontcare', '1', '2', '3', '4', 'last', 'next', 'prev', ]),
    },

    'slot_attributes': {
        'silence': [],
        'silence_time': [],
        'ludait': [],
        'task': [
            'user_informs',
            #'user_requests', 'user_confirms',
            #'system_informs', 'system_requests', 'system_confirms',
            #'system_iconfirms', 'system_selects',
        ],
        'from_stop': [
            'user_informs', 'user_requests', 'user_confirms',
            'system_informs', 'system_requests', 'system_confirms',
            'system_iconfirms', 'system_selects',
        ],
        'to_stop': [
            'user_informs', 'user_requests', 'user_confirms',
            'system_informs', 'system_requests', 'system_confirms',
            'system_iconfirms', 'system_selects',
        ],
        'via_stop': [
            'user_informs', 'user_requests', 'user_confirms',
            #'system_informs', 'system_requests',
            'system_confirms', 'system_iconfirms',
            #'system_selects',
        ],
        'from_city': [
            'user_informs', 'user_requests', 'user_confirms',
            'system_confirms', 'system_iconfirms',
        ],
        'to_city': [
            'user_informs', 'user_requests', 'user_confirms',
            'system_confirms', 'system_iconfirms',
        ],
        'via_city': [
            'user_informs', 'user_requests', 'user_confirms',
            'system_confirms', 'system_iconfirms',
        ],
        'in_city': [
            'user_informs', 'user_requests', 'user_confirms',
            'system_confirms', 'system_iconfirms',
        ],
        'departure_time': [
            'user_informs', 'user_requests', 'user_confirms',
            'system_informs',
            #'system_requests',
            'system_confirms', 'system_iconfirms', 'system_selects',
            'absolute_time',
        ],

        'departure_time_rel': [
            'user_informs', 'user_requests', 'user_confirms',
            'system_informs',
            #'system_requests',
            'system_confirms', 'system_iconfirms', 'system_selects',
            'relative_time',
        ],
        'arrival_time': [
            'user_informs', 'user_requests', 'user_confirms',
            'system_informs',
            #'system_requests',
            'system_confirms', 'system_iconfirms', 'system_selects',
            'absolute_time',
        ],
        'arrival_time_rel': [
            'user_informs', 'user_requests', 'user_confirms',
            'system_informs',
            #'system_requests',
            'system_confirms', 'system_iconfirms', 'system_selects',
            'relative_time',
        ],
        'time': [
            'user_informs', 'user_requests', 'user_confirms',
            'system_confirms', 'system_iconfirms', 'system_selects',
            'absolute_time',
        ],
        'time_rel': [
            'user_informs', 'user_requests', 'user_confirms',
            'system_confirms', 'system_iconfirms', 'system_selects',
            'relative_time',
        ],
        'duration': [
            'user_requests',
            'relative_time',
        ],
        'ampm': [
            'user_informs', 'user_requests', 'user_confirms',
            'system_informs', 'system_requests', 'system_confirms',
            'system_iconfirms',
            'system_selects',
        ],
        # not implemented yet
        'date': [
            'user_informs', 'user_requests', 'user_confirms',
            'system_informs',
            #'system_requests',
            'system_confirms', 'system_iconfirms', 'system_selects',
        ],

        'date_rel': [
            'user_informs', 'user_requests', 'user_confirms',
            'system_informs',
            #'system_requests',
            'system_confirms', 'system_iconfirms', 'system_selects',
        ],
        'centre_direction': [
            'user_informs', 'user_requests', 'user_confirms',
            'system_informs', 'system_requests', 'system_confirms',
            'system_iconfirms', 'system_selects',
        ],
        'num_transfers': [
            'user_requests',
            'system_informs',
        ],
        'vehicle': [
            'user_informs', 'user_requests', 'user_confirms',
            'system_informs',
            #'system_requests',
            'system_confirms', 'system_iconfirms', 'system_selects',
        ],
        'alternative': [
            'user_informs',
            'system_informs',
            #'system_requests',
            'system_confirms',
            #'system_iconfirms',
            #'system_selects',
        ],
        'current_time': [
            'system_informs',
            'absolute_time',
        ],
        'route_alternative': [
            # this is necessary to be defined as it is a state variable used by the policy and automatically added to
            # the dialogue state
        ],

        'lta_task': [],
        'lta_time': [],
        'lta_date': [],
        'lta_departure_time': [],
        'lta_arrival_time': [],

        # not implemented yet
        'transfer_stops': [
            'user_requests',
        ],
        'temperature': [
            'temperature',
        ],
        'min_temperature': [
            'temperature_int',
        ],
        'max_temperature': [
            'temperature',
        ],
    },
    'reset_on_change': {
        # reset slots when any of the specified slots has changed, for matching changed slots a regexp is used
        'route_alternative': [
            '^from_stop$', '^to_stop$', '^via_stop$',
            '^departure_time$', '^departure_time_rel$',
            '^arrival_time$', '^arrival_time_rel$',
        ],
    },
    'last_talked_about': {
        # introduces new slots as a marginalisation of different inputs
        # this is performed by converting dialogue acts into inform acts
        'lta_time': {
            # the following means, every time I talk about the time, it supports the value time in slot time_sel
            'time': [('', '^time$', ''), ],
            # the following means, every time I talk about the time_rel, it supports the value time_rel in slot time_sel
            'time_rel': [('', '^time_rel$', ''), ],
            # as a consequence, the last slot the user talked about will have the highest probability in the ``time_sel``
            # slot
        },
        'lta_date': {
            'date': [('', '^date$', ''), ],
            'date_rel': [('', '^date_rel$', ''), ],
        },
        'lta_departure_time': {
            'departure_time': [('', '^departure_time$', ''), ],
            'departure_time_rel': [('', '^departure_time_rel$', ''), ],
            'time': [('', '^time$', ''), ],
            'time_rel': [('', '^time_rel$', ''), ],
        },
        'lta_arrival_time': {
            'arrival_time': [('', '^arrival_time$', ''), ],
            'arrival_time_rel': [('', '^arrival_time_rel$', ''), ],
        },
        'lta_task': {
            'weather': [('', '^task$', '^weather$'), ],
            'find_connection': [('', '^task$', '^find_connection$'), ('', '^departure_', ''), ('', '^arrival_', ''),
                                ('', '^from_stop$', ''), ('', '^to_stop$', ''),
                                ('', '^duration$', '')],
        },
    },

    'compatibility': {
        'stop_city': [
            'from_stop', 'to_stop', 'via_stop',
        ],
        'city_stop': [
            'from_city', 'to_city', 'via_city', 'in_city',
        ],
    },
    'compatible_values': {
        'stop_city': {},
        'city_stop': {},
    },

    'default_values': {
        'in_city': 'Praha',
    },

    # translation of the values for TTS output
    'value_translation': {
        'ampm': {
            'morning': 'ráno',
            'am': 'dopoledne',
            'pm': 'odpoledne',
            'evening': 'večer',
            'night': 'v noci'
        },
        'vehicle': {
            'BUS': 'autobusem',
            'INTERCITY_BUS': 'meziměstským autobusem',
            'TRAM': 'tramvají',
            'SUBWAY': 'metrem',
            'TRAIN': 'vlakem',
            'CABLE_CAR': 'lanovkou',
            'FERRY': 'přívozem',
            'TROLLEYBUS': 'trolejbusem',
        },
        'date_rel': {
            'today': 'dnes',
            'tomorrow': 'zítra',
            'day_after_tomorrow': 'pozítří'
        },
        'alternative': {
            'dontcare': 'libovolný',
            '1': 'první',
            '2': 'druhý',
            '3': 'třetí',
            '4': 'čtvrtý',
            'last': 'poslední',
            'next': 'předchozí',
            'prev': 'následující',
        }
    },
}


def add_slot_values_from_database(slot, category, exceptions=set()):
    for value in database.get(category, tuple()):
        if value not in exceptions:
            ontology['slots'][slot].add(value)

add_slot_values_from_database('from_stop', 'stop')
add_slot_values_from_database('to_stop', 'stop')
add_slot_values_from_database('via_stop', 'stop')
add_slot_values_from_database('from_city', 'city')
add_slot_values_from_database('to_city', 'city')
add_slot_values_from_database('via_city', 'city')
add_slot_values_from_database('in_city', 'city')
add_slot_values_from_database('departure_time', 'time', exceptions=set(['now']))
add_slot_values_from_database('departure_time_rel', 'time')
add_slot_values_from_database('arrival_time', 'time', exceptions=set(['now']))
add_slot_values_from_database('arrival_time_rel', 'time')
add_slot_values_from_database('time', 'time', exceptions=set(['now']))
add_slot_values_from_database('time_rel', 'time')
add_slot_values_from_database('date_rel', 'date_rel')


def load_compatible_values(fname, slot1, slot2):
    with codecs.open(fname, 'r', 'UTF-8') as fh:
        for line in fh:
            if line.startswith('#'):
                continue
            val_slot1, val_slot2 = line.strip().split('\t')
            # add to list of compatible values in both directions
            subset = ontology['compatible_values'][slot1 + '_' + slot2].get(val_slot1, set())
            ontology['compatible_values'][slot1 + '_' + slot2][val_slot1] = subset
            subset.add(val_slot2)
            subset = ontology['compatible_values'][slot2 + '_' + slot1].get(val_slot2, set())
            ontology['compatible_values'][slot2 + '_' + slot1][val_slot2] = subset
            subset.add(val_slot1)


dirname = os.path.dirname(os.path.abspath(__file__))
load_compatible_values(os.path.join(dirname, CITIES_STOPS_FNAME), 'city', 'stop')
