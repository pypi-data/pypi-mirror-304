import sys,os,re
from .SchemaEntity import SchemaEntity  
from .SchemaReplacer import SchemaReplacer  

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.transformer.deco.SchemaTransformerDeco import SchemaTransformerDeco
from sele.transformer.Transformer import Transformer

class SchemaTransformerChain(Transformer):
  '''
  Basic behavior chain, it's a handler too
  '''
  kind = 'chain'

  @SchemaTransformerDeco()
  def resolve(self,request):
    '''
    Deal the atom by the event chain
    '''
    handler = self.__get_chain()
    return handler.handle(request)

  def __get_chain(self):
    '''
    Converters must be executed sequentially
    '''
    # writer
    entity = SchemaEntity()
    replacer = SchemaReplacer()

    entity.set_next(replacer)

    return entity
