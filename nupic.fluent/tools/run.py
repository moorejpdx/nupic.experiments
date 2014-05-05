#!/usr/bin/env python
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
Groups together code used for creating a NuPIC model and dealing with IO.
(This is a component of the One Hot Gym Prediction Tutorial.)
"""
import importlib
import sys
import csv
import datetime

from nupic.data.inference_shifter import InferenceShifter
from nupic.frameworks.opf.modelfactory import ModelFactory

import nupic_output


DESCRIPTION = (
  "Starts a NuPIC model from the model params returned by the swarm\n"
  "and pushes each line of input from the gym into the model. Results\n"
  "are written to an output file (default) or plotted dynamically if\n"
  "the --plot option is specified.\n"
  "NOTE: You must run ./swarm.py before this, because model parameters\n"
  "are required to run NuPIC.\n"
)
MODEL_NAME = "swarm_foxeat"
DATA_DIR = "./data/associations"
MODEL_PARAMS_DIR = "./model_params"
# '7/2/10 0:00'
#DATE_FORMAT = "%m/%d/%y %H:%M"


def createModel(modelParams):
  model = ModelFactory.create(modelParams)
  model.enableInference({"predictedField": "object"})
  return model



def getModelParamsFromName(modelName):
  importName = "model_params.%s_model_params" % (
    modelName.replace(" ", "_").replace("-", "_")
  )
  print "Importing model params from %s" % importName
  try:
    importedModelParams = importlib.import_module(importName).MODEL_PARAMS
  except ImportError:
    raise Exception("No model params exist for '%s'. Run swarm first!"
                    % modelName)
  return importedModelParams



def runIoThroughNupic(inputData, model, modelName, plot):
  inputFile = open(inputData, "rb")
  csvReader = csv.reader(inputFile)
  # skip header rows
  csvReader.next()
  csvReader.next()
  csvReader.next()

  shifter = InferenceShifter()
  if plot:
    output = nupic_output.NuPICPlotOutput([modelName])
  else:
    output = nupic_output.NuPICFileOutput([modelName])

  counter = 0
  for row in csvReader:
    counter += 1
    if (counter % 100 == 0):
      print "Read %i lines..." % counter
    #timestamp = datetime.datetime.strptime(row[0], DATE_FORMAT)
    #consumption = float(row[1])
    subject=row[0]
    verb=row[1]
    obj=row[2]
    result = model.run({
      "subject": subject,
      "verb": verb,
      "object":obj
    })

    if plot:
      result = shifter.shift(result)

    print "result: " + repr(result.inferences["multiStepBestPredictions"])
    prediction = result.inferences["multiStepBestPredictions"][1]
    output.write([subject], [verb], [obj], [prediction])

  inputFile.close()
  output.close()



def runModel(modelName, plot=False):
  print "Creating model from %s..." % modelName
  model = createModel(getModelParamsFromName(modelName))
  inputData = "%s/%s.txt" % (DATA_DIR, modelName.replace(" ", "_"))
  runIoThroughNupic(inputData, model, modelName, plot)



if __name__ == "__main__":
  print DESCRIPTION
  plot = False
  args = sys.argv[1:]
  if "--plot" in args:
    plot = True
  runModel(MODEL_NAME, plot=plot)
