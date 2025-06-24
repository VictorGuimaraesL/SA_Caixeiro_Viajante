import numpy as np
import random
import math


def calcular_distancia_total(rota, distancias): #Função que calcula a distância total de uma rota
    total = 0
    n = len(rota)
    for i in range(n):
        total += distancias[rota[i], rota[(i + 1) % n]] 
    return total

def simulated_annealing_tsp(distancias, initial_temp=50000, cooling_rate=0.9995, max_iter=100000): #Função que aplica o Simulated Annealing
    n_cidades = len(distancias)
    rota_atual = list(range(n_cidades))
    random.shuffle(rota_atual)
    distancia_atual = calcular_distancia_total(rota_atual, distancias)
    
    melhor_rota = rota_atual.copy()
    melhor_distancia = distancia_atual
    
    temperatura = initial_temp
    
    for i in range(max_iter): #Gera uma rota ao trocar duas cidades aleatórias da rota atual
        nova_rota = rota_atual.copy()
        a, b = random.sample(range(n_cidades), 2)
        nova_rota[a], nova_rota[b] = nova_rota[b], nova_rota[a]
        nova_distancia = calcular_distancia_total(nova_rota, distancias)
        
        delta_distancia = nova_distancia - distancia_atual
        
        if delta_distancia < 0 or random.random() < math.exp(-delta_distancia / temperatura): #Critério de aceitação
            rota_atual = nova_rota
            distancia_atual = nova_distancia
            
            if distancia_atual < melhor_distancia: #Atualização da melhor rota
                melhor_rota = rota_atual.copy()
                melhor_distancia = distancia_atual
        
        temperatura *= cooling_rate #Resfriamento da temperatura
        
        if i % 10000 == 0:
            print(f"Iteração {i}: Temp = {temperatura:.6f}, Melhor Distância = {melhor_distancia}")
    
    return melhor_rota, melhor_distancia

distancias = np.array([
 [ 0, 52, 59, 53, 20, 25, 50, 33, 76, 59],
 [52,  0, 49, 68, 59, 29, 30, 50, 61, 57],
 [59, 49,  0, 24, 50, 69, 38, 57, 74, 49],
 [53, 68, 24,  0, 47, 67, 52, 48, 72, 36],
 [20, 59, 50, 47,  0, 35, 62, 34, 82, 61],
 [25, 29, 69, 67, 35,  0, 43, 26, 70, 54],
 [50, 30, 38, 52, 62, 43,  0, 57, 39, 53],
 [33, 50, 57, 48, 34, 26, 57,  0, 64, 37],
 [76, 61, 74, 72, 82, 70, 39, 64,  0, 77],
 [59, 57, 49, 36, 61, 54, 53, 37, 77,  0]
])

melhor_rota_global = None
melhor_distancia_global = float('inf')
for _ in range(10):
    print(f'\nTentativa número {_+1}')
    rota, distancia = simulated_annealing_tsp(distancias)
    if distancia < melhor_distancia_global:
        melhor_rota_global, melhor_distancia_global = rota, distancia
print(f"\nMelhor rota encontrada: {melhor_rota_global}")
print(f"Distância total: {melhor_distancia_global} km")
