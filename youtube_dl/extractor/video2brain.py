# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor
from ..utils import int_or_none

class Video2BrainIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?video2brain\.com/(?P<lang>[a-z]+)/([a-z]+)/(?P<id>[a-z\-0-9A-Z]+)'
    
    def _real_extract(self, url):
        video_id = self._match_id(url)

        webpage = self._download_webpage(url, video_id)
        title = self._og_search_title(webpage)
        description = self._html_search_meta('description', webpage)
        thumbnail = self._og_search_thumbnail(webpage)

        xmlurl = self._search_regex(r'configuration:\s?"([^\"]+)"', webpage, 'XML descriptor URL')
        self.to_screen("%s: using xml url %s" % (video_id, xmlurl))
        if xmlurl is False:
            return False
        xml = self._download_xml(xmlurl, video_id, 'Downloading player XML')
        if xml is None:
            return False
        
        # Deal with extracting variables from XML
        streamer = xml.find('./config/src').text.strip()
        self.to_screen('%s: streamer url %s' % (video_id, streamer))
        rtmp_ext = 'mp4'

        formats = [{
            'format_id': 'rtmp_sd',
            'page_url': xmlurl,
            'url': streamer,
            'ext': rtmp_ext
        }]

        return {
            'id': story_id,
            'title': title,
            'formats': formats,
            'thumbnail': thumbnail,
            'description': description
            #'duration': duration,
        }
