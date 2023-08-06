import igraph as ig
import random
import numpy as np
import math
import collections
from graphcol.gulosos import Gulosos

class Exatos:

  """
  Classe que contém a implementação dos algoritmos exatos para coloração de grafos,
  """
    
  def cromatico_lawler(grafo):
    """
    Função que devolve o número cromático de um grafo. Como se trata de uma função de devolve o valor
    exato deve ser usada com cautela, pois para instâncias a partir de 10 vértices já é possível que
    o tempo de exeução da função ultrapasse 10 minutos. Por isso recomendamos uso em pequenas instâncias
    """

    def lawler(grafo):
      """
      Função responsável por fazer o controle das chamadas recursivas do algoritmo de Lawler,
      basicamente ela faz a primeira chamada recursiva e define algumas outras constantes
      importantes no processo.
      """
      tipo_arestas = np.dtype('int,int')
      n_vertices = grafo.vcount()
      lista_arestas = grafo.get_edgelist()
      array_arestas = np.array(lista_arestas, dtype = tipo_arestas)
      if n_vertices == 0:
        return math.inf
      if len(lista_arestas) == 0:
        return 1
      return cromatico_lawler(lista_arestas, n_vertices)
      
    def cromatico_lawler(arestas_grafo, n_vertices):
      """
      Função principal do algoritmo de Lawler responsável por fazer os testes de caso base e 
      chamar recursivamente as próximas etapas da recursão.
      """
      if n_vertices == 0:
        return math.inf
      if len(arestas_grafo) == 0:
        return 1
      if len(arestas_grafo) == 1 and n_vertices >= 2:
        return 2
      if ig.Graph(arestas_grafo).is_bipartite():
        return 2
      if ig.Graph(arestas_grafo).is_tree():
        return 2
      X_subgrafo = 0
      ids = 2**n_vertices
      for i in range(ids):
        id_subgrafo = bin(i)[2:].rjust(n_vertices, '0')
        X_subgrafo = n_vertices
        lista_vertices = [(len(id_subgrafo)-i-1) for i in range(len(id_subgrafo)) if id_subgrafo[i] == '1']
        arestas_subgrafo = [(x,y) for (x,y) in arestas_grafo if (x in lista_vertices) and (y in lista_vertices)]
        conjuntos_independentes_maximais = ig.Graph(arestas_grafo).subgraph_edges(arestas_subgrafo, delete_vertices = True).maximal_independent_vertex_sets()
        for conjunto_independente_maximal in conjuntos_independentes_maximais:
          vertices_limpo = [vertice for vertice in lista_vertices if vertice not in list(conjunto_independente_maximal)]
          vertices_limpo = [vertice for vertice in vertices_limpo if vertice in [u for (u,v) in arestas_grafo] + [v for (u,v) in arestas_grafo]]
          arestas_limpo = ig.Graph(arestas_grafo).subgraph(vertices_limpo).get_edgelist()
          X_subgrafo = min(X_subgrafo, cromatico_lawler(arestas_limpo, len(vertices_limpo)) + 1)
      return X_subgrafo
      
    return lawler(grafo)

  def dsatur_exato(grafo):
    """
    Função usada como interface do algoritmo dsatur exato, usada na
    primeira que começa a recursão que implementa o backtracking. A coisa
    mais importante que essa função faz é criar um primeira solução do dsatur 
    """
    numero_vertices = grafo.vcount()
    lista_adjacencias = grafo.get_adjlist()
    lista_arestas = grafo.get_edgelist()
    primeira_coloracao = Gulosos.dsatur(grafo).vs["cor"]
    melhor_resultado = len(set(primeira_coloracao))  

    def dsatur_recursao(grafo, melhor_resultado, coloracao = [], vertices_coloridos = []):
      """
      Função usada nas chamadas recursivas do Dsatur exato, funcionando como o
      backtracking do algoritmo
      """

      melhor_geral = melhor_resultado
      grafo_geral = grafo
      coloracao_original = coloracao
      vertices_coloridos_original = vertices_coloridos
      vertices_n_coloridos = vertices_coloridos.count(0)
      vertices_tentados = []
      tentativas_coloracao = 0

      while tentativas_coloracao < vertices_n_coloridos:

        vertices_coloridos = vertices_coloridos_original
        coloracao = coloracao_original

        if coloracao == None:
          vertices_coloridos = numero_vertices * [0]
          vertices_coloridos_auxiliar = vertices_coloridos
          grau_saturacao = FuncAux.atualiza_grau_sat(lista_adjacencias, vertices_coloridos)
          vertice_maior_grau = FuncAux.seleciona_vertice_dsatur(grau_saturacao, vertices_coloridos)
          cor = {vertice_maior_grau}
          coloracao = [cor]
          vertices_coloridos[vertice_maior_grau] = 1
          grafo.vs[vertice_maior_grau]['cor'] = coloracao.index(cor)
        else:
          grau_saturacao = FuncAux.atualiza_grau_sat(lista_adjacencias, vertices_coloridos)
          vertice_maior_grau = FuncAux.seleciona_vertice_dsatur(grau_saturacao, vertices_coloridos, vertices_tentados)
          for cor in coloracao:
            if FuncAux.conjunto_independente(lista_arestas, cor.union({vertice_maior_grau})):
              cor.add(vertice_maior_grau)
              grafo.vs[vertice_maior_grau]['cor'] = coloracao.index(cor)
              vertices_coloridos[vertice_maior_grau] = 1
              break
          if vertices_coloridos[vertice_maior_grau] == 0:
            cor = {vertice_maior_grau}
            coloracao.append(cor)
            grafo.vs[vertice_maior_grau]['cor'] = coloracao.index(cor)
            vertices_coloridos[vertice_maior_grau] = 1
        
        qntd_cores = len(set(coloracao))

        if len(vertices_coloridos) != numero_vertices and qntd_cores < melhor:
          melhor, grafo = dsatur_recursao(grafo, melhor_geral, coloracao, vertices_coloridos)
          if melhor < melhor_geral:
            vertices_tentados.append[vertice_maior_grau]
            tentativas_coloracao = tentativas_coloracao+1
            melhor_geral = melhor
            grafo_geral = grafo
          continue
        
        if len(vertices_coloridos) == numero_vertices:
          if qntd_cores < melhor_geral:
            melhor_geral = melhor
            grafo_geral = grafo
          return melhor_geral, grafo_geral

        if qntd_cores >= melhor:
          vertices_tentados.append[vertice_maior_grau]
          tentativas_coloracao = tentativas_coloracao+1
          continue

      return melhor_geral, grafo_geral
    
    melhor, grafo = dsatur_recursao(grafo, melhor_resultado)

    return grafo
  
class FuncAux:
  '''
  Classe que contém funções auxiliares usadas pelos algoritmos gulosos.
  '''
  def conjunto_independente(lista_arestas, subconjunto_vertices):
        '''
        Função que pega a lista de arestas de um grafo e um subconjunto de seus vértices e
         verifica se esse subconjunto é conjunto independente de vértices.
        
        Parameters:
        lista_arestas (list): Lista das arestas do grafo, cada aresta
         deve ser representada por uma tupla
        subconjunto_vertices (list): Subconjunto de vértices do grafo original
         qual deseja-se saber se o subconjunto de vértices passado forma
         ou não conjunto independente

        Returns:
        resultado: Retorna True se o subconjunto é independente,
         retorna False se não for
        '''
        for vertice_a in subconjunto_vertices:
            for vertice_b in subconjunto_vertices:
                if ((vertice_a, vertice_b) or (vertice_b, vertice_a)) in lista_arestas:
                    return False
        return True

  def atualiza_grau_sat(lista_adjacencias, vertices_coloridos):
        ''' 
        Função que devolve uma lista de grau de saturação, usada durante a execução do algoritmo DSatur.

        Parameters:
        lista_arestas (list): Lista das listas de adjacências de cada vértice.
        cores_vertice (list) : Lista com os vértices que já foram coloridos.

        Returns:
        list: Devolve a lista com o grau de saturação de cada vértice.
        '''
        grau_saturacao = len(vertices_coloridos) * [0]
        for vertice in range(len(vertices_coloridos)):
            for vertice_adjacente in lista_adjacencias[vertice]:
                if vertices_coloridos[vertice_adjacente] != 0:
                    grau_saturacao[vertice] += 1
        return grau_saturacao

  def seleciona_vertice_dsatur(grau_saturacao, vertices_coloridos, vertices_tentados = []):
        ''' 
        Função que recebe uma lista com o grau de saturação de todos os
         vértices de um grafo e devolve o vértice com maior grau de saturação.
        Caso haja mais de um vértice com maior grau de saturação o vértice devolvido
         é aletaório entre esses vértices de maior grau.

        Parameters:
        grau_saturacao (list): Lista com os graus de saturação de cada vértice.
        vertices_tentados (list): Vértices que no nó atual já tentou-se colorir

        Returns:
        int: Devolve inteiro que indica qual vértice ainda não colorido o com maior grau de saturação no grafo.
        '''
        vertices_n_coloridos_grau_max = []
        grau_max = 0
        for vertice in range(len(vertices_coloridos)):
          if vertice not in vertices_tentados and vertices_coloridos[vertice] == 0:
                if grau_saturacao[vertice] == grau_max:
                    vertices_n_coloridos_grau_max.append(vertice)
                elif grau_saturacao[vertice] > grau_max:
                    vertices_n_coloridos_grau_max.clear()
                    vertices_n_coloridos_grau_max.append(vertice)
                    grau_max = grau_saturacao[vertice]
        vertice_escolhido = random.choice(vertices_n_coloridos_grau_max)
        return vertice_escolhido