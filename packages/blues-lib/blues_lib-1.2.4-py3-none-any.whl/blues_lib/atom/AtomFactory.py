
# plain atoms
from .plain.DataAtom import DataAtom
from .plain.RegexpAtom import RegexpAtom
from .plain.URLAtom import URLAtom

# event atoms
from .event.ElementAtom import ElementAtom
from .event.ClickableAtom import ClickableAtom
from .event.FrameAtom import FrameAtom
from .event.RollinAtom import RollinAtom
from .event.PopupAtom import PopupAtom

# writer atoms
from .writer.InputAtom import InputAtom
from .writer.TextAreaAtom import TextAreaAtom
from .writer.FileAtom import FileAtom
from .writer.ChoiceAtom import ChoiceAtom
from .writer.SelectAtom import SelectAtom

# reader atoms
from .reader.AttrAtom import AttrAtom
from .reader.TextAtom import TextAtom
from .reader.ValueAtom import ValueAtom
from .reader.CssAtom import CssAtom
from .reader.ShotAtom import ShotAtom

# composite
from .composite.ArrayAtom import ArrayAtom
from .composite.MapAtom import MapAtom

# spider atoms
from .spider.BriefAtom import BriefAtom
from .spider.NewsAtom import NewsAtom
from .spider.ParaAtom import ParaAtom

class AtomFactory():

  # create plain Atoms
  def createData(self,title,value):
    return DataAtom(title,value)

  def createRegexp(self,title,value):
    return RegexpAtom(title,value)

  def createURL(self,title,value):
    return URLAtom(title,value)

  # create event Atoms
  def createElement(self,title,selector,value=None,parent_selector=None,timeout=None):
    return ElementAtom(title,selector,value,parent_selector,timeout)

  def createRollin(self,title,selector,value=None,parent_selector=None,timeout=None):
    return RollinAtom(title,selector,value,parent_selector,timeout)

  def createPopup(self,title,selector,value=None,parent_selector=None,timeout=None):
    return PopupAtom(title,selector,value,parent_selector,timeout)

  def createClickable(self,title,selector,value=None,parent_selector=None,timeout=None):
    return ClickableAtom(title,selector,value,parent_selector,timeout)

  def createFrame(self,title,selector,value='in',parent_selector=None,timeout=None):
    return FrameAtom(title,selector,value,parent_selector,timeout)
  
  # create writer Atoms
  def createInput(self,title,selector,value=None,parent_selector=None,timeout=None):
    return InputAtom(title,selector,value,parent_selector,timeout)

  def createTextArea(self,title,selector,value=None,LF_count=1,parent_selector=None,timeout=None):
    return TextAreaAtom(title,selector,value,LF_count,parent_selector,timeout)

  def createFile(self,title,selector,value=None,wait_time=5,parent_selector=None,timeout=None):
    return FileAtom(title,selector,value,wait_time,parent_selector,timeout)

  def createSelect(self,title,selector,value=True,parent_selector=None,timeout=None):
    return SelectAtom(title,selector,value,parent_selector,timeout)

  def createChoice(self,title,selector,value=True,parent_selector=None,timeout=None):
    return ChoiceAtom(title,selector,value,parent_selector,timeout)

  # reader atoms
  def createText(self,title,selector,value=None,parent_selector=None,timeout=None):
    return TextAtom(title,selector,value,parent_selector,timeout)

  def createValue(self,title,selector,value=None,parent_selector=None,timeout=None):
    return ValueAtom(title,selector,value,parent_selector,timeout)

  def createAttr(self,title,selector,value=None,parent_selector=None,timeout=None):
    return AttrAtom(title,selector,value,parent_selector,timeout)

  def createShot(self,title,selector=None,value=None,parent_selector=None,timeout=None):
    return ShotAtom(title,selector,value,parent_selector,timeout)

  def createCss(self,title,selector,value=None,parent_selector=None,timeout=None):
    return CssAtom(title,selector,value,parent_selector,timeout)
  
  # composite atoms
  def createArray(self,title,value=None):
    return ArrayAtom(title,value)

  def createMap(self,title,value=None):
    return MapAtom(title,value)

  # spider atoms
  def createPara(self,title,selector,value):
    return ParaAtom(title,selector,value)

  def createBrief(self,title,selector,value):
    return BriefAtom(title,selector,value)

  def createNews(self,title,selector,value):
    return NewsAtom(title,selector,value)
