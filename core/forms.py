from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Organizacao, User
from django import forms

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
            organizacao.membros.add(user)  # Adiciona o criador como membro
            organizacao.admin.add(user)  # Adiciona o criador como admin
        return organizacao