Analisador de Arquivos .RIS para Metadados Acadêmicos

https://img.shields.io/badge/License-CC_BY--NC_4.0-lightgrey.svg
📋 Descrição

Script em Python para processar arquivos .RIS e extrair estatísticas bibliométricas completas sobre publicações acadêmicas relacionadas a resíduos eletrônicos, e-waste e temas correlatos.

Nota sobre o Desenvolvimento: Este código foi desenvolvido com assistência de IA generativa (ChatGPT/DeepSeek) como ferramenta de apoio ao desenvolvimento, com extensiva personalização, validação e adaptação para o contexto específico da pesquisa sobre resíduos de equipamentos elétricos e eletrônicos.
✨ Funcionalidades

    📊 Análise Completa de Metadados: Processa todos os campos dos registros .RIS

    🔤 Busca por Palavras-Chave Específicas: 17 termos relacionados a resíduos eletrônicos

    📈 Estatísticas Consolidadas: Gera relatório único em CSV com todas as análises

    🌐 Suporte Multilingue: Identifica publicações em diferentes idiomas

    🎓 Classificação Automática: Distingue entre artigos, teses, livros, etc.

    🔄 Processamento em Lote: Analisa múltiplos arquivos .RIS simultaneamente

🛠️ Tecnologias Utilizadas

    Python 3.6+

    Pandas - Manipulação de dados

    Collections - Contadores e estruturas de dados

    Unicodedata - Normalização de texto

    Regex - Processamento de padrões em texto

🚀 Como Usar
Pré-requisitos

    Python 3.6 ou superior

    Bibliotecas padrão do Python (nenhuma instalação adicional necessária)

Instalação e Execução

    Baixe o script analisador_ris.py

    Coloque seus arquivos .RIS em uma pasta

    Execute o script:

bash

python analisador_ris.py

    Siga as instruções no terminal para informar o caminho da pasta

Estrutura de Entrada
text

sua_pasta/
├── arquivo1.ris
├── arquivo2.ris
└── arquivo3.ris

Formato de Saída

O script gera um único arquivo CSV organizado por categorias:

    estatisticas_completas_ris.csv

📊 Estatísticas Geradas
Categoria	Descrição	Exemplos
Tipos de Itens	Classificação por tipo de publicação	Artigos, Teses, Livros
Autores	Top 50 autores mais produtivos	Silva, J. (8 publicações)
Publicações por Ano	Distribuição temporal	2020: 15 publicações
Publicações por Idioma	Análise de idiomas	Português, Inglês, Espanhol
Publicações por Fonte	Periódicos e universidades	Revista X, Universidade Y
Palavras-Chave Gerais	Termos mais frequentes	sustentabilidade, reciclagem
Palavras-Alvo em KW	Ocorrências nos campos de keywords	"e-waste": 45 ocorrências
Palavras-Alvo em AB	Ocorrências nos resumos	"REEE": 23 ocorrências
🎯 Palavras-Chave Monitoradas

O script busca automaticamente por estes termos (com variações em português, inglês e espanhol):

    lixo eletrônico / e-waste / basura electrónica

    resíduo(s) eletrônico(s) / electronic waste / residuo(s) electrónico(s)

    REEE / WEEE

    waste electrical and electronic equipment

    lixo eletroeletrônico / resíduo eletroeletrônico

    E mais 12 termos específicos relacionados...

🏗️ Estrutura do Projeto
text

projeto-ris-analyser/
├── analisador_ris.py          # Script principal
├── README.md                  # Este arquivo
├── LICENSE                    # Licença CC BY-NC 4.0
└── exemplos/                  # Exemplos de uso (opcional)
    └── arquivo_exemplo.ris

🔧 Personalização
Modificando Palavras-Chave

Edite a lista PALAVRAS_CHAVE_ESPECIFICAS no script para adicionar ou modificar os termos de busca:
python

PALAVRAS_CHAVE_ESPECIFICAS = [
    "seu termo aqui",
    "outro termo importante",
    # ... outros termos
]

Adaptando para Outras Áreas

O código pode ser facilmente adaptado para outras áreas de pesquisa modificando:

    A lista de palavras-chave específicas

    Os campos analisados

    Os tipos de documentos reconhecidos

🤝 Contribuições

Contribuições são bem-vindas! Áreas de melhoria incluem:

    Suporte a mais formatos de entrada (BibTeX, EndNote)

    Novas análises estatísticas (redes de citação, colaboração)

    Interface gráfica

    Exportação para mais formatos (JSON, XLSX)

    Análise de sentimentos em resumos

📄 Licença

Este projeto está licenciado sob a Creative Commons Attribution-NonCommercial 4.0 International License.
Você pode:

    ✅ Copiar, distribuir e compartilhar o material

    ✅ Adaptar e modificar o código

    ✅ Usar para fins educacionais e de pesquisa

    ✅ Usar em projetos acadêmicos e científicos

Você NÃO pode:

    ❌ Usar para fins comerciais

    ❌ Revender o código ou derivados

    ❌ Usar em produtos ou serviços comerciais

🎓 Uso Acadêmico
Como Citareste Projeto
text

Ferramenta de Análise de Metadados .RIS. Desenvolvido com assistência de IA generativa. 
Disponível em: [URL do GitHub]

Transparência no Desenvolvimento

Este projeto foi desenvolvido com suporte de ferramentas de IA generativa como parte do processo de desenvolvimento. O código foi extensivamente validado, testado e adaptado para garantir sua eficácia na análise bibliométrica de pesquisas sobre resíduos eletrônicos.
🐛 Reportar Problemas

Encontrou um bug? Tem uma sugestão?

    Verifique se o problema já foi reportado nas Issues

    Se não encontrou, abra uma nova issue com:

        Descrição detalhada do problema

        Arquivos de exemplo (se possível)

        Mensagens de erro

        Configuração do ambiente

📞 Suporte

Para dúvidas sobre o uso do script:

    Consulte esta documentação

    Verifique as Issues no GitHub

    Entre em contato para discussões acadêmicas

🔍 Desenvolvimento e Metodologia
Processo de Desenvolvimento

    Solicitação Específica: Código desenvolvido sob demanda para pesquisa acadêmica

    Assistência de IA: Utilizada como ferramenta de apoio ao desenvolvimento

    Validação Rigorosa: Testes extensivos com dados reais de pesquisa

    Personalização: Adaptações específicas para o contexto de resíduos eletrônicos

Compromisso com Qualidade

    ✅ Código documentado e comentado

    ✅ Tratamento robusto de erros

    ✅ Suporte a múltiplas codificações

    ✅ Processamento eficiente de grandes volumes de dados

Desenvolvido para pesquisa acadêmica com transparência metodológica 📚✨

Última atualização: ${data}
