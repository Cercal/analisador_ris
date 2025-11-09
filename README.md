# Analisador de Arquivos .RIS para Metadados Acadêmicos

## Descrição

Script em Python para processar arquivos .RIS e extrair estatísticas bibliométricas sobre publicações acadêmicas relacionadas a resíduos eletrônicos e e-waste.

**Nota sobre Desenvolvimento:** Este código foi desenvolvido com assistência de IA generativa como ferramenta de apoio, com personalização e validação para pesquisa sobre resíduos eletrônicos.

## Funcionalidades

- Processa campos de registros .RIS
- Busca por 17 termos específicos de resíduos eletrônicos
- Gera relatório único em CSV
- Identifica publicações em diferentes idiomas
- Classifica tipos de documentos (artigos, teses, livros)
- Processa múltiplos arquivos simultaneamente

## Tecnologias

- Python 3.6+
- Pandas
- Collections
- Unicodedata
- Regex

## Como Usar

1. Baixe o script `analisador_ris.py`
2. Coloque arquivos .RIS em uma pasta
3. Execute: `python analisador_ris.py`
4. Informe o caminho da pasta quando solicitado

## Estrutura de Saída

Gera um arquivo CSV único com:
- Tipos de itens
- Autores (top 50)
- Publicações por ano
- Publicações por idioma  
- Publicações por fonte
- Palavras-chave gerais
- Palavras-alvo em KW e resumos

## Palavras-Chave Monitoradas

lixo eletrônico, resíduo eletrônico, resíduos eletrônicos, REEE, e-waste, electronic waste, WEEE, basura electrónica, residuos electrónicos, e outros termos relacionados.

## Licença

Creative Commons Attribution-NonCommercial 4.0 International

Permitido: uso educacional, pesquisa, adaptações
Proibido: uso comercial

## Desenvolvimento

Desenvolvido com suporte de IA generativa, validado e adaptado para pesquisa acadêmica sobre resíduos eletrônicos.

Última atualização: Novembro 2025
