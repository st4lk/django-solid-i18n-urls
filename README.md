Django solid_i18n urls
=====

[![Build Status](https://travis-ci.org/st4lk/django-solid-i18n-urls.png?branch=master)](https://travis-ci.org/st4lk/django-solid-i18n-urls) [![Coverage Status](https://coveralls.io/repos/st4lk/django-solid-i18n-urls/badge.png?branch=master)](https://coveralls.io/r/st4lk/django-solid-i18n-urls?branch=master)

solid_i18n contains middleware and url patterns to use default language at root path (without language prefix).

Default language is set in settings.LANGUAGE_CODE.


Requirements
-----------

- python (2.6, 2.7)
- django (1.4, 1.5)


Behaviour
-----------

There are two modes:

 1. `settings.SOLID_I18N_USE_REDIRECTS = False` (default). In that case i18n
 will not use redirects at all. If request doesn't have language prefix,
 then default language will be used. If request does have prefix, language
 from that prefix will be used.

 2. `settings.SOLID_I18N_USE_REDIRECTS = True`. In that case, for root paths (without
 prefix), django will [try to discover](https://docs.djangoproject.com/en/dev/topics/i18n/translation/#how-django-discovers-language-preference) user preferred language. If it doesn't equal to default language, redirect to path with corresponding
 prefix will occur. If preferred language is the same as default, then that request
 path will be processed (without redirect). Also see notes below.


Quick start
-----------

1. Install this package to your python distribution:

        - pip install solid_i18n

2. Set languages in settings.py:

        # Default language, that will be used for requests without language prefix
        LANGUAGE_CODE = 'en'

        # supported languages
        LANGUAGES = (
            ('en', 'English'),
            ('ru', 'Russian'),
        )

        # enable django translation
        USE_I18N = True

        # Optional. If you want to use redirects, set this to True
        SOLID_I18N_USE_REDIRECTS = False

3. Add `SolidLocaleMiddleware` instead of [LocaleMiddleware](https://docs.djangoproject.com/en/dev/topics/i18n/translation/#how-django-discovers-language-preference) to `MIDDLEWARE_CLASSES`:

        MIDDLEWARE_CLASSES = (
           'django.contrib.sessions.middleware.SessionMiddleware',
           'solid_i18n.middleware.SolidLocaleMiddleware',
           'django.middleware.common.CommonMiddleware',
        )

4. Use `solid_i18n_patterns` instead of [i18n_patterns](https://docs.djangoproject.com/en/dev/topics/i18n/translation/#django.conf.urls.i18n.i18n_patterns)

        from django.conf.urls import patterns, include, url
        from solid_i18n.urls import solid_i18n_patterns

        urlpatterns = patterns(''
            url(r'^sitemap\.xml$', 'sitemap.view', name='sitemap_xml'),
        )

        news_patterns = patterns(''
            url(r'^$', 'news.views.index', name='index'),
            url(r'^category/(?P<slug>[\w-]+)/$', 'news.views.category', name='category'),
            url(r'^(?P<slug>[\w-]+)/$', 'news.views.details', name='detail'),
        )

        urlpatterns += solid_i18n_patterns('',
            url(r'^about/$', 'about.view', name='about'),
            url(r'^news/', include(news_patterns, namespace='news')),
        )

5. Start the development server and visit http://127.0.0.1:8000/about/ to see English content. Visit http://127.0.0.1:8000/ru/about/ to see Russian content. If `SOLID_I18N_USE_REDIRECTS` was set to `True` and if your preferred language is equal to Russian, request to path http://127.0.0.1:8000/about/ will be redirected to http://127.0.0.1:8000/ru/about/. But if preferred language is English, http://127.0.0.1:8000/about/ will be shown.


Example site
-----------

Located [here](https://github.com/st4lk/django-solid-i18n-urls/tree/master/example), it is ready to use, just install solid_i18n (this package):

    pip install solid_i18n

clone example site:

    git clone https://github.com/st4lk/django-solid-i18n-urls.git

step in  example/ and run development server:

    cd django-solid-i18n-urls/example
    python manage.py runserver


Notes
-----------

- When using `SOLID_I18N_USE_REDIRECTS = True`, there is some nasty case. Suppose django has determined user preferred language incorrectly (maybe in user's browser preferred language is not equal to his realy preferred language, because for example it is not his computer) and it is Russian. Then on access to url without prefix, i.e. `'/'`, he will be redirected to `'/ru/'` (according to browsers preferred language). He wants to look english content (that is default language), but he can't, because he is always being redirected to `'/ru/'` from `'/'`. To avoid this, it is needed to set preferred language in his cookies (just `<a href="{{ specific language url}}">` will not work). For that purporse django's [set_language redirect view](https://docs.djangoproject.com/en/dev/topics/i18n/translation/#the-set-language-redirect-view) shall be used. See example in this package.

- Of course, you must specify translation for all languages you've marked as supported. For details look here: [https://docs.djangoproject.com/en/dev/topics/i18n/translation/](https://docs.djangoproject.com/en/dev/topics/i18n/translation/).
