import csv 
import re

class DeweyCode:
  dewey_dict = None 
  def  __init__(self, filename): 
    reader = csv.reader(open(filename, "r"))
    self.dewey_dict = {int(i[0]): i[1] for i in reader} 

  def dewey_classes(self, no): 
    classes = {} 
    top = (no/100)*100 if no != 0 else None
    mid = (no/10)*10 if no != 0 else None
    bot = no
    valid = True 

    classes["top"] = self.dewey_dict[top] if top in self.dewey_dict else None
    classes["mid"] = self.dewey_dict[mid] if mid in self.dewey_dict else None
    classes["bot"] = self.dewey_dict[bot] if bot in self.dewey_dict else None

    aslist = []
    for k,v in classes.iteritems(): 
      aslist.append(v)
      if v is None: valid = False
    return (classes, aslist) if valid else None

  def dewey_classes_extract(self, string):
    if string is None or string == "": return None
    no = None
    try:
      no = re.search("\d\d\d[\.]?\d?\d?\d?|\d\d\d\d*", string).group(0) 
    except AttributeError: 
      no = ""

    return self.dewey_classes(int(float(no))) if self.is_number(no) else None
  
  def is_number(self, string): 
    if type(string) is not str: return False
    number = True
    try: 
      float(string) 
    except ValueError: 
      number = False 
    return number 
