from django import forms


class WeatherSearchForm(forms.Form):
    city = forms.CharField(
        required=False,
        label="City",
        widget=forms.TextInput(attrs={"placeholder": "Kyiv"}),
    )
    lat = forms.FloatField(
        required=False,
        label="Latitude",
        widget=forms.NumberInput(attrs={"step": "any", "placeholder": "50.45"}),
    )
    lon = forms.FloatField(
        required=False,
        label="Longitude",
        widget=forms.NumberInput(attrs={"step": "any", "placeholder": "30.52"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        city = cleaned_data.get("city")
        lat = cleaned_data.get("lat")
        lon = cleaned_data.get("lon")

        if city:
            cleaned_data["lat"] = None
            cleaned_data["lon"] = None
            return cleaned_data

        if lat is not None and lon is not None:
            return cleaned_data

        raise forms.ValidationError("Provide either city or both latitude and longitude.")
