from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .forms import WeatherSearchForm
from .serializers import (
    WeatherRequestSerializer,
    WeatherResponseSerializer,
)
from .services.aggregator import get_aggregated_weather


class WeatherPageView(LoginRequiredMixin, FormView):
    template_name = "weather/index.html"
    form_class = WeatherSearchForm
    login_url = "login"

    def form_valid(self, form):
        weather = get_aggregated_weather(**form.cleaned_data)
        return self.render_to_response(
            self.get_context_data(form=form, weather=weather)
        )


class WeatherView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        input_serializer = WeatherRequestSerializer(data=request.query_params)
        input_serializer.is_valid(raise_exception=True)

        data = get_aggregated_weather(**input_serializer.validated_data)

        output_serializer = WeatherResponseSerializer(data)
        return Response(output_serializer.data)
