import pandas as pd
from database_utils import *

COLUNAS_CONSULTAS = {
    "Analitico_Contracheque": "Colunas retornadas: SIGLA_EMPRESA, CHAVE_FOLHA, DESCRICAO_FOLHA, MATRICULA, DATA_ADMISSAO, NOME, DATA_NASCIMENTO, DATA_APOSENTADORIA, CALCULO_APOSENTADORIA, TIPO_APOSENTADORIA, NOME_REGRA, CPF, CPF_INSTITUIDOR, MATRICULA_INSTITUIDOR, NOME_INSTITUIDOR, DATA_OBITO, NOME_SEXO, ESTADO_CIVIL, RACA_COR, NOME_TIPO_SANGUE, IND_CAPACIDADE_TRABALHO, IND_DEF_AUDITIVA, IND_DEF_FISICA, IND_DEF_INTELECTUAL, IND_DEF_MENTAL, IND_DEF_VISUAL, nome_deficiencia, DDD_CEL, CELULAR, DDD, TELEFONE, LOGRADOURO, NUMERO_ENDERECO, BAIRRO_ENDERECO, CIDADE_CIDADE, CEP, COMPLEMENTO_ENDERECO, EMAIL, EMAIL_ALTERNATIVO, CARGO_EFETIVO, ESPECIALIDADE, CARGO_COMISSIONADO, REGIME, DIVISAO, SITUACAO, TIPO_SERVIDOR, ESCOLARIDADE, FORMACAO, PLANO, CLASSE, PADRAO, CLASSE_PADRAO, COD_LOTACAO, LOTACAO, CIDADE_LOTACAO, BRUTO_999997, LIQUIDO_999999",
    "RH": "Colunas retornadas: MATRICULA, FUNCIONARIO, NOME, CPF, SEXO, DIVISAO, SITUACAO, TIPO_FUNCIONARIO, CARGO_EFETIVO, PLANO, REFERENCIA, CLASSE, NIVEL, PADRAO, GRUPO, ESPECIALIDADE, REGIME, DATA_ADMISSAO, DATA_NASCIMENTO, CARGO_COMISSIONADO, ORGAO",
    "Promocao": "Colunas retornadas: ORGAO, MATRICULA, NOME, CPF, PLANO, CARGO_EFETIVO, REFERENCIA, ESPECIALIDADE, DATA_INICIO",
    "Estagiários_Cadastro": " ORGAO, Nome, CPF, MATRICULA, data_nascimento, data_cadastro, INGRESSO, data_fim, data_previ_termino, semestre_inicio, horas_contrato, cod_lotacao, nome_lotacao",
    "Estagiários_em_Folha":"ORGAO, LOTAÇÃO, ESTAGIARIO, MATRICULA, CPF, FACULDADE, CURSO, data_nascimento, INGRESSO, data_fim, cod_lotacao, lotacao, VALOR",
    "Base_de_servidores_para_envio_ao_Picpay": " COD_INSTITUCIONAL, NOME, CPF_PESSOA, DIVISAO, SITUACAO, TIPO_FUNCIONARIO, CARGO_EFETIVO, CARGO_COMISSIONADO, PLANO, REFERENCIA, DATA_CADASTRO,CLASSE, NIVEL, PADRAO, ESPECIALIDADE, REGIME,  DATA_ADMISSAO,   TIPO,   COD_RUBRICA,    NOME_RUBRICA,  VALOR_CALCULADO,   ORGAO,   ID_EMPRESA, SIGLA_EMPRESA,  CHAVE_FOLHA, CATEGORIA_SERVIDOR, DESCRICAO_CATEGORIA_SERVIDOR, DATA_OBITO, NOME_SEXO, BRUTO, LIQUIDO  ",
    "Rubricas": "",
    "Aposentados_Funprev":""
}

CAMPOS_VISIVEIS = {
    "Analitico_Contracheque": ["mes", "ano", "empresa"],
    "Analitico_Prévia": ["mes", "ano", "empresa"],
    "RH": ["empresa"],
    "Promocao": ["empresa"],
    "Rubricas": ["mes", "ano", "empresa"],
    "Rubricas_por_codigo": ["cod_rubrica","mes", "ano", "empresa"],
    "Codigo_Rubrica": ["mes", "ano", "empresa"],
    "Pensionistas_Funprev": ["mes", "ano"],
    "Aposentados_Funprev": ["mes", "ano"],
    "Estagiários_em_Folha": ["mes", "ano", "empresa"],
    "Estagiários_Cadastro": ["mes", "ano", "empresa"],
    "Base_de_servidores_para_envio_ao_Picpay": ["mes", "ano", "empresa"],
}

def consulta_rh(cur, tabelas):
    dfs = []
    for tabela in tabelas:
        query = f"""
                WITH QUERY1 AS (
                    SELECT DISTINCT
                        PV.COD_INSTITUCIONAL AS MATRICULA,
                        F.ID_FUNCIONARIO,
                        HN.NOME,
                        PDC.CPF_PESSOA AS CPF,
                        RS.NOME_SEXO AS SEXO,
                        PD.NOME_DIVISAO AS DIVISAO,
                        PS.NOME_SITUACAO AS SITUACAO,
                        TF.NOME_TIPO_FUNCIONARIO AS TIPO_FUNCIONARIO,
                        CF.NOME_CATEGORIA_FUNCIONAL AS CARGO_EFETIVO,
                        C.NOME_CARREIRA AS PLANO,
                        CR.NOME_REFERENCIA AS REFERENCIA,
                        RCC.NOME_CLASSE AS CLASSE,
                        RCN.NOME_NIVEL AS NIVEL,
                        RCP.NOME_PADRAO AS PADRAO,
                        CG.NOME_GRUPO AS GRUPO,
                        CE.NOME_ESPECIALIDADE AS ESPECIALIDADE,
                        RT.NOME_REGIME AS  REGIME,
                        FI.DATA_POSSE AS DATA_ADMISSAO,
                        P.DATA_NASCIMENTO,
                        FC.NOME_FUNCAO_COMISSIONADA AS CARGO_COMISSIONADO,
                        E.SIGLA_EMPRESA AS ORGAO

                    FROM
                        SW_{tabela}.PESSOA_VINCULO PV
                        JOIN SW_PUBLICO.PESSOA_HISTORICO_NOMES HN ON HN.ID_PESSOA = PV.ID_PESSOA AND HN.DATA_FIM IS NULL
                        JOIN SW_PUBLICO.PESSOA_DOC_CPF PDC ON PDC.ID_PESSOA = PV.ID_PESSOA AND PDC.DATA_BAIXA IS NULL
                        JOIN SW_PUBLICO.PESSOA P ON P.ID_PESSOA = PV.ID_PESSOA
                        LEFT JOIN SW_PUBLICO.RHB_CARACT_FISICA_SEXO RS ON RS.ID_SEXO =  P.ID_SEXO
                        JOIN SW_{tabela}.FUNCIONARIO F ON F.ID_PESSOA_VINCULO = PV.ID_PESSOA_VINCULO
                        LEFT JOIN SW_{tabela}.FUNCIONARIO_PERFIL FP ON FP.ID_FUNCIONARIO = F.ID_FUNCIONARIO AND FP.DATA_FIM IS NULL
                        LEFT JOIN SW_{tabela}.RHB_PERFIL P ON P.ID_PERFIL = FP.ID_PERFIL
                        LEFT JOIN SW_PUBLICO.RHB_PERFIL_DIVISAO PD ON PD.ID_DIVISAO = P.ID_DIVISAO
                        LEFT JOIN SW_PUBLICO.RHB_PERFIL_SITUACAO PS ON PS.ID_SITUACAO = P.ID_SITUACAO
                        LEFT JOIN SW_PUBLICO.RHB_PERFIL_TIPO_FUNCIONARIO TF ON TF.ID_TIPO_FUNCIONARIO = FP.ID_TIPO_FUNCIONARIO
                        JOIN SW_{tabela}.FUNCIONARIO_INGRESSO FI ON FI.ID_FUNCIONARIO = F.ID_FUNCIONARIO
                        JOIN SW_PUBLICO.RHB_INGRESSO_REGIME_TRABALHO RT ON RT.ID_REGIME = FI.ID_REGIME
                        LEFT JOIN SW_{tabela}.FUNCIONARIO_REFERENCIA FR ON FR.ID_FUNCIONARIO = F.ID_FUNCIONARIO AND FR.DATA_TERMINO IS NULL
                        LEFT JOIN SW_{tabela}.RHB_CARREIRA_REFERENCIA CR ON CR.ID_REFERENCIA = FR.ID_REFERENCIA
                        LEFT JOIN SW_{tabela}.RHB_CARREIRA_CLASSE RCC ON RCC.ID_CLASSE = CR.ID_CLASSE
                        LEFT JOIN SW_{tabela}.RHB_CARREIRA_NIVEL RCN ON RCN.ID_NIVEL = CR.ID_NIVEL
                        LEFT JOIN SW_{tabela}.RHB_CARREIRA_PADRAO RCP ON RCP.ID_PADRAO = CR.ID_PADRAO
                        LEFT JOIN SW_{tabela}.RHB_CARREIRA_CATEGORIA_GRUPO CG ON CG.ID_GRUPO = FI.ID_GRUPO
                        LEFT JOIN SW_{tabela}.RHB_CARREIRA_CATEG_FUNCIONAL CF ON CF.ID_CATEGORIA_FUNCIONAL = FR.ID_CATEGORIA_FUNCIONAL
                        LEFT JOIN SW_{tabela}.RHB_CARREIRA C ON C.ID_CARREIRA = CF.ID_CARREIRA
                        LEFT JOIN SW_{tabela}.RHB_CARREIRA_CATEG_ESPECIALID CE ON CE.ID_ESPECIALIDADE = FR.ID_ESPECIALIDADE
                        LEFT JOIN SW_{tabela}.FUNCIONARIO_FUNCAO FF ON FF.ID_FUNCIONARIO = F.ID_FUNCIONARIO AND FF.DATA_FIM IS NULL
                        LEFT JOIN SW_{tabela}.RHB_FC_FUNCAO_COMISSIONADA FC ON FC.ID_FUNCAO_COMISSIONADA = FF.ID_FUNCAO_COMISSIONADA
                        --LEFT JOIN SW_{tabela}.FUNCIONARIO_FUNCAO_NOMEACAO FN ON FN.ID_FUNCIONARIO = F.ID_FUNCIONARIO
                        --LEFT JOIN SW_PUBLICO.NM_VAGA_CARGO_COMISSIONADO CC ON CC.ID_NM_VAGA_CARGO_COMISSIONADO = FN.ID_FUNCAO_COMISSIONADA
                        JOIN SW_PUBLICO.EMPRESA E ON E.SIGLA = '{tabela}'
                    WHERE
                        --RT.ID_REGIME IN (1, 2, 1000003, 1000343)
                        --AND FP.ID_TIPO_FUNCIONARIO in (1,2,1000000,1000380,1000400)
                        --AND PD.ID_DIVISAO in (1000060,1000180,1000160,1000020,1000860,1000030,1000999,1000979,1000799)
                        --AND PS.ID_SITUACAO in (1000103,1000210,1000030,1000029,1000040,1000000,1000031,1000032,1000033,1000034,1000035,1000060,1000061,1000062,1000037,1000038,1000039,1000002,1000003,1000004,1000020,1000021,1000022,1000200,1000320,1001200,1000760,1000681,1000840,1000780,1000140,1000240,1000560,1000640,1000720,1000740,1000800,1000180,1000181,1000700)
                        NOT PV.COD_INSTITUCIONAL IS NULL
                       
                )
                SELECT DISTINCT MATRICULA, ID_FUNCIONARIO,NOME, CPF, SEXO, DIVISAO, SITUACAO, TIPO_FUNCIONARIO, CARGO_EFETIVO, PLANO, REFERENCIA, CLASSE, NIVEL, PADRAO, GRUPO, ESPECIALIDADE, REGIME, DATA_ADMISSAO, DATA_NASCIMENTO, CARGO_COMISSIONADO, ORGAO, ID_EMPRESA FROM QUERY1

        """
        cur.execute(query)
        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        dfs.append(pd.DataFrame(rows, columns=columns))
    return pd.concat(dfs, ignore_index=True)

def consulta_analitico(cur, mes, ano, tabelas):
    dfs = []
    for tabela in tabelas:
        query = f"""
                            WITH CTE AS (
                                    SELECT                                
                                        E.SIGLA_EMPRESA,        
                                        F.CHAVE_FOLHA,
                                        F.DESCRICAO AS DESCRICAO_FOLHA,
                                        FC.COD_INSTITUCIONAL AS MATRICULA,
                                        FC.DATA_ADMISSAO,   
                                        FC.DATA_APOSENTADORIA AS DATA_APOSENTADORIA,
                                        FC.CALCULO_APOSENTADORIA,
                                        PRA.NOME_APOSENTADORIA AS TIPO_APOSENTADORIA,
                                        PRPR.NOME_REGRA,
                                        FC.NOME,
                                        FC.DATA_NASCIMENTO,
                                        FC.CPF_PESSOA AS CPF,
                                        FC.CPF_INSTITUIDOR,
                                        FC.MATRICULA_INSTITUIDOR,
                                        FC.NOME_INSTITUIDOR,
                                        PP.DATA_OBITO,
                                        RS.NOME_SEXO,
                                        PRIPC.nome_estado_civil AS ESTADO_CIVIL,
                                        CFRC.NOME_RACA_COR AS RACA_COR,
                                        RCFFR.NOME_TIPO_SANGUE,
                                        PCF.IND_CAPACIDADE_TRABALHO,
                                        PCF.IND_DEF_AUDITIVA,
                                        PCF.IND_DEF_FISICA,
                                        PCF.IND_DEF_INTELECTUAL,
                                        PCF.IND_DEF_MENTAL,
                                        PCF.IND_DEF_VISUAL,                         
                                        RCFD.nome_deficiencia, 
                                        PPEN.ddd_celular  AS DDD_CEL,
                                        PPEN.celular AS CELULAR, 
                                        PPEN.ddd AS DDD,
                                        PPEN.telefone_residencia AS TELEFONE, 
                                        PPEN.LOGRADOURO,
                                        PPEN.NUMERO_ENDERECO,
                                        PPEN.BAIRRO_ENDERECO,
                                        PPEN.CIDADE_CIDADE,
                                        PPEN.CEP,
                                        PPEN.COMPLEMENTO_ENDERECO,            
                                        PP.EMAIL,
                                        PP.EMAIL_ALTERNATIVO,
                                        --FI.JORNADA_DIARIA,
                                        --FI.JORNADA_SEMANAL,
                                        --FI.JORNADA_MENSAL,
                                        COALESCE(FC.CARGO, CF.NOME_CATEGORIA_FUNCIONAL) AS CARGO_EFETIVO,
                                            CASE WHEN FC.COD_ESPECIALIDADE IS NOT NULL THEN FC.COD_ESPECIALIDADE || ' - ' || FC.ESPECIALIDADE END AS ESPECIALIDADE,
                                        COALESCE(FC.FUNCAO, C.NOME_FUNCAO_COMISSIONADA) AS CARGO_COMISSIONADO,
                                        FC.REGIME AS REGIME,
                                        RPD.nome_divisao AS DIVISAO,
                                        RPS.nome_situacao AS SITUACAO,
                                        CASE
                                            WHEN FC.CATEGORIA IS NOT NULL THEN FC.CATEGORIA
                                            ELSE PTF.nome_tipo_funcionario
                                        END AS TIPO_SERVIDOR,
                                        --PECT.codigo AS COD_CATEGORIA,
                                        --PECT.descricao AS DESCRICAO_CATEGORIA,
                                        RIE.nome_escolaridade AS ESCOLARIDADE,
                                        RIC.nome_curso AS FORMACAO,
                                        FC.PLANO,
                                        FC.COD_CLASSE AS CLASSE,
                                        FC.COD_PADRAO AS PADRAO,
                                        CR.nome_referencia AS CLASSE_PADRAO,
                                        FC.COD_LOTACAO,
                                        FC.NOME_LOTACAO AS LOTACAO,
                                        M.NOME_MUNICIPIO AS CIDADE_LOTACAO,                                
                                        NVL((SELECT SUM(X.VALOR_CALCULADO) FROM SW_{tabela}.FOLHA_FICHA_FINANCEIRA X WHERE X.ID_FOLHA_FUNCIONARIO = FC.ID_FOLHA_FUNCIONARIO AND X.ID_RUBRICA IN (51027)), 0) AS BRUTO_999997,
                                        NVL((SELECT SUM(X.VALOR_CALCULADO) FROM SW_{tabela}.FOLHA_FICHA_FINANCEIRA X WHERE X.ID_FOLHA_FUNCIONARIO = FC.ID_FOLHA_FUNCIONARIO AND X.ID_RUBRICA IN (51025)), 0) AS LIQUIDO_999999,
                                        ROW_NUMBER() OVER (PARTITION BY FC.COD_INSTITUCIONAL, F.CHAVE_FOLHA ORDER BY FC.NOME) AS RN
                                    FROM 
                                        SW_{tabela}.FOLHA_CONTRACHEQUE FC
                                        JOIN SW_{tabela}.FOLHA F ON F.ID_FOLHA = FC.ID_FOLHA
                                        -- JOIN SW_{tabela}.FUNCIONARIO_INGRESSO FI ON FI.ID_FUNCIONARIO = FC.ID_FUNCIONARIO
                                        LEFT JOIN SW_{tabela}.FOLHA_FUNC_PERFIL FP ON FP.ID_FOLHA_FUNCIONARIO = FC.ID_FOLHA_FUNCIONARIO
                                        LEFT JOIN SW_{tabela}.FOLHA_FUNC_REFERENCIA FR ON FR.ID_FOLHA_PERFIL = FP.ID_FOLHA_PERFIL
                                        LEFT JOIN SW_{tabela}.FUNCIONARIO_REFERENCIA R ON R.ID_FUNCIONARIO_REFERENCIA = FR.ID_FUNCIONARIO_REFERENCIA
                                        LEFT JOIN SW_{tabela}.RHB_CARREIRA_CATEG_FUNCIONAL CF ON CF.ID_CATEGORIA_FUNCIONAL = R.ID_CATEGORIA_FUNCIONAL
                                        --LEFT JOIN SW_{tabela}.RHB_CARREIRA_CATEG_ESPECIALID E ON E.ID_ESPECIALIDADE = FI.ID_ESPECIALIDADE
                                        LEFT JOIN SW_{tabela}.FOLHA_FUNC_FUNCAO FF ON FF.ID_FOLHA_PERFIL = FP.ID_FOLHA_PERFIL
                                        LEFT JOIN SW_{tabela}.FUNCIONARIO_FUNCAO FU ON FU.ID_FUNCIONARIO_FUNCAO = FF.ID_FUNCIONARIO_FUNCAO
                                        LEFT JOIN SW_{tabela}.RHB_FC_FUNCAO_COMISSIONADA C ON C.ID_FUNCAO_COMISSIONADA = FU.ID_FUNCAO_COMISSIONADA
                                        LEFT JOIN SW_{tabela}.RHB_LOTACAO L ON L.COD_LOTACAO = FC.COD_LOTACAO
                                        LEFT JOIN SW_PUBLICO.RHB_CEP_MUNICIPIO_IBGE M ON M.ID_MUNICIPIO = L.ID_MUNICIPIO
                                        LEFT JOIN SW_PUBLICO.PESSOA PP ON PP.ID_PESSOA = FC.ID_PESSOA
                                        LEFT JOIN SW_PUBLICO.RHB_CARACT_FISICA_SEXO RS ON RS.ID_SEXO =  PP.ID_SEXO
                                        LEFT JOIN SW_PUBLICO.EMPRESA E ON E.SIGLA ='{tabela}'
                                        LEFT JOIN sw_{tabela}.funcionario_referencia FR ON  FC.ID_FUNCIONARIO = FR.id_funcionario
                                        LEFT JOIN sw_{tabela}.rhb_carreira_referencia CR ON  FR.id_referencia = CR.id_referencia
                                        LEFT JOIN sw_{tabela}.folha_fonte_sefaz FS ON FS.id_codigo_sefaz = F.ID_CODIGO_SEFAZ
                                        --LEFT JOIN sw_publico.rhb_ingresso_regime_trabalho IRG ON IRG.ID_REGIME = FI.ID_REGIME
                                        LEFT JOIN sw_{tabela}.rhb_perfil RP ON FP.ID_PERFIL = RP.ID_PERFIL
                                        LEFT JOIN sw_publico.rhb_perfil_divisao RPD ON RPD.ID_DIVISAO =  RP.ID_DIVISAO
                                        LEFT JOIN sw_publico.rhb_perfil_situacao RPS ON RPS.ID_SITUACAO = RP.ID_SITUACAO
                                        LEFT JOIN sw_publico.pessoa_endereco PPEN ON PPEN.ID_PESSOA = PP.ID_PESSOA
                                        LEFT JOIN sw_publico.rhb_instrucao_escolaridade RIE ON RIE.ID_ESCOLARIDADE = PP.ID_ESCOLARIDADE
                                        LEFT JOIN sw_publico.pessoa_escolaridade PPE ON PPE.ID_PESSOA = PP.ID_PESSOA
                                        LEFT JOIN sw_publico.rhb_instrucao_curso RIC ON RIC.id_curso = PPE.ID_CURSO
                                        LEFT JOIN sw_publico.pessoa_caracteristica_fisica PCF ON PCF.ID_PESSOA = PP.ID_PESSOA
                                        LEFT JOIN sw_publico.rhb_caract_fisica_raca_cor CFRC ON CFRC.id_raca_cor = PCF.id_raca_cor
                                        LEFT JOIN sw_publico.rhb_caract_fisica_fator_rh RCFFR ON RCFFR.id_tipo_sangue = PCF.id_tipo_sangue
                                        LEFT JOIN sw_publico.rhb_caract_fisica_deficiencia RCFD ON RCFD.id_deficiencia = PCF.id_deficiencia
                                        LEFT JOIN sw_publico.pessoa_estado_civil PEC ON PEC.id_pessoa = PP.id_pessoa
                                        LEFT JOIN sw_publico.rhb_inf_pessoal_estado_civil PRIPC ON PRIPC.id_estado_civil = PEC.id_estado_civil
                                        LEFT JOIN sw_{tabela}.rhb_perfil_perfil_tipo_func PPTF ON PPTF.ID_PERFIL = FP.ID_PERFIL
                                        LEFT JOIN sw_publico.rhb_perfil_tipo_funcionario PTF ON PTF.id_tipo_funcionario = PPTF.id_tipo_funcionario
                                        LEFT JOIN sw_{tabela}.func_aposentadoria FA ON FA.ID_FUNCIONARIO = FC.ID_FUNCIONARIO
                                        LEFT JOIN sw_publico.rhb_aposentadoria PRA ON PRA.ID_TIPO_APOSENTADORIA = FA.ID_TIPO_APOSENTADORIA
                                        LEFT JOIN sw_publico.rhb_aposentadoria_regra PRPR ON PRPR.ID_REGRA = FA.id_regra_tipo 
                                        --LEFT JOIN sw_{tabela}.funcionario_perfil FUNP ON FUNP.ID_PERFIL = FP.ID_PERFIL
                                        --LEFT JOIN sw_publico.esb_categoria_trabalhador PECT ON PECT.id_esb_categ_trabalhador = FUNP.id_esb_categ_trabalhador
                                        WHERE 
                                            FC.MES = {mes}
                                            AND FC.ANO = {ano}
                                            AND F.ID_TIPO_FOLHA != 1000003
                                            
                                            
                                    )
                                SELECT 
                                    SIGLA_EMPRESA,        
                                    CHAVE_FOLHA,
                                    DESCRICAO_FOLHA,
                                    MATRICULA,
                                    DATA_ADMISSAO,   
                                    NOME,
                                    DATA_NASCIMENTO,
                                    DATA_APOSENTADORIA,
                                    CALCULO_APOSENTADORIA,
                                    TIPO_APOSENTADORIA,
                                    NOME_REGRA,
                                    CPF,
                                    CPF_INSTITUIDOR,
                                    MATRICULA_INSTITUIDOR,
                                    NOME_INSTITUIDOR,
                                    DATA_OBITO,
                                    NOME_SEXO,
                                    ESTADO_CIVIL,
                                    RACA_COR,
                                    NOME_TIPO_SANGUE,
                                    IND_CAPACIDADE_TRABALHO,
                                    IND_DEF_AUDITIVA,
                                    IND_DEF_FISICA,
                                    IND_DEF_INTELECTUAL,
                                    IND_DEF_MENTAL,
                                    IND_DEF_VISUAL,                         
                                    nome_deficiencia,
                                    DDD_CEL,
                                    CELULAR, 
                                    DDD,
                                    TELEFONE,  
                                    LOGRADOURO,
                                    NUMERO_ENDERECO,
                                    BAIRRO_ENDERECO,
                                    CIDADE_CIDADE,
                                    CEP,
                                    COMPLEMENTO_ENDERECO,                              
                                    EMAIL,
                                    EMAIL_ALTERNATIVO,
                                    --JORNADA_DIARIA,
                                    --JORNADA_SEMANAL,
                                    --JORNADA_MENSAL,
                                    CARGO_EFETIVO,
                                    ESPECIALIDADE,
                                    CARGO_COMISSIONADO,
                                    REGIME,
                                    DIVISAO,
                                    SITUACAO,
                                    TIPO_SERVIDOR,
                                    --COD_CATEGORIA AS CATEGORIA_SERVIDOR,
                                    --DESCRICAO_CATEGORIA AS DESCRICAO_CATEGORIA_SERVIDOR,
                                    ESCOLARIDADE,
                                    FORMACAO,
                                    PLANO,
                                    CLASSE,
                                    PADRAO,
                                    CLASSE_PADRAO,
                                    COD_LOTACAO,
                                    LOTACAO,
                                    CIDADE_LOTACAO,
                                    BRUTO_999997,
                                    LIQUIDO_999999
                                FROM 
                                    CTE
                                WHERE 
                                    RN = 1
                                ORDER BY 
                                    CHAVE_FOLHA, 
                                    NOME
        """
        cur.execute(query)
        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        dfs.append(pd.DataFrame(rows, columns=columns))
    return pd.concat(dfs, ignore_index=True)

def consulta_referencias_promocao(cur, tabelas):
    dfs = []
    for tabela in tabelas:
        query = f"""
                                SELECT DISTINCT
                                    E.SIGLA_EMPRESA AS ORGAO,
                                    PV.COD_INSTITUCIONAL AS MATRICULA,
                                    PP.NOME,
                                    PDC.CPF_PESSOA AS CPF,
                                    RC.nome_carreira AS PLANO,
                                    RCCF.nome_categoria_funcional AS CARGO_EFETIVO,
                                    RCR.nome_referencia,
                                    CCE.nome_especialidade AS ESPECIALIDADE,
                                    FR.DATA_CADASTRO,
                                    FR.data_inicio,
                                    FI.DATA_EXERCICIO AS DATA_ADMISSAO
                                FROM 
                                    sw_{tabela}.pessoa_vinculo PV 
                                    LEFT JOIN sw_{tabela}.funcionario F ON F.id_pessoa_vinculo = PV.id_pessoa_vinculo
                                    LEFT JOIN SW_PUBLICO.PESSOA pp ON pp.ID_PESSOA = PV.ID_PESSOA
                                    LEFT JOIN sw_publico.pessoa_doc_cpf PDC ON PDC.id_pessoa = PV.id_pessoa
                                    LEFT JOIN sw_{tabela}.funcionario_referencia FR ON FR.id_funcionario = F.id_funcionario
                                    LEFT JOIN sw_{tabela}.rhb_carreira_categ_especialid CCE ON CCE.id_especialidade = FR.id_especialidade
                                    LEFT JOIN sw_{tabela}.rhb_carreira RC ON RC.id_carreira = FR.id_carreira
                                    LEFT JOIN sw_{tabela}.rhb_carreira_categ_funcional RCCF ON RCCF.id_categoria_funcional = FR.id_categoria_funcional
                                    LEFT JOIN sw_{tabela}.rhb_carreira_referencia RCR ON RCR.id_referencia = FR.id_referencia  
                                    LEFT JOIN SW_{tabela}.FUNCIONARIO_INGRESSO FI ON FI.ID_FUNCIONARIO = F.ID_FUNCIONARIO
                                    LEFT JOIN SW_PUBLICO.EMPRESA E ON E.SIGLA ='{tabela}'                                
                                WHERE
                                    PV.COD_INSTITUCIONAL IS NOT NULL
                                    AND RC.nome_carreira IS NOT NULL
                                ORDER BY
                                    PP.NOME
            """
        cur.execute(query)
        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        dfs.append(pd.DataFrame(rows, columns=columns))
    return pd.concat(dfs, ignore_index=True)

def consulta_rubrica(cur, mes, ano, tabelas):
    dfs = []
    for tabela in tabelas:
        query = f"""
    SELECT DISTINCT
            E.SIGLA_EMPRESA ORGAO,
            FF.COD_INSTITUCIONAL as MATRICULA,
            F.CHAVE_FOLHA,
            pp.NOME,
            pdc.CPF_PESSOA, 
            R.COD_RUBRICA,
            R.TIPO,
            R.NOME_RUBRICA,
            FFR.VALOR_CALCULADO,
            FFR.PRAZO_TOTAL,                                                                      
            pp.DATA_OBITO                                           

    FROM
        SW_{tabela}.FOLHA_FUNC FF
        LEFT JOIN SW_{tabela}.FOLHA F ON F.ID_FOLHA = FF.ID_FOLHA
        LEFT JOIN SW_{tabela}.FOLHA_FUNC_RUBRICA FFR ON  FFR.ID_FOLHA_FUNCIONARIO = FF.ID_FOLHA_FUNCIONARIO
        LEFT JOIN SW_PUBLICO.FOLHA_RUBRICA R ON   R.ID_RUBRICA = FFR.ID_RUBRICA
        LEFT JOIN SW_PUBLICO.EMPRESA E ON    E.SIGLA = '{tabela}'
        LEFT JOIN SW_PUBLICO.PESSOA_DOC_CPF pdc ON FF.ID_PESSOA_FUNCIONARIO = pdc.ID_PESSOA
        LEFT JOIN SW_PUBLICO.PESSOA pp ON pp.ID_PESSOA = FF.ID_PESSOA_FUNCIONARIO       
            
    WHERE
        R.TIPO IN ('R', 'D')
        AND F.MES = {mes}
        AND F.ANO = {ano}
        --AND FP.DATA_FIM IS NULL
        """
        cur.execute(query)
        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        dfs.append(pd.DataFrame(rows, columns=columns))
    return pd.concat(dfs, ignore_index=True)

def consulta_rubrica_por_codigo(cur, rubricas, mes, ano, tabelas):
    import pandas as pd
    dfs = []
    for tabela in tabelas:
        for rubrica in rubricas:
            query = f"""
                SELECT DISTINCT
                    E.SIGLA_EMPRESA ORGAO,
                    FF.COD_INSTITUCIONAL as MATRICULA,
                    F.CHAVE_FOLHA,
                    pp.NOME,
                    pdc.CPF_PESSOA, 
                    R.COD_RUBRICA,
                    R.TIPO,
                    R.NOME_RUBRICA,
                    FFR.VALOR_CALCULADO,
                    FFR.PRAZO_TOTAL,                                                                      
                    pp.DATA_OBITO                                           
                FROM
                    SW_{tabela}.FOLHA_FUNC FF
                    LEFT JOIN SW_{tabela}.FOLHA F ON F.ID_FOLHA = FF.ID_FOLHA
                    LEFT JOIN SW_{tabela}.FOLHA_FUNC_RUBRICA FFR ON  FFR.ID_FOLHA_FUNCIONARIO = FF.ID_FOLHA_FUNCIONARIO
                    LEFT JOIN SW_PUBLICO.FOLHA_RUBRICA R ON   R.ID_RUBRICA = FFR.ID_RUBRICA
                    LEFT JOIN SW_PUBLICO.EMPRESA E ON    E.SIGLA = '{tabela}'
                    LEFT JOIN SW_PUBLICO.PESSOA_DOC_CPF pdc ON FF.ID_PESSOA_FUNCIONARIO = pdc.ID_PESSOA
                    LEFT JOIN SW_PUBLICO.PESSOA pp ON pp.ID_PESSOA = FF.ID_PESSOA_FUNCIONARIO       
                WHERE
                    R.COD_RUBRICA = '{rubrica}'
                    AND F.MES = {mes}
                    AND F.ANO = {ano}
            """
            cur.execute(query)
            columns = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            dfs.append(pd.DataFrame(rows, columns=columns))

    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()


def consulta_pensionistas_funprev(cur, mes, ano):
    dfs = []
   
    query = f"""
SELECT
    FC.MATRICULA_INSTITUIDOR,
    FC.CPF_INSTITUIDOR,
    FC.NOME_INSTITUIDOR,
    FC.COD_INSTITUCIONAL MATRICULA_PENSIONISTA,
    FC.CPF_PESSOA CPF_PENSIONISTA,
    FC.NOME NOME_PENSIONISTA,
    OO.ID_PREV_ORIGEM ID_INF_PREVIDENCIA,
    PP.NOME_PLANO PLANO,
    E.RAZAO_SOCIAL EMPRESA,
    EG.NOME_ORGAO_EXTERNO ORGAO_EXTERNO,
    E2.RAZAO_SOCIAL EMPRESA_PAGAMENTO,
    CF.NOME_CATE_FUNC CATEGORIA_FUNCIONAL,
    PR.NOME_REFERENCIA REFERENCIA,
    OO.DATA_CADASTRO DATA_FIM,
    OO.OBSERVACAO,
    'PENSÃO CIVIL' TIPO,
    FC.OBITO_INSTITUIDOR,
    CF.NOME_CATE_FUNC AS CARGO,
    FFF.VALOR_CALCULADO AS VALOR_BRUTO,
    FFF2.VALOR_CALCULADO AS VALOR_LIQUIDO
FROM
    SW_FUNPREV.FOLHA_CONTRACHEQUE FC
    JOIN SW_FUNPREV.FUNC_PENSAO_CIVIL PC ON PC.ID_PENSIONISTA = FC.ID_PENSIONISTA
    LEFT JOIN SW_PUBLICO.PREV_PROP_ORGAO_ORIGEM OO ON OO.ID_PREV_ORIGEM = PC.ID_PREV_ORIGEM
    LEFT JOIN SW_PUBLICO.PREV_PROP_PLANO PP ON PP.ID_PLANO = OO.ID_PLANO
    LEFT JOIN SW_PUBLICO.EMPRESA E ON E.ID_EMPRESA = OO.ID_EMPRESA
    LEFT JOIN SW_PUBLICO.RHB_ORGAO_EXTERNO_GOVERNO EG ON EG.ID_ORGAO_EXTERNO = OO.ID_ORGAO_EXTERNO
    LEFT JOIN SW_PUBLICO.EMPRESA E2 ON E2.ID_EMPRESA = OO.ID_EMPRESA_PAGAMENTO
    LEFT JOIN SW_PUBLICO.PREV_PROP_CATE_FUNCIONAL CF ON CF.ID_CATE_FUNC = OO.ID_PLAN_CATE_FUNC
    LEFT JOIN SW_PUBLICO.PREV_PROP_REFERENCIA PR ON PR.ID_REFERENCIA = OO.ID_REFERENCIA
	JOIN SW_FUNPREV.FOLHA_FICHA_FINANCEIRA FFF ON FFF.ID_FOLHA_FUNCIONARIO = FC.ID_FOLHA_FUNCIONARIO AND FFF.ID_RUBRICA = 51027
	JOIN SW_FUNPREV.FOLHA_FICHA_FINANCEIRA FFF2 ON FFF2.ID_FOLHA_FUNCIONARIO = FC.ID_FOLHA_FUNCIONARIO AND FFF2.ID_RUBRICA = 51025
WHERE FC.MES = {mes}
    AND FC.ANO = {ano}
UNION ALL   
SELECT
    FC.MATRICULA_INSTITUIDOR,
    FC.CPF_INSTITUIDOR,
    FC.NOME_INSTITUIDOR,
    FC.COD_INSTITUCIONAL MATRICULA_PENSIONISTA,
    FC.CPF_PESSOA CPF_PENSIONISTA,
    FC.NOME NOME_PENSIONISTA,
    OO.ID_PREV_ORIGEM ID_INF_PREVIDENCIA,
    PP.NOME_PLANO PLANO,
    E.RAZAO_SOCIAL EMPRESA,
    EG.NOME_ORGAO_EXTERNO ORGAO_EXTERNO,
    E2.RAZAO_SOCIAL EMPRESA_PAGAMENTO,
    CF.NOME_CATE_FUNC CATEGORIA_FUNCIONAL,
    PR.NOME_REFERENCIA REFERENCIA,
    OO.DATA_CADASTRO DATA_FIM,
    OO.OBSERVACAO,
    'PENSÃO CIVIL SEM INSTITUIDOR' TIPO,
    FC.OBITO_INSTITUIDOR,
    CF.NOME_CATE_FUNC AS CARGO,
    FFF.VALOR_CALCULADO AS VALOR_BRUTO,
    FFF2.VALOR_CALCULADO AS VALOR_LIQUIDO
FROM
    SW_FUNPREV.FOLHA_CONTRACHEQUE FC
    JOIN SW_FUNPREV.PENS_CIVI_SEM_INSTITUIDOR PC ON PC.ID_FUNCIONARIO = FC.ID_FUNCIONARIO
    LEFT JOIN SW_PUBLICO.PREV_PROP_ORGAO_ORIGEM OO ON OO.ID_PREV_ORIGEM = PC.ID_PREV_ORIGEM
    LEFT JOIN SW_PUBLICO.PREV_PROP_PLANO PP ON PP.ID_PLANO = OO.ID_PLANO
    LEFT JOIN SW_PUBLICO.EMPRESA E ON E.ID_EMPRESA = OO.ID_EMPRESA
    LEFT JOIN SW_PUBLICO.RHB_ORGAO_EXTERNO_GOVERNO EG ON EG.ID_ORGAO_EXTERNO = OO.ID_ORGAO_EXTERNO
    LEFT JOIN SW_PUBLICO.EMPRESA E2 ON E2.ID_EMPRESA = OO.ID_EMPRESA_PAGAMENTO
    LEFT JOIN SW_PUBLICO.PREV_PROP_CATE_FUNCIONAL CF ON CF.ID_CATE_FUNC = OO.ID_PLAN_CATE_FUNC
    LEFT JOIN SW_PUBLICO.PREV_PROP_REFERENCIA PR ON PR.ID_REFERENCIA = OO.ID_REFERENCIA
	JOIN SW_FUNPREV.FOLHA_FICHA_FINANCEIRA FFF ON FFF.ID_FOLHA_FUNCIONARIO = FC.ID_FOLHA_FUNCIONARIO AND FFF.ID_RUBRICA = 51027
	JOIN SW_FUNPREV.FOLHA_FICHA_FINANCEIRA FFF2 ON FFF2.ID_FOLHA_FUNCIONARIO = FC.ID_FOLHA_FUNCIONARIO AND FFF2.ID_RUBRICA = 51025
WHERE 
    FC.MES = {mes}
    AND FC.ANO = {ano}
        """
    cur.execute(query)
    columns = [desc[0] for desc in cur.description]
    rows = cur.fetchall()
    dfs.append(pd.DataFrame(rows, columns=columns))
    return pd.concat(dfs, ignore_index=True)

def consulta_estagiarios_cadastro(cur, tabelas):
    dfs = []
    for tabela in tabelas:
        query = f"""
SELECT 
    E.SIGLA_EMPRESA AS ORGAO, 
    PP.nome, PDC.CPF_PESSOA, 
    PV.COD_INSTITUCIONAL, 
    pp.data_nascimento, 
    E.data_cadastro, 
    E.data_inicio AS INGRESSO, 
    E.data_fim, 
    E.data_previ_termino, 
    E.semestre_inicio, 
    E.horas_contrato, 
    RL.cod_lotacao, 
    RL.nome_lotacao 
FROM sw_{tabela}.estagiario E 
    JOIN sw_{tabela}.estagiario_lotacao EL ON EL.id_estagiario = E.id_estagiario 
    JOIN sw_{tabela}.rhb_lotacao RL ON RL.id_lotacao = EL.id_lotacao 
    JOIN SW_PUBLICO.EMPRESA E ON E.SIGLA = '{tabela}' 
    JOIN sw_{tabela}.estagiario_pagamento EP ON EP.id_estagiario = E.id_estagiario 
    JOIN sw_{tabela}.estag_folha EF ON EF.id_folha = EP.id_folha AND EF.mes = 10 AND EF.ano = 2024 
    JOIN sw_{tabela}.pessoa_vinculo PV ON PV.id_pessoa_vinculo = E.ID_PESSOA_VINCULO 
    JOIN sw_publico.pessoa PP ON PP.id_pessoa = PV.ID_PESSOA 
    JOIN SW_PUBLICO.PESSOA_DOC_CPF PDC ON PDC.ID_PESSOA = PV.ID_PESSOA
        """
        cur.execute(query)
        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        dfs.append(pd.DataFrame(rows, columns=columns))
    return pd.concat(dfs, ignore_index=True)

def consulta_estagiarios_folha(cur, mes, ano, tabelas):
    dfs = []
    for tabela in tabelas:
        query = f"""
SELECT 
    E.SIGLA_EMPRESA AS ORGAO, 
    RL.nome_lotacao AS LOTAÇÃO, 
    PP.nome AS ESTAGIARIO, 
    PV.COD_INSTITUCIONAL AS MATRICULA, 
    PDC.CPF_PESSOA AS CPF, 
    REE.nome_fantasia AS FACULDADE, 
    IC.nome_curso AS CURSO, 
    pp.data_nascimento, 
    E.data_inicio AS INGRESSO, 
    E.data_fim, 
    RL.cod_lotacao, 
    l.nome_lotacao AS lotacao, 
    ERP.VALOR 
    FROM sw_{tabela}.estagiario E 
        JOIN sw_{tabela}.estagiario_lotacao EL ON EL.id_estagiario = E.id_estagiario 
        JOIN sw_{tabela}.rhb_lotacao RL ON RL.id_lotacao = EL.id_lotacao 
        JOIN SW_PUBLICO.EMPRESA E ON E.SIGLA = '{tabela}' 
        JOIN sw_{tabela}.estagiario_pagamento EP ON EP.id_estagiario = E.id_estagiario 
        JOIN sw_{tabela}.estag_folha EF ON EF.id_folha = EP.id_folha AND EF.mes = 10 AND EF.ano = 2024 
        JOIN sw_{tabela}.pessoa_vinculo PV ON PV.id_pessoa_vinculo = E.ID_PESSOA_VINCULO 
    JOIN sw_publico.pessoa PP ON PP.id_pessoa = PV.ID_PESSOA 
    JOIN SW_PUBLICO.PESSOA_DOC_CPF PDC ON PDC.ID_PESSOA = PV.ID_PESSOA 
        JOIN sw_{tabela}.estag_pagamento_rubrica ERP ON ERP.id_estagiario = E.id_estagiario 
        JOIN sw_{tabela}.estagiario_curso EC ON EC.id_estagiario = E.id_estagiario 
    JOIN sw_publico.rhb_instrucao_curso IC ON IC.id_curso = EC.id_curso 
    JOIN sw_publico.rhb_entidade_externa REE ON REE.id_entidade_externa = EC.id_entidade_externa 
        LEFT JOIN sw_{tabela}.rhb_lotacao l ON l.id_lotacao = EL.id_lotacao 
WHERE 
    ERP.ANO_REFERENCIA = {ano} 
    AND ERP.MES_REFERENCIA = {mes} 
    AND ERP.id_rubrica IN ('51027')
        """
        cur.execute(query)
        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        dfs.append(pd.DataFrame(rows, columns=columns))
    return pd.concat(dfs, ignore_index=True)

def consulta_picpay(cur, mes, ano, tabelas):
    dfs = []
    for tabela in tabelas:
        query = f"""
SELECT DISTINCT
        FF.COD_INSTITUCIONAL,
        pp.NOME,
        pdc.CPF_PESSOA, 
        PD.NOME_DIVISAO DIVISAO,
        PS.NOME_SITUACAO SITUACAO,
        TF.NOME_TIPO_FUNCIONARIO TIPO_FUNCIONARIO,
        CF.NOME_CATEGORIA_FUNCIONAL CARGO_EFETIVO,
        NMVCC.descricao AS CARGO_COMISSIONADO,
        C.NOME_CARREIRA PLANO,
        CR.NOME_REFERENCIA REFERENCIA,
        FR.DATA_CADASTRO,
        RCC.NOME_CLASSE CLASSE,
        RCN.NOME_NIVEL NIVEL,
        RCP.NOME_PADRAO PADRAO,
        --CG.NOME_GRUPO GRUPO,
        CE.NOME_ESPECIALIDADE ESPECIALIDADE,
        RT.NOME_REGIME REGIME,
        FI.DATA_POSSE DATA_ADMISSAO,
        --R.TIPO,
        --R.COD_RUBRICA,
        --R.NOME_RUBRICA,
        --FFR.VALOR_CALCULADO,
        --PP.DATA_NASCIMENTO,
        E.SIGLA_EMPRESA ORGAO,
        E.ID_EMPRESA,
        E.SIGLA_EMPRESA,
        --F.CHAVE_FOLHA,  
        CT.CODIGO CATEGORIA_SERVIDOR,
        CT.DESCRICAO DESCRICAO_CATEGORIA_SERVIDOR,                                                                       
        pp.DATA_OBITO,
        prcfs.NOME_SEXO, 
        NVL((SELECT SUM(X.VALOR_CALCULADO) FROM SW_{tabela}.FOLHA_FICHA_FINANCEIRA X WHERE X.ID_FOLHA_FUNCIONARIO = FF.ID_FOLHA_FUNCIONARIO AND X.ID_RUBRICA IN (51027)), 0) AS BRUTO_999997,
        NVL((SELECT SUM(X.VALOR_CALCULADO) FROM SW_{tabela}.FOLHA_FICHA_FINANCEIRA X WHERE X.ID_FOLHA_FUNCIONARIO = FF.ID_FOLHA_FUNCIONARIO AND X.ID_RUBRICA IN (51025)), 0) AS LIQUIDO_999999                                       

FROM
    SW_{tabela}.FOLHA_FUNC FF
    LEFT JOIN SW_{tabela}.FOLHA F ON F.ID_FOLHA = FF.ID_FOLHA 
    LEFT JOIN SW_{tabela}.FOLHA_FUNC_RUBRICA FFR ON  FFR.ID_FOLHA_FUNCIONARIO = FF.ID_FOLHA_FUNCIONARIO
    LEFT JOIN SW_PUBLICO.FOLHA_RUBRICA R ON   R.ID_RUBRICA = FFR.ID_RUBRICA
    LEFT JOIN SW_PUBLICO.EMPRESA E ON    E.SIGLA = '{tabela}'
    LEFT JOIN SW_PUBLICO.PESSOA_DOC_CPF pdc ON FF.ID_PESSOA_FUNCIONARIO = pdc.ID_PESSOA
    LEFT JOIN SW_PUBLICO.PESSOA pp ON pp.ID_PESSOA = FF.ID_PESSOA_FUNCIONARIO 
    LEFT JOIN SW_{tabela}.FUNCIONARIO_PERFIL FP ON FP.ID_FUNCIONARIO = FF.ID_FUNCIONARIO AND FP.DATA_FIM IS NULL
    LEFT JOIN SW_PUBLICO.RHB_CARACT_FISICA_SEXO prcfs ON  pp.ID_SEXO = prcfs.ID_SEXO 
    LEFT JOIN SW_{tabela}.FUNCIONARIO_PERFIL FP ON FP.ID_FUNCIONARIO = FF.ID_FUNCIONARIO AND FP.DATA_FIM IS NULL
    LEFT JOIN SW_{tabela}.RHB_PERFIL P ON P.ID_PERFIL = FP.ID_PERFIL
    LEFT JOIN SW_PUBLICO.RHB_PERFIL_DIVISAO PD ON PD.ID_DIVISAO = P.ID_DIVISAO
    LEFT JOIN SW_PUBLICO.RHB_PERFIL_SITUACAO PS ON PS.ID_SITUACAO = P.ID_SITUACAO
    LEFT JOIN SW_PUBLICO.RHB_PERFIL_TIPO_FUNCIONARIO TF ON TF.ID_TIPO_FUNCIONARIO = FP.ID_TIPO_FUNCIONARIO
    LEFT JOIN SW_{tabela}.FUNCIONARIO_REFERENCIA FR ON FR.ID_FUNCIONARIO = FF.ID_FUNCIONARIO AND FR.DATA_TERMINO IS NULL
    LEFT JOIN SW_{tabela}.RHB_CARREIRA_REFERENCIA CR ON CR.ID_REFERENCIA = FR.ID_REFERENCIA
    LEFT JOIN SW_{tabela}.RHB_CARREIRA_CLASSE RCC ON RCC.ID_CLASSE = CR.ID_CLASSE
    LEFT JOIN SW_{tabela}.RHB_CARREIRA_NIVEL RCN ON RCN.ID_NIVEL = CR.ID_NIVEL
    LEFT JOIN SW_{tabela}.RHB_CARREIRA_PADRAO RCP ON RCP.ID_PADRAO = CR.ID_PADRAO
   -- LEFT JOIN SW_{tabela}.RHB_CARREIRA_CATEGORIA_GRUPO CG ON CG.ID_GRUPO = FI.ID_GRUPO
    LEFT JOIN SW_{tabela}.RHB_CARREIRA_CATEG_FUNCIONAL CF ON CF.ID_CATEGORIA_FUNCIONAL = FR.ID_CATEGORIA_FUNCIONAL
    LEFT JOIN SW_{tabela}.RHB_CARREIRA C ON C.ID_CARREIRA = CF.ID_CARREIRA
    LEFT JOIN SW_{tabela}.RHB_CARREIRA_CATEG_ESPECIALID CE ON CE.ID_ESPECIALIDADE = FR.ID_ESPECIALIDADE 
    JOIN SW_{tabela}.FUNCIONARIO_INGRESSO FI ON FI.ID_FUNCIONARIO = FF.ID_FUNCIONARIO
    JOIN SW_PUBLICO.RHB_INGRESSO_REGIME_TRABALHO RT ON RT.ID_REGIME = FI.ID_REGIME
    LEFT JOIN sw_{tabela}.funcionario_funcao_nomeacao FFN ON FFN.id_funcionario = FF.id_funcionario
    LEFT JOIN sw_publico.nm_vaga_cargo_comissionado NMVCC ON NMVCC.id_nm_vaga_cargo_comissionado = FFN.id_funcao_comissionada
    LEFT JOIN SW_PUBLICO.ESB_CATEGORIA_TRABALHADOR CT ON CT.ID_ESB_CATEG_TRABALHADOR = FP.ID_ESB_CATEG_TRABALHADOR
where
    F.MES = {mes}
    AND F.ANO = {ano}
    AND F.CHAVE_FOLHA LIKE '%-100'
        """
        cur.execute(query)
        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        dfs.append(pd.DataFrame(rows, columns=columns))
    return pd.concat(dfs, ignore_index=True)

def consulta_aposentados(cur, mes, ano):
    dfs = []
    query = f"""
WITH CTE AS (
  SELECT
    E.SIGLA ORGAO_PAGAMENTO,
    NVL(E2.SIGLA, FC.NOME_EMPRESA_ORIGEM) ORGAO_ORIGEM,
    FO.CHAVE_FOLHA,
    FO.MES,
    FO.ANO,
    CASE
        WHEN FO.TIPO_FOLHA_SEFAZ = 'C1' THEN 'Padrão'
        WHEN FO.TIPO_FOLHA_SEFAZ = 'C2' THEN 'Reintegrados'
        WHEN FO.TIPO_FOLHA_SEFAZ = 'C3' THEN 'Temporário'
        WHEN FO.TIPO_FOLHA_SEFAZ = 'C4' THEN 'Prestador'
        WHEN FO.TIPO_FOLHA_SEFAZ = 'C5' THEN 'Bolsistas'
        WHEN FO.TIPO_FOLHA_SEFAZ = 'C6' THEN 'Inativos'
        WHEN FO.TIPO_FOLHA_SEFAZ = 'C7' THEN 'Pensionistas'
        WHEN FO.TIPO_FOLHA_SEFAZ = 'C8' THEN 'RGPS'
        WHEN FO.TIPO_FOLHA_SEFAZ = 'C9' THEN 'RPPS'
    END TIPO_FOLHA_SEFAZ,
    FC.PLANO,
    FC.CARGO,
    FC.COD_CLASSE,
    FC.COD_PADRAO,
    FC.ESPECIALIDADE,
    FC.FUNCAO,
    RT.NOME_REGIME REGIME,
    CASE
        WHEN IG.IND_ESOCIAL_REG_PREV = 'V1' THEN 'Regime Geral da Previdência Social'
        WHEN IG.IND_ESOCIAL_REG_PREV = 'V2' THEN 'Regime Próprio de Previdência Social'
        WHEN IG.IND_ESOCIAL_REG_PREV = 'V3' THEN 'Regime de Previdência Social no Exterior'
    END REGIME_PREVIDENCIARIO,
    CASE
        WHEN PA.IND_FORMA_REVISAO = 'P' THEN 'Paridade'
        WHEN PA.IND_FORMA_REVISAO = 'R' THEN 'Reajuste Anual'
    END FORMA_REVISAO,
    FC.CALCULO_APOSENTADORIA,
    CASE
        WHEN PA.IND_CALCULO = 'R' THEN 'Remuneração'
        WHEN PA.IND_CALCULO = 'P' THEN 'Com Paridade'
        WHEN PA.IND_CALCULO = 'B' THEN 'Benefício Médio'
    END CALCULO,
    FC.COD_INSTITUCIONAL MATRICULA,
    FC.CPF_PESSOA CPF,
    FC.NOME,
    PPEN.ddd_celular  AS DDD_CEL,
    PPEN.celular AS CELULAR, 
    PPEN.ddd AS DDD,
    PPEN.telefone_residencia AS TELEFONE,
    NVL((SELECT SUM(X.VALOR_CALCULADO) FROM SW_FUNPREV.FOLHA_FICHA_FINANCEIRA X WHERE X.ID_FOLHA_FUNCIONARIO = FC.ID_FOLHA_FUNCIONARIO AND X.ID_RUBRICA IN (551182,1557289,50940,1557349,1555671,1555657,1553629)), 0) AS PROVENTOS,        
    NVL((SELECT SUM(X.VALOR_CALCULADO) FROM SW_FUNPREV.FOLHA_FICHA_FINANCEIRA X WHERE X.ID_FOLHA_FUNCIONARIO = FC.ID_FOLHA_FUNCIONARIO AND X.ID_RUBRICA IN (1556045,1561450,1561470,1561471,1561451,1556046,1555654,1555655)), 0) AS SUBSIDIO,  
    NVL((SELECT SUM(X.VALOR_CALCULADO) FROM SW_FUNPREV.FOLHA_FICHA_FINANCEIRA X WHERE X.ID_FOLHA_FUNCIONARIO = FC.ID_FOLHA_FUNCIONARIO AND X.ID_RUBRICA IN (1556047,1556048)), 0) AS VENCIMENTO,        
    NVL((SELECT SUM(X.VALOR_CALCULADO) FROM SW_FUNPREV.FOLHA_FICHA_FINANCEIRA X WHERE X.ID_FOLHA_FUNCIONARIO = FC.ID_FOLHA_FUNCIONARIO AND X.ID_RUBRICA IN (51027)), 0) AS BRUTO,
    112905,112906,122906,122908,132906,142905,152905,
    ROW_NUMBER() OVER (PARTITION BY FC.COD_INSTITUCIONAL, FO.CHAVE_FOLHA ORDER BY FC.NOME) AS RN
FROM
    SW_FUNPREV.FOLHA FO
    JOIN SW_FUNPREV.FOLHA_CONTRACHEQUE FC ON FC.ID_FOLHA = FO.ID_FOLHA
    JOIN SW_FUNPREV.FOLHA_FICHA_FINANCEIRA FF ON FF.ID_FOLHA_FUNCIONARIO = FC.ID_FOLHA_FUNCIONARIO
    JOIN SW_PUBLICO.FOLHA_RUBRICA R ON R.ID_RUBRICA = FF.ID_RUBRICA
    LEFT JOIN SW_FUNPREV.FUNCIONARIO_INGRESSO FI ON FI.ID_FUNCIONARIO = FC.ID_FUNCIONARIO
    LEFT JOIN SW_PUBLICO.RHB_INGRESSO_REGIME_TRABALHO RT ON RT.ID_REGIME = FI.ID_REGIME
    LEFT JOIN SW_FUNPREV.FUNCIONARIO_INF_GOVERNO IG ON IG.ID_FUNCIONARIO = FC.ID_FUNCIONARIO
    LEFT JOIN SW_PUBLICO.PREV_PROP_PLAN_PREV_APOSENT PA ON PA.ID_PESSOA = FC.ID_PESSOA 
    JOIN SW_PUBLICO.EMPRESA E ON E.SIGLA = 'FUNPREV'
    LEFT JOIN SW_PUBLICO.EMPRESA E2 ON E2.RAZAO_SOCIAL = FC.ORGAO_INSTITUIDOR
    LEFT JOIN SW_PUBLICO.PESSOA PP ON PP.ID_PESSOA = FC.ID_PESSOA
    LEFT JOIN sw_publico.pessoa_endereco PPEN ON PPEN.ID_PESSOA = PP.ID_PESSOA
WHERE
    FO.MES = {mes}
    AND FO.ANO = {ano}
    AND FO.TIPO_FOLHA_SEFAZ = 'C6' -- APOSENTADOS
    AND R.COD_RUBRICA = '999997'
    )
    SELECT 
    ORGAO_PAGAMENTO,
    ORGAO_ORIGEM,
    CHAVE_FOLHA,
    MES,
    ANO,
    TIPO_FOLHA_SEFAZ,
    PLANO,
    CARGO,
    COD_CLASSE,
    COD_PADRAO,
    ESPECIALIDADE,
    FUNCAO,
    REGIME,
    REGIME_PREVIDENCIARIO,
    MATRICULA,
    FORMA_REVISAO,
    CALCULO_APOSENTADORIA,
    CPF,
    NOME, 
    DDD_CEL,CELULAR, DDD,TELEFONE,
    PROVENTOS,SUBSIDIO,VENCIMENTO,BRUTO
     FROM 
      CTE
       WHERE 
         RN = 1
         ORDER BY 
         CHAVE_FOLHA
        """
    cur.execute(query)
    columns = [desc[0] for desc in cur.description]
    rows = cur.fetchall()
    dfs.append(pd.DataFrame(rows, columns=columns))
    return pd.concat(dfs, ignore_index=True)

