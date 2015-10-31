# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor
from ..utils import parse_iso8601


class NextMediaIE(InfoExtractor):
    _VALID_URL = r'http://hk.apple.nextmedia.com/[^/]+/[^/]+/(?P<date>\d+)/(?P<id>\d+)'
    _TESTS = [{
        'url': 'http://hk.apple.nextmedia.com/realtime/news/20141108/53109199',
        'md5': 'dff9fad7009311c421176d1ac90bfe4f',
        'info_dict': {
            'id': '53109199',
            'ext': 'mp4',
            'title': '【佔領金鐘】50外國領事議員撐場 讚學生勇敢香港有希望',
            'thumbnail': 're:^https?://.*\.jpg$',
            'description': 'md5:28222b9912b6665a21011b034c70fcc7',
            'timestamp': 1415456273,
            'upload_date': '20141108',
        }
    }]

    _URL_PATTERN = r'\{ url: \'(.+)\' \}'

    def _real_extract(self, url):
        news_id = self._match_id(url)
        page = self._download_webpage(url, news_id)
        return self._extract_from_nextmedia_page(news_id, url, page)

    def _extract_from_nextmedia_page(self, news_id, url, page):
        title = self._fetch_title(page)
        video_url = self._search_regex(self._URL_PATTERN, page, 'video url')

        attrs = {
            'id': news_id,
            'title': title,
            'url': video_url,  # ext can be inferred from url
            'thumbnail': self._fetch_thumbnail(page),
            'description': self._fetch_description(page),
        }

        timestamp = self._fetch_timestamp(page)
        if timestamp:
            attrs['timestamp'] = timestamp
        else:
            attrs['upload_date'] = self._fetch_upload_date(url)

        return attrs

    def _fetch_title(self, page):
        return self._og_search_title(page)

    def _fetch_thumbnail(self, page):
        return self._og_search_thumbnail(page)

    def _fetch_timestamp(self, page):
        dateCreated = self._search_regex('"dateCreated":"([^"]+)"', page, 'created time')
        return parse_iso8601(dateCreated)

    def _fetch_upload_date(self, url):
        return self._search_regex(self._VALID_URL, url, 'upload date', group='date')

    def _fetch_description(self, page):
        return self._og_search_property('description', page)


class NextMediaActionNewsIE(NextMediaIE):
    _VALID_URL = r'http://hk.dv.nextmedia.com/actionnews/[^/]+/(?P<date>\d+)/(?P<id>\d+)/\d+'
    _TESTS = [{
        'url': 'http://hk.dv.nextmedia.com/actionnews/hit/20150121/19009428/20061460',
        'md5': '05fce8ffeed7a5e00665d4b7cf0f9201',
        'info_dict': {
            'id': '19009428',
            'ext': 'mp4',
            'title': '【壹週刊】細10年男友偷食　50歲邵美琪再失戀',
            'thumbnail': 're:^https?://.*\.jpg$',
            'description': 'md5:cd802fad1f40fd9ea178c1e2af02d659',
            'timestamp': 1421791200,
            'upload_date': '20150120',
        }
    }]

    def _real_extract(self, url):
        news_id = self._match_id(url)
        actionnews_page = self._download_webpage(url, news_id)
        article_url = self._og_search_url(actionnews_page)
        article_page = self._download_webpage(article_url, news_id)
        return self._extract_from_nextmedia_page(news_id, url, article_page)


class AppleDailyRealtimeNewsIE(NextMediaIE):
    _VALID_URL = r'http://(www|ent).appledaily.com.tw/(realtimenews|enews)/[^/]+/[^/]+/(?P<date>\d+)/(?P<id>\d+)(/.*)?'
    _TESTS = [{
        'url': 'http://ent.appledaily.com.tw/enews/article/entertainment/20150128/36354694',
        'md5': 'a843ab23d150977cc55ef94f1e2c1e4d',
        'info_dict': {
            'id': '36354694',
            'ext': 'mp4',
            'title': '周亭羽走過摩鐵陰霾2男陪吃 九把刀孤寒看醫生',
            'thumbnail': 're:^https?://.*\.jpg$',
            'description': 'md5:b23787119933404ce515c6356a8c355c',
            'upload_date': '20150128',
        }
    }, {
        'url': 'http://www.appledaily.com.tw/realtimenews/article/strange/20150128/550549/%E4%B8%8D%E6%BB%BF%E8%A2%AB%E8%B8%A9%E8%85%B3%E3%80%80%E5%B1%B1%E6%9D%B1%E5%85%A9%E5%A4%A7%E5%AA%BD%E4%B8%80%E8%B7%AF%E6%89%93%E4%B8%8B%E8%BB%8A',
        'md5': '86b4e9132d158279c7883822d94ccc49',
        'info_dict': {
            'id': '550549',
            'ext': 'mp4',
            'title': '不滿被踩腳　山東兩大媽一路打下車',
            'thumbnail': 're:^https?://.*\.jpg$',
            'description': 'md5:2648aaf6fc4f401f6de35a91d111aa1d',
            'upload_date': '20150128',
        }
    }]

    _URL_PATTERN = r'\{url: \'(.+)\'\}'

    def _fetch_title(self, page):
        return self._html_search_regex(r'<h1 id="h1">([^<>]+)</h1>', page, 'news title')

    def _fetch_thumbnail(self, page):
        return self._html_search_regex(r"setInitialImage\(\'([^']+)'\)", page, 'video thumbnail', fatal=False)

    def _fetch_timestamp(self, page):
        return None


class AppleDailyAnimationNewsIE(AppleDailyRealtimeNewsIE):
    _VALID_URL = 'http://www.appledaily.com.tw/animation/[^/]+/[^/]+/(?P<date>\d+)/(?P<id>\d+)(/.*)?'
    _TESTS = [{
        'url': 'http://www.appledaily.com.tw/animation/realtimenews/new/20150128/5003671',
        'md5': '03df296d95dedc2d5886debbb80cb43f',
        'info_dict': {
            'id': '5003671',
            'ext': 'mp4',
            'title': '20正妹熱舞　《刀龍傳說Online》火辣上市',
            'thumbnail': 're:^https?://.*\.jpg$',
            'description': 'md5:23c0aac567dc08c9c16a3161a2c2e3cd',
            'upload_date': '20150128',
        }
    }, {
        # No thumbnail
        'url': 'http://www.appledaily.com.tw/animation/realtimenews/new/20150128/5003673/',
        'md5': 'b06182cd386ea7bc6115ec7ff0f72aeb',
        'info_dict': {
            'id': '5003673',
            'ext': 'mp4',
            'title': '半夜尿尿　好像會看到___',
            'description': 'md5:61d2da7fe117fede148706cdb85ac066',
            'upload_date': '20150128',
        },
        'expected_warnings': [
            'video thumbnail',
        ]
    }]

    def _fetch_title(self, page):
        return self._html_search_meta('description', page, 'news title')

    def _fetch_description(self, page):
        return self._html_search_meta('description', page, 'news description')
