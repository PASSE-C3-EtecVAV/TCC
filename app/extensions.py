import MySQLdb.cursors


def init_db(mysql):

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute(""" CREATE TABLE IF NOT EXISTS `usuarios` (
                                                                    `id` INT(11) NOT NULL AUTO_INCREMENT,
                                                                    `nome` VARCHAR(100) NOT NULL,
                                                                    `email` VARCHAR(100) NOT NULL,
                                                                    `senha` VARCHAR(255) NOT NULL,
                                                                    `tipo` ENUM('aluno','professor','coordenacao','prof_coorde') NOT NULL,
                                                                    PRIMARY KEY (`id`),
                                                                    UNIQUE KEY `email` (`email`)
                                                                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci AUTO_INCREMENT=2; """)
        
    cursor.execute(""" CREATE TABLE IF NOT EXISTS `turmas` (
                                                                    `id` INT(11) NOT NULL AUTO_INCREMENT,
                                                                    `nome` VARCHAR(6) NOT NULL,
                                                                    PRIMARY KEY (`id`)
                                                                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci AUTO_INCREMENT=9; """)
        
    cursor.execute(""" CREATE TABLE IF NOT EXISTS `disciplinas` (
                                                                    `id` INT(11) NOT NULL AUTO_INCREMENT,
                                                                    `nome` VARCHAR(50) NOT NULL,
                                                                    PRIMARY KEY (`id`)
                                                                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci AUTO_INCREMENT=18; """)
        
    cursor.execute(""" CREATE TABLE IF NOT EXISTS `arquivos` (
                                                                    `id` INT(11) NOT NULL AUTO_INCREMENT,
                                                                    `professor_id` INT(11) NOT NULL,
                                                                    `turma_id` INT(11) NOT NULL,
                                                                    `disciplina_id` INT(11) NOT NULL,
                                                                    `nome_original` VARCHAR(255) NOT NULL,
                                                                    `nome_arquivo` VARCHAR(255) NOT NULL,
                                                                    `data_upload` DATETIME DEFAULT CURRENT_TIMESTAMP(),
                                                                    PRIMARY KEY (`id`),
                                                                    KEY `professor_id` (`professor_id`),
                                                                    KEY `turma_id` (`turma_id`),
                                                                    KEY `disciplina_id` (`disciplina_id`),
                                                                    CONSTRAINT `arquivos_ibfk_1` FOREIGN KEY (`professor_id`) REFERENCES `usuarios` (`id`),
                                                                    CONSTRAINT `arquivos_ibfk_2` FOREIGN KEY (`turma_id`) REFERENCES `turmas` (`id`),
                                                                    CONSTRAINT `arquivos_ibfk_3` FOREIGN KEY (`disciplina_id`) REFERENCES `disciplinas` (`id`)
                                                                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci AUTO_INCREMENT=10; """)
        
    cursor.execute(""" CREATE TABLE IF NOT EXISTS `atividades` (
                                                                    `id` INT(11) NOT NULL AUTO_INCREMENT,
                                                                    `professor_id` INT(11) DEFAULT NULL,
                                                                    `disciplina_id` INT(11) DEFAULT NULL,
                                                                    `turma_id` INT(11) DEFAULT NULL,
                                                                    `titulo` VARCHAR(100) NOT NULL,
                                                                    `descricao` TEXT DEFAULT NULL,
                                                                    `arquivo` VARCHAR(255) DEFAULT NULL,
                                                                    `data_criacao` DATETIME DEFAULT CURRENT_TIMESTAMP(),
                                                                    `data_atraso` DATETIME NOT NULL,
                                                                    `data_encerramento` DATETIME NOT NULL,
                                                                    PRIMARY KEY (`id`),
                                                                    KEY `professor_id` (`professor_id`),
                                                                    KEY `disciplina_id` (`disciplina_id`),
                                                                    KEY `turma_id` (`turma_id`),
                                                                    CONSTRAINT `atividades_ibfk_1` FOREIGN KEY (`professor_id`) REFERENCES `usuarios` (`id`),
                                                                    CONSTRAINT `atividades_ibfk_2` FOREIGN KEY (`disciplina_id`) REFERENCES `disciplinas` (`id`),
                                                                    CONSTRAINT `atividades_ibfk_3` FOREIGN KEY (`turma_id`) REFERENCES `turmas` (`id`)
                                                                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci AUTO_INCREMENT=18; """)
        
    cursor.execute(""" 
                                                                    CREATE TABLE IF NOT EXISTS `entregas` (
                                                                    `id` INT(11) NOT NULL AUTO_INCREMENT,
                                                                    `atividade_id` INT(11) DEFAULT NULL,
                                                                    `aluno_id` INT(11) DEFAULT NULL,
                                                                    `arquivo` VARCHAR(255) DEFAULT NULL,
                                                                    `data_entrega` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(),
                                                                    `texto` TEXT DEFAULT NULL,
                                                                    `nome_arquivo` VARCHAR(255) DEFAULT NULL,
                                                                    `anotacao` TEXT DEFAULT NULL,
                                                                    PRIMARY KEY (`id`),
                                                                    KEY `atividade_id` (`atividade_id`),
                                                                    KEY `aluno_id` (`aluno_id`),
                                                                    CONSTRAINT `entregas_ibfk_1` FOREIGN KEY (`atividade_id`) REFERENCES `atividades` (`id`),
                                                                    CONSTRAINT `entregas_ibfk_2` FOREIGN KEY (`aluno_id`) REFERENCES `usuarios` (`id`)
                                                                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci AUTO_INCREMENT=21; """)
        
    cursor.execute(""" CREATE TABLE IF NOT EXISTS `postagens` (
                                                                    `id` INT(11) NOT NULL AUTO_INCREMENT,
                                                                    `titulo` VARCHAR(100) NOT NULL,
                                                                    `conteudo` TEXT NOT NULL,
                                                                    `data` DATETIME DEFAULT CURRENT_TIMESTAMP(),
                                                                    `professor_id` INT(11) NOT NULL,
                                                                    `turma_id` INT(11) NOT NULL,
                                                                    `disciplina_id` INT(11) NOT NULL,
                                                                    `arquivo` VARCHAR(255) DEFAULT NULL,
                                                                    PRIMARY KEY (`id`),
                                                                    KEY `professor_id` (`professor_id`),
                                                                    KEY `turma_id` (`turma_id`),
                                                                    KEY `disciplina_id` (`disciplina_id`),
                                                                    CONSTRAINT `postagens_ibfk_1` FOREIGN KEY (`professor_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
                                                                    CONSTRAINT `postagens_ibfk_2` FOREIGN KEY (`turma_id`) REFERENCES `turmas` (`id`) ON DELETE CASCADE,
                                                                    CONSTRAINT `postagens_ibfk_3` FOREIGN KEY (`disciplina_id`) REFERENCES `disciplinas` (`id`) ON DELETE CASCADE
                                                                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci AUTO_INCREMENT=19; """)
        
    cursor.execute(""" CREATE TABLE IF NOT EXISTS `turmas_disciplinas` (
                                                                    `id` INT(11) NOT NULL AUTO_INCREMENT,
                                                                    `turma_id` INT(11) DEFAULT NULL,
                                                                    `disciplina_id` INT(11) DEFAULT NULL,
                                                                    PRIMARY KEY (`id`),
                                                                    KEY `turma_id` (`turma_id`),
                                                                    KEY `disciplina_id` (`disciplina_id`),
                                                                    CONSTRAINT `turmas_disciplinas_ibfk_1` FOREIGN KEY (`turma_id`) REFERENCES `turmas` (`id`),
                                                                    CONSTRAINT `turmas_disciplinas_ibfk_2` FOREIGN KEY (`disciplina_id`) REFERENCES `disciplinas` (`id`)
                                                                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci AUTO_INCREMENT=20; """)
        
    cursor.execute(""" CREATE TABLE IF NOT EXISTS `usuarios_disciplinas` (
                                                                    `professor_id` INT(11) NOT NULL,
                                                                    `disciplina_id` INT(11) NOT NULL,
                                                                    `turma_id` INT(11) NOT NULL,
                                                                    PRIMARY KEY (`professor_id`,`disciplina_id`,`turma_id`),
                                                                    KEY `disciplina_id` (`disciplina_id`),
                                                                    KEY `turma_id` (`turma_id`),
                                                                    CONSTRAINT `usuarios_disciplinas_ibfk_1` FOREIGN KEY (`professor_id`) REFERENCES `usuarios` (`id`),
                                                                    CONSTRAINT `usuarios_disciplinas_ibfk_2` FOREIGN KEY (`disciplina_id`) REFERENCES `disciplinas` (`id`),
                                                                    CONSTRAINT `usuarios_disciplinas_ibfk_3` FOREIGN KEY (`turma_id`) REFERENCES `turmas` (`id`)
                                                                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci; """)
        
    cursor.execute(""" CREATE TABLE IF NOT EXISTS `usuarios_turmas` (
                                                                    `aluno_id` INT(11) NOT NULL,
                                                                    `turma_id` INT(11) DEFAULT NULL,
                                                                    PRIMARY KEY (`aluno_id`),
                                                                    KEY `turma_id` (`turma_id`),
                                                                    CONSTRAINT `usuarios_turmas_ibfk_1` FOREIGN KEY (`aluno_id`) REFERENCES `usuarios` (`id`),
                                                                    CONSTRAINT `usuarios_turmas_ibfk_2` FOREIGN KEY (`turma_id`) REFERENCES `turmas` (`id`)
                                                                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci; """)
        
    a = cursor.execute("SELECT * FROM `usuarios` WHERE `id` = '1'")
    if(a == 1):
        pass
    else:
        cursor.execute(""" INSERT INTO `usuarios` (`id`, `nome`, `email`, `senha`, `tipo`) VALUES
                                                                    (1, 'Adm', 'adm@adm.com', 'scrypt:32768:8:1$4376UZA9NxEZjdDz$ae8ac6e1eb9492c907a4773e404a736a132caaac18bbc9aaf1e073c7d08a8f8d938a52bd93e89d3c03b34ca5d557d8364f4680f2e64693610a90d9863a89fa3a', 'professor') """)
    mysql.connection.commit()
    cursor.close()