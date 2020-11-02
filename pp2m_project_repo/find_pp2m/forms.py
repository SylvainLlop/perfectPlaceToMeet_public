from django import forms

from .models import City


class CityForm(forms.Form):
    # --- Version city = forms.CharField
    # city_1 = forms.CharField(max_length=100, label='Ville 1')
    # city_2 = forms.CharField(max_length=100, label='Ville 2')
    # city_3 = forms.CharField(max_length=100, label='Ville 3')
    # ----------------------------------
    city_01 = forms.ModelChoiceField(queryset=City.objects.all(), label='Ville 1')
    city_02 = forms.ModelChoiceField(queryset=City.objects.all(), label='Ville 2')
    city_03 = forms.ModelChoiceField(queryset=City.objects.all(), label='Ville 3', required=False)
    city_04 = forms.ModelChoiceField(queryset=City.objects.all(), label='Ville 4', required=False)
    city_05 = forms.ModelChoiceField(queryset=City.objects.all(), label='Ville 5', required=False)
    city_06 = forms.ModelChoiceField(queryset=City.objects.all(), label='Ville 6', required=False)
    city_07 = forms.ModelChoiceField(queryset=City.objects.all(), label='Ville 7', required=False)
    city_08 = forms.ModelChoiceField(queryset=City.objects.all(), label='Ville 8', required=False)
    city_09 = forms.ModelChoiceField(queryset=City.objects.all(), label='Ville 9', required=False)
    city_10 = forms.ModelChoiceField(queryset=City.objects.all(), label='Ville 10', required=False)
    city_11 = forms.ModelChoiceField(queryset=City.objects.all(), label='Ville 11', required=False)
    city_12 = forms.ModelChoiceField(queryset=City.objects.all(), label='Ville 12', required=False)
    city_13 = forms.ModelChoiceField(queryset=City.objects.all(), label='Ville 13', required=False)
    city_14 = forms.ModelChoiceField(queryset=City.objects.all(), label='Ville 14', required=False)
    city_15 = forms.ModelChoiceField(queryset=City.objects.all(), label='Ville 15', required=False)
    city_16 = forms.ModelChoiceField(queryset=City.objects.all(), label='Ville 16', required=False)
    city_17 = forms.ModelChoiceField(queryset=City.objects.all(), label='Ville 17', required=False)
    city_18 = forms.ModelChoiceField(queryset=City.objects.all(), label='Ville 18', required=False)
    city_19 = forms.ModelChoiceField(queryset=City.objects.all(), label='Ville 19', required=False)
    city_20 = forms.ModelChoiceField(queryset=City.objects.all(), label='Ville 20', required=False)
    method_choices = [
        ("route_duration", "Temps en voiture"),
        ("route_distance", "Distance en voiture"),
        ("raw_distance", "Distance à vol d'oiseau"),
    ]
    method = forms.CharField(widget=forms.Select(choices=method_choices),
                               initial='route_duration',
                               required=True,
                               label='Méthode de calcul')
    criteria_choices = [
        ("community", "Collectif"),
        ("individual", "Individuel"),
    ]
    criteria = forms.CharField(widget=forms.Select(choices=criteria_choices),
                               initial='community',
                               required=True,
                               label='Critère')

    def clean(self):
        cleaned_data = super(CityForm, self).clean()

        return cleaned_data


class JourneyForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(), label='Ville', required=False)
    nb_people = forms.CharField(max_length=100, label='Gens', initial='1', required=False)
    conveyance_choices = [
        ("car", "En voiture"),
        ("train", "En voiture"),
    ]
    conveyance = forms.CharField(widget=forms.Select(choices=conveyance_choices),
                               initial='car',
                               required=False,
                               label='Moyen de transport')
    
    def clean(self):
        cleaned_data = super(JourneyForm, self).clean()

        return cleaned_data

