from wox import Wox,WoxAPI
import pyperclip
import json
import time

##################################################################
## Used some code from old plugin, Case Converter, by: shahisha ##
##################################################################

def json_wox(title, subtitle, icon, action=None, action_params=None, action_keep=None):
  json = {
      'Title': title,
      'SubTitle': subtitle,
      'IcoPath': icon
  }
  if action and action_params and action_keep:
      json.update({
          'JsonRPCAction': {
              'method': action,
              'parameters': action_params,
              'dontHideAfterAction': action_keep
          }
      })
  return json

def removeNonAscii(s): 
  return ''.join(i for i in s if ord(i)<126 and ord(i)>31)

def copy_to_clipboard(text):
  pyperclip.copy(text.strip())

def strip_clip(query):
  results = []
  try:
      clip = pyperclip.paste()
      if not clip:
           return results.append(json_wox('String not found in Clipboard',
                         str(e),
                         "icon.png"))
      else:
          variations = {
            'lowercase': str(pyperclip.paste().lower()),
            'uppercase': str(pyperclip.paste().upper()),
            'titlecase': str(pyperclip.paste().title()),
            'strip formatting': str(removeNonAscii(str(pyperclip.paste())))
          }
      
          for key, value in sorted(variations.items()):
              title = value
              subTitle = key
      
              results.append(json_wox(title,
                             subTitle.title(),
                             subTitle + ".png",
                             "copy_clip",
                             [str(title)],
                             True))
          return results
  except Exception as e:
       return results.append(json_wox('String not found in Clipboard',
                         str(e),
                         "icon.png"))

class StripClip(Wox):

  def query(self,query):
    return strip_clip(pyperclip.paste())

  def copy_clip(self, query):
    #copy to clipboard after pressing enter
    copy_to_clipboard(query)
    WoxAPI.hide_app()

if __name__ == "__main__":
  StripClip()