from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = 'home/home.html'

class About(TemplateView):
    template_name = 'home/about.html'
    
    
class Contact(TemplateView):
    template_name = 'home/contact.html'
