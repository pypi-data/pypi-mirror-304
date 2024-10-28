import sys,os,re
from abc import ABC,abstractmethod
sys.path.append(re.sub('test.*','blues_lib',os.path.realpath(__file__)))
from sele.transformer.schema.SchemaTransformerChain import SchemaTransformerChain     
from atom.AtomFactory import AtomFactory     
from atom.Atom import Atom
from pool.BluesMaterialIO import BluesMaterialIO

class ReleaserSchema(ABC):

  def __init__(self):

    self.atom_factory = AtomFactory()

    # { dict } standard material data entiry
    self.material = None
    
    # declare atom fields
    # { URLAtom } the form page
    self.url_atom = None
    # { ArrayAtom } the form controller atom list
    self.fill_atom = None
    # { ArrayAtom } the preview atom list
    self.preview_atom = None
    # { ArrayAtom } the submit atom list
    self.submit_atom = None
    # { ArrayAtom } the modal atom list, should be closed
    self.popup_atom = None
    
    # create atoms fields
    self.create_fields()

    # fillin the material value ,must after fields created
    self.fill_fields()
  
  def create_fields(self):
    self.create_url_atom()
    self.create_fill_atom()
    self.create_preview_atom()
    self.create_submit_atom()
    self.create_popup_atom()

  def fill_fields(self):
    '''
    Replace the placeholder in the schema by the materail entity data
    '''
    if not self.fill_atom:
      return
    request = SchemaTransformerChain().handle({
      'atom':self.fill_atom,
      'value':None, # fetch material by handler
    })
    self.material = request['value']
  
  @abstractmethod
  def create_url_atom(self):
    pass

  @abstractmethod
  def create_fill_atom(self):
    pass

  @abstractmethod
  def create_preview_atom(self):
    pass

  @abstractmethod
  def create_submit_atom(self):
    pass

  @abstractmethod
  def create_popup_atom(self):
    pass

