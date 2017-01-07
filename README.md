Django solid_i18n urls
=====

[![Build Status](https://travis-ci.org/st4lk/django-solid-i18n-urls.svg?branch=master)](https://travis-ci.org/st4lk/django-solid-i18n-urls)
[![Coverage Status](https://coveralls.io/repos/st4lk/django-solid-i18n-urls/badge.svg?branch=master)](https://coveralls.io/r/st4lk/django-solid-i18n-urls?branch=master)
[![Pypi version](https://img.shields.io/pypi/v/solid_i18n.svg)](https://pypi.python.org/pypi/solid_i18n)

solid_i18n contains middleware and url patterns to use default language at root path (without language prefix).

Default language is set in settings.LANGUAGE_CODE.

Deprecation notice
------------------
Starting from [Django 1.10](https://docs.djangoproject.com/en/dev/releases/1.10/#internationalization), built-in `i18n_patterns` accept optional argument `prefix_default_language`. If it is `False`, then Django will serve url without language prefix by itself. Look [docs](https://docs.djangoproject.com/en/dev/topics/i18n/translation/#django.conf.urls.i18n.i18n_patterns) for more details.

This package can still be useful in following cases (look below for settings details):
- You need `settings.SOLID_I18N_USE_REDIRECTS = True` behaviour
- You need `settings.SOLID_I18N_HANDLE_DEFAULT_PREFIX = True` behaviour
- You need `settings.SOLID_I18N_DEFAULT_PREFIX_REDIRECT = True` behaviour
- You need `settings.SOLID_I18N_PREFIX_STRICT = True` behaviour

In all other cases no need in current package, just use Django>=1.10.


Requirements
-----------

- python (2.7, 3.4, 3.5)
- django (1.8, 1.9, 1.10)

Release notes
-------------

[Here](https://github.com/st4lk/django-solid-i18n-urls/blob/master/RELEASE_NOTES.md)


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

        pip install solid_i18n

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

3. Add `SolidLocaleMiddleware` instead of [LocaleMiddleware](https://docs.djangoproject.com/en/dev/ref/middleware/#django.middleware.locale.LocaleMiddleware) to `MIDDLEWARE_CLASSES`:

        MIDDLEWARE_CLASSES = (
           'django.contrib.sessions.middleware.SessionMiddleware',
           'solid_i18n.middleware.SolidLocaleMiddleware',
           'django.middleware.common.CommonMiddleware',
        )

4. Use `solid_i18n_patterns` instead of [i18n_patterns](https://docs.djangoproject.com/en/dev/topics/i18n/translation/#django.conf.urls.i18n.i18n_patterns)

        from django.conf.urls import patterns, include, url
        from solid_i18n.urls import solid_i18n_patterns

        urlpatterns = solid_i18n_patterns(
            url(r'^about/$', 'about.view', name='about'),
            url(r'^news/', include(news_patterns, namespace='news')),
        )

5. Start the development server and visit http://127.0.0.1:8000/about/ to see english content. Visit http://127.0.0.1:8000/ru/about/ to see russian content. If `SOLID_I18N_USE_REDIRECTS` was set to `True` and if your preferred language is equal to Russian, request to path http://127.0.0.1:8000/about/ will be redirected to http://127.0.0.1:8000/ru/about/. But if preferred language is English, http://127.0.0.1:8000/about/ will be shown.

Settings
--------

- `SOLID_I18N_USE_REDIRECTS = False`    
If `True`, redirect to url with non-default language prefix from url without prefix, if user's language is not equal to default. Otherwise url without language prefix will always render default language content (see [behaviour section](#behaviour) and [notes](#notes) for details).

- `SOLID_I18N_HANDLE_DEFAULT_PREFIX = False`    
If `True`, both urls `/...` and `/en/...` will render default language content (in this example 'en' is default language).
Otherwise, `/en/...` will return 404 status_code.

- `SOLID_I18N_DEFAULT_PREFIX_REDIRECT = False`    
If `True`, redirect from url with default language prefix to url without any prefix, i.e. redirect from `/en/...` to `/...` if 'en' is default language.

- `SOLID_I18N_PREFIX_STRICT = False`    
Experimental. If `True`, paths like `/my-slug/` will call your view on that path, if language my-slug doesn't exists (here `my` is supported language).

    Example.

        # settings.py
        LANGUAGES = (
            ('en', 'English'),
            ('my', 'Burmese'),
        )

        # urls.py
        urlpatterns = solid_i18n_patterns('',
            url(r'^my-slug/$', some_view),
        )

    If `SOLID_I18N_PREFIX_STRICT=False`, then url /my-slug/ will respond with 404, since language `my-slug` is not found.
    This happens, because we have a registered language tag `my`. Language tag can have form like this:

        language-region

    So django in this case tries to find language 'my-slug'. But it fails and that is why django respond 404.
    And your view `some_view` will not be called.

    But, if we set `SOLID_I18N_PREFIX_STRICT=True`, then resolve system will get language only from exact 'my' prefix.
    In case of /my-slug/ url the prefix is not exact, and our `some_view` will be found and called.

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

- Don't mix together settings `SOLID_I18N_HANDLE_DEFAULT_PREFIX` and `SOLID_I18N_DEFAULT_PREFIX_REDIRECT`. You should choose only one of them.
