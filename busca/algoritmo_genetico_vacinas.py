#!/usr/bin/env python
# coding: utf-8

# In[2]:


import random
import datetime
#from matplotlib import pyplot as plt
from math import sin, cos, sqrt, atan2, radians


# In[38]:


localidades = {
    'a': {'lat': -25.444722860176192, 'lon': -49.24107206417748, 'central': True, 'nome': 'CEMEPAR'}, 
    'b': {'lat': -25.427760452743378, 'lon': -49.313461329443214, 'central': True, 'nome': 'PAVILHÃO DE EVENTOS DO PARQUE BARIGUI'}, 
    'c': {'lat': -25.367996862203757, 'lon': -49.268784872187695, 'central': False, 'nome': 'US VILA DIANA'}, 
    'd': {'lat': -25.413519597715336, 'lon': -49.3013147771024, 'central': True, 'nome': 'US BOM PASTOR'}, 
    'e': {'lat': -25.461704486990964, 'lon': -49.316751504788606, 'central': True, 'nome': 'US SANTA QUITÉRIA I'}, 
    'f': {'lat': -25.478719928784678, 'lon': -49.272697921604504, 'central': False, 'nome': 'US FANNY-LINDOIA'}, 
    'g': {'lat': -25.49732101972271, 'lon': -49.227632019488134, 'central': False, 'nome': 'US WALDEMAR MONASTIER'}, 
    'h': {'lat': -25.45227869196361, 'lon': -49.217568300307384, 'central': False, 'nome': 'US CAJURU'}, 
    'i': {'lat': -25.480253158446637, 'lon': -49.33671464392894, 'central': False, 'nome': 'US SÃO MIGUEL'}, 
    'j': {'lat': -25.53760821551448, 'lon': -49.27329235524565, 'central': False, 'nome': 'US SÃO JOÃO DEL REY'}, 
    'k': {'lat': -25.560825101607314, 'lon': -49.336507547175266, 'central': False, 'nome': 'US MORADIAS SANTA RITA'}  
}


# In[21]:


def distance(origem, destino):
    R = 6373.0
    lat1 = radians(localidades[origem]['lat'])
    lon1 = radians(localidades[origem]['lon'])
    lat2 = radians(localidades[destino]['lat'])
    lon2 = radians(localidades[destino]['lon'])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    if datetime.datetime.now().hour in range(7, 9) or datetime.datetime.now().hour in range(16, 19):
        if localidades[origem]['central'] and localidades[destino]['central']:
            distance = distance * 2
        elif localidades[origem]['central'] or localidades[destino]['central']:
            distance = distance * 1.5
    return distance


# In[22]:


def random_sample():
    sample = list(localidades.keys())[1:]
    random.shuffle(sample)
    return ['a'] + sample + ['a']


# In[6]:


def fitness(sample):
    total_dist = 0
    for i in range(len(sample) - 1):
        total_dist = total_dist + distances[sample[i]][sample[i+1]]
    return ((100/total_dist)**5)


# In[7]:


def mutacao(sample, pMUT):
    for i in range(10):
        if random.randint(0, 1):
            index = random.randint(1, 9)
            sample[index], sample[index + 1] = sample[index + 1], sample[index]
        else:
            index = random.randint(2, 10)
            sample[index], sample[index -1] = sample[index - 1], sample[index]
    return sample


# In[8]:


def roleta(populacao, total):
    current = 0
    goal = random.uniform(0,total)
    for i in range(len(populacao)):
        current = current + populacao[i]['fitness']
        if current > goal:
            return populacao[i]
    return -1


# In[9]:


def crossover(a, b):
    a = a[1:-1]
    b = b[1:-1]
    a_cross = a[:5]
    b_cross = b[5:]
    for i in range(5):
        if not b[5+i] in a_cross:
            a_cross = a_cross + [b[5+i]]
        else:
            for b_un in b:
                if not b_un in a_cross:
                    a_cross = a_cross + [b_un]
                    break
        if not a[i] in b_cross:
            b_cross = b_cross[:i] + [a[i]] + b_cross[i:]
        else:
            for a_un in a:
                if not a_un in b_cross:
                    b_cross = b_cross[:i] + [a_un] + b_cross[i:]
                    break
    
    return ['a'] + a_cross + ['a'], ['a'] + b_cross + ['a']


# In[10]:


distances = {}
for i in range(len(localidades.keys())):
    for j in range(len(localidades.keys())):
        ii = list(localidades.keys())[i]
        jj = list(localidades.keys())[j]
        dist = distance(ii, jj)
        try:
            distances[ii][jj] = dist
        except:
            distances[ii] = {jj: dist}


# In[43]:


num_populacao = 100
iteracoes = 1000
pct_mutacao = 0.1
pct_crossover = 0.5
max_values = []
populacao = []
for i in range(num_populacao):
    sample = random_sample()
    populacao.append({'caminho': sample, 'fitness': fitness(sample)})

for i in range(iteracoes):
    filhos = []
    for i in range(num_populacao - 1):
        if not i%2:
            #print(i)
            if random.uniform(0,1) < pct_crossover:
                f1, f2 = crossover(populacao[i]['caminho'], populacao[i + 1]['caminho'])
            else:
                f1, f2 = populacao[i]['caminho'].copy(), populacao[i + 1]['caminho'].copy()
            f1 = mutacao(f1, pct_mutacao)
            f2 = mutacao(f2, pct_mutacao)
            filhos.append({'caminho': f1, 'fitness': fitness(f1)})
            filhos.append({'caminho': f2, 'fitness': fitness(f2)})
    escolhidos = []
    populacao = populacao + filhos
    total = sum([p['fitness'] for p in populacao])
    #print(total)
    for i in range(num_populacao):
        escolhido = roleta(populacao, total)['caminho']
        escolhidos.append({'caminho': escolhido, 'fitness': fitness(escolhido)})
    populacao = escolhidos
    max_values.append(max([caminho['fitness'] for caminho in populacao]))
    #populacao.sort(key=lambda x: x['fitness'], reverse=True)
    #populacao = populacao[:100]
    #print(populacao[0])

populacao.sort(key=lambda x: x['fitness'], reverse=True)
melhor = populacao[0]
print(f'Execução finalizada, o melhor caminho, com o valor de fitness={melhor["fitness"]} é:')
for i, localidade in enumerate(melhor['caminho']):
    print(f"{i+1} - {localidades[localidade]['nome']}")


# In[40]:


#populacao.sort(key=lambda x: x['fitness'], reverse=True)
#for p in populacao:
#    print(p)


# In[47]:


#plt.plot(max_values)
#plt.show()


# In[ ]:




