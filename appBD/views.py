# Variables del proyecto
from .models import Articulos, Marca, CategoriaCard, VentaArticulo, Ventas, SoporteTicket, DatosUsuario
from .filtro import COLOR_CHOICES, TIPO_CHOICES, GENERO_CHOICES, TALLAS_CHOICES, PRECIOS
from .forms import ArticuloForm, MarcaForm, MarcasCardsForm, DatosCompraForm
from .forms import EditarUsuarioForm
from .forms import SoporteTicketForm
from .forms import UserRegisterForm
from .forms import LoginForm

# Librerias
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib import messages
from django.http import FileResponse, HttpResponse
from django.db import transaction
from django.db.models import Q
from django.conf import settings
from collections import Counter
from datetime import datetime, timedelta
import os
import json

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Cuenta creada para {username}. ¡Ahora puedes iniciar sesión!')
            return redirect('login')  # Redirigir al login tras el registro
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})



def SesionIniciada(request) -> bool:
    return request.user.is_authenticated

def VerArticulo(request, id):
    Articulo = Articulos.objects.get(id=id)
    todos = Articulos.objects.all().order_by('?')[:6]
    data={"Articulo": Articulo, 'todos': todos}
    return render(request, 'ver-articulo.html', data)

def IndexPagina(request):
    Articulo = Articulos.objects.all().order_by('?')[:6]
    return render(request, 'index.html', {'Articulos': Articulo})

def Index_Create(request):
    if SesionIniciada(request):
        Articulo=Articulos.objects.all() #Select * from Articulo
        Marcas=Marca.objects.all() #Select * from MarcaS
        cards=CategoriaCard.objects.all() #Select * from Color
        data={'Marcas':Marcas,'Articulo':Articulo, 'cards':cards, 'EsAdmin':True}
        return render(request,'index-create.html',data)

    return redirect('login')

def Index_Create2(request):
    if SesionIniciada(request):
        Articulo=Articulos.objects.all() #Select * from Articulo
        Marcas=Marca.objects.all() #Select * from MarcaS
        cards=CategoriaCard.objects.all() #Select * from Color
        data={'Marcas':Marcas,'Articulo':Articulo, 'cards':cards, 'EsAdmin':True}
        return render(request,'index-create-style.html',data)

    return redirect('login')


def Index_Image(request, image):
    image_path = os.path.join(settings.MEDIA_ROOT, 'imagenes/'+ image)
    try:
        img_file = open(image_path, 'rb')  
        return FileResponse(img_file, content_type='image/jpeg')
    except FileNotFoundError:
        return render("Imagen no encontrada", status=404)

## Cards de articulos ##

def Index_usuario(request):
    Articulo=Articulos.objects.all() #Select * from Articulo
    data={'Articulo':Articulo}
    return render(request,'index.html',data)

def Index_Marcas(request):
    cards=CategoriaCard.objects.all() #Select * from cards
    data={'cards':cards}
    return render(request,'marcas.html',data)

def Index_ArticulosMarcaBuscar(request, id):
    Marca=Marca.objects.get(id=id) #Select * from MarcaS
    Articulo=Articulos.objects.filter(marca=id)  # Use filter instead of get to retrieve multiple objects
    data={'Articulo':Articulo, 'Marca':Marca }
    return render(request,'marcasbuscadas.html',data)

def Create_Articulos(request):
    form=ArticuloForm()
    if request.method=='POST':
        form=ArticuloForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect("/dashboard")
    data={'form':form,'titulo':'Agregar Articulos'}
    return render(request,'create-Articulos.html',data)

def Create_cards(request):
    if request.method=='POST':
        form=MarcasCardsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect("/dashboard")

    form=MarcasCardsForm()
    data={'form':form,'titulo':'Agregar cards'}
    return render(request,'create-Articulos.html',data)


def Update_Articulos(request,id):
    Articulo=Articulos.objects.get(id=id)
    form=ArticuloForm(instance=Articulo)
    if request.method=='POST':
        form=ArticuloForm(request.POST,request.FILES, instance=Articulo)
        if form.is_valid(): #todos los datos se cargaron
            Articulo.imagen=form.cleaned_data['imagen']
            Articulo.nombre=form.cleaned_data['nombre']
            Articulo.precio=form.cleaned_data['precio']
            Articulo.descripcion=form.cleaned_data['descripcion']
            Articulo.color=form.cleaned_data['color']
            Articulo.genero=form.cleaned_data['genero']
            Articulo.marca=form.cleaned_data['marca']
            Articulo.talla=form.cleaned_data['talla']
            Articulo.tipo=form.cleaned_data['tipo']
            Articulo.save()
        return redirect("/dashboard")
    data={'form':form,'titulo':'Actualizar Articulos'}
    return render(request,'create-Articulos.html',data)


def Update_cards(request,id):
    cards=CategoriaCard.objects.get(id=id)
    form=MarcasCardsForm(instance=cards)
    if request.method=='POST':
        form=MarcasCardsForm(request.POST,request.FILES, instance=cards)
        if form.is_valid(): #todos los datos se cargaron
            cards.titulo=form.cleaned_data['titulo']
            cards.imagen=form.cleaned_data['imagen']
            MarcaNueva=form.cleaned_data['marca']
            cards.marca=MarcaNueva
            cards.save()
        return redirect("/dashboard")
    data={'form':form,'titulo':'Actualizar card','prev':'/dashboard/categoria/'}
    return render(request,'create-Articulos.html',data)


def Update_Marca(request,id):
    marca=Marca.objects.get(id=id)
    form=MarcaForm(instance=Marca)
    if request.method=='POST':
        form=MarcaForm(request.POST,request.FILES, instance=marca)
        if form.is_valid():
            marca.nombre=form.cleaned_data['nombre']
            marca.empresa=form.cleaned_data['empresa']
            marca.linea=form.cleaned_data['linea']
            marca.save()
        return redirect("/index-create")
    data={'form':form,'titulo':'Actualizar Marca de Zapatos'}
    return render(request,'create-catalogo.html',data)

def Update_Usuario(request, id):
    datos_usuario=DatosUsuario.objects.get(id=id)
    form=EditarUsuarioForm(instance=datos_usuario)
    if request.method=='POST':
        form=EditarUsuarioForm(request.POST, request.FILES, instance=datos_usuario)
        if form.is_valid():
            form.save()
        return redirect("/dashboard/usuarios/")
    data={'form':form,'titulo':'Actualizar Usuario','prev':'/dashboard/usuarios/'}
    return render(request,'create-Articulos.html',data)



def Create_Marca(request):
    form=MarcaForm()
    if request.method=='POST':
        form=MarcaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect("/dashboard/marcas")
    data={'form':form,'titulo':'Agregar Marca de Zapatos'}
    return render(request,'create-Articulos.html',data)

def View_Articulos(request,id):
    Articulo=Articulos.objects.get(id=id)
    data={"Articulo": Articulo}
    return render(request,'ver-Articulo.html',data)

def View_Usuario(request,id):
    datos_usuario=DatosUsuario.objects.get(id=id)
    data={"datos_usuario": datos_usuario}
    return render(request,'perfil.html',data)

def View_Ticket(request,id):
    Ticket=SoporteTicket.objects.get(id=id)
    data={"Ticket": Ticket}
    return render(request,'ver-ticket.html',data)

def View_cards(request,id):
    card=CategoriaCard.objects.get(id=id)
    data={"card": card}
    return render(request,'ver-card.html',data)

def View_Marca(request,id):
    Marca=Marca.objects.get(id=id)
    data={"Marca": Marca}
    return render(request,'ver-Marca.html',data)


def Delete_Usuario(request,id):
    datos_usuario=DatosUsuario.objects.get(id=id)
    datos_usuario.delete()
    return redirect("/dashboard/usuarios/")


def Delete_Articulos(request,id):
    Articulo=Articulos.objects.get(id=id)
    Articulo.delete()
    return redirect("/dashboard/articulos")

def Delete_cards(request,id):
    cards=CategoriaCard.objects.get(id=id)
    cards.delete()
    return redirect("/dashboard/categoria")


def Delete_Marca(request,id):
    marca=Marca.objects.get(id=id)
    marca.delete()
    return redirect("/dashboard")

def Index_catalogo(request):
    Articulo=Articulos.objects.filter(stock__gt=0) #Select * from Articulo where stock>0
    marca=Marca.objects.all() #Select * from Marca

    if request.GET.get('precio'):
        # Vaciar Articulos para luego añadir los filtrados
        Articulo = Articulos.objects.none()
        GetPrecios = request.GET.get('precio').split(',')
        # Filtrar por precio y precio - 10000
        for precio in GetPrecios:
            PrecioNumero = int(precio)
            # Añadir articulos con el precio y el precio - 10000
            Articulo = Articulo | Articulos.objects.filter(precio__range=[PrecioNumero-10000, PrecioNumero])
    
    if request.GET.get('color'):
        Colores = request.GET.get('color').split(',')
        Articulo = Articulo.filter(color__in=Colores)

    if request.GET.get('genero'):
        Generos = request.GET.get('genero').split(',')
        Articulo = Articulo.filter(genero__in=Generos)
    
    if request.GET.get('marca'):
        Marcas = request.GET.get('marca').split(',')
        Articulo = Articulo.filter(marca__in=Marcas)
    
    if request.GET.get('talla'):
        Tallas = request.GET.get('talla').split(',')
        Articulo = Articulo.filter(talla__in=Tallas)
    
    if request.GET.get('tipo'):
        Tipos = request.GET.get('tipo').split(',')
        Articulo = Articulo.filter(tipo__in=Tipos)
    
    Articulo = Articulo[:24]

    data={'Articulo':Articulo,'Marca':marca, 'Precios':PRECIOS, 'Colores':COLOR_CHOICES, 'Tipo':TIPO_CHOICES, 'Genero':GENERO_CHOICES, 'Talla':TALLAS_CHOICES}
    return render(request,'catalogo.html',data)


def Login(request):
    data = {}
    form = LoginForm()

    if SesionIniciada(request):
        return redirect("/index")

    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                response = redirect("/dashboard")
                return response
            else:
                data['error'] = "Usuario o contraseña incorrectos"
    
    data['form'] = form
    return render(request,'login.html',data)



def shoe_list(request):
    # Manejo de los filtros
    precios = request.GET.getlist('precio')
    colores = request.GET.getlist('color')
    generos = request.GET.getlist('genero')
    marcas = request.GET.getlist('marca')
    tallas = request.GET.getlist('talla')
    tipos = request.GET.getlist('tipo')

    shoes = Articulos.objects.all()

    if precios:
        shoes = shoes.filter(precio__in=precios)
    if colores:
        shoes = shoes.filter(color__in=colores)
    if generos:
        shoes = shoes.filter(genero__in=generos)
    if marcas:
        shoes = shoes.filter(marca__in=marcas)
    if tallas:
        shoes = shoes.filter(talla__in=tallas)
    if tipos:
        shoes = shoes.filter(tipo__in=tipos)

    # Obtener los choices para colores, géneros, y tallas
    color_choices = COLOR_CHOICES
    genero_choices = GENERO_CHOICES
    talla_choices = TALLAS_CHOICES  
    tipo_choices = TIPO_CHOICES  

    return render(request, 'catalogo.html', {
        'shoes': shoes,
        'Precios': precios,  # Asegúrate de que este sea tu diccionario de precios
        'Colores': color_choices,
        'Genero': genero_choices,
        'Marca': marcas.objects.all(),
        'Talla': talla_choices,
        'Tipo': tipo_choices,

    })

def view_carrito(request):
    if request.method == 'POST':
        form_datos_compra = DatosCompraForm(request.POST)
        if form_datos_compra.is_valid():
            # Crear una nueva cuenta de usuario
            user = None
            if form_datos_compra.cleaned_data['crear_usuario']:
                user = User.objects.create_user(
                    username=form_datos_compra.cleaned_data['username'],
                    password=form_datos_compra.cleaned_data['password']
                )
                user.save()

                # Autenticar al usuario
                user = authenticate(username=form_datos_compra.cleaned_data['username'], password=form_datos_compra.cleaned_data['password'])

            # Crear un nuevo valor en el modelo DatosUsuario
            datos_usuario = DatosUsuario.objects.create(
                user=user,
                nombre=form_datos_compra.cleaned_data['nombre'],
                apellido_Paterno=form_datos_compra.cleaned_data['apellido_Paterno'],
                apellido_Materno=form_datos_compra.cleaned_data['apellido_Materno'],
                correo=form_datos_compra.cleaned_data['correo'],
                direccion=form_datos_compra.cleaned_data['direccion'],
                telefono=form_datos_compra.cleaned_data['telefono'],
                codigo_postal=form_datos_compra.cleaned_data['codigo_postal']
            )
            datos_usuario.save()

            return redirect('/carrito/pagar')
            

    carrito = request.session.get('carrito', {})
    Articulo = Articulos.objects.filter(id__in=carrito)
    total = sum(art.precio for art in Articulo)

    form_datos_compra = DatosCompraForm()
    mostrar_modal = not request.user.is_authenticated

    context = {
        'Articulo': Articulo,
        'total': total,
        'Carrito': carrito,
        'form_datos_compra' : form_datos_compra,
        'mostrar_modal': mostrar_modal
    }
    
    return render(request, 'carrito.html', context)

def agregar_al_carrito(request, id):
    Articulo = get_object_or_404(Articulos, id=id)
    if Articulo.stock <= 0:
        return render(request, 'catalogo.html', {'Mensaje': f"El artículo {Articulo.nombre} está agotado.", 'Redireccionar':'/catalogo'})

    id=str(id)
    carrito = request.session.get('carrito', {})

    if id in carrito:
        carrito[id] += 1
    else:
        carrito[id] = 1

    request.session['carrito'] = carrito

    return redirect('/carrito')

def limpiar_carrito(request):
    request.session['carrito'] = {}
    return redirect('/carrito')


def quitar_del_carrito(request, id):
    id=str(id)
    carrito = request.session.get('carrito', {})

    carrito.pop(id)
    request.session['carrito'] = carrito

    return redirect('/carrito')

def sumar_al_carrito(request, id):
    Articulo = get_object_or_404(Articulos, id=id)
    id=str(id)
    carrito = request.session.get('carrito', {})

    # Verificar que no sobrepase el stock
    if carrito.get(id, 0) > Articulo.stock:
        return HttpResponse(status=400)

    carrito.update({id: carrito[id] + 1})
    request.session['carrito'] = carrito
    
    # Devolver 200 OK
    return HttpResponse(status=200)

def restar_del_carrito(request, id):
    id=str(id)
    carrito = request.session.get('carrito', {})

    carrito.update({id: carrito[id] - 1})
    if carrito[id] <= 0:
        carrito.pop(id)
    request.session['carrito'] = carrito
    
    # Devolver 200 OK
    return HttpResponse(status=200)

def cambiar_cantidad_carrito(request, id):
    Articulo = get_object_or_404(Articulos, id=id)
    id=str(id)
    parametros_json = request.body.decode('utf-8')
    parametros = json.loads(parametros_json)
    cantidad = parametros["cantidad"]

    if cantidad > Articulo.stock:
        return HttpResponse(status=400)

    carrito = request.session.get('carrito', {})

    carrito.update({id: cantidad})
    request.session['carrito'] = carrito

    return redirect('/carrito')

def pagar_carrito(request):
    carrito = request.session.get('carrito', {})
    carrito_ids = list(carrito.keys())
    total = 0

    factura=[]
    for id in carrito_ids:
        # descontar stock
        SubArticulo = Articulos.objects.get(id=id)
        SubArticulo.stock -= carrito.get(id)
        SubArticulo.save()

        total += SubArticulo.precio * carrito.get(id)
    
        factura.append((SubArticulo, carrito.get(id)))
    
    # Obtener DatosUsuario si el usuario está autenticado
    datos_usuario = None
    if request.user.is_authenticated:
        datos_usuario = DatosUsuario.objects.get(user=request.user)

    # Inicio Procesar pago

    with transaction.atomic():
        Ventafinal = Ventas.objects.create(total=0)

        for articulo_id, cantidad in carrito.items():
            SubArticulo = Articulos.objects.get(id=articulo_id)
            VentaArticulo.objects.create(venta=Ventafinal, articulo=SubArticulo, cantidad=cantidad, datos=datos_usuario)
            
        Ventafinal.total = total
        Ventafinal.save()

    # Fin Procesar pago

    carrito.clear()
    request.session['carrito'] = carrito

    return render(request, 'Carrito.html', {'Mensaje': f"Compra realizada con éxito. Total: ${total}"})

def Dashboard(request):
    return render(request, 'index-admin-dashboard.html')

def DashboardVentas(request):
    total_productos = Articulos.objects.count()
    total_marcas = Marca.objects.count()
    total_categorias = CategoriaCard.objects.count()
    
    # Obtener la cantidad total de stock disponible
    total_stock = sum(articulo.stock for articulo in Articulos.objects.all())

    # Contar artículos por marca
    articulos_por_marca = Counter(articulo.marca for articulo in Articulos.objects.all())
    marcas = [marca.nombre for marca in Marca.objects.all()]
    cantidades = [articulos_por_marca[marca] for marca in marcas]
    
    # Obtener la lista de artículos
    articulos = Articulos.objects.all()
    # Obtener las ventas de los ultimos 7 dias
    hoy = datetime.now()
    hace_7_dias = hoy - timedelta(days=7)
    ventas = Ventas.objects.filter(fecha__range=[hace_7_dias, hoy]).order_by('-id')

    context = {
        'total_productos': total_productos,
        'total_marcas': total_marcas,
        'total_categorias': total_categorias,
        'total_stock': total_stock,
        'marcas': marcas,
        'cantidades': cantidades,
        'articulos': articulos,  # Agregado
        'ventas': ventas,
    }
    
    return render(request, 'index-admin-ventas.html', context)

def DashboardTickets(request):
    tickets = SoporteTicket.objects.all()
    return render(request, 'index-admin-soporte.html', {'tickets': tickets})

def DashboardCrud(request):
    articulos = Articulos.objects.all()
    marcas = Marca.objects.all()
    cards = CategoriaCard.objects.all()
    return render(request, 'index-admin-crud.html', {'articulos': articulos, 'marcas': marcas, 'cards': cards})

def DashboardArticulos(request):
    pagina = 1
    if request.GET.get('pagina', 1):
        pagina = int( request.GET.get('pagina', 1) )

    articulos_por_pagina = 15
    inicio = (pagina - 1) * articulos_por_pagina
    fin = inicio + articulos_por_pagina
    articulos = Articulos.objects.all()[inicio:fin]

    cantidad_articulos = Articulos.objects.count()
    cantidad_paginas = cantidad_articulos // articulos_por_pagina
    cantidad_paginas = (cantidad_articulos + articulos_por_pagina - 1) // articulos_por_pagina
    paginas = list(range(1, cantidad_paginas + 1))

    return render(request, 'index-admin-articulos.html', {'Articulos': articulos, 'Pagina': pagina, 'CantidadPaginas': paginas})

def DashboardMarcas(request):
    pagina = 1
    if request.GET.get('pagina', 1):
        pagina = int( request.GET.get('pagina', 1) )

    marca_por_pagina = 15
    inicio = (pagina - 1) * marca_por_pagina
    fin = inicio + marca_por_pagina
    marca = Marca.objects.all()[inicio:fin]

    # Tambien enviar la cantidad de paginas
    cantidad_marcas = Marca.objects.count()
    cantidad_paginas = cantidad_marcas // marca_por_pagina

    return render(request, 'index-admin-marcas.html', {'Marca': marca, 'Pagina': pagina, 'CantidadPaginas': cantidad_paginas})

def DashboardCards(request):
    pagina = 1
    if request.GET.get('pagina', 1):
        pagina = int( request.GET.get('pagina', 1) )

    card_por_pagina = 15
    inicio = (pagina - 1) * card_por_pagina
    fin = inicio + card_por_pagina
    Card = CategoriaCard.objects.all()[inicio:fin]

    # Tambien enviar la cantidad de paginas
    cantidad_card = CategoriaCard.objects.count()
    cantidad_paginas = cantidad_card // card_por_pagina

    return render(request, 'index-admin-categorias.html', {'cards': Card, 'Pagina': pagina, 'CantidadPaginas': cantidad_paginas})

def DashboardUsuario(request):
    pagina = 1
    if request.GET.get('pagina', 1):
        pagina = int( request.GET.get('pagina', 1) )

    usuario_por_pagina = 15
    inicio = (pagina - 1) * usuario_por_pagina
    fin = inicio + usuario_por_pagina
    Usuario = DatosUsuario.objects.all()[inicio:fin]

    # Tambien enviar la cantidad de paginas
    cantidad_usuario = DatosUsuario.objects.count()
    cantidad_paginas = cantidad_usuario // usuario_por_pagina

    return render(request, 'index-admin-usuarios.html', {'datos_usuario': Usuario, 'Pagina': pagina, 'CantidadPaginas': cantidad_paginas})

def buscar(request):
    query = request.GET.get('q')

    if query:
        # Filtrar en ambos modelos usando Q objects
        resultados_articulos = Articulos.objects.filter(
            Q(nombre__icontains=query) | Q(marca__nombre__icontains=query)
        )
        resultados_marcas = Marca.objects.filter(
            Q(nombre__icontains=query) | Q(linea__icontains=query)
        )
    
        return render(request, 'resultados_busqueda.html', {
            'query': query,
            'resultados_articulos': resultados_articulos,
            'resultados_marcas': resultados_marcas
        })
    
    return render(request, 'resultados_busqueda.html', {
        'query': query,
        'resultados_articulos': None,
        'resultados_marcas': None
    })

def CrearTicketSoporte(request):
    if request.method == 'POST':
        form = SoporteTicketForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Ticket creado con éxito.')
            return redirect('/soporte')
    else:
        form = SoporteTicketForm()
    return render(request, 'soporte-ticket.html', {'form': form})

def MarcarComoResueltoView(request, id):
    ticket = get_object_or_404(SoporteTicket, id=id)
    ticket.resuelto = True
    ticket.save()
    return redirect('/dashboard/soporte/')


def Index_perfil(request):
    # Obtener la sesion
    session = get_object_or_404(Session, session_key=request.COOKIES.get("sessionid"))
    session_data = session.get_decoded()
    uid = session_data.get('_auth_user_id')

    # Obtener el usuario
    user = get_object_or_404(User, id=uid)
    
    # Obtener datosusuario usando el usuario
    datos_usuario = get_object_or_404(DatosUsuario, user_id=user.id)

    """
    if request.method == 'POST':
        form = DatosCompraForm(request.POST, instance=datos_usuario)
        if form.is_valid():
            form.save()
            return redirect('perfil_usuario')
    else:
        form = DatosCompraForm(instance=datos_usuario)
    """

    context = {
        # 'form': form,
        'datos_usuario': datos_usuario,
    }
    return render(request, 'perfil.html', context)