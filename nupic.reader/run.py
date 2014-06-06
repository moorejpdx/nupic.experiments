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
import datetime
import os
import io
import re
from optparse import OptionParser

#nupic libraries
from nupic.frameworks.opf.modelfactory import ModelFactory
from utils import nupic_output

#pattern libraries
from pattern.en import parsetree


DESCRIPTION = (
  "Starts a NuPIC model from the model params returned by the swarm\n"
  "and pushes each line of input from the gym into the model. Results\n"
  "are written to an output file (default) \n"
  "NOTE: You must run ./swarm.py before this, because model parameters\n"
  "are required to run NuPIC.\n"
)
MODEL_PARAMS_DIR = "./model_params"


def createModel(modelParams):
  model = ModelFactory.create(modelParams)
  model.enableInference({"predictedField": "word"})
  return model



def getModelParamsFromName(filePath):
  importName = "model_params.%s_model_params" % (
    filePath.replace(" ", "_").replace("-", "_")
  )
  importName = "model_params.Universal_model_params"
  print "Importing model params from %s" % importName
  try:
    importedModelParams = importlib.import_module(importName).MODEL_PARAMS
  except ImportError:
    raise Exception("No model params exist for '%s'. Run swarm first!"
                    % filePath)
  return importedModelParams



def runIoThroughNupic(inputData, model, filePath):
  name = os.path.splitext(os.path.basename(filePath))[0]
  #inputFile = open(inputData, "rb")
  # skip header rows
  #print inputFile

  #print ("[%s]:[%s]", ['word'], ['prediction'])

#  output = nupic_output.NuPICFileOutput([name])

  with io.open(filePath, "rU") as f:
    l_text = f.read()
    print l_text

    # cleanup periods to always have 2 spaces after them if there's a single space
    l_text = re.sub(r'([!\.\?]) (\w)', r'\1  \2', l_text)
    # cleanup odd unicode quotes to be normal single quotes
    l_text = re.sub(u'[\u2019]', r"'", l_text)
    # unicode dash to normal dash
    l_text = re.sub(u'[\u2014]', r"-", l_text)
    # unicode dash to double quotes
    l_text = re.sub(u'[\u201c]', r'"', l_text)
    l_text = re.sub(u'[\u201d]', r'"', l_text)

    # remove the rest of the unicode "stuff"
    l_text = l_text.encode('ascii','ignore')

    l_parsetree = parsetree(l_text)

    #build RE matches
    re_first_letter = re.compile(r'^[A-Z]')
    re_punct = re.compile(r'[\.\?!]$')

    for sentence in l_parsetree:
      print sentence.string
      match = re_first_letter.search(sentence.string.strip())
      if not match:
        #print ("    NO CAPS")
        continue

      match = re_punct.search(sentence.string.strip())
      if not match:
        #print ("    NO PUNCTUATION")
        continue

      print sentence.string
      for l_word in sentence.words:
        #print "  word: " + repr(l_word)
        print "  word: " + l_word.string

        result = model.run({
          "word": word,
        })
        #prediction1 = result.inferences["multiStepBestPredictions"][1]
        #prediction2 = result.inferences["multiStepBestPredictions"][2]
        #prediction3 = result.inferences["multiStepBestPredictions"][3]
        #prediction4 = result.inferences["multiStepBestPredictions"][4]
        #prediction5 = result.inferences["multiStepBestPredictions"][5]
        #prediction6 = result.inferences["multiStepBestPredictions"][6]
        #print ("prediction: %s, %s, %s,%s,%s,%s" %  prediction1, prediction2,prediction3,prediction4,prediction5,prediction6)
        #output.write([word], [prediction1])

        print "result:  " + repr(result)
        print
        print "****************************************************"

  #output.close()


def runModel(filePath):
  name = os.path.splitext(os.path.basename(filePath))[0]
  print "Creating model from %s..." % name
  #model = createModel(getModelParamsFromName(name)) 
  model = None
  inputData = "%s.txt" % (filePath.replace(" ", "_"))
  runIoThroughNupic(inputData, model, filePath)



if __name__ == "__main__":
  print DESCRIPTION
  parser = OptionParser("%prog textfile [options]")
  parser.add_option(
      "--checkpoint",
      dest="checkpoint",
      help="Directory to save model to and load model from")
  parser.add_option(
      "-r",
      "--reset-sequences",
      dest="resetSequences",
      action="store_true",
      default=False,
      help="Reset the model sequence after every line")

  (options, args) = parser.parse_args()

  if not len(args):
    parser.print_help()
    print
    raise(Exception("textfile required"))

  runModel(args[0])
#  runModel(MODEL_NAME)

