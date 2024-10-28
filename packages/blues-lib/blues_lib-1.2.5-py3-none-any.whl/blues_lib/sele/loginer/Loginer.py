import sys,os,re
from abc import ABC, abstractmethod
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.browser.BluesProxyChrome import BluesProxyChrome     
from pool.DBTableIO import DBTableIO
from util.BluesURL import BluesURL      
from util.BluesDateTime import BluesDateTime        
from util.BluesConsole import BluesConsole        

class Loginer(ABC):
  def __init__(self):
    # schema extrinsic state
    # { LoginerSchema } 
    self.schema = None
    # { LoginerBrowser }
    self.browser = None

    # create fields
    self.init()
    
    #  intrinsic state
    # { DBTableIO }
    self.io = DBTableIO('naps_loginer')
    #  { str } the site's main domain
    self.domain = BluesURL.get_main_domain(self.log_in)
  
  def init(self):
    '''
    Create the shcema and extract to fields
    '''
    self.create_schema()
    self.create_fields()
    self.create_subtype_fields()
    
  def login(self):
    '''
    Final template method
    '''
    try:
      # open the log in page
      self.open()
      # fill in the account and submit
      self.perform()
      # verify log in status
      self.verify()
      # save cookie to local file
      self.cookie()
    except Exception as e:
      BluesConsole.error('Login failure: %s' % e)
    finally:
      self.quit()
  
  # === create schema and fields ===
  @abstractmethod
  def create_schema(self):
    pass

  def create_fields(self):
    '''
    Extract base atom's value to fields
    '''
    # { str } the login page url
    self.log_in = self.schema.log_in_atom.get_value()
    # { str } the login page element css selector
    self.log_in_element = self.schema.log_in_element_atom.get_selector()
    # { dict } the proxy's config
    self.proxy_config = self.schema.proxy_atom.get_value()
    # { dict } the cookies filter config
    self.cookie_filter_config = self.schema.cookie_filter_atom.get_value()
    # { int } the interval that wait the url changes (login and redirect to the hompage)
    self.verify_wait_period = self.schema.verify_wait_period_atom.get_value()

  @abstractmethod
  def create_subtype_fields(self):
    '''
    Extract typed atom's value to fields
    '''
    pass
  
  # === behavior step methods ===

  def open(self):
    proxy_config = self.proxy_config if self.proxy_config else self.__get_default_proxy_config()
    self.browser = BluesProxyChrome(proxy_config,self.cookie_filter_config)
    self.browser.interactor.navi.open(self.log_in)

  @abstractmethod
  def perform(self):
    '''
    The subclass must implement this method
    '''
    pass

  def verify(self):
    '''
    Check whether the login succeeds based on the url link change
    No need to wait for the page to load after the jump
    QRCode wait some minutes to wait the user login one the phone
    '''
    if self.log_in_element:
      stat = not self.browser.waiter.querier.query(self.log_in_element,timeout=5)
    else:
      stat = self.browser.waiter.ec.url_changes(self.log_in,self.verify_wait_period)
    if stat:
      BluesConsole.success('Login successfully, ready to save cookies')
      # You must wait for the http request to load, otherwise you cannot get the cookie
    else:
      raise Exception('Login failure, verify failure')
    
  def cookie(self):
    BluesDateTime.count_down({
      'duration':10,
      'title':'wait http request to save cookie'
    })
    cookie_file = self.browser.save_cookies()
    if cookie_file:
      BluesConsole.success('The cookie has been successfully obtained and saved')
    else:
      BluesConsole.success('Cookie acquisition failure')

  def quit(self):
    if self.browser:
      self.browser.interactor.navi.quit()

  # ==== tool method ===
  def pause(self,title='',seconds=2):
    '''
    pause in perform steps
    '''
    BluesDateTime.count_down({
      'duration':seconds,
      'title':title if title else 'Pause'
    })

  def __get_default_proxy_config(self):
    main_domain = BluesURL.get_main_domain(self.log_in)
    scopes = [".*%s.*" % main_domain]
    return {
      "scopes":scopes,
    }
