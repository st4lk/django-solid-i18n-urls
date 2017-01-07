from django.conf.urls import url, include
from django.views.generic import TemplateView

from solid_i18n.urls import solid_i18n_patterns

urlpatterns = solid_i18n_patterns(
    url(r'^$', TemplateView.as_view(template_name="home.html"), name='home'),
    url(r'^about/$', TemplateView.as_view(template_name="about.html"),
        name='about'),
)

# without i18n
urlpatterns += [
    url(r'^onelang/', TemplateView.as_view(template_name="onelang.html"),
        name='onelang'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]
