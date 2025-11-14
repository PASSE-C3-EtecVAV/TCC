# 📚 P.A.S.S.E – Plataforma de Apoio ao Sistema de Sala de Ensino

[![Status do Projeto](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)](https://github.com/PASSE-C3-EtecVAV/TCC)
![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![Flask](https://img.shields.io/badge/framework-Flask-orange.svg)
![MySQL](https://img.shields.io/badge/banco-MySQL-lightgrey.svg)
![Licença](https://img.shields.io/badge/licença-GPL--3.0-green.svg)

---

## 📖 Sobre o Projeto

O **P.A.S.S.E** foi desenvolvido como Trabalho de Conclusão de Curso (TCC) no curso Técnico em Desenvolvimento de Sistemas da **ETEC Vasco Antonio Venchiarutti (Centro Paula Souza)**.

É uma alternativa **gratuita, escalável e acessível** ao Microsoft Teams, pensada para otimizar a comunicação, o compartilhamento de arquivos e a organização acadêmica em instituições públicas de ensino.

O projeto faz uso da AWS (Amazon Web Services) na camada Free Tier, permitindo que sua execução e armazenamento sejam gratuitos dentro dos limites do plano educacional e promocional oferecido pela plataforma.

---

## ✨ Benefícios

- **Baixo custo** → baseado em tecnologias gratuitas ou open source  
- **Acessibilidade** → interface responsiva em qualquer dispositivo  
- **Escalabilidade** → suporte para nuvem e armazenamento distribuído  
- **Foco educacional** → funcionalidades ajustadas à realidade escolar  

---

## 🔍 Funcionalidades

- Sistema de **login diferenciado** para alunos, professores e coordenadores  
- **Gerenciamento de turmas e disciplinas** com vínculo entre usuários  
- **Postagens com anexos** (documentos, imagens, PDFs)  
- **Atividades** com envio, prazos, feedback e controle de entregas  
- **Gerenciamento de arquivos** por disciplina/turma  
- **Painel administrativo** para coordenadores e gestores  

---

## ⚙️ Tecnologias Utilizadas

| Componente        | Tecnologia                     |
|-------------------|--------------------------------|
| **Back-end**      | Python (Flask)                 |
| **Banco de Dados**| MySQL                          |
| **Front-end**     | HTML5, CSS3, JavaScript, Bootstrap |
| **Armazenamento** | Suporte em nuvem               |
| **Controle de Versão** | Git + GitHub              |

---

## 🚀 Como Executar

### 🔧 Pré-requisitos
- Python 3.x  
- MySQL  
- Git  

### 📌 Passos

1. Clone o repositório  
   ```bash
   git clone https://github.com/PASSE-C3-EtecVAV/TCC.git
   cd TCC
   ```

2. Crie e ative o ambiente virtual  
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. Instale as dependências  
   ```bash
   pip install -r requirements.txt
   ```

4. Configure o banco de dados
   - Crie o Banco de Dados com nome "tcc"
   - O Banco de Dados já é configurado pelo proprio sistema!

6. Execute a aplicação  
   ```bash
   flask run.py
   ```
   E acesse o Link que aparece no Terminal
---

## 👥 Desenvolvedores

- Abner Peixoto Santana Brochado  
- Bruno Honorato Passos  
- Gustavo Soares Araujo Evangelista dos Anjos  
- Vitor Alberto Gonçalves Brandt  

---

## 📝 Licença

Este projeto está sob a licença **GPL-3.0**.  
Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 💡 Motivação e Impacto

Com os sucessivos cortes no orçamento da educação pública (mais de **R$ 10 bilhões** entre 2021 e 2025), ferramentas comerciais como o Microsoft Teams sofreram severas restrições, impactando professores e alunos.  

O **P.A.S.S.E** surge como uma **alternativa econômica** e **funcional**, aproveitando tecnologias open source e infraestrutura em nuvem para **garantir acessibilidade, escalabilidade e eficiência** no ensino público brasileiro.
