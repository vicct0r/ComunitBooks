from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from stdimage import StdImageField


class UsuarioManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('O Email é obrigatório!')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('O usuário precisa ativar "is_superuser"!')
        
        if extra_fields.get('is_staff', True) is not True:
            raise ValueError('O usuário precisa ativar "is_staff"!')
        
        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField('Email', unique=True, max_length=100)
    is_verified = models.BooleanField(default=False)
    telefone = models.CharField('Telefone', max_length=12)
    is_staff = models.BooleanField('Membro da Equipe', default=False)
    img = StdImageField(
                        'Imagem', 
                        upload_to='profiles', 
                        variations={'thumb':{'width':360, 'height':360, 'crop':True}},
                        blank=True,
                        null=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'telefone']
    objects = UsuarioManager()

    def __str__(self):
        return self.email