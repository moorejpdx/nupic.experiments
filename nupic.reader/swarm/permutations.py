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

"""
Template file used by ExpGenerator to generate the actual
permutations.py file by replacing $XXXXXXXX tokens with desired values.

This permutations.py file was generated by:
'/Users/moorej/sandbox/nupic/nupic/build/release/lib/python2.7/site-packages/nupic/frameworks/opf/exp_generator/ExpGenerator.pyc'
"""

import os

from nupic.swarming.permutationhelpers import *

# The name of the field being predicted.  Any allowed permutation MUST contain
# the prediction field.
# (generated from PREDICTION_FIELD)
predictedField = 'word'




permutations = {
  'aggregationInfo': {   'days': 0,
    'fields': [],
    'hours': 0,
    'microseconds': 0,
    'milliseconds': 0,
    'minutes': 0,
    'months': 0,
    'seconds': 0,
    'weeks': 0,
    'years': 0},

  'modelParams': {
    

    'sensorParams': {
      'encoders': {
          u'word': PermuteEncoder(fieldName='word', encoderClass='SDRCategoryEncoder', w=21, n=121, ),
  '_classifierInput': dict(classifierOnly=True, n=121, fieldname='word', w=21, type='SDRCategoryEncoder', ),
      },
    },

    'spParams': {
        'synPermInactiveDec': PermuteFloat(0.0003, 0.1),

    },

    'tpParams': {
        'activationThreshold': PermuteInt(12, 16),
  'minThreshold': PermuteInt(9, 12),
  'pamLength': PermuteInt(1, 5),

    },

    'clParams': {
        'alpha': PermuteFloat(0.0001, 0.1),

    },
  }
}


# Fields selected for final hypersearch report;
# NOTE: These values are used as regular expressions by RunPermutations.py's
#       report generator
# (fieldname values generated from PERM_PREDICTED_FIELD_NAME)
report = [
          '.*word.*',
         ]

# Permutation optimization setting: either minimize or maximize metric
# used by RunPermutations.
# NOTE: The value is used as a regular expressions by RunPermutations.py's
#       report generator
# (generated from minimize = "multiStepBestPredictions:multiStep:errorMetric='avg_err':steps=\[1, 2, 3, 4, 5, 6\]:window=1000:field=word")
minimize = "multiStepBestPredictions:multiStep:errorMetric='avg_err':steps=\[1, 2, 3, 4, 5, 6\]:window=1000:field=word"

minParticlesPerSwarm = 5

inputPredictedField = 'auto'







maxModels = 200

#############################################################################
def permutationFilter(perm):
  """ This function can be used to selectively filter out specific permutation
  combinations. It is called by RunPermutations for every possible permutation
  of the variables in the permutations dict. It should return True for valid a
  combination of permutation values and False for an invalid one.

  Parameters:
  ---------------------------------------------------------
  perm: dict of one possible combination of name:value
        pairs chosen from permutations.
  """

  # An example of how to use this
  #if perm['__consumption_encoder']['maxval'] > 300:
  #  return False;
  #
  return True
