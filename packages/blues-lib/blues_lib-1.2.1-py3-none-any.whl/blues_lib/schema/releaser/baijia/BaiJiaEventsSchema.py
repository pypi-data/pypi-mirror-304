import sys,os,re,json
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.releaser.EventsReleaserSchema import EventsReleaserSchema

class BaiJiaEventsSchema(EventsReleaserSchema):

  def create_url_atom(self):
    self.url_atom = self.atom_factory.createURL('events page','https://baijiahao.baidu.com/builder/rc/edit?type=events')

  def create_fill_atom(self):
    # use the filed plachehoders
    image_atom = [
      self.atom_factory.createClickable('Popup the dialog','.uploader-plus'),
      # value placeholder 1: material_body_image ,set wait_time as 5
      self.atom_factory.createFile('Select images','.cheetah-upload input','material_body_image',5),
      self.atom_factory.createClickable('Upload images','.cheetah-modal-footer button.cheetah-btn-primary'),
    ]

    atoms = [
      # value placeholder 2: material_body_text
      self.atom_factory.createTextArea('content','#content','material_body_text',2),
      self.atom_factory.createArray('images',image_atom),
    ]

    self.fill_atom = self.atom_factory.createArray('fields',atoms)

  def create_preview_atom(self):
    return None

  def create_submit_atom(self):
    atoms = [
      self.atom_factory.createClickable('submit','.cheetah-public .events-op-bar-pub-btn'),
    ]
    self.submit_atom = self.atom_factory.createArray('submit',atoms)

  def create_popup_atom(self):
    return None

