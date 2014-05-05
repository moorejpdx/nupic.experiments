# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2014, Numenta, Inc.  Unless you have purchased from
# Numenta, Inc. a separate commercial license for this software code, the
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

import os
import pickle

import numpy
# This is the class corresponding to the C++ optimized Temporal Pooler
#from nupic.research.TP10X2 import TP10X2 as TP
from nupic.research.TP import TP

from fluent.term import Term


class Model():


  def __init__(self,
               numberOfCols=16384, cellsPerColumn=8,
                initialPerm=0.5, connectedPerm=0.5,
                minThreshold=164, newSynapseCount=164,
                permanenceInc=0.1, permanenceDec=0.0,
                activationThreshold=164,
                pamLength=10,
                checkpointDir=None):

    self.tp = TP(numberOfCols=numberOfCols, cellsPerColumn=cellsPerColumn,
                initialPerm=initialPerm, connectedPerm=connectedPerm,
                minThreshold=minThreshold, newSynapseCount=newSynapseCount,
                permanenceInc=permanenceInc, permanenceDec=permanenceDec,
                
                # 1/2 of the on bits = (16384 * .02) / 2
                activationThreshold=activationThreshold,
                globalDecay=0, burnIn=1,
                #verbosity=3,  # who knows what this does...
                checkSynapseConsistency=False,
                pamLength=pamLength)

    self.checkpointDir = checkpointDir
    self.checkpointPklPath = None
    self.checkpointDataPath = None
    self._initCheckpoint()


  def _initCheckpoint(self):
    if self.checkpointDir:
      if not os.path.exists(self.checkpointDir):
        os.makedirs(self.checkpointDir)

      self.checkpointPklPath = self.checkpointDir + "/model.pkl"
      self.checkpointDataPath = self.checkpointDir + "/model.data"


  def canCheckpoint(self):
    return self.checkpointDir != None


  def hasCheckpoint(self):
    return (os.path.exists(self.checkpointPklPath) and
            os.path.exists(self.checkpointDataPath))


  def load(self):
    if not self.checkpointDir:
      raise(Exception("No checkpoint directory specified"))

    if not self.hasCheckpoint():
      raise(Exception("Could not find checkpoint file"))
      
    with open(self.checkpointPklPath, 'rb') as f:
      self.tp = pickle.load(f)

    self.tp.loadFromFile(self.checkpointDataPath)


  def save(self):
    if not self.checkpointDir:
      raise(Exception("No checkpoint directory specified"))

    self.tp.saveToFile(self.checkpointDataPath)

    with open(self.checkpointPklPath, 'wb') as f:
      pickle.dump(self.tp, f)


  def feedTerm(self, term, learn=True):
    """ Feed a Term to model, returning next predicted Term """
    tp = self.tp
    array = numpy.array(term.toArray(), dtype="uint32")
    tp.resetStats()
    tp.compute(array, enableLearn = learn, computeInfOutput = True)
    #print "ret:  " + repr(ret)
    #if ret.all() == array.all():
    #  print "EQUAL to input"
    ret = tp.getStats()
    #ret = tp.printStates()

    print "ret: " + repr(ret)
    print
    print
    print "*****************************************"

    predictedCells = tp.getPredictedState()
    predictedColumns = predictedCells.max(axis=1)
    
    predictedBitmap = predictedColumns.nonzero()[0].tolist()
    return Term().createFromBitmap(predictedBitmap)
  

  def resetSequence(self):
    print "RESET"
    self.tp.reset()
