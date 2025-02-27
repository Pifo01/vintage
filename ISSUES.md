# Problemas encontrados

- **Version de MariaDB no soportada**
- **No se reciben o no se muestra ningun Zapato en la pagina**
- **Los datos en los formulario no se muestran correctamente**

## Version de MariaDB no soportada

Al intentar ejecutar o instalar el modulo que ejecuta la libreria MySQL genera un error que la version de MariaDB no es soportada. Este problema esta directamente relacionado con la version de Django y Python que se esta utilizando. Para solucionar este problema se debe instalar una version especifica de Django y Python que soporte la version de MariaDB que se esta utilizando.

### Solucion
- Instalar una version de python menor o igual a la 3.11, aqui hay un enlace de descarga de [Python 3.11.9](https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe)
- Instalar una version de Django menor o igual a la 3.1, para instalarlo se ejecuta el siguiente comando:
```bash
pip install Django==3.1
```
O tambien se puede instalar todas las librerias usando el archivo `requirements.txt` que se encuentra en la carpeta del proyecto, para instalarlo se ejecuta el siguiente comando:
```bash
pip install -r requirements.txt
```

## No se reciben o no se muestra ningun Zapato en la pagina

Cuando se intentaba hacer una iteracion o buscar todos los zapatos de una variable, por ejemplo `Zapatos`, varias veces pasaba que no se mostraba ningun zapato en la pagina, esto se debe a que la variable `Zapatos` no estaba siendo pasada correctamente a la plantilla HTML.

### Solucion

- En la vista que se debe declarar la variable con su respectivo nombre, su nombre esta relacionado directamente por el nombre colocado el diccionario a su izquierda, aqui un ejemplo:
```python
def zapatos(request):
    zapatos = Zapato.objects.all()
    data = {
        'zapatos': zapatos
    }

    return render(request, 'zapatos.html', data)
```
Se observa como la variable `zapatos` se pasa a la plantilla HTML con el nombre `zapatos`.

> Nota:
> No confundir el nombre de la variable que se pasa a la plantilla HTML con el nombre de la clase del modelo, en este caso `Zapato`.
>
> Para evitar confusiones y malentendidos, se recomienda que el nombre de la variable sea totalmente distinto o que proporcionen informacion adicional.

Aqui hay otra solucion que se puede aplicar en el archivo `views.py`:
```python
def zapatos(request):
    TodosLosZapatos = Zapato.objects.all()
    data = {
        'ListaZapatos': TodosLosZapatos
    }

    return render(request, 'zapatos.html', data)
```
De esta forma, para buscar y mostrar todos los zapatos, se utiliza la variable **ListaZapatos** en la plantilla HTML.

Aqui hay un ejemplo de como se puede mostrar los zapatos en la plantilla HTML en base a la segunda solucion:
```html
{% for zapato in ListaZapatos %}
    <p>{{ zapato.nombre }}</p>
{% endfor %}
```

## Los datos en los formulario no se muestran correctamente

Cuando intentamos mostrar los datos de un formulario usando de base un modelo, algunos modelos que incluyan llave foranea se muestran de la siguiente forma:
```sh
# Forma 1
<QuerySet [<Model: Model object (1)>, <Model: Model object (2)>, <Model: Model object (3)>]>

# Forma 2
<Zapato Object (1)>
<Zapato Object (2)>
```

Aun si no se ha tocado el codigo en la plantilla HTML o en `form.py`, los datos no se muestran correctamente. Este problema se debe a que el modelo no tiene un metodo `__str__` que permita mostrar los datos de una forma mas legible.

### Solucion
- Agregar un metodo `__str__` en el modelo que se quiere mostrar de una forma mas legible, por ejemplo:
```python
class Zapato(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
```