from django.contrib import admin
from weather.models import Location, WeatherSource, CurrentWeather


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("city", "country", "lat", "lon")
    search_fields = ("city", "country")


@admin.register(WeatherSource)
class WeatherSourceAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")


@admin.register(CurrentWeather)
class CurrentWeatherAdmin(admin.ModelAdmin):
    list_display = ("location", "temperature", "source", "observed_at")
    list_filter = ("source",)
    search_fields = ("location__city",)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
