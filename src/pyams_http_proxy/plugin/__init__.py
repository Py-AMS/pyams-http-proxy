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

"""PyAMS_http_proxy.plugin module

This module defines base proxy plug-in class.
"""

import re


__docformat__ = 'restructuredtext'


class ProxyPlugin:
    """Base proxy plug-in class"""

    @staticmethod
    def apply_to(request, config):
        """Check if plug-in should be applied to given request"""
        filters = config.get('filters', None)
        if not filters:
            return True
        for getter in filters:
            method, path = getter.split()
            if (request.method in method.split('|')) and re.match(path, request.url.path):
                return True
        return False
