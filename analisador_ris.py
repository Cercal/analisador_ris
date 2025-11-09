import os
import glob
import re
import unicodedata
import pandas as pd
from collections import Counter
import csv

def normalizar_texto(texto):
    """
    Normaliza o texto removendo acentos, convertendo para minúsculas
    e removendo caracteres especiais
    """
    if not texto:
        return ""
    
    # Remove acentos
    texto = unicodedata.normalize('NFKD', str(texto))
    texto = ''.join([c for c in texto if not unicodedata.combining(c)])
    
    # Converte para minúsculas
    texto = texto.lower()
    
    # Remove caracteres especiais, mantendo apenas letras, números e espaços
    texto = re.sub(r'[^a-z0-9\s]', ' ', texto)
    
    # Remove espaços extras
    texto = ' '.join(texto.split())
    
    return texto

def parse_ris_file(file_path):
    """
    Função para ler e parsear um arquivo .RIS
    Retorna uma lista de dicionários, onde cada dicionário é um registro
    """
    registros = []
    registro_atual = {}
    
    try:
        # Tenta diferentes codificações
        codificacoes = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        linhas = None
        
        for encoding in codificacoes:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    linhas = file.readlines()
                break
            except UnicodeDecodeError:
                continue
        
        if linhas is None:
            print(f"  ❌ Erro de codificação no arquivo: {os.path.basename(file_path)}")
            return []
            
    except Exception as e:
        print(f"  ❌ Erro ao ler arquivo {file_path}: {e}")
        return []
    
    for linha in linhas:
        linha = linha.strip()
        
        # Fim do registro
        if linha == 'ER  -':
            if registro_atual:
                registros.append(registro_atual)
                registro_atual = {}
        
        # Campo RIS (formato: "XX  - valor")
        elif len(linha) >= 6 and linha[2:4] == '  -':
            campo = linha[0:2].strip()
            valor = linha[6:].strip()
            
            # Para campos que podem ter múltiplos valores (AU, KW), armazena como lista
            if campo in ['AU', 'KW']:
                if campo not in registro_atual:
                    registro_atual[campo] = []
                registro_atual[campo].append(valor)
            else:
                registro_atual[campo] = valor
    
    # Não esquecer o último registro se não terminou com ER
    if registro_atual:
        registros.append(registro_atual)
    
    return registros

def determinar_tipo_item(registro):
    """
    Determina o tipo do item baseado no campo TY e M3
    """
    tipo = registro.get('TY', 'Desconhecido')
    
    if tipo == 'THES':
        # Para teses, pega o tipo do campo M3
        return registro.get('M3', 'Tese não especificada')
    elif tipo == 'JOUR':
        return 'Artigo de Periódico'
    elif tipo == 'BOOK':
        return 'Livro'
    elif tipo == 'CHAP':
        return 'Capítulo de Livro'
    elif tipo == 'CONF':
        return 'Conferência'
    else:
        return tipo

def determinar_fonte(registro):
    """
    Determina a fonte/periódico baseado no tipo
    """
    tipo = registro.get('TY', '')
    
    if tipo == 'JOUR':
        return registro.get('T2', registro.get('JO', 'Periódico não especificado'))
    elif tipo == 'THES':
        return registro.get('PB', 'Universidade não especificada')
    else:
        return registro.get('PB', registro.get('T2', 'Fonte não especificada'))

def contar_palavras_chave_especificas(texto, palavras_chave):
    """
    Conta a ocorrência de palavras-chave específicas em um texto
    """
    if not texto:
        return {}
    
    texto_normalizado = normalizar_texto(texto)
    contagem = {}
    
    for palavra in palavras_chave:
        palavra_normalizada = normalizar_texto(palavra)
        # Conta ocorrências (case insensitive e sem acentos)
        contagem[palavra] = texto_normalizado.count(palavra_normalizada)
    
    return contagem

def processar_ris_estatisticas(pasta_entrada):
    """
    Processa todos os arquivos .RIS e gera estatísticas completas
    """
    # Lista de palavras-chave específicas para busca
    PALAVRAS_CHAVE_ESPECIFICAS = [
        "lixo eletrônico",
        "resíduo eletrônico", 
        "resíduos eletrônicos",
        "resíduos de equipamentos elétricos e eletrônicos",
        "REEE",
        "lixo eletroeletrônico",
        "resíduo eletroeletrônico",
        "resíduos eletroeletrônicos",
        "e-waste",
        "electronic waste",
        "waste electrical and electronic equipment",
        "WEEE",
        "basura electrónica",
        "residuo electrónico",
        "residuos electrónicos",
        "residuos de aparatos eléctricos y electrónicos",
        "REEE"
    ]
    
    # Encontrar todos os arquivos .ris na pasta
    arquivos_ris = glob.glob(os.path.join(pasta_entrada, "*.ris"))
    
    if not arquivos_ris:
        print("❌ Nenhum arquivo .ris encontrado na pasta especificada.")
        return
    
    print(f"📁 Encontrados {len(arquivos_ris)} arquivo(s) .ris")
    
    # Estruturas para armazenar estatísticas
    todos_registros = []
    contagem_tipos = Counter()
    contagem_autores = Counter()
    contagem_anos = Counter()
    contagem_idiomas = Counter()
    contagem_fontes = Counter()
    todas_palavras_chave = Counter()
    contagem_palavras_especificas_kw = Counter()
    contagem_palavras_especificas_ab = Counter()
    
    # Processar cada arquivo
    for arquivo_ris in arquivos_ris:
        print(f"🔍 Processando: {os.path.basename(arquivo_ris)}")
        
        registros = parse_ris_file(arquivo_ris)
        todos_registros.extend(registros)
        
        print(f"  ✅ {len(registros)} registros processados")
    
    # Processar estatísticas
    for registro in todos_registros:
        # Tipo de item
        tipo = determinar_tipo_item(registro)
        contagem_tipos[tipo] += 1
        
        # Autores
        autores = registro.get('AU', [])
        if isinstance(autores, list):
            for autor in autores:
                if autor:  # Remove autores vazios
                    contagem_autores[autor] += 1
        elif autores:  # Se for string única
            contagem_autores[autores] += 1
        
        # Ano de publicação
        ano = registro.get('PY', 'Ano não especificado')
        contagem_anos[ano] += 1
        
        # Idioma
        idioma = registro.get('LA', 'Idioma não especificado')
        contagem_idiomas[idioma] += 1
        
        # Fonte/Periódico
        fonte = determinar_fonte(registro)
        contagem_fontes[fonte] += 1
        
        # Palavras-chave gerais
        keywords = registro.get('KW', [])
        if isinstance(keywords, list):
            for kw in keywords:
                if kw:
                    kw_normalizada = normalizar_texto(kw)
                    todas_palavras_chave[kw_normalizada] += 1
                    
                    # Contar palavras-chave específicas em KW
                    contagem_kw = contar_palavras_chave_especificas(kw, PALAVRAS_CHAVE_ESPECIFICAS)
                    for palavra, count in contagem_kw.items():
                        if count > 0:
                            contagem_palavras_especificas_kw[palavra] += count
        elif keywords:
            kw_normalizada = normalizar_texto(keywords)
            todas_palavras_chave[kw_normalizada] += 1
            contagem_kw = contar_palavras_chave_especificas(keywords, PALAVRAS_CHAVE_ESPECIFICAS)
            for palavra, count in contagem_kw.items():
                if count > 0:
                    contagem_palavras_especificas_kw[palavra] += count
        
        # Palavras-chave específicas no resumo
        abstract = registro.get('AB', '')
        if abstract:
            contagem_ab = contar_palavras_chave_especificas(abstract, PALAVRAS_CHAVE_ESPECIFICAS)
            for palavra, count in contagem_ab.items():
                if count > 0:
                    contagem_palavras_especificas_ab[palavra] += count
    
    # Gerar relatórios
    print(f"\n{'='*60}")
    print("📊 RELATÓRIO COMPLETO DE ANÁLISE .RIS")
    print(f"{'='*60}")
    
    # 1. Tipo de Itens
    print(f"\n📋 TIPOS DE ITENS ({len(contagem_tipos)} tipos encontrados):")
    for tipo, count in contagem_tipos.most_common():
        print(f"   • {tipo}: {count} ocorrências")
    
    # 2. Autores
    print(f"\n👥 AUTORES (Top 20 de {len(contagem_autores)} autores):")
    for autor, count in contagem_autores.most_common(20):
        print(f"   • {autor}: {count} publicação(ões)")
    
    # 3. Publicações por Ano
    print(f"\n📅 PUBLICAÇÕES POR ANO ({len(contagem_anos)} anos):")
    for ano, count in sorted(contagem_anos.items()):
        print(f"   • {ano}: {count} publicação(ões)")
    
    # 4. Publicações por Idioma
    print(f"\n🌐 PUBLICAÇÕES POR IDIOMA ({len(contagem_idiomas)} idiomas):")
    for idioma, count in contagem_idiomas.most_common():
        print(f"   • {idioma}: {count} publicação(ões)")
    
    # 5. Publicações por Periódico/Base
    print(f"\n📚 PUBLICAÇÕES POR FONTE (Top 20 de {len(contagem_fontes)} fontes):")
    for fonte, count in contagem_fontes.most_common(20):
        print(f"   • {fonte}: {count} publicação(ões)")
    
    # 6. Palavras-chave Gerais
    print(f"\n🔤 PALAVRAS-CHAVE GERAIS (Top 30 de {len(todas_palavras_chave)} palavras):")
    for palavra, count in todas_palavras_chave.most_common(30):
        print(f"   • {palavra}: {count} ocorrência(s)")
    
    # 7. Palavras-chave Específicas em KW
    print(f"\n🎯 PALAVRAS-CHAVE ESPECÍFICAS EM CAMPO KW:")
    for palavra, count in contagem_palavras_especificas_kw.most_common():
        if count > 0:
            print(f"   • {palavra}: {count} ocorrência(s)")
    
    # 8. Palavras-chave Específicas em AB
    print(f"\n📝 PALAVRAS-CHAVE ESPECÍFICAS EM RESUMOS (AB):")
    for palavra, count in contagem_palavras_especificas_ab.most_common():
        if count > 0:
            print(f"   • {palavra}: {count} ocorrência(s)")
    
    # Exportar para CSV ÚNICO
    exportar_para_csv_unico(
        contagem_tipos, contagem_autores, contagem_anos, 
        contagem_idiomas, contagem_fontes, todas_palavras_chave,
        contagem_palavras_especificas_kw, contagem_palavras_especificas_ab,
        pasta_entrada, len(todos_registros)
    )
    
    return {
        'total_registros': len(todos_registros),
        'tipos': dict(contagem_tipos),
        'autores': dict(contagem_autores),
        'anos': dict(contagem_anos),
        'idiomas': dict(contagem_idiomas),
        'fontes': dict(contagem_fontes),
        'palavras_chave_gerais': dict(todas_palavras_chave),
        'palavras_especificas_kw': dict(contagem_palavras_especificas_kw),
        'palavras_especificas_ab': dict(contagem_palavras_especificas_ab)
    }

def exportar_para_csv_unico(contagem_tipos, contagem_autores, contagem_anos, 
                           contagem_idiomas, contagem_fontes, todas_palavras_chave,
                           contagem_palavras_especificas_kw, contagem_palavras_especificas_ab,
                           pasta_entrada, total_registros):
    """
    Exporta todas as estatísticas para um único arquivo CSV
    """
    # Criar DataFrame único
    dados_completos = []
    
    # 1. Metadados básicos
    dados_completos.append({
        'Categoria': 'METADADOS',
        'Item': 'Total de Registros Processados',
        'Quantidade': total_registros,
        'Detalhes': ''
    })
    
    # 2. Tipos de Itens
    dados_completos.append({
        'Categoria': 'TIPOS DE ITENS',
        'Item': '---',
        'Quantidade': '',
        'Detalhes': f'Total de {len(contagem_tipos)} tipos encontrados'
    })
    for tipo, count in contagem_tipos.most_common():
        dados_completos.append({
            'Categoria': 'TIPOS DE ITENS',
            'Item': tipo,
            'Quantidade': count,
            'Detalhes': ''
        })
    
    # 3. Autores (Top 50)
    dados_completos.append({
        'Categoria': 'AUTORES',
        'Item': '---',
        'Quantidade': '',
        'Detalhes': f'Top 50 de {len(contagem_autores)} autores encontrados'
    })
    for autor, count in contagem_autores.most_common(50):
        dados_completos.append({
            'Categoria': 'AUTORES',
            'Item': autor,
            'Quantidade': count,
            'Detalhes': ''
        })
    
    # 4. Publicações por Ano
    dados_completos.append({
        'Categoria': 'PUBLICAÇÕES POR ANO',
        'Item': '---',
        'Quantidade': '',
        'Detalhes': f'Distribuição em {len(contagem_anos)} anos'
    })
    for ano, count in sorted(contagem_anos.items()):
        dados_completos.append({
            'Categoria': 'PUBLICAÇÕES POR ANO',
            'Item': ano,
            'Quantidade': count,
            'Detalhes': ''
        })
    
    # 5. Publicações por Idioma
    dados_completos.append({
        'Categoria': 'PUBLICAÇÕES POR IDIOMA',
        'Item': '---',
        'Quantidade': '',
        'Detalhes': f'Total de {len(contagem_idiomas)} idiomas'
    })
    for idioma, count in contagem_idiomas.most_common():
        dados_completos.append({
            'Categoria': 'PUBLICAÇÕES POR IDIOMA',
            'Item': idioma,
            'Quantidade': count,
            'Detalhes': ''
        })
    
    # 6. Publicações por Fonte
    dados_completos.append({
        'Categoria': 'PUBLICAÇÕES POR FONTE',
        'Item': '---',
        'Quantidade': '',
        'Detalhes': f'Top 30 de {len(contagem_fontes)} fontes encontradas'
    })
    for fonte, count in contagem_fontes.most_common(30):
        dados_completos.append({
            'Categoria': 'PUBLICAÇÕES POR FONTE',
            'Item': fonte,
            'Quantidade': count,
            'Detalhes': ''
        })
    
    # 7. Palavras-chave Gerais (Top 50)
    dados_completos.append({
        'Categoria': 'PALAVRAS-CHAVE GERAIS',
        'Item': '---',
        'Quantidade': '',
        'Detalhes': f'Top 50 de {len(todas_palavras_chave)} palavras-chave'
    })
    for palavra, count in todas_palavras_chave.most_common(50):
        dados_completos.append({
            'Categoria': 'PALAVRAS-CHAVE GERAIS',
            'Item': palavra,
            'Quantidade': count,
            'Detalhes': ''
        })
    
    # 8. Palavras-chave Específicas em KW
    dados_completos.append({
        'Categoria': 'PALAVRAS-CHAVE ESPECÍFICAS (KW)',
        'Item': '---',
        'Quantidade': '',
        'Detalhes': 'Ocorrências das palavras-alvo no campo de palavras-chave'
    })
    for palavra, count in contagem_palavras_especificas_kw.most_common():
        if count > 0:
            dados_completos.append({
                'Categoria': 'PALAVRAS-CHAVE ESPECÍFICAS (KW)',
                'Item': palavra,
                'Quantidade': count,
                'Detalhes': ''
            })
    
    # 9. Palavras-chave Específicas em AB
    dados_completos.append({
        'Categoria': 'PALAVRAS-CHAVE ESPECÍFICAS (AB)',
        'Item': '---',
        'Quantidade': '',
        'Detalhes': 'Ocorrências das palavras-alvo nos resumos'
    })
    for palavra, count in contagem_palavras_especificas_ab.most_common():
        if count > 0:
            dados_completos.append({
                'Categoria': 'PALAVRAS-CHAVE ESPECÍFICAS (AB)',
                'Item': palavra,
                'Quantidade': count,
                'Detalhes': ''
            })
    
    # Criar DataFrame e exportar
    df = pd.DataFrame(dados_completos)
    
    # Nome do arquivo de saída
    arquivo_saida = os.path.join(pasta_entrada, "estatisticas_completas_ris.csv")
    
    # Exportar para CSV
    df.to_csv(arquivo_saida, index=False, encoding='utf-8-sig')
    
    print(f"\n💾 Arquivo CSV único exportado: {arquivo_saida}")
    print(f"   • Total de linhas: {len(df)}")
    print(f"   • Categorias incluídas: 9")
    print(f"   • Formato: Categoria, Item, Quantidade, Detalhes")

def main():
    """
    Função principal
    """
    print("🔍 ANALISADOR DE ARQUIVOS .RIS - CSV ÚNICO")
    print("=" * 50)
    
    # Obter caminho da pasta
    pasta_entrada = input("Digite o caminho da pasta com os arquivos .ris: ").strip().strip('"')
    
    if not os.path.exists(pasta_entrada):
        print("❌ Pasta não encontrada!")
        return
    
    # Processar estatísticas
    estatisticas = processar_ris_estatisticas(pasta_entrada)
    
    if estatisticas:
        print(f"\n🎉 ANÁLISE CONCLUÍDA COM SUCESSSO!")
        print(f"📊 Total de registros processados: {estatisticas['total_registros']}")
        print(f"💾 Arquivo único gerado: estatisticas_completas_ris.csv")

if __name__ == "__main__":
    main()
