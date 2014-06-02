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

import io
import re
from optparse import OptionParser

#pattern libraries
from pattern.en import parsetree


def makeWordlist(filePath):

  with io.open(filePath, "rU") as f:
    l_text = f.read()
    #print l_text

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
      #print sentence.string
      match = re_first_letter.search(sentence.string.strip())
      if not match:
        #print ("    NO CAPS")
        continue

      match = re_punct.search(sentence.string.strip())
      if not match:
        #print ("    NO PUNCTUATION")
        continue

      #print sentence.string
      for l_word in sentence.words:
        #print "  word: " + repr(l_word)
        print l_word.string



if __name__ == "__main__":
  parser = OptionParser("%prog textfile ")

  (options, args) = parser.parse_args()

  if len(args) != 1:
    parser.print_help()
    print
    raise(Exception("%prog textfile"))


  makeWordlist(args[0])

