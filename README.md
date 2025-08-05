# 📚 P.A.S.S.E (Plataforma de Apoio ao Sistema de Sala de Ensino)

Uma alternativa gratuita e escalável ao Microsoft Teams para instituições de ensino.

## 🧩 Sobre o Projeto

Este projeto foi desenvolvido como Trabalho de Conclusão de Curso (TCC) do curso Técnico em Desenvolvimento de Sistemas na ETEC Vasco Antonio Venchiarutti. A plataforma tem como objetivo principal facilitar a comunicação e o compartilhamento de arquivos entre alunos e professores, especialmente em contextos educacionais com limitações orçamentárias.

Com base em tecnologias gratuitas e de fácil manutenção, o sistema permite que professores compartilhem atividades por turma e disciplina, promovendo uma organização eficiente e acessível dentro das instituições públicas de ensino.

> 💡 **Motivação:** Diante dos sucessivos cortes no orçamento da educação pública no Brasil, a proposta surge como uma alternativa de baixo custo ao Microsoft Teams, sem comprometer a usabilidade ou funcionalidade.

---

## ⚙️ Tecnologias Utilizadas

- **Back-end:** [Flask](https://flask.palletsprojects.com/) (Python)
- **Banco de Dados:** [MySQL](https://www.mysql.com/) com armazenamento em nuvem
- **Front-end:** HTML5, CSS3 e JavaScript

---

## 🔐 Funcionalidades

- Sistema de login para alunos e professores
- Cadastro e gerenciamento de turmas e disciplinas
- Upload e download de arquivos organizados por matéria (alunos) e por turma (professores)
- Interface intuitiva com design responsivo
- Integração com banco de dados relacional em nuvem
- Organização eficiente de conteúdo pedagógico

---

## 🧱 Estrutura do Projeto

```
/app
│   ├── static/        # Arquivos estáticos (CSS, JS, imagens)
│   ├── templates/     # Páginas HTML (Jinja2)
│   ├── routes/        # Arquivos com rotas Flask
│   ├── models/        # Modelos e conexões com o banco MySQL
│   └── app.py         # Arquivo principal do Flask
/config
│   └── db_config.py   # Configuração da conexão com banco
README.md
requirements.txt
```

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

## 📌 Observações

Este sistema foi desenvolvido com foco nas necessidades de escolas públicas do Estado de São Paulo, especialmente as vinculadas ao **Centro Paula Souza (CPS)**, buscando oferecer uma alternativa funcional diante da limitação de ferramentas comerciais como o Microsoft Teams.

---
