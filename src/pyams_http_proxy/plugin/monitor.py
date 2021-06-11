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

"""PyAMS_http_proxy.plugin.monitor module

Small plug-in module used for monitoring.

This plug-in doesn't do a real proxy but returns a static response defined into
it's configuration.
"""

__docformat__ = 'restructuredtext'

from starlette.responses import JSONResponse, Response

from pyams_http_proxy.plugin import ProxyPlugin
from pyams_http_proxy.proxy import LOGGER


class Monitor(ProxyPlugin):
    """A small proxy used for service monitoring"""

    config_name = 'monitor'

    @staticmethod
    def init_plugin():
        """Plugin global initialization"""
        LOGGER.info("Loaded monitoring plug-in")

    @staticmethod
    def init_proxy(base_path, settings):
        """Plugin base path initialization"""
        LOGGER.info("Monitoring plug-in init: %s (%s)", base_path, settings)

    @staticmethod
    async def pre_handler(request, config):  # pylint: disable=unused-argument
        """Logger pre-handler"""
        return request

    @staticmethod
    async def post_handler(request, response, config):  # pylint: disable=unused-argument
        """Monitor post-handler"""
        content = config.get('content', None)
        factory = Response if isinstance(content, str) else JSONResponse
        return factory(status_code=config.get('status_code', 200),
                       content=content,
                       media_type=config.get('media_type', 'text/plain'))
