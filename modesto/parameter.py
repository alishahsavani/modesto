from __future__ import division

import pandas as pd
import logging
import modesto.utils as ut

class Parameter(object):

    def __init__(self, name, description, unit, val=None):
        """
        Class describing a parameter

        :param name: Name of the parameter (str)
        :param description: Description of the parameter (str)
        :param unit: Unit of the parameter (e.g. K, W, m...) (str)
        :param val: Value of the parameter, if not given, it becomes None
        """

        self.name = name
        self.description = description
        self.unit = unit

        self.value = val

        self.logger = logging.getLogger('modesto.parameter.Parameter')
        self.logger.info('Initializing Parameter {}'.format(name))

    def change_value(self, new_val):
        """
        Change the value of the parameter

        :param new_val:
        :return:
        """
        self.value = new_val

    def check(self):
        """
        Check whether the value of the parameter is known, otherwise an error is raised

        """
        if self.value is None:
            return False
        else:
            return True

    def get_description(self):
        """

        :return: A description of the parameter
        """
        if self.value is None:
            return 'Description: {}\nUnit: {}'.format(self.description, self.unit)
        else:
            return 'Description: {}\nUnit: {}\nValue: {}'.format(self.description, self.unit, self.value)

    def get_value(self, time=None):
        """

        :return: Current value of the parameter
        """

        if self.value is None:
            self.logger.warning('{} does not have a value yet'.format(self.name))

        if (time is not None) and (not isinstance(self.value, pd.DataFrame)):
            self.logger.warning('{} is not a time series'.format(self.name))

        return self.value

    def v(self, time=None):
        return self.get_value(time)


class DesignParameter(Parameter):

    def __init__(self, name, description, unit, val=None):
        """
        Class that describes a design parameter

        :param name: Name of the parameter (str)
        :param description: Description of the parameter (str)
        :param unit: Unit of the parameter (e.g. K, W, m...) (str)
        :param val: Value of the parameter, if not given, it becomes None
        """

        Parameter.__init__(self, name, description, unit, val)


class StateParameter(Parameter):

    def __init__(self, name, description, unit, init_type, val=None, ub=None, lb=None, slack=False):
        """
        Class that describes an initial state parameter

        :param name: Name of the parameter (str)
        :param description: Description of the parameter (str)
        :param unit: Unit of the parameter (e.g. K, W, m...) (str)
        :param init_type: Type of initialization constraint (str):
        Possibilities are: fixedVal: A value is chosen by te user
                           cyclic: Begin and end state must be equel
                           free: Begin state can be freely chosen by optimization
        :param val: Value of the parameter, if not given, it becomes None
        """

        Parameter.__init__(self, name, description, unit, val)

        self.init_types = ['fixedVal', 'cyclic', 'free']
        # TODO FixedVal, documentation!
        assert init_type in self.init_types, '%s is not an allowed type of initialization constraint'
        self.init_type = init_type

        self.ub = ub
        self.lb = lb
        self.slack = slack

    def change_init_type(self, new_type):
        """
        Change the type of initialization constraint associated with the parameter

        :param new_type: Name of the new type of initialization constraint
        """

        if new_type not in self.init_types:
            raise IndexError('%s is not an allowed type of initialization constraint')

        self.init_type = new_type

    def change_upper_bound(self, new_ub):
        """
        Change the allowed upper value of a state,
        if None, no upper bound will be set

        :param new_ub: New value of the upper bound
        """
        self.ub = new_ub

    def change_lower_bound(self, new_lb):
        """
        Change the allowed lower value of a state,
        if None, no lower bound will be set

        :param new_lb: New value of the upper bound
        """
        self.lb = new_lb

    def change_slack(self, new_slack):
        """
        Change value of the slack,
        If False, no slack for this state will be introduced
        if True, a slack for this variable will be introduced

        :param new_slack: New value of the upper bound
        """
        self.slack = new_slack

    def get_description(self):
        return Parameter.get_description(self) + '\nInitType: {} \nUpper bound: {} \nLower bound: {} \nSlack: {}'\
            .format(self.init_type, self.ub, self.lb, self.slack)


class DataFrameParameter(Parameter):

    def __init__(self, name, description, unit, time_step=None, val=None):
        """
        Class that describes a parameter with a value consisting of a dataframe

        :param name: Name of the parameter (str)
        :param description: Description of the parameter (str)
        :param unit: Unit of the parameter (e.g. K, W, m...) (str)
        :param time_step: Sampling time of the optimization problem
        :param val: Value of the parameter, if not given, it becomes None
        """
        if isinstance(val, pd.DataFrame):
            raise TypeError('The value of this parameter (user/weather data)should be a pandas DataFrame')

        self.time_step = time_step
        Parameter.__init__(self, name, description, unit, val)

    def get_value(self, time=None):
        """
        Returns the value of the parameter at a certain time

        :param time:
        :return:
        """

        if time is None:
            return self.value.ix[:, 0].tolist()
        elif self.value is None:
            print 'Warning: {} does not have a value yet'.format(self.name)
            return None
        else:
            if time >= len(self.value.index):
                raise IndexError('{} is not a valid index for the {} parameter'.format(time, self.name))
            return self.value.iloc[time][0]

    def v(self, time=None):
        return self.get_value(time)

    def change_value(self, new_val):
        """
        Change the value of the Dataframe parameter

        :param new_val: New value of the parameter
        """

        assert isinstance(new_val, pd.DataFrame), \
            'The new value of {} should be a pandas DataFrame'.format(self.name)

        if self.time_step is not None:
            new_val = ut.resample(new_val, new_sample_time=self.time_step)

        self.value = new_val


class UserDataParameter(DataFrameParameter):

    def __init__(self, name, description, unit, val=None):
        """
        Class that describes a user data parameter

        :param name: Name of the parameter (str)
        :param description: Description of the parameter (str)
        :param unit: Unit of the parameter (e.g. K, W, m...) (str)
        :param val: Value of the parameter, if not given, it becomes None
        """

        DataFrameParameter.__init__(self, name, description, unit, val)


class WeatherDataParameter(DataFrameParameter):
    def __init__(self, name, description, unit, val=None):
        """
        Class that describes a weather data parameter

        :param name: Name of the parameter (str)
        :param description: Description of the parameter (str)
        :param unit: Unit of the parameter (e.g. K, W, m...) (str)
        :param val: Value of the parameter, if not given, it becomes None
        """

        DataFrameParameter.__init__(self, name, description, unit, val)
