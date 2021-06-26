from django.db import models

class Provedor(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length = 200)
    apellidos = models.CharField(max_length = 255)
    direccion = models.CharField(max_length = 255)
    telefono = models.CharField(max_length = 12)
    def __str__(self):
        return self.nombre+' '+self.apellidos

class Producto(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length = 200)
    precio = models.DecimalField(max_digits=7, decimal_places=2)
    fecha = models.DateField(auto_now=True)
    provedor = models.ForeignKey(Provedor, on_delete = models.CASCADE)
    def __str__(self):
        return self.nombre+': '+str(self.precio)

class Cliente(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length = 200)
    apellidos = models.CharField(max_length = 255)
    direccion = models.CharField(max_length = 255)
    telefono = models.CharField(max_length = 12)
    def __str__(self):
        return self.nombre+' '+self.apellidos

class Compra(models.Model):
    id = models.AutoField(primary_key = True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    