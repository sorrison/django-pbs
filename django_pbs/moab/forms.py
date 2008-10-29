from django import forms


servers = (
    ('tango-m.vpac.org', 'Tango'),
    ('wexstan.vpac.org', 'Wexstan'),
    ('edda-m.vpac.org', 'Edda'),
)


class ShowstartForm(forms.Form):

    server = forms.ChoiceField(choices=servers)
    procs = forms.IntegerField()
    time = forms.IntegerField()
