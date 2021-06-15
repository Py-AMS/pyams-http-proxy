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

"""PyAMS_http_proxy.plugin.head_filter module

This proxy plug-in can be used to add or remove headers from input request.

Plug-in specific configuration:
 - removed: list of headers names which must be removed from input request
 - added: object containing headers which must be removed from input request.
"""

__docformat__ = 'restructuredtext'

from pyams_http_proxy.plugin import ProxyPlugin
from pyams_http_proxy.proxy import LOGGER


class RequestHeaders(ProxyPlugin):
    """A proxy plugin used to add or remove headers from input request"""

    config_name = 'request_headers'

    @staticmethod
    def init_plugin():
        """Plugin global initialization"""
        LOGGER.info("Loaded request headers filter")

    @staticmethod
    def init_proxy(base_path, settings):
        """Plugin base path initialization"""
        LOGGER.info("Request headers filter init: %s (%s)", base_path, settings)

    @staticmethod
    async def pre_handler(request, config):  # pylint: disable=unused-argument
        """Logger pre-handler"""
        added = config.get('added', {})
        removed = config.get('removed', ())
        if added or removed:
            headers = getattr(request.state, 'headers', dict(request.headers))
            for key, value in added.items():
                headers[key.lower()] = value
            for key in removed:
                if key.lower() in headers:
                    del headers[key.lower()]
            request.state.headers = headers
        return request

    @staticmethod
    async def post_handler(request, response, config):  # pylint: disable=unused-argument
        """Logger post-handler"""
        return response
