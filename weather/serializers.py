from rest_framework import serializers


class WeatherRequestSerializer(serializers.Serializer):
    city = serializers.CharField(required=False)
    lat = serializers.FloatField(required=False)
    lon = serializers.FloatField(required=False)

    def validate(self, data):
        city = data.get("city")
        lat = data.get("lat")
        lon = data.get("lon")

        if city:
            return data

        if lat is not None and lon is not None:
            return data

        raise serializers.ValidationError(
            "Provide either city OR both lat and lon"
        )

class WeatherResponseSerializer(serializers.Serializer):
    city = serializers.CharField()
    temperature = serializers.FloatField()
    feels_like = serializers.FloatField()
    humidity = serializers.FloatField()
    pressure = serializers.IntegerField()
    description = serializers.ListField(child=serializers.CharField())
    sources = serializers.ListField(child=serializers.CharField())
