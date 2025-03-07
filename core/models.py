from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser precisa ter is_superuser=True')
        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser precisa ter is_staff=True')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField('E-mail', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email
    

# Obtém o modelo CustomUser
User = get_user_model()

# Modelo de Organização
class Organizacao(models.Model):
    nome = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    descricao = models.TextField()
    membros = models.ManyToManyField(User, related_name='membros_organizacao')
    eventos = models.ManyToManyField('Evento', related_name='eventos_organizacao')

    def __str__(self):
        return self.nome


# Modelo de Grupo
class Grupo(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    membros = models.ManyToManyField(User, related_name='membros_grupo')

    def __str__(self):
        return self.nome


# Modelo de Imagem (para associar imagens a posts)
class Imagem(models.Model):
    imagem = models.ImageField(upload_to='posts/')
    descricao = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Imagem {self.id}"


# Modelo de Post
class Post(models.Model):
    descricao = models.CharField(max_length=255)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    conteudo = models.TextField()
    imagens = models.ManyToManyField(Imagem, related_name='imagens_post', blank=True)

    def __str__(self):
        return f"Post de {self.autor.email} - {self.descricao[:50]}"


# Modelo de Evento
class Evento(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='eventos')
    tipo = models.CharField(max_length=50)
    data = models.DateTimeField()
    modalidade = models.CharField(max_length=50, choices=[('presencial', 'Presencial'), ('online', 'Online'), ('hibrido', 'Híbrido')])
    link = models.URLField(max_length=200, null=True, blank=True)
    participantes = models.ManyToManyField(User, related_name='participantes_evento', blank=True)

    def __str__(self):
        return f"Evento: {self.nome} - {self.data.strftime('%Y-%m-%d')}"
