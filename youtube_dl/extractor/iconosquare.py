from __future__ import unicode_literals

from .common import InfoExtractor
from ..utils import int_or_none


class IconosquareIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?(?:iconosquare\.com|statigr\.am)/p/(?P<id>[^/]+)'
    _TEST = {
        'url': 'http://statigr.am/p/522207370455279102_24101272',
        'md5': '6eb93b882a3ded7c378ee1d6884b1814',
        'info_dict': {
            'id': '522207370455279102_24101272',
            'ext': 'mp4',
            'title': 'Instagram media by @aguynamedpatrick (Patrick Janelle)',
            'description': 'md5:644406a9ec27457ed7aa7a9ebcd4ce3d',
            'timestamp': 1376471991,
            'upload_date': '20130814',
            'uploader': 'aguynamedpatrick',
            'uploader_id': '24101272',
            'comment_count': int,
            'like_count': int,
        },
    }

    def _real_extract(self, url):
        video_id = self._match_id(url)

        webpage = self._download_webpage(url, video_id)

        media = self._parse_json(
            self._search_regex(
                r'window\.media\s*=\s*({.+?});\n', webpage, 'media'),
            video_id)

        formats = [{
            'url': f['url'],
            'format_id': format_id,
            'width': int_or_none(f.get('width')),
            'height': int_or_none(f.get('height'))
        } for format_id, f in media['videos'].items()]
        self._sort_formats(formats)

        title = self._html_search_regex(
            r'<title>(.+?)(?: *\(Videos?\))? \| (?:Iconosquare|Statigram)</title>',
            webpage, 'title')

        timestamp = int_or_none(media.get('created_time') or media.get('caption', {}).get('created_time'))
        description = media.get('caption', {}).get('text')

        uploader = media.get('user', {}).get('username')
        uploader_id = media.get('user', {}).get('id')

        comment_count = int_or_none(media.get('comments', {}).get('count'))
        like_count = int_or_none(media.get('likes', {}).get('count'))

        thumbnails = [{
            'url': t['url'],
            'id': thumbnail_id,
            'width': int_or_none(t.get('width')),
            'height': int_or_none(t.get('height'))
        } for thumbnail_id, t in media.get('images', {}).items()]

        return {
            'id': video_id,
            'title': title,
            'description': description,
            'thumbnails': thumbnails,
            'timestamp': timestamp,
            'uploader': uploader,
            'uploader_id': uploader_id,
            'comment_count': comment_count,
            'like_count': like_count,
            'formats': formats,
        }
