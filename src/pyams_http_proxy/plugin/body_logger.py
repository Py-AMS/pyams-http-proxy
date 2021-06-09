#
# Copyright (c) 2015-2021 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_http_proxy.plugin.body_logger module

A small plug-in used to log request body in system logger.

Plug-in specific configuration:
 - level: log level; 'info' by default

"""

__docformat__ = 'restructuredtext'

import logging
from json import JSONDecodeError

from pyams_http_proxy.plugin import ProxyPlugin
from pyams_http_proxy.proxy import LOGGER


class BodyLogger(ProxyPlugin):
    """A proxy plugin used to rewrite JSON attributes"""

    config_name = 'body_logger'

    @staticmethod
    def init_plugin():
        """Plugin global initialization"""
        LOGGER.info("Loaded request body logger")

    @staticmethod
    def init_proxy(base_path, settings):
        """Plugin base path initialization"""
        LOGGER.info("Body logger init: %s (%s)", base_path, settings)

    @staticmethod
    async def pre_handler(request, config):  # pylint: disable=unused-argument
        """Logger pre-handler"""
        try:
            body = await request.json()
        except JSONDecodeError:
            body = await request.form()
            if not body:
                body = await request.body()
        level = logging.getLevelName(config.get('level', 'info').upper())
        LOGGER.log(level, "request url: %s", request.url)
        LOGGER.log(level, "request body: %s", body)
        return request

    @staticmethod
    async def post_handler(request, response, config):  # pylint: disable=unused-argument
        """Logger post-handler"""
        return response
