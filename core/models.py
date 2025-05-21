from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, BaseUserManager
from stdimage.models import StdImageField
from django.utils import timezone
from django.utils.timezone import localtime, now

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
    perfil_img = StdImageField('profile_img', upload_to='profile_img', null=True, blank=True, variations={'thumbnail': {'width': 500,'height': 500, 'crop': True}})

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email

# Obtém o modelo CustomUser
User = get_user_model()

class Base(models.Model):
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    modified_at = models.DateTimeField('Modificado em', auto_now=True)
    deleted_at = models.DateTimeField('Deletado em', blank=True, null=True)

    class Meta:
        abstract = True

# Modelo de Organização
class Organizacao(Base):
    nome = models.CharField(max_length=100)
    logo = StdImageField('logo', upload_to='organization_logo_img', null=True, blank=True, variations={'thumbnail': {'width': 500,'height': 500, 'crop': True}})
    descricao = models.TextField()
    membros = models.ManyToManyField(User, related_name='membros_organizacao')
    eventos = models.ManyToManyField('Evento', related_name='eventos_organizacao')
    admin = models.ManyToManyField(User, related_name='admins_organizacao')

    def __str__(self):
        return self.nome


# Modelo de Grupo
class Grupo(Base):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grupo_admins', null=True, blank='True')
    membros = models.ManyToManyField(User, related_name='membros_grupo', null=True, blank='True')
    organizacao = models.ForeignKey(Organizacao, on_delete=models.CASCADE, null=True, blank='True', related_name='grupos_organizacao')
    tipo = models.CharField(max_length=50, choices=[('privado', 'Privado'), ('publico', 'Público')], default='publico')
    grupo_img = StdImageField(
        'grupo_img',
        upload_to='grupo_img',
        null=True,
        blank=True,
        variations={
            'thumbnail': {
                'width': 500,
                'height': 500,
                'crop': True
            }
        }
    )

    capa_grupo_img = StdImageField(
        'capa_grupo_img',
        upload_to='capa_grupo_img',
        null=True,
        blank=True,
        variations={
            'cover': {
                'width': 1000,
                'height': 500,
                'crop': True
            }
        }
    )

    def __str__(self):
        return self.nome


# Modelo de Imagem (para associar imagens a posts)
class Imagem(Base):
    imagem = StdImageField('posts_img', upload_to='posts_img', null=True, blank=True)
    descricao = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Imagem {self.id}"


# Modelo de Post
class Post(Base):
    titulo = models.CharField(max_length=255)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='grupo_posts')
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    conteudo = models.TextField()
    imagens = models.ManyToManyField(Imagem, related_name='imagens_post', blank=True, null=True)

    def hourCounter(self):
        now = timezone.now()
        diff = now - self.created_at
        seconds = diff.total_seconds()

        minutes = seconds / 60
        if minutes < 60:
            return f"{round(minutes)} min"

        hours = seconds / 3600
        if hours < 24:
            return f"{int(hours)} h"

        days = seconds / 86400
        if days < 365:
            return f"{int(days)} d"

        months = days / 30
        if months < 12:
            return f"{int(months)} mo"

        years = days / 365
        return f"{int(years)} yr"

    def likes_count(self):
        return self.likes.count()

    def user_liked(self, user):
        return self.likes.filter(user=user).exists()

    def __str__(self):
        return f"Post de {self.autor.email} - {self.titulo[:50]}"

class Like(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'post')

class Comment(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()

# Modelo de Evento
class Evento(Base):
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

class ChatRoom(Base):
    is_group = models.BooleanField(default=False)
    participants = models.ManyToManyField(User, related_name='chat_rooms')

    def get_room_name(self):
        if not self.is_group and self.participants.count() == 2:
            ids = sorted([str(user.id) for user in self.participants.all()])
            return f"{ids[0]}_{ids[1]}"
        return f"group_{self.id}"

class Message(Base):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
