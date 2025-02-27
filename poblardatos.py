# poblardatos.py


from django.utils import timezone
from faker import Faker
import django
import random
import os

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProyectoBD.settings')
django.setup()

from appBD.models import Articulos, Marca, CategoriaCard, VentaArticulo, Ventas, DatosUsuario
from appBD.filtro import TIPO_CHOICES, COLOR_CHOICES, GENERO_CHOICES, TALLAS_CHOICES
from django.contrib.auth.models import User


imagenes = []

# Busca todas las imagenes dentro de "./media/imagenes" y quitales cualquier caracter "[", "]", " ", "-"
for root, dirs, files in os.walk("./media/imagenes"):
    for file in files:
        if file.endswith(".jpg") or file.endswith(".png"):
            nuevonombre = file.replace("[", "").replace("]", "").replace(" ", "").replace("-", "")
            os.rename(os.path.join(root, file), os.path.join(root, nuevonombre))
            imagenes.append(f"/imagenes/{nuevonombre}")

if False: exit()

fake = Faker()

def create_zapato_marca(n=10):
    marcas = []
    for _ in range(n):
        marca = Marca(
            nombre=fake.company(),
            empresa=fake.company_suffix(),
            linea=fake.word()
        )
        marca.save()
        marcas.append(marca)
    return marcas

def create_articulos(marcas, n=50):
    articulos = []
    for _ in range(n):
        articulo = Articulos.objects.create(
            imagen=random.choice(imagenes),
            nombre=fake.word(),
            precio=random.randint(1000, 100000),
            descripcion=fake.text(max_nb_chars=150),
            stock=random.randint(1, 100),
            marca=random.choice(marcas),
            color=random.choice(COLOR_CHOICES)[0],
            genero=random.choice(GENERO_CHOICES)[0],
            talla=random.choice(TALLAS_CHOICES)[0],
            tipo=random.choice(TIPO_CHOICES)[0]
        )
        articulo.save()
        articulos.append(articulo)
    return articulos

def create_categoria_card(marcas, n=10):
    categorias = []
    for _ in range(n):
        categoria = CategoriaCard.objects.create(
            titulo=fake.word(),
            imagen=random.choice(imagenes),
            marca=random.choice(marcas)
        )
        categoria.save()
        categorias.append(categoria)
    return categorias

def create_ventas(articulos, usuarios, n=20):
    ventas = []
    for _ in range(n):
        venta = Ventas(
            fecha=fake.date_time_this_year(),
            total=random.randint(100, 10000)
        )
        venta.save()
        num_articulos = random.randint(1, 5)
        for _ in range(num_articulos):
            VentaArticulo.objects.create(
                venta=venta,
                articulo=random.choice(articulos),
                cantidad=random.randint(1, 10),
                datos=random.choice(usuarios)
            )
        ventas.append(venta)
    return ventas

def create_usuarios(n=10):
    datosusuarios = []
    for _ in range(n):
        usuario = User.objects.create_user(
            username=fake.user_name(),
            password="user",
            email=fake.email()
        )
        usuario.save()
        datousuario = DatosUsuario.objects.create(
            user=usuario,
            nombre=fake.first_name(),
            apellido_Paterno=fake.last_name(),
            apellido_Materno=fake.last_name(),
            correo=usuario.email,
            telefono=fake.phone_number(),
            direccion=fake.address(),
            codigo_postal=fake.zipcode(),
        )
        datousuario.save()
        datosusuarios.append(datousuario)
    return datosusuarios

if __name__ == '__main__':
    usuarios = create_usuarios()
    marcas = create_zapato_marca()
    articulos = create_articulos(marcas)
    categorias = create_categoria_card(marcas)
    ventas = create_ventas(articulos, usuarios)
    print("Datos de prueba poblados correctamente.")