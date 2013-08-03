from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="home.html"), name='home'),
    url(r'^about/$', TemplateView.as_view(template_name="about.html"),
        name='about'),
)

urlpatterns += patterns('',
    url(r'^onelang/', TemplateView.as_view(template_name="onelang.html"),
        name='onelang'),
    (r'^i18n/', include('django.conf.urls.i18n')),
)
