from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Organizacao, User, Grupo, Evento
from django import forms

TIPO_EVENTO_CHOICES = [
    ('reuniao', 'Reunião'),
    ('tarefa', 'Tarefa'),
    ('evento', 'Evento'),
    ('treinamento', 'Treinamento'),
    ('apresentacao', 'Apresentação'),
    ('outro', 'Outro'),
]

class CustomUserCreateForm(UserCreationForm):
	class Meta:
		model = CustomUser #Definindo o modelo
		fields = {'first_name', 'last_name'} #Devemos passar o que foi exatamente descrito no 'REQUIRED_FIELDS' presente no arquivo models do custom
		labels = {'username': 'Username/E-mail'} #Passando label para o campo 'username'

	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		user.email = self.cleaned_data["username"]
		if commit:
			user.save()
		return user

class CustomUserChangeForm(UserChangeForm):
	class Meta:
		model = CustomUser #Definindo o modelo
		fields = {'first_name', 'last_name'} #Devemos passar o que foi exatamente descrito no 'REQUIRED_FIELDS' presente no arquivo models do custom


class OrganizacaoForm(forms.ModelForm):
    class Meta:
        model = Organizacao
        fields = ['nome', 'logo']

    def save(self, user, commit=True):
        organizacao = super().save(commit=False)
        if commit:
            organizacao.save()
            organizacao.membros.add(user)
            organizacao.admin.add(user)
        return organizacao

class GroupForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = ['nome', 'descricao', 'membros', 'grupo_img', 'capa_grupo_img', 'tipo']

        labels = {
            'nome': 'Nome do Grupo',
            'descricao': 'Descrição',
            'membros': 'Membros',
            'grupo_img': 'Imagem do Grupo',
            'capa_grupo_img': 'Imagem do Capa do Grupo',
            'tipo': 'Tipo de Grupo',
        }

        widgets = {
            'descricao': forms.Textarea(attrs={'placeholder': 'Descreva o grupo', 'rows': 2}),
        }

    def save(self, user, commit=True):
        organization = Organizacao.objects.filter(
            deleted_at__isnull=True, membros=user
        ).first()

        grupo = super().save(commit=False)  # Não salva ainda

        grupo.admin = user
        if organization:
            grupo.organizacao = organization

        if commit:
            grupo.save()
            grupo.membros.add(user)

        return grupo

class EventoForm(forms.ModelForm):
    tipo = forms.ChoiceField(
        choices=TIPO_EVENTO_CHOICES, # Corrigido para usar TIPO_EVENTO_CHOICES definido neste arquivo
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True,
        label='Tipo'
    )

    descricao = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 2,
            'class': 'form-control'
        }),
        label='Descrição',
        required=True
    )

    participantes = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'id': 'select-participantes',
            'class': 'form-select',
            'multiple': 'multiple'
        }),
        required=False,
        label='Participantes'
    )
    link = forms.URLField(required=False)

    class Meta:
        model = Evento
        fields = ['nome', 'descricao', 'tipo', 'data', 'modalidade', 'link', 'participantes']
        widgets = {
            'data': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)

        if user:
            organization = Organizacao.objects.filter(membros=user).first()
            if organization:
                self.fields['participantes'].queryset = User.objects.filter(
                    membros_organizacao=organization)
            else:
                self.fields['participantes'].queryset = User.objects.none()

            if instance is None:
                self.fields['participantes'].queryset = self.fields['participantes'].queryset.exclude(id=user.id)