from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Crea y guarda un usuario con correo electrónico y contraseña.
        """
        if not email:
            raise ValueError('El correo debe ser proporcionado')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Crea un superusuario con el correo electrónico y contraseña dados.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuario debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    is_active = models.BooleanField(default=True)  # Siempre activo por defecto
    is_staff = models.BooleanField(default=False)  # No es staff por defecto
    is_superuser = models.BooleanField(default=False)  # No es superusuario por defecto

    # Clave foránea a Role
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    def __str__(self):
        return self.email

from django.db import models

class Categoria(models.Model):
    # Definimos los campos de la categoría
    codigo = models.CharField(max_length=100, unique=True)  # Código de la categoría
    nombre = models.CharField(max_length=100)  # Nombre de la categoría
    estado = models.CharField(max_length=20, choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')])  # Estado de la categoría

    def __str__(self):
        return self.nombre  # Representación legible de la categoría en el admin y otros lugares

    class Meta:
        db_table = 'categoria'  # Nombre de la tabla en la base de datos, si no se especifica Django usa el nombre del modelo en minúsculas




class Producto(models.Model):
    codigo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    estado = models.CharField(max_length=10, choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')])

    # Relación con la categoría (mantienes la clave foránea)
    nombre_categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        db_table = 'productos'

    def __str__(self):
        return self.nombre