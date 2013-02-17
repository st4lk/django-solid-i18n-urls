Django solid_i18n urls
=====

Tested on Django 1.4.

solid_i18n contains middleware and url patterns to enable i18n urls without redirects. Some search engines don't index site with redirects well.

With solid_i18n, default language will be used for request
without language prefix. Non default languages works same as builtin [i18n_patterns](https://docs.djangoproject.com/en/dev/topics/i18n/translation/#django.conf.urls.i18n.i18n_patterns).


Quick start
-----------

1. Install this package to your python distribution

2. Set languages in settings.py:

        # Default language, that will be used for requests without language prefix
        LANGUAGE_CODE = 'ru'

        # supported languages
        LANGUAGES = (
            ('ru', 'Russian'),
            ('en', 'English'),
        )

        # enable django translation
        USE_I18N = True

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

5. Start the development server and visit http://127.0.0.1:8000/about/ to see Russian content. Visit http://127.0.0.1:8000/en/about/ to see English content. Of course, you must specify translation for all languages you've marked as supported. For details look here: [https://docs.djangoproject.com/en/dev/topics/i18n/translation/](https://docs.djangoproject.com/en/dev/topics/i18n/translation/)
