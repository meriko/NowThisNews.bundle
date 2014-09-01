TITLE  = 'Now This News'
PREFIX = '/video/nowthisnews'
ART    = 'art-default.jpg'
ICON   = 'icon-default.png'

USER_AGENT = 'Mozilla/5.0 (iPad; CPU OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53'
BASE_URL = 'http://www.nowthisnews.com'

RE_VIDEO = Regex('{file: *"(http:\/\/.*\.m3u8)"}')

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
    
    for item in pageElement.xpath("//*[@id='playlist']//*[@class='entry']"):
        try:
            videoInfo = item.xpath("following-sibling::script/text()")[0]
            hls_url   = RE_VIDEO.search(videoInfo).groups()[0]
        except:
            continue
            
        videoTitle = item.xpath(".//*[@class='info']//a/text()")[0]
        videoThumb = item.xpath(".//img/@src")[0]
        videoSummary = item.xpath(".//*[@class='age']/text()")[0] + '\r\n\r\n' + videoTitle
        
        oc.add(
            CreateVideoClipObject(
                url = hls_url,
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

####################################################################################################
@route(PREFIX + '/CreateVideoClipObject', include_container = bool) 
def CreateVideoClipObject(url, title, thumb, summary, include_container = False):
    vco = VideoClipObject(
            key = 
                Callback(
                    CreateVideoClipObject,
                    url = url,
                    title = title,
                    thumb = thumb,
                    summary = summary,
                    include_container = True
                ),
            rating_key = title,
            title = title,
            thumb = thumb,
            summary = summary,
            items = [
                MediaObject(
                    video_resolution = 720,
                    audio_channels = 2,
                    parts = [
                        PartObject(
                            key = HTTPLiveStreamURL(url = url)
                        )
                    ]
                )
            ]
    )
    
    if include_container:
        return ObjectContainer(objects = [vco])
    else:
        return vco
