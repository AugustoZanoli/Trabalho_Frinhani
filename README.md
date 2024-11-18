# 📚 Sistema de Recomendação de Matrículas 

Este projeto é um sistema de recomendação para matrículas em disciplinas acadêmicas. Ele utiliza um **grafo de disciplinas** com pré-requisitos, carga horária e outros atributos para sugerir as melhores disciplinas para o próximo período com base em prioridades calculadas. 

---

## 🚀 **Recursos principais**
- Carregamento de um grafo de disciplinas a partir de um arquivo JSON.
- Coleta interativa de informações sobre disciplinas já cursadas.
- Geração de recomendações personalizadas com base em uma fórmula de prioridade.
- Ordenação das disciplinas mais importantes para matrícula.
- Exibição do tempo de execução das etapas.

---

## 🛠️ **Como funciona?**

1️⃣ **Estrutura do Grafo:**  
O grafo de disciplinas deve ser armazenado em um arquivo `grafo_disciplina.json`, com o seguinte formato:

```json
{
    "Disciplina1": {
        "Obrigatoria": 1,
        "Anual": 0,
        "Semestre": 1,
        "Periodo": 2,
        "Prerequisitos": ["DisciplinaX", "DisciplinaY"],
        "CargaHoraria": 60
    },
    "Disciplina2": {
        "Obrigatoria": -1,
        "Anual": 0,
        "Semestre": 1,
        "Periodo": 1,
        "Prerequisitos": [],
        "CargaHoraria": 45
    }
} 
```

`Prerequisitos:` Lista de disciplinas que devem ser concluídas antes.

`Obrigatoria / Optativa:` Define se é obrigatória (1) ou optativa (1).

`Anual / Semestre:` Indica se a disciplina é anual ou semestral.

`Periodo:` O período sugerido para cursar.

`CargaHoraria:` A carga horária total da disciplina.

---

## 2️⃣ **Fórmula de Prioridade**
A prioridade de uma disciplina é calculada com base na fórmula:

```
round((200 * O + 40 * A + 20 * S + 80 * N + P_prereq) * (1.1 - (periodo / 10)) * (carga_horaria / 60), 2)
```

Onde:

`O:` Obrigatoriedade (1 ou 0).

`A:` Anualidade (1 ou 0).

`S:` Semestralidade (1 ou 0).

`N:` Indicador binário (1 ou 0) para presença de pré-requisitos.

`P_prereq:` Número de pré-requisitos atendidos.

`carga_horaria:` Carga horária total da disciplina.

---

## 📋 **Fluxo de Execução**

1️⃣ Carregamento do Grafo

O sistema carrega as informações do arquivo JSON e organiza as disciplinas em um grafo.

2️⃣ Coleta de Status das Disciplinas

O sistema pergunta ao usuário, uma por uma, se as disciplinas já foram cursadas.
Exemplo de interação:

```
Você já cursou a disciplina Cálculo 1? (s/n):
```

3️⃣ Cálculo de Prioridade

Para cada disciplina disponível, a fórmula de prioridade é usada para determinar sua relevância para matrícula.

4️⃣ Recomendações

Até 5 disciplinas são recomendadas, ordenadas por prioridade.

---

## **📊 Exemplo de Saída**
Após responder às perguntas, o sistema exibe:

```
Recomendações de matrícula (máximo de 5 disciplinas):
1. Disciplina: Algoritmos e Estruturas de Dados, Prioridade: 8.75
2. Disciplina: Redes de Computadores, Prioridade: 7.85
...
```

Caso nenhuma disciplina seja recomendada:
```
Nenhuma disciplina disponível para matrícula no momento.
```

---

## **🖥️ Como executar o sistema?**

`Pré-requisitos:`
- Python 3.x instalado no sistema.

- Arquivo grafo_disciplina.json configurado no formato correto.

`Passos:`

1- Certifique-se de que o arquivo grafo_disciplina.json esteja no mesmo diretório que o script.

2- Execute o script no terminal:

```
python recomendacao_matriculas.py
```

3- Responda às perguntas interativas sobre as disciplinas já cursadas.

4- Veja as recomendações de matrícula geradas pelo sistema.

---

## **🕒 Medição de Desempenho**
O sistema exibe o tempo de execução das seguintes etapas:

- Carregamento do grafo.

- Coleta de status das disciplinas.

- Geração das recomendações.

- Tempo total de execução.

Exemplo de saída:

```
Tempo para carregar o grafo: 0.12 segundos  
Tempo para coletar status das disciplinas: 1.45 segundos  
Tempo para gerar recomendações: 0.08 segundos  
Tempo total de execução: 1.65 segundos
```

---

## **🤝 Contribuições**
- Augusto de Camargos Zanoli
- Matheus Anthony 
