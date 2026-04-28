from django.db import models


class Location(models.Model):
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True)

    lat = models.FloatField()
    lon = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("city", "country")


class WeatherSource(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class CurrentWeather(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    source = models.ForeignKey(WeatherSource, on_delete=models.CASCADE)

    temperature = models.FloatField()
    feels_like = models.FloatField(null=True, blank=True)

    humidity = models.IntegerField(null=True, blank=True)
    pressure = models.IntegerField(null=True, blank=True)

    wind_speed = models.FloatField(null=True, blank=True)

    description = models.CharField(max_length=255, blank=True)

    observed_at = models.DateTimeField()
    fetch_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("location", "source", "observed_at")


class Forecast(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    source = models.ForeignKey(WeatherSource, on_delete=models.CASCADE)

    date = models.DateField()

    min_temp = models.FloatField()
    max_temp = models.FloatField()

    humidity = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ("location", "source", "date")


class AggregatedWeather(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    temperature = models.FloatField()
    sources_used = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)


class WeatherRequest(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)

    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)

    status = models.CharField(max_length=20)
    response_time_ms = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
