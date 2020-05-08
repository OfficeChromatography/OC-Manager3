from django import forms
PROP_CHOICES =(
    ("1", "N Bands"),
    ("2", "Lenght"),
)
class SampleAppForm(forms.Form):
    motor_speed = forms.IntegerField(
                                    label='MotorSpeed',
                                    widget=forms.NumberInput(
                                    attrs={'class': 'form-control'}))

    delta_y = forms.IntegerField(   label='Delta Y',
                                    widget=forms.NumberInput(
                                    attrs={'class': 'form-control'}))

    delta_x = forms.IntegerField(   label='Delta X',
                                    widget=forms.NumberInput(
                                    attrs={'class': 'form-control'}))

    pressure = forms.IntegerField(  label='Pressure',
                                    widget=forms.NumberInput(
                                    attrs={'class': 'form-control'}))

    delta_pressure = forms.IntegerField(   label='Delta Pressure',
                                            widget=forms.NumberInput(
                                            attrs={'class': 'form-control'}))

    size_x = forms.IntegerField(    label='X Size',
                                    widget=forms.NumberInput(
                                    attrs={'class': 'form-control'}))

    size_y = forms.IntegerField(    label='Y Size',
                                    widget=forms.NumberInput(
                                    attrs={'class': 'form-control'}))

    offset_x = forms.IntegerField(    label='X Offset',
                                    widget=forms.NumberInput(
                                    attrs={'class': 'form-control'}))

    offset_y = forms.IntegerField(    label='Y Offset',
                                    widget=forms.NumberInput(
                                    attrs={'class': 'form-control'}))

    main_property = forms.ChoiceField(choices = PROP_CHOICES, label='Main Property', widget=forms.Select(attrs={'class':'form-control'}))

    n_bands = forms.IntegerField(   label='N° Bands',
                                    required=False,
                                    widget=forms.NumberInput(
                                    attrs={'class': 'form-control'}))

    length = forms.IntegerField(    label='Length',
                                    required=False,
                                    widget=forms.NumberInput(
                                    attrs={'class': 'form-control'}))

    height = forms.IntegerField(    label='Height',
                                    widget=forms.NumberInput(
                                    attrs={'class': 'form-control'}))

    gap = forms.IntegerField(       label='Gap',
                                    widget=forms.NumberInput(
                                    attrs={'class': 'form-control'}))
