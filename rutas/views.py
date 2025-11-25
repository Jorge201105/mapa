import json
from django.shortcuts import render, redirect
from django.conf import settings
from .models import PuntoEntrega
import requests
import random # Para simular el algoritmo de optimización inicialmente

def mapa_view(request):
    puntos_entrega = PuntoEntrega.objects.all().order_by('orden_optimo') # Ordena si ya hay un orden
    puntos_json = json.dumps([{
        'nombre': p.nombre,
        'direccion': p.direccion,
        'latitud': float(p.latitud),
        'longitud': float(p.longitud)
    } for p in puntos_entrega])

    return render(request, 'rutas/mapa.html', {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        'puntos_entrega_json': puntos_json
    })

def agregar_punto(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        direccion = request.POST['direccion']
        # Aquí deberías usar la API de geocodificación de Google para obtener latitud y longitud
        # Por ahora, usaremos valores de ejemplo o podrías pedirlos directamente en el formulario
        latitud = request.POST.get('latitud')
        longitud = request.POST.get('longitud')

        # Ejemplo muy básico de geocodificación si no se proporcionan lat/lng
        if not latitud or not longitud:
            try:
                geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={direccion}&key={settings.GOOGLE_MAPS_API_KEY}"
                response = requests.get(geocode_url)
                data = response.json()
                if data['status'] == 'OK':
                    location = data['results'][0]['geometry']['location']
                    latitud = location['lat']
                    longitud = location['lng']
                else:
                    # Manejar error de geocodificación
                    print(f"Error de geocodificación: {data['status']}")
                    return render(request, 'rutas/mapa.html', {'error': 'No se pudo geocodificar la dirección.'})
            except Exception as e:
                print(f"Error al llamar a la API de geocodificación: {e}")
                return render(request, 'rutas/mapa.html', {'error': 'Error de conexión con la API de geocodificación.'})


        PuntoEntrega.objects.create(nombre=nombre, direccion=direccion, latitud=latitud, longitud=longitud)
        return redirect('mapa')
    return redirect('mapa') # Si se accede directamente a /agregar_punto sin POST, redirige al mapa

def optimizar_ruta(request):
    if request.method == 'POST':
        puntos = list(PuntoEntrega.objects.all())
        punto_inicio = {'latitud': float(request.POST['lat_inicio']), 'longitud': float(request.POST['lng_inicio'])}

        # -------------------------------------------------------------------------------------------------------
        # AQUÍ ES DONDE INTEGRARÁS TU ALGORITMO DE OPTIMIZACIÓN CON IA
        # Para empezar, vamos a simular una optimización aleatoria para tener una base.
        # Más adelante, integrarás un algoritmo como Recocido Simulado, Algoritmos Genéticos o un TSP Solver.
        #
        # Necesitarás:
        # 1. Obtener las matrices de distancia/tiempo entre todos los puntos (inicio, reparto, inicio).
        #    Esto se hace con la Google Maps Distance Matrix API.
        # 2. Implementar tu algoritmo de optimización (IA).
        #    El objetivo es minimizar la distancia total.
        # 3. Guardar el nuevo orden en los objetos PuntoEntrega.
        # -------------------------------------------------------------------------------------------------------

        # Simulación de optimización (reemplaza esto con tu IA)
        random.shuffle(puntos) # ¡Esto es solo un placeholder!
        for i, punto in enumerate(puntos):
            punto.orden_optimo = i + 1
            punto.save()

        # Calcular el consumo de bencina
        # Necesitas la secuencia de puntos optimizada y la Distance Matrix API.
        # Por ahora, solo mostraremos un mensaje.
        # Desafío: Implementar el cálculo de distancia total y consumo aquí.

        return redirect('mapa')
    return redirect('mapa')