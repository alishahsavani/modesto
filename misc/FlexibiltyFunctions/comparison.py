from __future__ import division

import logging
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from modesto.main import Modesto
import parameters
import math
import numpy as np
import os
# import graphs

logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s %(name)-36s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')
logger = logging.getLogger('Main.py')

"""

Settings

"""

n_buildings = 3
horizon = 24*1*3600
start_time = pd.Timestamp('20140101')

time_index = pd.date_range(start=start_time, periods=int(horizon/3600)+1, freq='H')
n_points = int(math.ceil(n_buildings / 2))

"""

Cases

"""

model_cases = {'Ideal':
               {'pipe_model': 'Ideal',
                'time_step': 'StSt',
                'building_model': 'RCmodel'},
               'Building':
               {'pipe_model': 'StSt',
                'time_step': 'StSt',
                'building_model': 'RCmodel'},
               'Pipe':
               {'pipe_model': 'Dynamic',
                'time_step': 'StSt',
                'building_model': 'Fixed'},
               'Combined':
               {'pipe_model': 'Dynamic',
                'time_step': 'StSt',
                'building_model': 'RCmodel'}
               }

flex_cases = {'Reference':
                  {'price_profile': 'constant'},
              'Flexibility':
                  {'price_profile': 'step'}
              }

streets = {'MixedStreet': ['SFH_T_5_ins_TAB', 'SFH_T_5_TAB', 'SFH_T_5_ins_TAB',
                           'SFH_T_5_TAB', 'SFH_T_5_ins_TAB', 'SFH_T_5_TAB',
                           'SFH_T_5_ins_TAB', 'SFH_T_5_TAB', 'SFH_T_5_ins_TAB',
                           'SFH_T_5_TAB'],
           'OldStreet': ['SFH_T_5_TAB', 'SFH_T_5_TAB', 'SFH_T_5_TAB',
                          'SFH_T_5_TAB', 'SFH_T_5_TAB', 'SFH_T_5_TAB',
                          'SFH_T_5_TAB', 'SFH_T_5_TAB', 'SFH_T_5_TAB',
                          'SFH_T_5_TAB'],
           'NewStreet': ['SFH_T_5_ins_TAB', 'SFH_T_5_ins_TAB', 'SFH_T_5_ins_TAB',
                         'SFH_T_5_ins_TAB', 'SFH_T_5_ins_TAB', 'SFH_T_5_ins_TAB',
                         'SFH_T_5_ins_TAB', 'SFH_T_5_ins_TAB', 'SFH_T_5_ins_TAB',
                         'SFH_T_5_ins_TAB']}

distribution_pipes = {'MixedStreet': [50] * n_points,
                      'OldStreet': [50] * n_points,
                      'NewStreet': [50] * n_points}

service_pipes = {'MixedStreet': [20] * n_buildings,
                 'OldStreet': [20] * n_buildings,
                 'NewStreet': [20] * n_buildings}

districts = []


pipe_models = {'Ideal': 'SimplePipe',
               'StSt': 'ExtensivePipe',
               'Dynamic': 'NodeMethod'}
price_profiles = {'constant': pd.Series(0, time_index),
                  'step': pd.Series([1]*int(len(time_index)*0.7) + [2]*int(len(time_index)-len(time_index)*0.7))}
building_models = {'RCmodel': 'RCmodel',
                   'Fixed': 'BuildingFixed'}
time_steps = {'StSt': 3600,
              'Dynamic': 300}

"""

Initializing results

"""

Building_heat_use = {}
Heat_injection = {}

"""

Setting up graph

"""


def street_graph(n_buildings, building_model, draw=True):
    """
    Generate the graph for a street

    :param n_points: The number of points to which 2 buildings are connected
    :return:
    """

    G = nx.DiGraph()

    G.add_node('Producer', x=0, y=0, z=0,
               comps={'plant': 'ProducerVariable'})

    for i in range(n_points):
        G.add_node('p' + str(i), x=30 * (i + 1), y=0, z=0,
                   comps={})
        G.add_node('Building' + str(i), x=30 * (i + 1), y=30, z=0,
                   comps={'building': building_model})

        if n_points + i + 1 <= n_buildings:
            G.add_node('Building' + str(n_points + i), x=30 * (i + 1), y=-30, z=0,
                       comps={'building': building_model})

    G.add_edge('Producer', 'p0', name='dist_pipe0')
    for i in range(n_points - 1):
        G.add_edge('p' + str(i), 'p' + str(i + 1), name='dist_pipe' + str(i + 1))

    for i in range(n_points):
        G.add_edge('p' + str(i), 'Building' + str(i), name='serv_pipe' + str(i))

        if n_points + i + 1 <= n_buildings:
            G.add_edge('p' + str(i), 'Building' + str(n_points + i), name='serv_pipe' + str(n_points + i))

    if draw:

        coordinates = {}
        for node in G.nodes:
            coordinates[node] = (G.nodes[node]['x'], G.nodes[node]['y'])

        nx.draw(G, coordinates, with_labels=True, node_size=0)
        plt.show()

    return G


"""

Running cases

"""

selected_flex_cases= ['Reference']
selected_model_cases = ['Ideal', 'Building', 'Pipe', 'Combined']
selected_street_cases = ['MixedStreet']
selected_district_cases = []


for case in selected_model_cases:
    Building_heat_use[case] = {}
    Heat_injection[case] = {}

    time_step = time_steps[model_cases[case]['time_step']]
    pipe_model = pipe_models[model_cases[case]['pipe_model']]
    graph = street_graph(n_buildings, building_models[model_cases[case]['building_model']], draw=False)

    optmodel = Modesto(horizon, time_step, pipe_model, graph)

    if pipe_model == 'NodeMethod':
        flag_nm = True
    else:
        flag_nm = False

    if pipe_model == 'SimplePipe':
        flag_i = True
    else:
        flag_i = False

    optmodel.change_params(parameters.get_general_params())

    for street in selected_street_cases:
        Building_heat_use[case][street] = {}
        Heat_injection[case][street] = {}

        for i in range(n_buildings):

            if flag_nm:
                b_params = parameters.get_building_params(flag_nm,
                                                          heat_profile=Building_heat_use['Building'][street]['Reference'][i])
            else:
                b_params = parameters.get_building_params(flag_nm, max_heat=3000, model_type=streets[street][i])

            optmodel.change_params(b_params, 'Building' + str(i), 'building')

            p_params = parameters.get_pipe_params(pipe_model, service_pipes[street][i])
            optmodel.change_params(p_params, None, 'serv_pipe' + str(i))

        for i in range(n_points):
            p_params = parameters.get_pipe_params(pipe_model, distribution_pipes[street][i])
            optmodel.change_params(p_params, None, 'dist_pipe' + str(i))

        for flex_case in selected_flex_cases:
            Building_heat_use[case][street][flex_case] = {}
            Heat_injection[case][street][flex_case] = {}

            cost = price_profiles[flex_cases[flex_case]['price_profile']]
            prod_params = parameters.get_producer_params(flag_nm, cost)
            optmodel.change_params(prod_params, 'Producer', 'plant')

            print '\n CASE: ', case, ' ', street, ' ', flex_case, '\n--------------------------------------\n'

            optmodel.compile(start_time)
            optmodel.set_objective('cost')

            optmodel.solve()

            for i in range(n_buildings):
                Building_heat_use[case][street][flex_case][i] = \
                    optmodel.get_result('heat_flow', node='Building' + str(i), comp='building', state=True)

            Heat_injection[case][street][flex_case] = optmodel.get_result('heat_flow', node='Producer', comp='plant')