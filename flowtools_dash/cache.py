from flask_caching import Cache

#Using SimpleCache configuration, because we're not deploying it online yet.
#Later on, we'll use something like RedisCaching. This file will look way more complicated.

cache = Cache(config={
    'CACHE_TYPE': 'SimpleCache',        # In-memory caching
    'CACHE_DEFAULT_TIMEOUT': 300        # Default timeout (in seconds) for cached items. (Five minutes.)
})

def init_cache(app):
    #initialize cache within a given Dash app
    #use: init_cache(app)
    cache.init_app(app.server)