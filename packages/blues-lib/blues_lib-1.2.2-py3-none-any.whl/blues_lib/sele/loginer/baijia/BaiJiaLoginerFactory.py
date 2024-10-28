import sys,os,re
from .BaiJiaAccountLoginer import BaiJiaAccountLoginer   
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.loginer.LoginerFactory import LoginerFactory

class BaiJiaLoginerFactory(LoginerFactory):
  def create_account(self):
    return BaiJiaAccountLoginer()

  def create_mac(self):
    pass
