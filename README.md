# Lesson Plan Manager

Sistema simples para gerenciamento de planos de aula, desenvolvido como parte de um desafio técnico para a vaga de Estágio em Suporte e Manutenção de Software.

A aplicação permite cadastrar, consultar, editar e excluir planos de aula. Também possui uma funcionalidade chamada Smart Assist, que gera recomendações de conteúdos, recursos de apoio e tags com base nas informações principais da aula.

## Objetivo do projeto

O objetivo do projeto é criar uma aplicação simples para apoiar professores e conteudistas na organização de planos de aula.

Como o desafio é voltado para uma vaga de estágio, a estrutura foi pensada para ser direta, fácil de entender e simples de manter. Em uma evolução futura, o backend poderia ser separado em arquivos de rotas, modelos e serviços.

## Funcionalidades implementadas

- Cadastro de planos de aula
- Listagem de planos de aula
- Edição de planos existentes
- Exclusão de planos
- Busca por título
- Filtro por disciplina
- Filtro por tag
- Filtro por data prevista
- Ordenação por título ou data de cadastro
- Smart Assist com recomendações automáticas
- Loading visual durante a geração das recomendações
- Tratamento de erro no frontend
- Endpoint de health check
- Uso de `data-testid` em elementos importantes da interface

## Tecnologias utilizadas

### Backend

- Python
- Flask
- Flask-CORS
- Flask-SQLAlchemy
- SQLite

### Frontend

- HTML
- CSS
- JavaScript

### Outros

- GitHub
- Variáveis de ambiente com `.env.example`
- `.gitignore` para evitar envio de arquivos sensíveis

## Estrutura do projeto

```txt
lesson-plan-manager/
│
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
│
├── .gitignore
└── README.md
