from django.views.generic import TemplateView

class HomeView(TemplateView):

    template_name = "home.html"


# class TestView(TemplateView):

#     template_name = "test.html"

#     def get_context_data(self, **kwargs):

#         context = super(TestView, self).get_context_data(**kwargs)

#         for 


#         return context