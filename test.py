import urllib.request
import urllib.error
import concurrent.futures
import time

URL = "http://127.0.0.1:8000/health"
TOTAL_REQUESTS = 120

def make_request(req_id):
    try:
        req = urllib.request.Request(URL, headers={'User-Agent': 'Bot-Tester/1.0'})
        with urllib.request.urlopen(req) as response:
            return req_id, response.getcode()
    except urllib.error.HTTPError as e:
        return req_id, e.code
    except Exception as e:
        return req_id, "Error"

def main():
    print("=====================================================")
    print(" Iniciando prueba de resiliencia (Anti-Bot Testing) ")
    print("=====================================================")
    print(f"Enviando {TOTAL_REQUESTS} peticiones recurrentes a {URL}...")
    
    start_time = time.time()
    results = []
    
    # Lanzar múltiples peticiones de manera concurrente para simular el comportamiento de un bot
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(make_request, i): i for i in range(TOTAL_REQUESTS)}
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
            
    end_time = time.time()
    
    # Agrupar las respuestas obtenidas
    status_counts = {}
    for req_id, status in results:
        status_counts[status] = status_counts.get(status, 0) + 1
        
    print(f"\nTiempo total de la prueba: {end_time - start_time:.2f} segundos\n")
    print("=== RESUMEN DE CÓDIGOS DE RESPUESTA ===")
    
    for status, count in sorted(status_counts.items(), key=lambda x: str(x[0])):
        if status == 429:
            print(f" -> HTTP {status} (Too Many Requests): {count} - ¡PROTECCIÓN ANTI-BOT ACTIVADA CORRECTAMENTE! 🛡️")
        elif status == 200:
            print(f" -> HTTP {status} (OK): {count} peticiones exitosamente procesadas antes del límite.")
        else:
            print(f" -> HTTP {status}: {count} peticiones.")

if __name__ == "__main__":
    main()
