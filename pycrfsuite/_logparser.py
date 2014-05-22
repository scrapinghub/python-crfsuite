# -*- coding: utf-8 -*-
from __future__ import absolute_import
import re


class TrainLogParser(object):

    def __init__(self):
        self.state = None
        self.buf = []
        self.featgen_percent = -2
        self.featgen_num_features = None
        self.featgen_seconds = None
        self.optimization_log = []
        self.iterations = []
        self.last_iteration = None
        self.training_seconds = None
        self.storing_seconds = None
        self.storing_log = []

    def feed(self, line):
        if self.state is None:
            self.state = 'STARTING'
            self.STARTING(line)
            return 'start'
        meth = getattr(self, self.state)
        return meth(line)

    def STARTING(self, line):
        if line.startswith('Feature generation'):
            self.state = 'FEATGEN'

    def FEATGEN(self, line):
        if line in "0123456789.10":
            self.featgen_percent += 2
            return 'featgen_progress'

        m = re.match(r"Number of features: (\d+)", line)
        if m:
            self.featgen_num_features = int(m.group(1))
            return None

        if self._seconds(line) is not None:
            self.featgen_seconds = self._seconds(line)
            self.state = 'AFTER_FEATGEN'
            return 'featgen_end'

    def AFTER_FEATGEN(self, line):
        if self._iteration_head(line) is not None:
            self.state = 'ITERATION'
            return self.ITERATION(line)

        self.optimization_log.append(line)

    def ITERATION(self, line):
        if self._iteration_head(line) is not None:
            self.last_iteration = {
                'num': self._iteration_head(line),
                'log': [],
            }
            self.iterations.append(self.last_iteration)
        elif line == '\n':
            self.state = 'AFTER_ITERATION'
            return 'iteration'
        else:
            self.last_iteration['log'].append(line)

    def AFTER_ITERATION(self, line):
        if self._iteration_head(line) is not None:
            self.state = 'ITERATION'
            return self.ITERATION(line)

        m = re.match(r"Total seconds required for training: (\d+\.\d+)", line)
        if m:
            self.training_seconds = float(m.group(1))

        if line.startswith('Storing the model'):
            self.state = 'STORING'
            return 'optimization_end'

    def STORING(self, line):
        if line == '\n':
            return 'end'
        elif self._seconds(line):
            self.storing_seconds = self._seconds(line)
        self.storing_log.append(line)

    def _iteration_head(self, line):
        m = re.match(r'\*{5} Iteration #(\d+) \*{5}\n', line)
        if m:
            return int(m.group(1))

    def _seconds(self, line):
        m = re.match(r'Seconds required: (\d+\.\d+)', line)
        if m:
            return float(m.group(1))

    def __repr__(self):
        return "TrainLogParser()"





