# Python-MIP
## Guia de instalação

O [Python-MIP](https://www.python-mip.com/) é uma biblioteca desenvolvida em linguagem Python para a resolução de modelos de programação linear, programação inteira, e programação linear-inteira mista. Ele foi integralmente desenvolvido no [Departamento de Computação](http://www3.decom.ufop.br/decom/inicio/) da [Universidade Federal de Ouro Preto (UFOP)](https://www.ufop.br/), por [Túlio Toffolo](http://www3.decom.ufop.br/toffolo/pt-br/) e [Haroldo Santos](http://www.decom.ufop.br/haroldo/).

Este pacote é um método simples para modelar e resolver problemas desta classe. Ele é uma linguagem de descrição que pode ser utilizada para efetivamente modelar e traduzir um problema de otimização. Além disso, esta modelagem pode ser incorporada em solvers comerciais, como o [CPC](https://github.com/coin-or/Cbc) e o [Gurobi](https://www.gurobi.com/), para a resolução destes problemas.

Esta biblioteca requer o uso do Python 3.5 ou versões mais novas. Sua instalação é simples e pode ser realizada com o comando 

```bash
pip install mip
```

Esta instalação básica já contém, também, o solver CPC, que é uma ótima alternativa livre e gratuita para a resolução de problemas de programação linear inteira mista. Caso seja de interesse, pode-se também instalar o Gurobi, que é um dos melhores resolvedores de programação linear inteira mista do mercado, junto ao Python-MIP, seguindo o passo-a-passo disponível [aqui](https://python-mip.readthedocs.io/en/latest/install.html).

Em computadores pessoais, ainda é possível instalar o [pypy](https://www.pypy.org/), que é um compilador Python *just-in-time* capaz de acelerar (e muito) a execução de códigos e scripts Python. Recomenda-se fortemente o uso do pypy junto do Python-MIP ou qualquer outro pacote Python que venha a ser instalado no computador.

Infelizmente, o pypy ainda não está disponível nos laboratórios da UNIFAL, mas será incluído para o próximo semestre. Em seu computador pessoal, a instalação do pypy pode ser realizada com o comando

```bash
pypy3 -m pip install mip
```

## Uso do Python-MIP

Um script Python com Python-MIP pode ser construído adicionando a seguinte linha ao cabeçalho de seu código

```python
from mip import *
```

### Criando modelos de otimização

Um modelo de otimização genérico pode ser criado com a função

```python
m = Model()
```

Por padrão, é criado um modelo de **minimização**. Entretanto, também é possível criarmos um modelo de **maximização** passando um argumento ao método ```model``` no momento de sua chamada:

```python
m = Model(sense=MAXIMIZE)
```

Além disso, também é possível trocar o *solver* CPC pelo Gurobi com o argumento

```python
m = Model(solver_name=GRB)
```

### Adicionando variáveis

Variáveis de decisão podem ser incluídas com o método ```add_var()```. Sem parâmetros, uma única variável de decisão real é criada e retornada

```python
x = m.add_var()
```

Entretanto, podemos criar um vetor de variáveis facilmente utilizando a sintaxe de inicialização de listas do Python. Vamos supor que você esteja interessado em criar um vetor com ```n = 10``` variáveis e salva-las em uma lista para posterior uso. Estas variáveis podem ser criadas com o comando

```python
n = 10
x = [m.add_var() for i in range(n)]
```

Variáveis também podem ser binárias ou inteiras. Para isto, basta incluir um novo parâmetro no método ```add_var()```. Para variáveis binárias, faz-se

```python
x = m.add_var(var_type=BINARY)
```

Já para variáveis inteiras, pode-se escrever

```python
x = m.add_var(var_type=INTEGER)
```

#### Adicionando limites as variáveis

Uma coisa que estudamos é que as variáveis podem ter um limite inferior (*lower bound*) ou um limite superior (*upper bound*). Na maioria de nossos exemplos, temos que o limite inferior de uma variável sempre é zero, isto é, que o menor valor permitido para a variável é igual a zero.

É muito simples integrar este tipo de limite na declaração das variáveis utilizando o parâmetro ```lb``` (para limite inferior) ou ```ub``` (para limite superior). Por exemplo, para criarmos um vetor de 5 variáveis inteiras entre 0 e 50, podemos utilizar o comando

```python
n = 5
x = [m.add_var(var_type=INTEGER, lb = 0, ub = 50) for i in range(n)]
```

De forma análoga, é possível criar um vetor com 30 variáveis reais maiores ou igual a zero com o comando

```python
n = 30
x = [m.add_var(lb = 0) for i in range(n)]
```

#### Adicionando nomes as variáveis

É possível adicionar, de forma opicional, nomes a cada uma das variáveis criadas de forma simples. Estes nomes poderão ser utilizados no processo de *debug* do modelo criado ou como forma de visualização do modelo criado. Por exemplo, podemos criar uma variável real ```z``` de nome ```cost```, com um limite inferior de ```-10``` e um limite superior de ```10``` com o comando

```python
z = m.add_var(name='cost', lb = -10, ub = 10)
```

### Adicionando restrições

Podemos adicionar restrições de igualdade e desigualdades. Todas as restrições são incorporadas no modelo ```m``` criado anteriormente.

Por exemplo, podemos adicionar a restrição $x + y \leq 10$ fazendo
```python
m += x + y <= 10
```
Também é muito fácil incorporarmos restrições com somatórios utilizando o comando ```xsum()```. Por exemplo, imagine a restrição de capacidade $\sum_{i = 0}^n w_i x_i \leq c$. Esta restrição pode ser inserida com o comando

```python
m += xsum(w[i]*x[i] for i in range(n)) <= c
```

#### Adicionando nomes as restrições

De forma similar as variáveis, as restrições do modelo também podem ter nomes. Estes nomes de restrições também podem ser úteis no momento do *debug* do modelo desenvolvido.

Pode-se adicionar o nome de uma restrição de forma simples, inserindo-o após a restrição linear, separando ambos por uma vírgula. Por exemplo, para inserir o nome ```capacidade``` na restrição anterior podemos fazer
```python
m += xsum(w[i]*x[i] for i in range(n)) <= c, 'capacidade'
```

### Adicionando a função objetivo

Por fim, podemos adicionar a função objetivo do modelo utilizando o método ```objective``` do modelo. Por exemplo, para criarmos uma função objetivo $\sum_{i = 0}^n c_i x_i$, podemos fazer

```python
m.objective = xsum(c[i]*x[i] for i in range(n))
```

Apesar de não descrito aqui, esta função objetivo é de **minimização**, pois o modelo foi criado com ```sense=MINIMIZE``` (o padrão do Python-MIP). Entretanto, é possível aqui alterar o sentido da função objetivo utilizando os métodos ```minimize()``` ou ```maximize()```. Por exemplo, para fazer a função objetivo anterior ser uma função de **maximização**, podemos escrever

```python
m.objective = maximize(xsum(c[i]*x[i] for i in range(n)))
```

### Salvando, carregando e checando o modelo desenvolvido

As funções ```read()``` e ```write()``` podem ser utilizadas para, respectivamente, ler e escrever em disco os modelos desenvolvidos.

Dois formatos de modelo são disponíveis:
 - **.lp**: Um formato de modelo mais próximo do que um humano consegue ler e *debugar*. Deve ser utilizado para verificar a corretude do modelo desenvolvido.
 - **.mps**: Um formato de modelo utilizado por *solvers* de programação linear inteira mista. É uma boa maneira de exportar o modelo desenvolvido para outras aplicações ou outros usuários.

Para salvar um modelo ```m``` em disco utilizando o formato *.lp*, podemos utilizar o comando
```python
m.write('meu_modelo.lp)
```
Já para lermos um modelo em disco salvo previamente utilizando o modelo *.mps*, podemos fazer
```python
m.read('modelo_salvo.mps')
```

### Resolvendo o modelo

Para resolver o modelo utiliza-se o método ```optimize()```. Este método tem [alguns parâmetros](https://docs.python-mip.com/en/latest/classes.html#mip.Model.optimize). Entretanto, o mais importante deles é o ```max_seconds```, que fixa um tempo limite para a resolução do modelo.

Por exemplo, para resolver o modelo ```m``` criado anteriormente com um limite de tempo de 1 hora (3600 segundos), podemos fazer

```python
m.optimize(max_seconds=3600)
```

O método ```optimize()``` retorna uma variável de *status*, indicando se o modelo foi resolvido na otimalidade (OPTIMAL), se o modelo foi resolvido de forma aproximada (FEASIBLE), ou se nenhuma solução viável foi encontrada (NO_SOLUTION_FOUND). Para armazenar o *status*, devemos salvar o retorno do método ```optimize()``` fazendo
```python
status = m.optimize(max_seconds=3600)
```

Cada *status* tem um diferente significado:
 - **OPTIMAL**: Indica que a solução ótima do modelo foi encontrada.
 - **FEASIBLE**: Indica que, ao menos, uma solução viável para o modelo foi encontrada dentro do tempo limite. Entretanto, a solução não foi provada ser ótima.
 - **NO_SOLUTION_FOUND**: Indica que nenhuma solução viável foi encontrada dentro do tempo limite. Este *status* é muito comum em problemas NP-Completos de programação linear inteira mista. 

Outros *status* também existem, a saber
 - **INFEASIBLE**: Não existe nenhuma solução para o modelo. Corresponde a um sistema linear impossível.
 - **INT_INFEASIBLE**: O mesmo que o anterior, mas indicando a inexistência de soluções inteiras.
 - **UNBOUNDED**: Modelos irrestritos, possuindo infinitas soluções. Corresponde a um sistema linear possível e inderteminado.

### Checando o resultado

Após a otimização, é necessário então verificar os valores de solução obtidos e os valores das variáveis de decisão. 

Modelos de programação inteira ou programação linear inteira mista possuem dois valores de solução. O primeiro, denominado ```objective_value```, corresponde ao valor da função objetivo. Já o segundo, denominado ```objective_bound```, corresponde a uma estimativa do valor da função objetivo. Esta aproximação é computada relaxando as condições de integralidade das variáveis, isto é, fazendo com que elas sejam reais ao invés de inteiras.

Para checarmos estes valores, podemos fazer

```python
status = m.optimize(max_seconds=3600)
if status == OptimizationStatus.OPTIMAL:
    print('Solução ótima de custo {} encontrada'.format(m.objective_value))
elif status == OptimizationStatus.FEASIBLE:
    print('Solução de custo {} encontrada. Melhor aproximação da solução ótima é {}'.format(m.objective_value, m.objective_bound))
elif status == OptimizationStatus.NO_SOLUTION_FOUND:
    print('Nenhuma solução encontrada. A melhor aproximação encontrada para a solução ótima é {}'.format(m.objective_bound))
```

#### Checando as variáveis

Também após a otimização, é possível verificar os valores das variáveis na solução de melhor função objetivo obtida. Para isto, basta fazer um *loop* pelas variáveis do modelo e imprimir seus valores

```python
if status == OptimizationStatus.OPTIMAL or status == OptimizationStatus.FEASIBLE:
    print('Solução:')
    for v in m.vars:
        print('{} : {}'.format(v.name, v.x))
```

Observe que só faz sentido fazermos tal *loop* se o *status* do modelo é **OPTIMAL** ou **FEASIBLE**, pois estes são os únicos *status* que indicam que uma solução viável foi obtida.

Normalmente, só nos é interessante obter as variáveis que foram utilizadas na função objetivo. Assim, podemos melhorar o código acima para não imprimir as variáveis com valor zero, isto é, não imprimir as variáveis que não foram utilizadas. Podemos fazer

```python
if status == OptimizationStatus.OPTIMAL or status == OptimizationStatus.FEASIBLE:
    print('Solução:')
    for v in m.vars:
       # Imprimir somente os não-zeros
       if abs(v.x) > 1e-6: # Contornando o erro numérico
          print('{} : {}'.format(v.name, v.x))
```

Neste código, o valor $1e^{-6}$ indica um erro numérico muito comum em resolvedores de programação linear inteira mista. Tal valor, equivalente a $0.000001$, por vezes é obtido como um *bug* decorrente das intensas multiplicações de matrizes realizadas pelo método Simplex durante a resolução do sistema de equações lineares. Desta maneira, é uma boa prática considerar variáveis com valor menor ou igual a $1e^{-6}$ como zero.

## Documentação e ajuda

Apesar de ser simples de usar e extretamente poderoso, o Python-MIP ainda não é um pacote extremamente famoso ou utilizado pela comunidade científica ou pelo mercado. Desta menira, não existe uma grande quantidade de discussões acerca dos métodos e de suas bibliotecas na Internet.

Assim, a maior fonte de ajuda para trabalhar com o Python-MIP é justamente [sua documentação oficial](https://docs.python-mip.com/en/latest/index.html), principalmente as [descrições de suas classes, métodos e variáveis](https://docs.python-mip.com/en/latest/classes.html).

Outros exemplos práticos podem ser encontrados no artigo aqui em anexo e na documentação oficial do método.