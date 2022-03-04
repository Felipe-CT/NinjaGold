from django.shortcuts import render, redirect
import random


def home(request):
    if request.method == "GET":
        request.session['movimientos'] = request.POST.get('movimientos', 10)
        request.session['goldstatus'] = 0
        request.session['contador'] = 0
        request.session['estado'] = False
        request.session['activities'] = []
        return render(request, 'app/home.html')

    if request.method == "POST":
            request.session['movimientos'] = request.POST.get('movimientos', 10)
            request.session['goldstatus'] = 0
            request.session['contador'] = 0
            request.session['estado'] = False
            request.session['activities'] = []
            return render(request, '/NinjaGold/procesar')

def procesar(request, valor=''):
    if request.method == "GET":
        return render(request, 'app/index.html')

    print(f"desde procesar:{request.get_full_path()}")
    building = valor
    if valor == '':
        building = request.POST['building']
    diccionario = [{'name': 'granja', 'min': 10, 'max': 20}, {'name': 'cueva', 'min': 5, 'max': 10}, {
        'name': 'casa', 'min': 2, 'max': 5}, {'name': 'casino', 'min': -50, 'max': 50}]
    for i in range(4):
        numero = 0
        if diccionario[i]["name"] == building:
            numero = int(
                round(random.random()*(((diccionario[i]["max"])-(diccionario[i]["min"])))+(diccionario[i]["min"])))
            print(
                f" se obtiene {numero} desde {building}")
            request.session['goldstatus'] += numero
            request.session['contador'] += 1
            if (building == 'granja') or (building == 'cueva') or (building == 'casa'):
                form = building
                mensaje = f'<h5> Has ganado {numero} de oro!</h5>'
                request.session['activities'].append(mensaje)
            else:
                if((building == 'casino') and numero == 50):
                    form = building
                    mensaje = f'<h5>Cuanta suerte! te llevas el premio mayor (50).</h5>'
                    request.session['activities'].append(mensaje)
                elif((building == 'casino') and numero > 0):
                    form = building
                    mensaje = f'<h5>Has ganado {numero} de oro!</h5>'
                    request.session['activities'].append(mensaje)
                elif((building == 'casino') and numero == 0):
                    form = building
                    mensaje = f'<h5>¿solo entraste a mirar?</h5>'
                    request.session['activities'].append(mensaje)
                    request.session['contador'] -= 1
                elif((building == 'casino') and numero > -49):
                    form = building
                    mensaje = f'<h5>No siempre se gana, mejor suerte a la proxima.</h5>'
                    request.session['activities'].append(mensaje)
                elif((building == 'casino') and numero == -50):
                    form = building
                    mensaje = f'<h5>El casino agradece tus 50 de oro, has ganado un turno adicional.</h5>'
                    request.session['activities'].append(mensaje)
                    request.session['contador'] -= 2
    return redirect('/NinjaGold/process_money')


def process_money(request):
    context = {
        'goldstatus': request.session['goldstatus'],
        'estado': request.session['estado'],
        'contador': request.session['contador'],
        'actividad': request.session['activities'],
        'movimientostotal': int(request.session['movimientos']) - request.session['contador'],
    }
    return render(request, 'app/index.html', context)
