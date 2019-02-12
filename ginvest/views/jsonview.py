import json
from django import http
from django.views.generic import View


class JSONResponseView(View):

    def post(self, request, *args, **kwargs):

        self.request = request
        return self.render_to_response()

    def render_to_response(self):
        return http.HttpResponse(json.dumps(self.get_context_data()), content_type="application/json")