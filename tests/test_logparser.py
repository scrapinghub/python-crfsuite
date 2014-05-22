# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from pycrfsuite._logparser import TrainLogParser

events = [
    'start',
    'featgen_start',
    'featgen_progress',
    'featgen_end',
    'optimization_start',
    'iteration',
    'optimization_end',
    'storing_start',
    'storing_end',
    'end',
]

log1 = [
    'Holdout group: 2\n',
    '\n',
    'Feature generation\n',
    'type: CRF1d\n',
    'feature.minfreq: 0.000000\n',
    'feature.possible_states: 0\n',
    'feature.possible_transitions: 1\n',
    '0', '.', '.', '.', '.',
    '1', '.', '.', '.', '.',
    '2', '.', '.', '.', '.',
    '3', '.', '.', '.', '.',
    '4', '.', '.', '.', '.',
    '5', '.', '.', '.', '.',
    '6', '.', '.', '.', '.',
    '7', '.', '.', '.', '.',
    '8', '.', '.', '.', '.',
    '9', '.', '.', '.', '.',
    '10',
    '\n',
    'Number of features: 3948\n',
    'Seconds required: 0.022\n',
    '\n',

    'L-BFGS optimization\n',
    'c1: 1.000000\n',
    'c2: 0.001000\n',
    'num_memories: 6\n',
    'max_iterations: 5\n',
    'epsilon: 0.000010\n',
    'stop: 10\n',
    'delta: 0.000010\n',
    'linesearch: MoreThuente\n',
    'linesearch.max_iterations: 20\n',
    '\n',
    '***** Iteration #1 *****\n',
    'Loss: 1450.519004\n',
    'Feature norm: 1.000000\n',
    'Error norm: 713.784994\n',
    'Active features: 1794\n',
    'Line search trials: 1\n',
    'Line search step: 0.000228\n',
    'Seconds required for this iteration: 0.008\n',
    'Performance by label (#match, #model, #ref) (precision, recall, F1):\n',
    '    B-LOC: (0, 0, 6) (0.0000, 0.0000, 0.0000)\n',
    '    O: (306, 339, 306) (0.9027, 1.0000, 0.9488)\n',
    '    B-ORG: (0, 0, 9) (0.0000, 0.0000, 0.0000)\n',
    '    B-PER: (0, 0, 3) (0.0000, 0.0000, 0.0000)\n',
    '    I-PER: (0, 0, 4) (0.0000, 0.0000, 0.0000)\n',
    '    B-MISC: (0, 0, 5) (0.0000, 0.0000, 0.0000)\n',
    '    I-ORG: (0, 0, 5) (0.0000, 0.0000, 0.0000)\n',
    '    I-LOC: (0, 0, 1) (0.0000, 0.0000, 0.0000)\n',
    '    I-MISC: (0, 0, 0) (******, ******, ******)\n',
    'Macro-average precision, recall, F1: (0.100295, 0.111111, 0.105426)\n',
    'Item accuracy: 306 / 339 (0.9027)\n',
    'Instance accuracy: 3 / 10 (0.3000)\n',
    '\n',
    '***** Iteration #2 *****\n',
    'Loss: 1363.687719\n',
    'Feature norm: 1.178396\n',
    'Error norm: 370.827506\n',
    'Active features: 1540\n',
    'Line search trials: 1\n',
    'Line search step: 1.000000\n',
    'Seconds required for this iteration: 0.004\n',
    'Performance by label (#match, #model, #ref) (precision, recall, F1):\n',
    '    B-LOC: (0, 0, 6) (0.0000, 0.0000, 0.0000)\n',
    '    O: (306, 339, 306) (0.9027, 1.0000, 0.9488)\n',
    '    B-ORG: (0, 0, 9) (0.0000, 0.0000, 0.0000)\n',
    '    B-PER: (0, 0, 3) (0.0000, 0.0000, 0.0000)\n',
    '    I-PER: (0, 0, 4) (0.0000, 0.0000, 0.0000)\n',
    '    B-MISC: (0, 0, 5) (0.0000, 0.0000, 0.0000)\n',
    '    I-ORG: (0, 0, 5) (0.0000, 0.0000, 0.0000)\n',
    '    I-LOC: (0, 0, 1) (0.0000, 0.0000, 0.0000)\n',
    '    I-MISC: (0, 0, 0) (******, ******, ******)\n',
    'Macro-average precision, recall, F1: (0.100295, 0.111111, 0.105426)\n',
    'Item accuracy: 306 / 339 (0.9027)\n',
    'Instance accuracy: 3 / 10 (0.3000)\n',
    '\n',
    '***** Iteration #3 *****\n',
    'Loss: 1309.171814\n',
    'Feature norm: 1.266322\n',
    'Error norm: 368.739493\n',
    'Active features: 1308\n',
    'Line search trials: 1\n',
    'Line search step: 1.000000\n',
    'Seconds required for this iteration: 0.003\n',
    'Performance by label (#match, #model, #ref) (precision, recall, F1):\n',
    '    B-LOC: (0, 0, 6) (0.0000, 0.0000, 0.0000)\n',
    '    O: (306, 339, 306) (0.9027, 1.0000, 0.9488)\n',
    '    B-ORG: (0, 0, 9) (0.0000, 0.0000, 0.0000)\n',
    '    B-PER: (0, 0, 3) (0.0000, 0.0000, 0.0000)\n',
    '    I-PER: (0, 0, 4) (0.0000, 0.0000, 0.0000)\n',
    '    B-MISC: (0, 0, 5) (0.0000, 0.0000, 0.0000)\n',
    '    I-ORG: (0, 0, 5) (0.0000, 0.0000, 0.0000)\n',
    '    I-LOC: (0, 0, 1) (0.0000, 0.0000, 0.0000)\n',
    '    I-MISC: (0, 0, 0) (******, ******, ******)\n',
    'Macro-average precision, recall, F1: (0.100295, 0.111111, 0.105426)\n',
    'Item accuracy: 306 / 339 (0.9027)\n',
    'Instance accuracy: 3 / 10 (0.3000)\n',
    '\n',
    '***** Iteration #4 *****\n',
    'Loss: 1019.561634\n',
    'Feature norm: 1.929814\n',
    'Error norm: 202.976154\n',
    'Active features: 1127\n',
    'Line search trials: 1\n',
    'Line search step: 1.000000\n',
    'Seconds required for this iteration: 0.003\n',
    'Performance by label (#match, #model, #ref) (precision, recall, F1):\n',
    '    B-LOC: (0, 0, 6) (0.0000, 0.0000, 0.0000)\n',
    '    O: (306, 339, 306) (0.9027, 1.0000, 0.9488)\n',
    '    B-ORG: (0, 0, 9) (0.0000, 0.0000, 0.0000)\n',
    '    B-PER: (0, 0, 3) (0.0000, 0.0000, 0.0000)\n',
    '    I-PER: (0, 0, 4) (0.0000, 0.0000, 0.0000)\n',
    '    B-MISC: (0, 0, 5) (0.0000, 0.0000, 0.0000)\n',
    '    I-ORG: (0, 0, 5) (0.0000, 0.0000, 0.0000)\n',
    '    I-LOC: (0, 0, 1) (0.0000, 0.0000, 0.0000)\n',
    '    I-MISC: (0, 0, 0) (******, ******, ******)\n',
    'Macro-average precision, recall, F1: (0.100295, 0.111111, 0.105426)\n',
    'Item accuracy: 306 / 339 (0.9027)\n',
    'Instance accuracy: 3 / 10 (0.3000)\n',
    '\n',
    '***** Iteration #5 *****\n',
    'Loss: 782.637378\n',
    'Feature norm: 3.539391\n',
    'Error norm: 121.725020\n',
    'Active features: 1035\n',
    'Line search trials: 1\n',
    'Line search step: 1.000000\n',
    'Seconds required for this iteration: 0.003\n',
    'Performance by label (#match, #model, #ref) (precision, recall, F1):\n',
    '    B-LOC: (2, 5, 6) (0.4000, 0.3333, 0.3636)\n',
    '    O: (305, 318, 306) (0.9591, 0.9967, 0.9776)\n',
    '    B-ORG: (0, 0, 9) (0.0000, 0.0000, 0.0000)\n',
    '    B-PER: (2, 4, 3) (0.5000, 0.6667, 0.5714)\n',
    '    I-PER: (4, 12, 4) (0.3333, 1.0000, 0.5000)\n',
    '    B-MISC: (0, 0, 5) (0.0000, 0.0000, 0.0000)\n',
    '    I-ORG: (0, 0, 5) (0.0000, 0.0000, 0.0000)\n',
    '    I-LOC: (0, 0, 1) (0.0000, 0.0000, 0.0000)\n',
    '    I-MISC: (0, 0, 0) (******, ******, ******)\n',
    'Macro-average precision, recall, F1: (0.243606, 0.332970, 0.268070)\n',
    'Item accuracy: 313 / 339 (0.9233)\n',
    'Instance accuracy: 3 / 10 (0.3000)\n',
    '\n',
    'L-BFGS terminated with the maximum number of iterations\n',
    'Total seconds required for training: 0.022\n',
    '\n',
    'Storing the model\n',
    'Number of active features: 1035 (3948)\n',
    'Number of active attributes: 507 (3350)\n',
    'Number of active labels: 9 (9)\n',
    'Writing labels\n',
    'Writing attributes\n',
    'Writing feature references for transitions\n',
    'Writing feature references for attributes\n',
    'Seconds required: 0.003\n',
    '\n'
]

log2 = [
    'Feature generation\n', # featgen_start
    'type: CRF1d\n',
    'feature.minfreq: 0.000000\n',
    'feature.possible_states: 0\n',
    'feature.possible_transitions: 1\n',
    '0', '.', '.', '.', '.',  # featgen_progress
    '1', '.', '.', '.', '.',
    '2', '.', '.', '.', '.',
    '3', '.', '.', '.', '.',
    '4', '.', '.', '.', '.',
    '5', '.', '.', '.', '.',
    '6', '.', '.', '.', '.',
    '7', '.', '.', '.', '.',
    '8', '.', '.', '.', '.',
    '9', '.', '.', '.', '.',
    '10',
    '\n',
    'Number of features: 4379\n',
    'Seconds required: 0.021\n',  # featgen_end
    '\n',
    'Averaged perceptron\n',
    'max_iterations: 5\n',
    'epsilon: 0.000000\n',
    '\n',
    '***** Iteration #1 *****\n',  # iteration
    'Loss: 16.359638\n',
    'Feature norm: 112.848688\n',
    'Seconds required for this iteration: 0.005\n',  # iteration end
    '\n',
    '***** Iteration #2 *****\n',
    'Loss: 12.449970\n',
    'Feature norm: 126.174821\n',
    'Seconds required for this iteration: 0.004\n',
    '\n',
    '***** Iteration #3 *****\n',
    'Loss: 9.451751\n',
    'Feature norm: 145.482678\n',
    'Seconds required for this iteration: 0.003\n',
    '\n',
    '***** Iteration #4 *****\n',
    'Loss: 8.652287\n',
    'Feature norm: 155.495167\n',
    'Seconds required for this iteration: 0.003\n',
    '\n',
    '***** Iteration #5 *****\n',
    'Loss: 7.442703\n',
    'Feature norm: 166.818487\n',
    'Seconds required for this iteration: 0.002\n',
    '\n',
    'Total seconds required for training: 0.017\n',  # optimization_end
    '\n',
    'Storing the model\n',  # storing_start
    'Number of active features: 2265 (4379)\n',
    'Number of active attributes: 1299 (3350)\n',
    'Number of active labels: 9 (9)\n',
    'Writing labels\n',
    'Writing attributes\n',
    'Writing feature references for transitions\n',
    'Writing feature references for attributes\n',
    'Seconds required: 0.007\n',  # storing_end
    '\n'  # end
]


# def test_parser():
#     parser = TrainLogParser()
#     for line in log2:
#         # print(line, end='')
#         event = parser.feed(line)
#         if event:
#             print('--------> %s' % event)
#
#         if event == 'featgen_progress':
#             print(parser.featgen_percent)
#
#         elif event == 'featgen_end':
#             print(parser.featgen_seconds, parser.featgen_num_features)
#
#         elif event == 'iteration':
#             print(parser.last_iteration['num'])
#             print(''.join(parser.last_iteration['log']))
#
#         elif event == 'optimization_end':
#             print(parser.training_seconds)
#             print(parser.iterations)
#             print(parser.optimization_log)
#
#         elif event == 'end':
#             print(parser.storing_seconds)
#             print(parser.storing_log)
#
#     assert 0
