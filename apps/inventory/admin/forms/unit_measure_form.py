from django import forms
from ...models import UnitMeasure

class UnitMeasureForm(forms.ModelForm):
    class Meta:
        model = UnitMeasure
        fields = ["name", "abbreviation"]