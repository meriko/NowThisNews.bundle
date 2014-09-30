TITLE  = 'NowThis News'
PREFIX = '/video/nowthisnews'
ART    = 'art-default.jpg'
ICON   = 'icon-default.png'

USER_AGENT = 'Mozilla/5.0 (iPad; CPU OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53'
BASE_URL = 'http://nowthisnews.com'

BROKEN_HEADER = 'No longer available'
BROKEN_MESSAGE = 'Due to a recent update of the nowthisnews.com website, this channel is no longer available. Since the new website uses a format that is very unfriendly w.r.t. making a channel out of, no effort will be made to make this channel work again until if/when the website is updated again. Please try out the Newsy channel instead which offers similiar content. The Newsy channel can be found in the official Channel Directory. Thank you for your understanding!'

###################################################################################################
def Start():
    ObjectContainer.title1 = TITLE
    ObjectContainer.art    = R(ART)
    DirectoryObject.thumb  = R(ICON)
    
    HTTP.CacheTime             = CACHE_1HOUR
    HTTP.Headers['User-agent'] = USER_AGENT
    
###################################################################################################
@handler(PREFIX, TITLE, thumb = ICON, art = ART)
def MainMenu():
    oc = ObjectContainer(title2 = "BROKEN")
    
    oc.add(
        DirectoryObject(
            key = Callback(Broken),
            title = BROKEN_HEADER,
            summary = BROKEN_MESSAGE 
            
        )
    )

    return oc

####################################################################################################
@route(PREFIX + '/Broken')
def Broken():
    oc = ObjectContainer()
    oc.header = BROKEN_HEADER
    oc.message = BROKEN_MESSAGE
    return oc