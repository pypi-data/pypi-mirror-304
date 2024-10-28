import sys,os,re,json
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.releaser.VideoReleaserSchema import VideoReleaserSchema

class ChannelsVideoSchema(VideoReleaserSchema):

  def create_url_atom(self):
    self.url_atom = self.atom_factory.createURL('Video page','https://channels.weixin.qq.com/platform/post/create')

  def create_fill_atom(self):

    atoms = [
      # value placeholder 2: material_body_text
      self.atom_factory.createTextArea('content','#content','material_body_text',2),
    ]

    #self.fill_atom = self.atom_factory.createArray('fields',atoms)

  def create_preview_atom(self):
    return None

  def create_submit_atom(self):
    atoms = [
      self.atom_factory.createClickable('submit','.cheetah-public .Video-op-bar-pub-btn'),
    ]
    #self.submit_atom = self.atom_factory.createArray('submit',atoms)

  def create_popup_atom(self):
    return None

