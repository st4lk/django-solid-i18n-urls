from django.conf import settings


def solid_i18n(request):
    example_vars = {
        'SOLID_I18N_USE_REDIRECTS': settings.SOLID_I18N_USE_REDIRECTS,
    }
    return {"example_vars": example_vars}
