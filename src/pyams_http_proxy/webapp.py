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

"""PyAMS_http_proxy.webapp module

Base webapp module for easy Gunicorn integration.
"""


try:
    from elasticapm.contrib.starlette import ElasticAPM, make_apm_client
except ImportError:
    ElasticAPM = make_apm_client = None

from pyams_http_proxy.proxy import ProxyApplication


__docformat__ = 'restructuredtext'


if ElasticAPM is not None:

    class ProxyAPM(ElasticAPM):
        """Custom proxy APM"""
        async def __call__(self, scope, receive, send):
            scope['app'] = self.app
            return await super().__call__(scope, receive, send)


async def create_application(config):
    """Proxy application factory"""
    app = await ProxyApplication.create(config)
    if ElasticAPM is not None:
        apm_config = config.get('apm')
        if apm_config is not None:
            apm_client = make_apm_client(apm_config)
            app = ProxyAPM(app, client=apm_client)
    return app
