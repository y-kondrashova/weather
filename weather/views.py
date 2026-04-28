from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import (
    WeatherRequestSerializer,
    WeatherResponseSerializer,
)
from .services.aggregator import get_aggregated_weather


class WeatherView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        input_serializer = WeatherRequestSerializer(data=request.query_params)
        input_serializer.is_valid(raise_exception=True)

        data = get_aggregated_weather(**input_serializer.validated_data)

        output_serializer = WeatherResponseSerializer(data)
        return Response(output_serializer.data)