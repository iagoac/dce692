from itertools import product
from sys import stdout as out
from mip import Model, xsum, minimize, BINARY

# Lista de cidades
places = ['Antwerp', 'Bruges', 'C-Mine', 'Dinant', 'Ghent',
'Grand-Place de Bruxelles', 'Hasselt', 'Leuven',
'Mechelen', 'Mons', 'Montagne de Bueren', 'Namur',
'Remouchamps', 'Waterloo']

# Matriz de distâncias entre as cidades
dists = [[83, 81, 113, 52, 42, 73, 44, 23, 91, 105, 90, 124, 57],
[161, 160, 39, 89, 151, 110, 90, 99, 177, 143, 193, 100],
[90, 125, 82, 13, 57, 71, 123, 38, 72, 59, 82],
[123, 77, 81, 71, 91, 72, 64, 24, 62, 63],
[51, 114, 72, 54, 69, 139, 105, 155, 62],
[70, 25, 22, 52, 90, 56, 105, 16],
[45, 61, 111, 36, 61, 57, 70],
[23, 71, 67, 48, 85, 29],
[74, 89, 69, 107, 36],
[117, 65, 125, 43],
[54, 22, 84],
[60, 44],
[97],
[]]

# Número de nós e lista de vértices
n, V = len(dists), set(range(len(dists)))

# Montando a matriz de distâncias completa
c = [[0 if i == j
    else dists[i][j-i-1] if j > i
    else dists[j][i-j-1]
    for j in V] for i in V]

# Criando o modelo
model = Model()

# Adicionando variáveis binárias indicando se um arco vai ser utilizado ou não
x = [[model.add_var(var_type=BINARY) for j in V] for i in V]

# Variáveis contínuas para eliminação de ciclos
# Esta restrição funciona utilizando rótulos nas cidades
y = [model.add_var() for i in V]

# Função objetivo: minimizar o custo total
model.objective = minimize(xsum(c[i][j]*x[i][j] for i in V for j in V))

# Restrição: sair de cada cidade somente uma vez
for i in V:
    model += xsum(x[i][j] for j in V - {i}) == 1

# Restrição: entrar em cada cidade somente uma vez
for i in V:
    model += xsum(x[j][i] for j in V - {i}) == 1

# Eliminação de sub-rotas
for (i, j) in product(V - {0}, V - {0}):
    if i != j:
        model += y[i] - (n+1)*x[i][j] >= y[j]-n

# Otimização do modelo. Observe o tempo limite
model.optimize(max_seconds=30)

# Verificando se uma ou mais soluções foram encontradas
if model.num_solutions:
    out.write('Rota com distância %g encontrada: %s'
    % (model.objective_value, places[0]))

    nc = 0
    while True:
        nc = [i for i in V if x[nc][i].x >= 0.99][0]
        out.write(' -> %s' % places[nc])
        if nc == 0:
            break
    out.write('\n')