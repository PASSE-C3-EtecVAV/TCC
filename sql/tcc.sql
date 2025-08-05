-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 01/07/2025 às 20:48
-- Versão do servidor: 10.4.32-MariaDB
-- Versão do PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `tcc`
--

-- --------------------------------------------------------

--
-- Estrutura para tabela `atividades`
--

CREATE TABLE `atividades` (
  `id` int(11) NOT NULL,
  `professor_id` int(11) DEFAULT NULL,
  `disciplina_id` int(11) DEFAULT NULL,
  `turma_id` int(11) DEFAULT NULL,
  `titulo` varchar(100) NOT NULL,
  `descricao` text DEFAULT NULL,
  `arquivo` varchar(255) DEFAULT NULL,
  `data_criacao` datetime DEFAULT current_timestamp(),
  `data_atraso` datetime NOT NULL,
  `data_encerramento` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `disciplinas`
--

CREATE TABLE `disciplinas` (
  `id` int(11) NOT NULL,
  `nome` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `entregas`
--

CREATE TABLE `entregas` (
  `id` int(11) NOT NULL,
  `atividade_id` int(11) DEFAULT NULL,
  `aluno_id` int(11) DEFAULT NULL,
  `arquivo` varchar(255) DEFAULT NULL,
  `data_entrega` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `turmas`
--

CREATE TABLE `turmas` (
  `id` int(11) NOT NULL,
  `nome` varchar(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `turmas`
--

INSERT INTO `turmas` (`id`, `nome`) VALUES
(1, '1C¹'),
(2, '1C²');

-- --------------------------------------------------------

--
-- Estrutura para tabela `turmas_disciplinas`
--

CREATE TABLE `turmas_disciplinas` (
  `id` int(11) NOT NULL,
  `turma_id` int(11) DEFAULT NULL,
  `disciplina_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nome` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `senha` varchar(255) NOT NULL,
  `tipo` enum('aluno','professor','coordenacao','prof_coorde') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `usuarios`
--

INSERT INTO `usuarios` (`id`, `nome`, `email`, `senha`, `tipo`) VALUES
(2, 'Adm', 'adm@adm.com', 'scrypt:32768:8:1$MlIiPY1qlsddxDpR$f884d53525089814546c24f805c4f447f629f6581b8fd7e4bd6ef568f31871b2cbb5d22bdd1d1e7bc1be8cc06d5d21d8be49b658ef210650e246f2e46b254ebc', 'coordenacao'),
(3, 'Gustavo Soares Araujo Evangelista dos Anjos', 'gustavo.anjos14@etec.sp.gov.br', 'scrypt:32768:8:1$mIk86aPka1A6sFmC$3bcaf648300ac6a899e15c513848d6cbff8fb0f1d9163dcff12b4550f1dbeed6ef', 'aluno'),
(4, 'Heloize Silva de Paula', 'heloize.paula@etec.sp.gov.br', 'scrypt:32768:8:1$qIwzfzTd5Rb3pQNS$0e06e6d94417dcce977a7360bc056a83b38224b011b1c0ce6c40d083b470548b8f', 'aluno'),
(5, 'Bruno Honorato Passos', 'bruno.passos@etec.sp.gov.br', 'scrypt:32768:8:1$5hJ9EkzgHkYiaqsE$b726d1c692c58ef13619ad4ad9dc81f30e30f3760229770ce9e290315c491486ac', 'aluno'),
(6, 'Madureira', 'madureira.madu@etec.sp.gov.br', 'scrypt:32768:8:1$nN2JAvVAvE7QmzHz$c1085bdba0e97d9f0201ccb48659854e3d9d9718049b156e5021359f42661c89fd301acb5e3c18919ac94cf9428237537013ba1222163fa32d0371f5a5217064', 'coordenacao'),
(7, 'Supervisor', 'supervisor@supervisor.com', 'scrypt:32768:8:1$1PPQgZxIpNIxrLP9$2b320f257ac1cfe47e99d9575238549c3f5a0f79d9de220680af5df88c3b7ac78a1285a1aca045accb2f113bf2776a34b5ef274e3548d4bd598af8fbefa9f23b', 'coordenacao'),
(8, 'Ronildo', 'ronildo@etec.sp.gov.br', 'scrypt:32768:8:1$BAerhjDqCXEPFYZ8$c42eb64283536ad19b41bedd9f3f1eaa225b45a797568ae3d6af45a6fd47091aaaf61729310db62d39b8e618ba6636a91519338e6fbc77d7a750c671e66a4111', 'prof_coorde');

-- --------------------------------------------------------

--
-- Estrutura para tabela `usuarios_disciplinas`
--

CREATE TABLE `usuarios_disciplinas` (
  `professor_id` int(11) NOT NULL,
  `disciplina_id` int(11) NOT NULL,
  `turma_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `usuarios_turmas`
--

CREATE TABLE `usuarios_turmas` (
  `aluno_id` int(11) NOT NULL,
  `turma_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `usuarios_turmas`
--

INSERT INTO `usuarios_turmas` (`aluno_id`, `turma_id`) VALUES
(4, 1),
(5, 1),
(3, 2);

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `atividades`
--
ALTER TABLE `atividades`
  ADD PRIMARY KEY (`id`),
  ADD KEY `professor_id` (`professor_id`),
  ADD KEY `disciplina_id` (`disciplina_id`),
  ADD KEY `turma_id` (`turma_id`);

--
-- Índices de tabela `disciplinas`
--
ALTER TABLE `disciplinas`
  ADD PRIMARY KEY (`id`);

--
-- Índices de tabela `entregas`
--
ALTER TABLE `entregas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `atividade_id` (`atividade_id`),
  ADD KEY `aluno_id` (`aluno_id`);

--
-- Índices de tabela `turmas`
--
ALTER TABLE `turmas`
  ADD PRIMARY KEY (`id`);

--
-- Índices de tabela `turmas_disciplinas`
--
ALTER TABLE `turmas_disciplinas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `turma_id` (`turma_id`),
  ADD KEY `disciplina_id` (`disciplina_id`);

--
-- Índices de tabela `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Índices de tabela `usuarios_disciplinas`
--
ALTER TABLE `usuarios_disciplinas`
  ADD PRIMARY KEY (`professor_id`,`disciplina_id`,`turma_id`),
  ADD KEY `disciplina_id` (`disciplina_id`),
  ADD KEY `turma_id` (`turma_id`);

--
-- Índices de tabela `usuarios_turmas`
--
ALTER TABLE `usuarios_turmas`
  ADD PRIMARY KEY (`aluno_id`),
  ADD KEY `turma_id` (`turma_id`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `atividades`
--
ALTER TABLE `atividades`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `disciplinas`
--
ALTER TABLE `disciplinas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `entregas`
--
ALTER TABLE `entregas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `turmas`
--
ALTER TABLE `turmas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de tabela `turmas_disciplinas`
--
ALTER TABLE `turmas_disciplinas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Restrições para tabelas despejadas
--

--
-- Restrições para tabelas `atividades`
--
ALTER TABLE `atividades`
  ADD CONSTRAINT `atividades_ibfk_1` FOREIGN KEY (`professor_id`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `atividades_ibfk_2` FOREIGN KEY (`disciplina_id`) REFERENCES `disciplinas` (`id`),
  ADD CONSTRAINT `atividades_ibfk_3` FOREIGN KEY (`turma_id`) REFERENCES `turmas` (`id`);

--
-- Restrições para tabelas `entregas`
--
ALTER TABLE `entregas`
  ADD CONSTRAINT `entregas_ibfk_1` FOREIGN KEY (`atividade_id`) REFERENCES `atividades` (`id`),
  ADD CONSTRAINT `entregas_ibfk_2` FOREIGN KEY (`aluno_id`) REFERENCES `usuarios` (`id`);

--
-- Restrições para tabelas `turmas_disciplinas`
--
ALTER TABLE `turmas_disciplinas`
  ADD CONSTRAINT `turmas_disciplinas_ibfk_1` FOREIGN KEY (`turma_id`) REFERENCES `turmas` (`id`),
  ADD CONSTRAINT `turmas_disciplinas_ibfk_2` FOREIGN KEY (`disciplina_id`) REFERENCES `disciplinas` (`id`);

--
-- Restrições para tabelas `usuarios_disciplinas`
--
ALTER TABLE `usuarios_disciplinas`
  ADD CONSTRAINT `usuarios_disciplinas_ibfk_1` FOREIGN KEY (`professor_id`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `usuarios_disciplinas_ibfk_2` FOREIGN KEY (`disciplina_id`) REFERENCES `disciplinas` (`id`),
  ADD CONSTRAINT `usuarios_disciplinas_ibfk_3` FOREIGN KEY (`turma_id`) REFERENCES `turmas` (`id`);

--
-- Restrições para tabelas `usuarios_turmas`
--
ALTER TABLE `usuarios_turmas`
  ADD CONSTRAINT `usuarios_turmas_ibfk_1` FOREIGN KEY (`aluno_id`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `usuarios_turmas_ibfk_2` FOREIGN KEY (`turma_id`) REFERENCES `turmas` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
