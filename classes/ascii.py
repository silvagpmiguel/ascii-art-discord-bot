import json
import os

class Ascii:
  def __init__(self, depth=6, path="fonts/ansi_shadow.json"):
    self.depth = depth
    self.path = path
    with open(path) as f:
      self.font = json.load(f)

  def getLetter(self, letter):
    return self.font['letters'][letter]

  def getDepth(self):
    return self.depth

  def getAvailableLetters(self):
    return self.font['letters'].keys()

  def getLimit(self):
    return self.font['limit']

  def getAvailableFontsToString(self):
    aux = os.listdir('fonts')
    fonts = ""
    for filename in aux:
      fonts += '\n- ' + filename[:-5] 
    return fonts

  def getAvailableFonts(self):
    return os.listdir('fonts')
    
  def setFont(self, font):
    with open('fonts/'+font) as f:
      self.font = json.load(f)
