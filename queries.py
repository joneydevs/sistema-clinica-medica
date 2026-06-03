LISTAR_PACIENTES = """
SELECT
    id,
    nome,
    celular,
    email
FROM paciente
ORDER BY id;
"""

LISTAR_MEDICOS = """
SELECT
    id,
    nome, 
    especialidade,
    email,
    celular
FROM profissional
ORDER BY id;
"""

LISTAR_CONSULTAS = """
SELECT 
    c.id AS ID_consulta, 
    p.nome AS paciente, 
    pr.nome AS médico, 
    c.data_hora AS Data_hora_consulta,
    c.status AS status_consulta 
FROM consulta c 
JOIN paciente p ON c.paciente_id = p.id 
JOIN profissional pr ON c.profissional_id = pr.id 
ORDER BY c.data_hora;
"""

BUSCAR_PACIENTE_POR_NOME = """
SELECT 
    id, 
    nome, 
    celular,
    email 
FROM paciente 
WHERE nome ILIKE %s
ORDER BY id;
"""

BUSCAR_MEDICO_POR_NOME = """
SELECT 
    id, 
    nome, 
    especialidade, 
    email, 
    celular 
FROM profissional 
WHERE nome ILIKE %s
ORDER BY id;
"""


# --- PACIENTES ---
INSERIR_PACIENTE = """
INSERT INTO paciente (nome, email, celular) 
VALUES (%s, %s, %s);
"""

# --- MÉDICOS / PROFISSIONAIS ---
INSERIR_PROFISSIONAL = """
INSERT INTO profissional (nome, especialidade, email, celular) 
VALUES (%s, %s, %s, %s);
"""

# --- CONSULTAS ---
BUSCAR_PROFISSIONAIS_POR_ESPECIALIDADE = """
SELECT id, nome, especialidade 
FROM profissional 
WHERE especialidade ILIKE %s;
"""

BUSCAR_DETALHES_PROFISSIONAL = """
SELECT nome, especialidade 
FROM profissional 
WHERE id = %s;
"""

VERIFICAR_OCUPACAO_MEDICO_30_DIAS = """
SELECT
    data_hora::date,
    COUNT(*)
FROM consulta
WHERE profissional_id = %s
    AND data_hora::date BETWEEN current_date AND current_date + 30
    AND status != 'CANCELADA'
GROUP BY data_hora::date;
"""

VERIFICAR_HORARIO_DISPONIVEL = """
SELECT id FROM consulta
WHERE profissional_id = %s
    AND data_hora = %s
    AND status != 'CANCELADA';
"""

BUSCAR_PACIENTES_POR_APROXIMACAO = """
SELECT id, nome 
FROM paciente 
WHERE nome ILIKE %s 
ORDER BY id;
"""

INSERIR_CONSULTA = """
INSERT INTO consulta (paciente_id, profissional_id, data_hora, status) 
VALUES (%s, %s, %s, 'MARCADA');
"""

BUSCAR_RESUMO_AGENDAMENTO = """
SELECT 
    p.nome,
    pr.nome,
    pr.especialidade
FROM consulta c
JOIN paciente p ON p.id = c.paciente_id
JOIN profissional pr ON pr.id = c.profissional_id
WHERE c.paciente_id = %s 
    AND c.profissional_id = %s 
    AND c.data_hora = %s;
"""

BUSCAR_PACIENTE_POR_ID = """
SELECT 
    nome, 
    email, 
    celular 
FROM paciente 
WHERE id = %s;
"""

DELETAR_PACIENTE_POR_ID = """
DELETE FROM paciente WHERE id = %s;
"""

BUSCAR_PROFISSIONAL_POR_ID = """
SELECT 
    id, 
    nome, 
    especialidade, 
    email, 
    celular 
FROM profissional 
WHERE id = %s
ORDER BY id;
"""

DELETAR_PROFISSIONAL_POR_ID = """
DELETE 
FROM profissional 
WHERE id = %s;
"""

BUSCAR_CONSULTAS_POR_NOME_PACIENTE = """
SELECT
    c.id, 
    p.nome,
    pr.nome,
    pr.especialidade,
    c.data_hora,
    c.status
FROM consulta c
JOIN paciente p ON p.id = c.paciente_id
JOIN profissional pr ON pr.id = c.profissional_id
WHERE p.nome ILIKE %s;
"""

UPDATE_CONSULTA_POR_ID = """
UPDATE consulta
SET status = 'CANCELADA'
WHERE id = %s;
"""

UPDATE_PACIENTE_POR_ID = """
UPDATE paciente 
SET nome = %s, email = %s, celular = %s 
WHERE id = %s;
"""


UPDATE_PROFISSIONAL_POR_ID = """
UPDATE profissional 
SET nome = %s, especialidade = %s, email = %s, celular = %s 
WHERE id = %s;
"""