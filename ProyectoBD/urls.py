"""
URL configuration for ProyectoBD project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from appBD import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.IndexPagina),
    path('buscar/', views.buscar),
    path('index-usuario',views.IndexPagina),
    path('admin/', admin.site.urls),
    path('create-Articulos/',views.Create_Articulos),
    path('view-Articulos/<int:id>',views.VerArticulo),
    path('delete-Articulos/<int:id>',views.Delete_Articulos),
    path('update-Articulos/<int:id>',views.Update_Articulos),

    path('view-usuario/<int:id>',views.View_Usuario),
    path('delete-usuario/<int:id>',views.Delete_Usuario),

    path('delete-marcazapato/<int:id>',views.Delete_Marca),
    path('update-marcazapato/<int:id>',views.Update_Marca),

    path('articulo/<int:id>',views.VerArticulo),
    path('marcas/',views.Index_Marcas),
    path('marcas/<int:id>',views.Index_ArticulosMarcaBuscar),
    path('create-cards/',views.Create_cards),
    path('delete-cards/<int:id>',views.Delete_cards), 
    path('update-cards/<int:id>',views.Update_cards),

    path('media/imagenes/<str:image>',views.Index_Image),
    path('media/cards/<str:image>',views.Index_Image), 
    path('index-create2/',views.Index_Create),
    path('view-ticket/<int:id>',views.View_Ticket),
    path('true-ticket/<int:id>', views.MarcarComoResueltoView), 
    path('index-create/',views.Index_Create2),
    path('catalogo/',views.Index_catalogo),
    path('catalogobuscar/', views.shoe_list),

    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), 
    path('profile/', views.Index_perfil),
    path('carrito/', views.view_carrito),
    path('agregar-al-carrito/<int:id>', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('quitar-del-carrito/<int:id>', views.quitar_del_carrito, name='quitar_del_carrito'),
    path('carrito/sumar/<int:id>', views.sumar_al_carrito, name='sumar_cantidad'),
    path('carrito/restar/<int:id>', views.restar_del_carrito, name='restar_cantidad'),
    path('carrito/cambiar/<int:id>', views.cambiar_cantidad_carrito, name='cambiar_cantidad'),
    path('carrito/limpiar/', views.limpiar_carrito, name='limpiar_carrito'),
    path('carrito/pagar/', views.pagar_carrito, name='pagar'),
    path('soporte/', views.CrearTicketSoporte, name='soporte'),
    
    path('dashboard/', views.Dashboard),
    path('dashboard/ventas/', views.DashboardVentas),
    path('dashboard/soporte/', views.DashboardTickets), 
    path('dashboard/articulos/',views.DashboardArticulos),

    path('dashboard/marcas/',views.DashboardMarcas),
    path('dashboard/marcas/crear/',views.Create_Marca),
    path('dashboard/marcas/ver/<int:id>',views.View_Marca),
    path('dashboard/marcas/actualizar/<int:id>',views.Update_Marca),
    path('dashboard/marcas/borrar/<int:id>',views.Delete_Marca),

    path('dashboard/categoria/',views.DashboardCards),
    path('dashboard/categoria/crear/',views.Create_cards),
    path('dashboard/categoria/ver/<int:id>',views.View_cards),
    path('dashboard/categoria/actualizar/<int:id>',views.Update_cards),
    path('dashboard/categoria/borrar/<int:id>',views.Delete_cards),

    path('dashboard/usuarios/',views.DashboardUsuario),
    path('dashboard/usuarios/ver/<int:id>',views.View_Usuario),
    path('dashboard/usuarios/actualizar/<int:id>',views.Update_Usuario),
    path('dashboard/usuarios/borrar/<int:id>',views.Delete_Usuario),
]
