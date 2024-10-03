from django.views.generic import TemplateView


class AboutUsView(TemplateView):
    template_name = 'about_us.html'


class TermsAndConditionsView(TemplateView):
    template_name = 'terms_and_conditions.html'
