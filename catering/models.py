from django.db import models


class Plato(models.Model):
    CATEGORIAS = [
        ('entrada', 'Entrada'),
        ('principal', 'Principal'),
        ('postre', 'Postre'),
        ('bebida', 'Bebida'),
    ]

    nombre      = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    precio      = models.DecimalField(max_digits=8, decimal_places=2)
    categoria   = models.CharField(max_length=20, choices=CATEGORIAS)
    disponible  = models.BooleanField(default=True)
    imagen_url  = models.URLField(blank=True)
    creado_en   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"


class Reserva(models.Model):
    nombre_cliente    = models.CharField(max_length=255)
    email             = models.EmailField()
    telefono          = models.CharField(max_length=20)
    fecha_evento      = models.DateField()
    cantidad_personas = models.IntegerField()
    mensaje           = models.TextField(blank=True)
    creado_en         = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_cliente} - {self.fecha_evento}"