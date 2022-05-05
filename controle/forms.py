from django.forms import ModelForm

from controle.models import Controller


class FileForm(ModelForm):
    class Meta:
        labels = {
            'file': 'Envie o arquivo'
        }
        model = Controller
        fields = "__all__"
