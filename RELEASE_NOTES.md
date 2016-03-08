solid_i18n release notes
========================

v1.2.0
------
- Add django 1.9 support
- Drop django 1.4 support

Issues: [#32](https://github.com/st4lk/django-solid-i18n-urls/issues/32)

v1.1.1
------
- fix django 1.8 `AppRegistryNotReady("Apps aren't loaded yet.")`

Issues: [#29](https://github.com/st4lk/django-solid-i18n-urls/issues/29)

v1.1.0
------

 - Use 301 redirect in case of `SOLID_I18N_DEFAULT_PREFIX_REDIRECT`
 - Upload wheel

Issues: [#24](https://github.com/st4lk/django-solid-i18n-urls/issues/24), [#20](https://github.com/st4lk/django-solid-i18n-urls/issues/20)

v1.0.0
------

 - Add django 1.8 support

Issues: [#8](https://github.com/st4lk/django-solid-i18n-urls/issues/8), [#19](https://github.com/st4lk/django-solid-i18n-urls/issues/19)

v0.9.1
------

 - fix working with [set_language](https://docs.djangoproject.com/en/dev/topics/i18n/translation/#set-language-redirect-view) and `SOLID_I18N_HANDLE_DEFAULT_PREFIX = True`

Issues: [#17](https://github.com/st4lk/django-solid-i18n-urls/issues/17)

v0.8.1
------

 - fix url reverse in case of `SOLID_I18N_HANDLE_DEFAULT_PREFIX = True`
 - simplify django version checking

Issues: [#13](https://github.com/st4lk/django-solid-i18n-urls/issues/13), [#14](https://github.com/st4lk/django-solid-i18n-urls/issues/14)

v0.7.1
------

 - add settings `SOLID_I18N_HANDLE_DEFAULT_PREFIX` and `SOLID_I18N_DEFAULT_PREFIX_REDIRECT`

Issues: [#12](https://github.com/st4lk/django-solid-i18n-urls/issues/12)

v0.6.1
------

 - handle urls with default language prefix explicitly set

Issues: [#10](https://github.com/st4lk/django-solid-i18n-urls/issues/10)

v0.5.1
------

 - add django 1.7 support
 - add python 3.4 support

Issues: [#6](https://github.com/st4lk/django-solid-i18n-urls/issues/6)

v0.4.3
------

 - fix http header 'Vary Accept-Language'

Issues: [#4](https://github.com/st4lk/django-solid-i18n-urls/issues/4)

v0.4.2
------

 - stop downgrading Django from 1.6.x to 1.6
 - include requirements.txt in distribution
 - minor docs updates

Issues: [#3](https://github.com/st4lk/django-solid-i18n-urls/issues/3)

v0.4.1
------
Add python 3.2, 3.3 support.

Issues: [#2](https://github.com/st4lk/django-solid-i18n-urls/issues/2)

v0.3.1
------

Add django 1.6 support

v0.2.1
------

Update README and data for pypi

v0.2
----

First version in pypi
