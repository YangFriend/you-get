#!/usr/bin/env python

import urllib.request
import urllib.parse
import json
import re

from ..util import log
from ..common import get_content, download_urls, print_info, playlist_not_supported, url_size

__all__ = ['naver_download_by_url']


def naver_download_by_url(url, info_only=False, **kwargs):
    ep = 'https://apis.naver.com/rmcnmv/rmcnmv/vod/play/v2.0/{}?key={}'
    page = get_content(url)
    og_video_url = re.search(r"<meta\s+property=\"og:video:url\"\s+content='(.+?)'>", page).group(1)
    params_dict = urllib.parse.parse_qs(urllib.parse.urlparse(og_video_url).query)
    vid = params_dict['vid'][0]
    key = params_dict['outKey'][0]
    meta_str = get_content(ep.format(vid, key))
    meta_json = json.loads(meta_str)
    if 'errorCode' in meta_json:
        log.wtf(meta_json['errorCode'])
    title = meta_json['meta']['subject']
    videos = meta_json['videos']['list']
    video_list = sorted(videos, key=lambda video: video['encodingOption']['width'])
    video_url = video_list[-1]['source']
    # size = video_list[-1]['size']
    # result wrong size
    size = url_size(video_url)
    print_info(site_info, title, 'mp4', size)
    if not info_only:
        download_urls([video_url], title, 'mp4', size, **kwargs)

site_info = "naver.com"
download = naver_download_by_url
download_playlist = playlist_not_supported('naver')
