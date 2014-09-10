TITLE  = 'NowThis News'
PREFIX = '/video/nowthisnews'
ART    = 'art-default.jpg'
ICON   = 'icon-default.png'

USER_AGENT = 'Mozilla/5.0 (iPad; CPU OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53'
BASE_URL = 'http://nowthisnews.com'

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
    oc = ObjectContainer()

    title = 'Recent'
    oc.add(
        DirectoryObject(
            key =
                Callback(
                    Videos,
                    title = title,
                    url = BASE_URL + '/'
                ),
            title = title
        )
    )

    pageElement = HTML.ElementFromURL(BASE_URL)
    
    for item in pageElement.xpath("//*[@id='navigation']//li"):
        url = item.xpath(".//a/@href")[0]
        
        if not url.startswith("http"):
            url = BASE_URL + url
        
        title = item.xpath(".//a/text()")[0]
        
        oc.add(
            DirectoryObject(
                key =
                    Callback(
                        Videos,
                        title = title,
                        url = url
                    ),
                title = title
            )         
        )
    
    
    return oc

####################################################################################################
@route(PREFIX + '/Videos', page = int)
def Videos(title, url, page = 1):
    oc = ObjectContainer(title2 = title)
    
    pageElement = HTML.ElementFromURL(url + "?page=" + str(page))
    
    for item in pageElement.xpath("//*[@id='playlist']//*[contains(@class,'entry')]"):        
        videoURL = item.xpath(".//*[@class='info']//a/@href")[0]
        
        if not videoURL.startswith('http'):
            videoURL = BASE_URL + videoURL
            
        videoTitle = item.xpath(".//*[@class='info']//a/text()")[0]
        videoThumb = item.xpath(".//img/@src")[0]
        videoSummary = item.xpath(".//*[@class='age']/text()")[0] + '\r\n\r\n' + videoTitle
        
        oc.add(
            VideoClipObject(
                url = videoURL,
                title = videoTitle,
                thumb = videoThumb,
                summary = videoSummary
            )
        )
        
    if len(oc) < 1:
        oc.header  = "Sorry"
        oc.message = "Couldn't find any content"
    else:
        nextPage = pageElement.xpath("//*[@id='content']//a/@href")
        
        if nextPage:
            oc.add(
                NextPageObject(
                    key =
                        Callback(
                            Videos,
                            title = title,
                            url = url,
                            page = page + 1
                        ),
                    title = 'More ...'
                )
            )
      
    return oc
