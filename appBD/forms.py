from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import OperationalError
from django import forms 

from .models import CategoriaCard
from .models import SoporteTicket
from .models import DatosUsuario
from .models import Marca
from .models import Articulos
from .models import DatosUsuario

class LoginForm(forms.Form):
    username = forms.CharField(label='Nombre de usuario', max_length=100)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    remember_me = forms.BooleanField(label='Recuérdame', required=False)

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

def ObtenerMarcas():
    lista_marcas = []
    try:
        marcas = Marca.objects.all()
        for marca in marcas:
            lista_marcas.append((marca.id, marca.nombre))
    except:
        lista_marcas = []
    return lista_marcas

class ArticuloForm(forms.ModelForm):
    class Meta:
        model=Articulos
        fields='__all__'
        widgets = {
            # 'imagen': forms.FileInput(attrs={'accept': 'image/*'}),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super(ArticuloForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['descripcion'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['precio'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['stock'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['marca'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['imagen'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['color'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['genero'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['talla'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['tipo'].widget.attrs.update({
            'class': 'form-control',
        })

class MarcasCardsForm(forms.ModelForm):
    class Meta:
        model=CategoriaCard
        fields='__all__'
    
    def __init__(self, *args, **kwargs):
        super(MarcasCardsForm, self).__init__(*args, **kwargs)
        self.fields['titulo'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['marca'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['imagen'].widget.attrs.update({
            'class': 'form-control',
        })

class MarcaForm(forms.ModelForm):
    class Meta:
        model=Marca
        fields='__all__'

class SoporteTicketForm(forms.ModelForm):
    class Meta:
        model=SoporteTicket
        fields=['nombre', 'correo', 'mensaje']
    
    def __init__(self, *args, **kwargs):
        super(SoporteTicketForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['correo'].widget.attrs.update({
            'class': 'form-control',
            'type': 'email',
            'placeholder': 'correo@example.com'
        })
        self.fields['mensaje'].widget.attrs.update({
            'class': 'form-control',
        })

class DatosCompraForm(forms.ModelForm):
    class Meta:
        model=DatosUsuario
        fields=['nombre', 'apellido_Paterno', 'apellido_Materno', 'direccion', 'correo', 'telefono', 'codigo_postal']
    
    crear_usuario = forms.BooleanField(label='Crear cuenta', required=False, initial=False)
    username = forms.CharField(label='Nombre de usuario', max_length=100, required=False, disabled=True)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput, required=False, disabled=True)

    def __init__(self, *args, **kwargs):
        super(DatosCompraForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['apellido_Paterno'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['apellido_Materno'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['direccion'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['correo'].widget.attrs.update({
            'class': 'form-control',
            'type': 'email',
            'placeholder': 'correo@example.com'
        })
        self.fields['telefono'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['codigo_postal'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['crear_usuario'].widget.attrs.update({
            'class': 'form-check-input',
        })
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
        })


class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model=DatosUsuario
        fields=['nombre', 'apellido_Paterno', 'apellido_Materno', 'direccion', 'correo', 'telefono', 'codigo_postal']

    def __init__(self, *args, **kwargs):
        super(EditarUsuarioForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['apellido_Paterno'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['apellido_Materno'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['direccion'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['correo'].widget.attrs.update({
            'class': 'form-control',
            'type': 'email',
            'placeholder': 'nuevo@correo.com'
        })
        self.fields['telefono'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['codigo_postal'].widget.attrs.update({
            'class': 'form-control',
        })