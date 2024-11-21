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
    "XDES01": {
    "Obrigatoria": 1,
    "Anual": 0,
    "Semestre": 1,
    "Periodo": 1,
    "Prerequisitos": [],
    "Horario": [["3N12", "5N34"] ,["3M45", "4M45"]],
    "Equivalente": {
      "ECOP11A": [["2M45", "3M12"], ["4M23", "5M45"], ["2M23", "3M45"], ["2M45", "3M23"]]
    }
  },
  "MAT00A": {
    "Obrigatoria": 1,
    "Anual": 0,
    "Semestre": 0,
    "Periodo": 1,
    "Prerequisitos": [],
    "Horario": [["3N12", "5N12"],["2N12", "4N34"],  ["2N12", "4N12"], ["2T34", "4T12"], ["2M45", "4M23"], ["3T12", "6T12"], ["2T34", "4T34"], ["3T34", "5T34"]],
    "Equivalente": {
      "MATI2301": []
    }
  },
```

`Prerequisitos:` Lista de disciplinas que devem ser concluídas antes.

`Obrigatoria / Optativa:` Define se é obrigatória (1) ou optativa (-1).

`Anual:` Indica se a disciplina é anual ou semestral.

`Semestre:` Indica se a disciplina é de um semestre futuro, atual ou anterior.

`Periodo:` O período sugerido para cursar.

---

## 2️⃣ **Fórmula de Prioridade**
A prioridade de uma disciplina é calculada com base na fórmula:

```
round((200 * O + 40 * A + 20 * S + 80 * N + P_prereq) * (1.1 - (periodo / 10)), 2)
```

Onde:

`O:` Obrigatoriedade (1 ou 0).

`A:` Anualidade (1 ou 0).

`S:` Localização de semestre (1, 0 ou -10).

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

Após isso pergunta para qual semestre o aluno está se matriculando.
Exemplo de interação:

```
Qual o período atual? (Ex: 1, 2, 3, ...): 
```

3️⃣ Cálculo de Prioridade

Para cada disciplina disponível, a fórmula de prioridade é usada para determinar sua relevância para matrícula.

4️⃣ Recomendações

Até 5 disciplinas são recomendadas, ordenadas por prioridade.

---

## **📊 Exemplo de Saída**
Após responder às perguntas, o sistema exibe:

```
_______________________________________________________________________

Recomendações de matrícula (máximo de 5 disciplinas):

Disciplina: XDES01 | Prioridade: 220.0 | Horarios: ['3N12', '5N34']
Disciplina: MAT00A | Prioridade: 220.0 | Horarios: ['2N12', '4N34']
Disciplina: IEPG01 | Prioridade: 220.0 | Horarios: ['3N345']
Disciplina: IEPG22 | Prioridade: 220.0 | Horarios: ['4N12']
Disciplina: SAHC04 | Prioridade: 220.0 | Horarios: ['6N12']

_______________________________________________________________________
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

3- Responda às perguntas interativas sobre as disciplinas já cursadas e sobre o semestre que deseja cursar.

4- Veja as recomendações de matrícula geradas pelo sistema.

---

## **🤝 Contribuições**
- Augusto de Camargos Zanoli
- Lucas Silva Pinheiro
- Matheus Anthony Pereira Abreu
- Tomás Francisco Rossetto Lavez
