import logging
import os
import pathlib

from mopidy import core
from mopidy.core import LibraryController

import tornado.web

logger = logging.getLogger(__name__)


class ImageHandler(tornado.web.StaticFileHandler):
    def get_cache_time(self, *args):
        return self.CACHE_MAX_AGE


class IndexHandler(tornado.web.RequestHandler):
    def initialize(self, root):
        self.root = root

    def get(self, path):
        return self.render("index.html", images=self.uris())

    def get_template_path(self):
        return pathlib.Path(__file__).parent / "www"

    def uris(self):
        for _, _, files in os.walk(self.root):
            yield from files


class AlbumHandler(tornado.web.RequestHandler):
    def initialize(self, config, core):
        self.config = config
        self.core = core
        self.lc = LibraryController(core.backends.get(), core)

    def get(self):

        albums = self.lc.browse(uri="local:directory?type=album")
        images = self.lc.get_images([x.uri for x in albums])

        self.write("<p>albums</p>")
        for album in albums:
            image = images[album.uri][0] if images.get(album.uri) else None
            self.write("<p>{} {}</p>".format(album.name, images[album.uri]))
            if image:
                self.write("<img src={} style=\"width:150px;height:150px;\"/>".format(image.uri))
