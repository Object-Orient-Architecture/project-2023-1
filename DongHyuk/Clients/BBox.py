class BBox:
  '''
  #TODO : ABSTRACTION
  Constructor Overloading
  '''
  
  def __init__(self,minx:float,miny:float,maxx:float,maxy:float):
    '''
    properties : minx | miny | maxx | maxy
    '''
    self.minx = minx
    self.miny = miny
    self.maxx = maxx
    self.maxy = maxy
    
  def __init__(self,coords,width,height):
    '''
    get coords of Bbox by center coords and width, height(Rectangular)
    '''
    self.minx = coords[0] - width/2
    self.miny = coords[1] - height/2
    self.maxx = coords[0] + width/2
    self.maxy = coords[1] + height/2
  
  def __init(self,coords,length):
    '''
    get coords of Bbox by center coords and length(Square)
    '''
    self.minx = coords[0] - length/2
    self.miny = coords[1] - length/2
    self.maxx = coords[0] + length/2
    self.maxy = coords[1] + length/2
  
  def __str__(self):
    '''
    format : 'minx,miny,maxx,maxy'
    '''
    return f'{self.minx},{self.miny},{self.maxx},{self.maxy}'