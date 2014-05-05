# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2013, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------


## This file defines parameters for a prediction experiment.

###############################################################################
#                                IMPORTANT!!!
# This params file is dynamically generated by the RunExperimentPermutations
# script. Any changes made manually will be over-written the next time
# RunExperimentPermutations is run!!!
###############################################################################


from nupic.frameworks.opf.expdescriptionhelpers import importBaseDescription

# the sub-experiment configuration
config ={
  'aggregationInfo' : {'seconds': 0, 'fields': [], 'months': 0, 'days': 0, 'years': 0, 'hours': 0, 'microseconds': 0, 'weeks': 0, 'minutes': 0, 'milliseconds': 0},
  'modelParams' : {'sensorParams': {'encoders': {'_classifierInput': {'fieldname': 'object', 'classifierOnly': True, 'type': 'SDRCategoryEncoder', 'w': 21, 'n': 121}, u'verb': None, u'object': {'type': 'SDRCategoryEncoder', 'fieldname': 'object', 'name': 'object', 'w': 21, 'n': 121}, u'subject': {'type': 'SDRCategoryEncoder', 'fieldname': 'subject', 'name': 'subject', 'w': 21, 'n': 121}}}, 'spParams': {'synPermInactiveDec': 0.0056410714285714293}, 'tpParams': {'minThreshold': 11, 'activationThreshold': 13, 'pamLength': 1}, 'clParams': {'alpha': 0.0054517857142857146}},

}

mod = importBaseDescription('../description.py', config)
locals().update(mod.__dict__)
