from django.shortcuts import render
from django.db import IntegrityError
from django.shortcuts import redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import SubirDumentoImagenForm
from .models import SubirDumentoImagen



@login_required
def upload(request):
    form = SubirDumentoImagenForm() 
    if request.method == "POST":
        try:
            form = SubirDumentoImagenForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.user_contact_id = request.user.id
                post.save()
                return redirect("/upload/")
            else:
                return render(request, 'index.html', {'form': form, 'error': 'Error de formulario'})
        except:
            return render(request, 'index.html', {'form': form, 'error': 'No se pudo subir a la base de datos'})
    else:
        return render(request, 'index.html', {'form': form})


@login_required
def listarData(request):
    data = SubirDumentoImagen.objects.filter(user_contact_id=request.user.id)
    print(data)
    return render(request=request, template_name="list_img_file.html", context={'data': data})


def user_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']

        findUser = authenticate(request, username=username, password=password)
        print(findUser)

        if username != '' and password != '':
            if findUser is not None:
                try:
                    login(request, findUser)
                    return redirect('/home')
                except IntegrityError:
                    return render(request, 'login.html', {
                        'error': 'No se puede ingresar'
                    })
            else:
                return render(request, 'login.html', {
                    'error': 'Nombre de usuario y contraseña no existe'
                })
        else:
            return render(request, 'login.html', {
                'error': 'Se requieren rellenar los campos'
            })


def user_logout(request):
    logout(request)
    return redirect('/')


def user_register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        findUser = User.objects.filter(username=username).exists()
        print(findUser)

        if findUser != True:
            if username != '' and email != '' and password != '':
                try:
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                    )
                    user.save()
                    login(request, user)
                    return redirect('/home')
                except IntegrityError:
                    return render(request, 'register.html', {
                        'error': 'No se puede ingresar'
                    })
            else:
                return render(request, 'register.html', {
                    'error': 'Se requieren rellenar los campos'
                })
        else:
            return render(request, 'register.html', {
                'error': 'Nombre de usuario existente'
            })
