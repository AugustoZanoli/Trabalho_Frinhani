import json
import time  # Importando a biblioteca time para medir o tempo

# Função para carregar o grafo de disciplinas de um arquivo JSON
def carregar_grafo_de_arquivo(arquivo):
    with open(arquivo, 'r') as f:
        grafo = json.load(f)
    return grafo

def calcular_prioridade(O, A, S, periodo, P_prereq):
    N = 1 if P_prereq else 0
    return round((200 * O + 40 * A + 20 * S + 80 * N + P_prereq) * (1.1 - (periodo / 10)), 2)

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

# Função DFS para explorar o grafo de disciplinas
def dfs(disciplina, grafo, status_do_curso, visitados, p):
    if disciplina in visitados:
        return []

    visitados.add(disciplina)
    recomendacoes = []
    dados = grafo[disciplina]
    status = status_do_curso.get(disciplina, "nao_cursada")
    prereqs = dados["Prerequisitos"]

    # Usando "Obrigatoria" se existir, caso contrário usa "Optativa"
    O = dados.get("Obrigatoria", dados.get("Optativa", 0))
    A = dados.get("Anual", 0)
    periodo = dados.get("Periodo", 0)
    
    # Definindo pontuação de semestralidade com base no período atual
    if int(p) == int(periodo):
        S = 1
    elif int(p) < int(periodo):
        S = -10
    else:
        S = 0

    # Verifica se a disciplina pode ser recomendada
    if status != "aprovada":
        if all(status_do_curso.get(pr, "nao_cursada") == "aprovada" for pr in prereqs):
            prioridade = calcular_prioridade(O, A, S, periodo, int(bool(prereqs)))
            recomendacoes.append((disciplina, prioridade))

    # Explora recursivamente os pré-requisitos
    for prereq in prereqs:
        recomendacoes.extend(dfs(prereq, grafo, status_do_curso, visitados, p))

    return recomendacoes


# Função para recomendar matrículas usando DFS
def recomendar_matriculas_dfs(grafo, status_do_curso, p):
    recomendacoes = []
    visitados = set()

    for disciplina in grafo:
        if disciplina not in visitados:
            recomendacoes.extend(dfs(disciplina, grafo, status_do_curso, visitados, p))

    # Ordenar recomendações por prioridade
    recomendacoes.sort(key=lambda x: x[1], reverse=True)

    # Filtrar até 5 recomendações com controle de horário
    recomendacao_final = []
    horarios = {
        "2": {"M": [], "T": [], "N": []},
        "3": {"M": [], "T": [], "N": []},
        "4": {"M": [], "T": [], "N": []},
        "5": {"M": [], "T": [], "N": []},
        "6": {"M": [], "T": [], "N": []},
        "7": {"M": [], "T": [], "N": []}
    }

    while len(recomendacao_final) < 5 and recomendacoes:
        disciplina_tuple = recomendacoes.pop(0)
        disciplina, pontuacao = disciplina_tuple
        disciplina_adicionada = False
        
        # Tenta adicionar a disciplina principal em qualquer um de seus horários
        for conjunto_horario in grafo[disciplina]["Horario"]:
            pode_adicionar = True
            
            # Verifica se esse horário está livre
            for horario_turma in conjunto_horario:
                dia = horario_turma[0]
                periodo = horario_turma[1]
                horas = horario_turma[2:]
                
                # Se qualquer horário estiver ocupado, não pode usar este conjunto
                if any(h in horarios[dia][periodo] for h in horas):
                    pode_adicionar = False
                    break
            
            # Se encontrou um horário válido, adiciona a disciplina
            if pode_adicionar:
                for horario in conjunto_horario:
                    dia = horario[0]
                    periodo = horario[1]
                    for h in horario[2:]:
                        horarios[dia][periodo].append(h)
                
                recomendacao_final.append((disciplina, pontuacao, conjunto_horario))
                disciplina_adicionada = True
                break
        
        # Só tenta equivalentes se não conseguiu adicionar a disciplina principal
        if not disciplina_adicionada:
            disciplinas_equivalentes = grafo[disciplina]["Equivalente"]
            for equiv_codigo, equiv_horarios in disciplinas_equivalentes.items():
                for conjunto_horario in equiv_horarios:
                    pode_adicionar = True
                    
                    # Verifica se esse horário está livre
                    for horario in conjunto_horario:
                        dia = horario[0]
                        periodo = horario[1]
                        horas = horario[2:]
                        
                        if any(h in horarios[dia][periodo] for h in horas):
                            pode_adicionar = False
                            break
                    
                    # Se encontrou um horário válido para a equivalente, adiciona
                    if pode_adicionar:
                        for horario in conjunto_horario:
                            dia = horario[0]
                            periodo = horario[1]
                            for h in horario[2:]:
                                horarios[dia][periodo].append(h)
                        
                        recomendacao_final.append((equiv_codigo, pontuacao, conjunto_horario))
                        disciplina_adicionada = True
                        break
                
                if disciplina_adicionada:
                    break

    return recomendacao_final


# Fluxo principal atualizado para usar DFS
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

while True:
    periodo = input("Qual o período atual? (Ex: 1, 2, 3, ...): ")
    if periodo.isdigit() and int(periodo) >= 1:
        break
    print("Período inválido. Por favor, insira um período válido. (1 ou superior)")

# Gerar recomendações usando DFS
recomendacoes = recomendar_matriculas_dfs(grafo_das_disciplinas, status_do_curso, periodo)

# Medir o tempo para gerar as recomendações
tempo_recomendacoes = time.time() - (inicio_tempo + tempo_carregar_grafo + tempo_status_disciplinas)
print(f"Tempo para gerar recomendações: {tempo_recomendacoes:.2f} segundos")

# Exibir recomendações
print("_______________________________________________________________________")
print("\nRecomendações de matrícula (máximo de 5 disciplinas):\n")
if recomendacoes:
    for disciplina, prioridade, horario in recomendacoes:
        print(f"Disciplina: {disciplina} | Prioridade: {prioridade} | Horarios: {horario}")
else:
    print("Nenhuma disciplina disponível para matrícula no momento.")

print("\n_______________________________________________________________________")
# Medir o tempo total de execução
tempo_total = time.time() - inicio_tempo
print(f"\nTempo total de execução: {tempo_total:.2f} segundos")
