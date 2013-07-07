from django.conf.urls import patterns, url
from solid_i18n.urls import solid_i18n_patterns
from django.views.generic import TemplateView

urlpatterns = solid_i18n_patterns('',
    url(r'^$', TemplateView.as_view(template_name="home.html"), name='home'),
    url(r'^about/$', TemplateView.as_view(template_name="about.html"),
        name='about'),
)

# without i18n
urlpatterns += patterns('',
    url(r'^onelang/', TemplateView.as_view(template_name="onelang.html"),
        name='onelang')
)
