import json
from collections import deque
import time  # Importando a biblioteca time para medir o tempo

# Função para carregar o grafo de disciplinas de um arquivo JSON
def carregar_grafo_de_arquivo(arquivo):
    with open(arquivo, 'r') as f:
        grafo = json.load(f)
    return grafo

def calcular_prioridade(O, A, S, periodo, P_prereq, carga_horaria):
    N = 1 if P_prereq else 0
    return round((200 * O + 40 * A + 20 * S + 80 * N + P_prereq) * (1.1 - (periodo / 10)) * (carga_horaria / 60), 2)

# Função para coletar informações sobre disciplinas cursadas, considerando pré-requisitos
def obter_disciplinas_cursadas(grafo):
    status_do_curso = {}
    visitados = set()

    # Função auxiliar para verificar se a disciplina pode ser perguntada
    def pode_perguntar(disciplina):
        dados = grafo[disciplina]
        prereqs = dados["Prerequisitos"]
        # A disciplina pode ser perguntada se todos os seus pré-requisitos foram cursados e aprovados
        return all(status_do_curso.get(pr, "nao_cursada") == "aprovada" for pr in prereqs)

    for disciplina in grafo:
        # Se a disciplina pode ser perguntada com base nos pré-requisitos
        if pode_perguntar(disciplina):
            status = input(f"Você já cursou a disciplina {disciplina}? (s/n): ").strip().lower()
            if status == "s":
                status_do_curso[disciplina] = "aprovada"
            else:
                status_do_curso[disciplina] = "nao_cursada"
            visitados.add(disciplina)
        else:
            status_do_curso[disciplina] = "nao_cursada"
    
    return status_do_curso

# Função BFS para explorar o grafo de disciplinas
def bfs(disciplina, grafo, status_do_curso, visitados):
    fila = deque([disciplina])  # Iniciando a fila com a primeira matéria
    recomendacoes = []
    
    while fila:
        atual = fila.popleft()
        if atual in visitados:
            continue

        visitados.add(atual)
        dados = grafo[atual]
        status = status_do_curso.get(atual, "nao_cursada")
        prereqs = dados["Prerequisitos"]

        # Usando "Obrigatoria" se existir, caso contrário usa "Optativa"
        O = dados.get("Obrigatoria", dados.get("Optativa", 0))
        A = dados.get("Anual", 0)
        S = dados.get("Semestre", 0)
        periodo = dados.get("Periodo", 0)
        carga_horaria = dados.get("CargaHoraria", 0)

        # Verifica se a disciplina pode ser recomendada
        if status != "aprovada":
            # Se todos os pré-requisitos foram cumpridos, recomenda essa disciplina
            if all(status_do_curso.get(pr, "nao_cursada") == "aprovada" for pr in prereqs):
                prioridade = calcular_prioridade(O, A, S, periodo, int(bool(prereqs)), carga_horaria)
                recomendacoes.append((atual, prioridade))

        # Adiciona os vizinhos à fila
        for vizinho in grafo:
            if atual in grafo[vizinho]["Prerequisitos"] and vizinho not in visitados:
                fila.append(vizinho)
    
    return recomendacoes
 

# Função para gerar recomendações
def recomendar_matriculas(grafo, status_do_curso):
    recomendacoes = []
    visitados = set()
    
    for disciplina in grafo:
        if disciplina not in visitados:
            recomendacoes.extend(bfs(disciplina, grafo, status_do_curso, visitados))
    
    # Ordena as recomendações pela prioridade (maior para menor)
    recomendacoes.sort(key=lambda x: x[1], reverse= True)
    
    # Limita as recomendações a no máximo 5
    recomendacoes = recomendacoes[:5]
    
    return recomendacoes

# Fluxo principal
print("Bem-vindo ao sistema de recomendação de matrícula!")
print("Responda às perguntas para que possamos recomendar as melhores disciplinas.")

# Medir o tempo total de execução
inicio_tempo = time.time()

# Carregar o grafo de disciplinas a partir de um arquivo JSON
grafo_das_disciplinas = carregar_grafo_de_arquivo("grafo_disciplina.json")

# Medir o tempo para carregar o grafo
tempo_carregar_grafo = time.time() - inicio_tempo
print(f"Tempo para carregar o grafo: {tempo_carregar_grafo:.2f} segundos")

# Perguntar sobre cada disciplina com base nos pré-requisitos
status_do_curso = obter_disciplinas_cursadas(grafo_das_disciplinas)

# Medir o tempo para coletar o status das disciplinas
tempo_status_disciplinas = time.time() - (inicio_tempo + tempo_carregar_grafo)
print(f"Tempo para coletar status das disciplinas: {tempo_status_disciplinas:.2f} segundos")

# Gerar recomendações
recomendacoes = recomendar_matriculas(grafo_das_disciplinas, status_do_curso)

# Medir o tempo para gerar as recomendações
tempo_recomendacoes = time.time() - (inicio_tempo + tempo_carregar_grafo + tempo_status_disciplinas)
print(f"Tempo para gerar recomendações: {tempo_recomendacoes:} segundos")

# Exibir recomendações
print("\nRecomendações de matrícula (máximo de 5 disciplinas):")
if recomendacoes:
    for disciplina, prioridade in recomendacoes:
        print(f"Disciplina: {disciplina}, Prioridade: {prioridade}")
else:
    print("Nenhuma disciplina disponível para matrícula no momento.")

# Medir o tempo total de execução
tempo_total = time.time() - inicio_tempo
print(f"\nTempo total de execução: {tempo_total:} segundos")
