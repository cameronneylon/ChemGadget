#!/usr/bin/env python
#
#!/usr/bin/python2.4
#
# 
"""ChemGadget - a ChemSpider robot for Wave.

Gives you the an image of a named chemical for text in a blip. 
"""

__author__ = 'cameron.neylon@stfc.ac.uk (Cameron Neylon)'

from waveapi import events
from waveapi import model
from waveapi import robot
from waveapi import document
import re

import ChemSpiPy

def OnBlipSubmitted(properties, context):
    blip = context.GetBlipById(properties['blipId'])
    contents = blip.GetDocument().GetText()
    key = '(chem)'
    leftdelim = '\\['
    query = '([a-zA-Z0-9-]{1,20})'
    image = '(;image)'
    rightdelim = '\\]'

    compiledregex = re.compile(key+leftdelim+query+image+rightdelim, re.IGNORECASE|re.DOTALL)
    chemicallist = compiledregex.finditer(contents)


    if chemicallist != None:
        compoundlist = []
        for chemicalname in chemicallist:  # Just pull off first one in list
            r = document.Range(0,0)
            r.start = chemicalname.start()
            r.end = chemicalname.end() + 1
            query = chemicalname.group(2)
            compound = ChemSpiPy.simplesearch(query) # obtain chemspider ID
            compoundlist.append(compound)

        compound = compoundlist[0]
        if compound.molfile == '':
            compound.molfile = """241
  -OEChem-10200920453D

  6  6  0     0  0  0  0  0  0999 V2000
   -0.7040   -1.2194   -0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.7040   -1.2194   -0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
   -1.4081   -0.0000   -0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    1.4081    0.0000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
   -0.7040    1.2194    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.7040    1.2194   -0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
  1  2  2  0  0  0  0
  1  3  1  0  0  0  0
  2  4  1  0  0  0  0
  3  5  2  0  0  0  0
  4  6  2  0  0  0  0
  5  6  1  0  0  0  0
M  END
"""
        gadgeturl = 'http://www.danhagon.me.uk/Wave/ChemSpiderDoodleGadgetMVCDev.xml'
        gadget = document.Gadget(gadgeturl) # setup gadget instance
        blip.GetDocument().InsertElement(r.start, gadget) # insert gadget
        delta = {'molfile' : compound.mol} # set state with molfile for CSID
        blip.GetDocument().GadgetSubmitDelta(gadget, delta) # submit the delta




def OnRobotAdded(properties, context):
  """Invoked when the robot has been added."""
  root_wavelet = context.GetRootWavelet()
  root_wavelet.CreateBlip().GetDocument().SetText("Hello, I'm ChemGadget, I will insert a 3d chemical gadget where you have placed the text  chem[chemicalName;image].  This is Version 0.1 of ChemGadget")



if __name__ == '__main__':
  ChemGadget = robot.Robot('chemgadget',
                         image_url='http://www.chemspider.com/ImagesHandler.ashx?id=236',
			 version = '1',
                         profile_url='http://www.google.com')
  ChemGadget.RegisterHandler(events.BLIP_SUBMITTED, OnBlipSubmitted)
  ChemGadget.RegisterHandler(events.WAVELET_SELF_ADDED, OnRobotAdded)

  ChemGadget.Run(debug=True)
