from django import forms

from .models import City


class JourneyForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(), label='Ville', required=True)
    nb_people = forms.CharField(max_length=100, label='Gens', initial='1', required=True)
    conveyance_choices = [
        ("car", "En voiture"),
        ("train", "En voiture"),
    ]
    conveyance = forms.CharField(widget=forms.Select(choices=conveyance_choices),
                               initial='car',
                               required=True,
                               label='Moyen de transport')
    
    def clean(self):
        cleaned_data = super(JourneyForm, self).clean()
        print('cleaned_data')
        print(cleaned_data)

        return cleaned_data


class ParamForm(forms.Form):
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
        cleaned_data = super(ParamForm, self).clean()

        return cleaned_data