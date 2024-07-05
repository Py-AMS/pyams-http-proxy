Changelog
=========

1.7.0
-----
 - added support for "includes" config option, to update initial configuration
   with other files or directories contents

1.6.0
-----
 - updated Elasticsearch client settings
 - reuse current HTTP client instead of creating a new one in lifespan handler

1.5.0
-----
 - added Elasticsearch APM support
 - updated Elasticsearch logger to handle all transport exceptions
 - updated HTTPx package API

1.4.0
-----
 - updated Elasticsearch logger to be able to update incoming request payload before
   indexing; this is actually used to obfuscate elements from JSON body...
 - added tests in proxy to only decode bytes

1.3.3
-----
 - updated proxy headers getter to handle requests and response correctly

1.3.2
-----
 - updated proxy URL getter to handle null remotes used for service monitoring

1.3.1
-----
 - updated request headers plug-in configuration name

1.3.0
-----
 - added headers filter plug-in, to add or remove headers from incoming request
 - improved support for plug-ins handling request headers

1.2.0
-----
 - added "context extension" by providing a "++ext++" URL path element; this
   allows to access several contexts with a same base URL

1.1.0
-----
 - added monitoring plug-in

1.0.3
-----
 - small update in JSON configuration file format

1.0.2
-----
 - Gitlab-CI update

1.0.1
-----
 - removed reference to Pyramid in doctests

1.0.0
-----
 - initial release
