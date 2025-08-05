# 📚 P.A.S.S.E – Plataforma de Apoio ao Sistema de Sala de Ensino

![Status](https://img.shields.io/badge/status-active-success.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![Flask](https://img.shields.io/badge/Flask-Framework-red.svg)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange.svg)

Uma alternativa gratuita, escalável e acessível ao Microsoft Teams para instituições de ensino público, desenvolvida para otimizar a comunicação e o compartilhamento de arquivos entre professores e alunos.

---

## 🧩 Sobre o Projeto

O **P.A.S.S.E** foi desenvolvido como parte do **Trabalho de Conclusão de Curso (TCC)** do curso **Técnico em Desenvolvimento de Sistemas** da **ETEC Vasco Antonio Venchiarutti (Centro Paula Souza)**.  

A plataforma foi projetada para enfrentar as dificuldades causadas pelos cortes orçamentários na educação pública no Brasil, que impactaram diretamente o uso de ferramentas pagas como o Microsoft Teams. Nosso objetivo é oferecer uma **solução gratuita, funcional e de fácil manutenção**, capaz de atender às necessidades de comunicação e organização pedagógica de escolas públicas.

---

## ✨ Principais Benefícios

- **Baixo custo:** solução gratuita que elimina a necessidade de licenças caras.
- **Acessibilidade:** interface intuitiva e responsiva, acessível de qualquer dispositivo com internet.
- **Escalabilidade:** uso de computação em nuvem para maior capacidade de armazenamento.
- **Foco educacional:** projetado especificamente para ambientes escolares, com recursos de turmas, disciplinas, postagens e atividades.

---

## 🔐 Funcionalidades

- **Sistema de Login:** acesso diferenciado para professores, coordenadores e alunos.
- **Gerenciamento de Turmas e Disciplinas:** cadastro e vinculação de usuários.
- **Postagens:** criação, edição e exclusão de postagens com anexos para comunicação interna.
- **Atividades:** envio, entrega e gerenciamento de atividades com prazos e feedback dos professores.
- **Controle de Entregas:** professores podem visualizar, anotar e gerenciar as atividades entregues.
- **Gerenciamento de Arquivos:** upload e download organizado por turma e disciplina.
- **Painel Administrativo:** para gestão de usuários, disciplinas e turmas.

---

## ⚙️ Tecnologias Utilizadas

- **Back-end:** [Flask](https://flask.palletsprojects.com/) (Python)
- **Banco de Dados:** [MySQL](https://www.mysql.com/) (com suporte para nuvem)
- **Front-end:** HTML5, CSS3, JavaScript, [Bootstrap](https://getbootstrap.com/)
- **Armazenamento:** Computação em nuvem para maior disponibilidade e escalabilidade
- **Controle de Versão:** [Git](https://git-scm.com/) e [GitHub](https://github.com)

---

## 🧱 Estrutura do Projeto

```
/app
│   ├── static/        # Arquivos estáticos (CSS, JS, imagens, uploads)
│   ├── templates/     # Páginas HTML (Flask/Jinja2)
│   ├── routes/        # Rotas Flask e controladores
│   ├── models/        # Modelos e conexões com banco de dados
│   └── app.py         # Arquivo principal do Flask
/config
│   └── db_config.py   # Configurações de conexão com MySQL
README.md
requirements.txt
```

---

## 🚀 Instalação e Execução

### **Pré-requisitos**

- Python 3.x
- MySQL Server
- Git

### **Passos**

1. Clone o repositório:
   ```bash
   git clone https://github.com/seuusuario/passe.git
   cd passe
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure o banco de dados:
   - Crie o banco MySQL e ajuste o arquivo `config/db_config.py` com suas credenciais.
   - Importe o script SQL disponível em `/db/tcc.sql`.

5. Execute o projeto:
   ```bash
   flask run
   ```

6. Acesse o sistema em: (Achar um locla para hospedagem)

---

## 👨‍🏫 Desenvolvedores

- Abner Peixoto Santana Brochado  
- Bruno Honorato Passos  
- Gustavo Soares Araujo Evangelista dos Anjos  
- Vitor Alberto Gonçalves Brandt  

---

## 📄 Licença

Este projeto está sob a licença [MIT](LICENSE).

---

## 💡 Motivação e Impacto

Com os sucessivos cortes no orçamento da educação pública (mais de **R$ 10 bilhões** entre 2021 e 2025), ferramentas comerciais como o Microsoft Teams sofreram severas restrições, impactando professores e alunos.  

O **P.A.S.S.E** surge como uma **alternativa econômica** e **funcional**, aproveitando tecnologias open source e infraestrutura em nuvem para **garantir acessibilidade, escalabilidade e eficiência** no ensino público brasileiro.
