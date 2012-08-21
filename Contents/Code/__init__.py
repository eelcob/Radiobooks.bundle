# -*- coding: utf-8 -*-

###################################################################################################

PLUGIN_TITLE              = 'Radiobooks'
PLUGIN_PREFIX             = '/music/radiobooks'

RADIOBOOKS_RSS            = 'http://www.radiobooks.eu/xml/rss.php?lang=%s'
RADIOBOOKS_LANGUAGE       = [
                              ['EN', 'Radiobooks (English)'],
                              ['NL', 'Radioboeken (Nederlands)'],
                              ['FR', 'Radiolivre (Français)'],
                              ['ES', 'Radiolibro (Español)']
                            ]

CACHE_INTERVAL            = 86400

# Default artwork and icon(s)
PLUGIN_ARTWORK            = 'art-default.png'
PLUGIN_ICON_DEFAULT       = 'icon-default.png'

###################################################################################################

def Start():
  Plugin.AddPrefixHandler(PLUGIN_PREFIX, MainMenu, L("PLUGIN_TITLE"))

  Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
  Plugin.AddViewGroup('Details', viewMode='InfoList', mediaType='items')

  # Set the default MediaContainer attributes
  MediaContainer.title1         = L("PLUGIN_TITLE")
  MediaContainer.viewGroup      = 'List'
  MediaContainer.art            = R(PLUGIN_ARTWORK)

  # Set the default cache time
  HTTP.SetCacheTime(CACHE_INTERVAL)

###################################################################################################

def UpdateCache():
  for i in range(0, len(RADIOBOOKS_LANGUAGE)):
    HTTP.Request(RADIOBOOKS_RSS % RADIOBOOKS_LANGUAGE[i][0])

###################################################################################################

def CreatePrefs():
  Prefs.Add(id='numItems', type='enum', default='25', label=L("PREFS_ITEMS"), values='10|25|50|100')

###################################################################################################

def MainMenu():
  dir = MediaContainer()

  for i in range(0, len(RADIOBOOKS_LANGUAGE)):
    icon = 'icon-' + RADIOBOOKS_LANGUAGE[i][0] + '.png'
    dir.Append(Function(DirectoryItem(Listbooks, title=RADIOBOOKS_LANGUAGE[i][1], thumb=R(icon)), i=i, title=RADIOBOOKS_LANGUAGE[i][1], icon=icon, start=0))

  dir.Append(PrefsItem(L("PREFERENCES"), thumb=R(PLUGIN_ICON_DEFAULT)))

  return dir

###################################################################################################

def Listbooks(sender, i, title, icon, start):
  dir = MediaContainer(viewGroup='Details', title2=title)

  books = HTML.ElementFromURL(RADIOBOOKS_RSS % RADIOBOOKS_LANGUAGE[i][0], encoding='UTF-8', errors='ignore').xpath('//channel/item')

  end = start+int(10)
  if end > len(books):
    end = len(books)

  for j in range(start, end):
    title       = Cleanup(books[j].xpath('./title')[0].text)
    description = Cleanup(books[j].xpath('./description')[0].text)
    date        = books[j].xpath('./pubdate')[0].text
    date        = Datetime.ParseDate(date).strftime('%a %b %d, %Y')
    url         = books[j].xpath('./enclosure')[0].get('url')

    dir.Append(TrackItem(url, title=title, artist='', album='Radiobooks', subtitle=date, summary=description, thumb=R(icon)))

  if end < len(books):
    dir.Append(Function(DirectoryItem(Listbooks, title=L("MORE"), thumb=R(icon)), i=i, title=title, icon=icon, start=end))

  return dir

###################################################################################################

# Let's hope this is temporary!
def Cleanup(text):
  text = text.replace('Â', '')

  text = text.replace('Ã¢', 'â')
  text = text.replace('Ã¡', 'á')

  text = text.replace('Ã§', 'ç')

  text = text.replace('Ã©', 'é')
  text = text.replace('Ã¨', 'è')
  text = text.replace('Ã«', 'ë')
  text = text.replace('Ãª', 'ê')

  text = text.replace('Ã¯', 'ï')
  text = text.replace('Ã®', 'î')
  text = text.replace('Ã­', 'í')

  text = text.replace('Ã´', 'ô')
  text = text.replace('Ã³', 'ó')

  text = text.replace('Ã»', 'û')
  text = text.replace('Ã¼', 'ü')
  text = text.replace('Ã¹', 'ù')
  text = text.replace('Ãº', 'ú')

  text = text.replace('Ã±', 'ñ')

  text = text.replace('Ã', 'à')
  text = text.replace('Â', '')
  text = text.replace('', '')

  text = text.replace('à«à', '«')
  text = text.replace('à«', '«')
  text = text.replace('à»', '»')

  text = text.replace('â', '-')

  return text
