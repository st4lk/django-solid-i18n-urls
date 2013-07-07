from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="home.html"), name='home'),
    url(r'^about/$', TemplateView.as_view(template_name="about.html"),
        name='about'),
)

urlpatterns += patterns('',
    url(r'^onelang/', TemplateView.as_view(template_name="onelang.html"),
        name='onelang')
)
