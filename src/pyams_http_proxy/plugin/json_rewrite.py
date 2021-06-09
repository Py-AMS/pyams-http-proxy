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

"""PyAMS_http_proxy.plugin.json_rewrite module

This proxy plugin can be used to rewrite value of some fields which can be
found in JSON response.

Plug-in specific configuration:
 - attributes: can be set as a list of dotted attributes names, or as an object; if set as an
   object, object's properties are the names of JSON attributes which may be updated, and values
   are a "from"/"to" dict containing source and replacement strings.
 - from: if "attributes" is a strings array, contains the source string to be replaced in all
   given attributes
 - to: if "attributes" is a strings array, contains the attributes replacement string for all
   given attributes
"""

__docformat__ = 'restructuredtext'

import json
from json import JSONDecodeError

from starlette.responses import JSONResponse, Response

from pyams_http_proxy.plugin import ProxyPlugin
from pyams_http_proxy.proxy import LOGGER


class JSONUrlRewriter(ProxyPlugin):
    """A proxy plugin used to rewrite JSON attributes"""

    config_name = 'json_rewrite'

    @staticmethod
    def init_plugin():
        """Plugin global initialization"""
        LOGGER.info("Loaded JSON URL rewriter")

    @staticmethod
    def init_proxy(base_path, settings):
        """Plugin base path initialization"""
        LOGGER.info("JSON rewrite URL init: %s (%s)", base_path, settings)

    @staticmethod
    async def pre_handler(request, config):  # pylint: disable=unused-argument
        """Logger pre-handler"""
        return request

    @staticmethod
    async def post_handler(request, response, config):  # pylint: disable=unused-argument
        """Logger post-handler"""
        if isinstance(response, Response):
            body = response.body
        else:
            body = ''
            async for chunk in response.aiter_text():
                body += chunk
        try:
            body = json.loads(body)
            attributes = config['attributes']
            if isinstance(attributes, list):
                attributes = dict((
                    (attr, {
                        'from': config.get('from'),
                        'to': config.get('to')
                    })
                    for attr in attributes
                ))
            for attr, settings in attributes.items():
                mapping = body
                names = attr.split('.')
                for name in names[:-1]:
                    mapping = mapping.get(name, {})
                name = names[-1]
                if name not in mapping:
                    continue
                mapping[name] = mapping[name].replace(settings['from'], settings['to'])
        except JSONDecodeError:
            LOGGER.exception("JSON decoding error")
        return JSONResponse(body, status_code=response.status_code)
