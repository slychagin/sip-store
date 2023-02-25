from datetime import date

from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'
    initial = date.today().strftime("%Y-%m-%d")


class TimeInput(forms.TimeInput):
    input_type = 'time'
