from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

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