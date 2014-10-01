ALL_NEWS_URL = 'https://api.nowthismedia.com/v1/assets?cursor=%s'
COLLECTIONS = 'https://api.nowthismedia.com/v1/collections'
COLLECTION_URL = 'https://api.nowthismedia.com/v1/collections/%s/assets?cursor=%%s'

HTTP_HEADERS = {
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36',
	'X-NT-API-TOKEN': '9000ede3a923ce7f8329b8089652b111'
}

####################################################################################################
def Start():

	ObjectContainer.title1 = 'NowThis News'
	HTTP.CacheTime = 300

####################################################################################################
@handler('/video/nowthisnews', 'NowThis News')
def MainMenu():

	oc = ObjectContainer()

	oc.add(DirectoryObject(
		key = Callback(Videos, title='Latest', slug='all'),
		title = 'Latest'
	))

	json_obj = JSON.ObjectFromURL(COLLECTIONS, headers=HTTP_HEADERS, cacheTime=CACHE_1DAY)

	for c in json_obj['collections']:

		oc.add(DirectoryObject(
			key = Callback(Videos, title=c['collection']['name'], slug=c['collection']['namespace']),
			title = c['collection']['name']
		))

	return oc

####################################################################################################
@route('/video/nowthisnews/videos/{slug}')
def Videos(title, slug, cursor=''):

	oc = ObjectContainer(title2=title)

	if slug == 'all':
		url = ALL_NEWS_URL
	else:
		url = COLLECTION_URL % (slug)

	if cursor == '':
		url = url.split('?cursor=')[0]
	else:
		url = url % (cursor)

	json_obj = JSON.ObjectFromURL(url, headers=HTTP_HEADERS)

	for a in json_obj['assets']:

		video = a['video']

		video_url = video['long_url']
		video_title = video['name']
		video_summary = video['description']
		video_thumb = video['thumbnail_medium']
		video_duration = int(float(video['duration'])*1000)
		video_originally_available_at = Datetime.ParseDate(video['created_at']).date()

		oc.add(VideoClipObject(
			url = video_url,
			title = video_title,
			summary = video_summary,
			thumb = Resource.ContentsOfURLWithFallback(url=video_thumb),
			duration = video_duration,
			originally_available_at = video_originally_available_at
		))

	if 'cursor' in json_obj and 'next' in json_obj['cursor']:

		oc.add(NextPageObject(
			key = Callback(Videos, title=title, slug=slug, cursor=json_obj['cursor']['next']),
			title = 'More ...'
		))

	return oc
