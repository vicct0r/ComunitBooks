# Enunciado: Sistema de Biblioteca Comunitária

## 📖 Objetivo
Desenvolver uma plataforma onde membros de uma comunidade possam compartilhar livros de forma organizada, com regras flexíveis que incentivem a colaboração e garantam a integridade dos acervos pessoais.

## 🏷️ Regras de Negócio

### 1. Cadastro de Livros
- Todo usuário cadastrado pode adicionar livros ao sistema
- Informações obrigatórias:
  - Título (mínimo 3 caracteres)
  - Autor (mínimo 3 caracteres)
  - Estado de conservação (Novo/Usado/Danificado)
- O sistema deve:
  - Criar identificadores únicos e legíveis para cada livro
  - Classificar automaticamente por gênero com base no título

### 2. Empréstimos
- Prazo padrão: 14 dias
- Limites:
  - Máximo de 3 livros por usuário simultaneamente
  - 1 renovação permitida (+7 dias)
- Restrições:
  - Doadores podem definir regras especiais para seus livros
  - Usuários com atrasos superiores a 5 dias ficam bloqueados

### 3. Sistema de Reputação
- Pontos positivos:
  - +2 pontos por livro doado
  - +1 ponto por devolução antecipada
- Pontos negativos:
  - -5 pontos por atraso na devolução
- Benefícios:
  - Acesso a livros exclusivos após atingir 100 pontos
  - Prioridade em listas de espera

### 4. Notificações
- Tipos de alertas:
  1. Aviso de devolução (3 dias antes do prazo)
  2. Confirmação de empréstimo
  3. Disponibilidade de livro desejado
- Canais:
  - E-mail (obrigatório)
  - Telegram (opcional)

### 5. Busca e Recomendações
- Filtros obrigatórios:
  - Por título/autor
  - Por gênero literário
  - Por disponibilidade
- Sistema de sugestões:
  - Baseado em livros já emprestados
  - "Quem pegou X também pegou Y"

## 🎯 Expectativas do Cliente
"Quero que os usuários sintam que estão pegando livros emprestados de amigos, não de uma biblioteca formal. O sistema deve ser simples o suficiente para minha avó usar, mas inteligente o bastante para evitar abusos."

## 📆 Entregas Esperadas
1. **Versão Inicial (MVP):**
   - Cadastro e empréstimo básico de livros
   - Sistema de reputação simplificado
2. **Versão 2.0:**
   - Integração com mensageiros
   - Clubes de leitura por livro
3. **Versão 3.0:**
   - Mapa de livros disponíveis por proximidade
   - Sistema de trocas além de empréstimos