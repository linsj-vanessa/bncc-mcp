# Changelog

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/).

## [2.0.0] - 2026-08-13

Release major do **BNCC MCP 2.0** — fork mantido em
[linsj-vanessa/bncc-mcp](https://github.com/linsj-vanessa/bncc-mcp).
Esta versão consolida e expande todas as funcionalidades do projeto original,
adicionando cobertura pedagógica completa para o componente de Computação.

### Adicionado
- **`objeto_conhecimento` para Computação**: campo preenchido em todas as
  141 habilidades de Computação via API `bncc.api.br`, alinhando o componente
  ao mesmo nível de detalhamento dos demais componentes do Ensino Fundamental.
- **Mapa de Foco para Computação**: suporte a `em_foco` e campos pedagógicos
  (`mf_classificacao`, `mf_conhecimento_previo`, `mf_objetivos`,
  `mf_competencias`, `mf_habilidades_relacionadas`, `mf_comentarios`) no
  `bncc_comp.csv` — Computação agora é coberta pelo `bncc_mapa_de_foco` em
  pé de igualdade com Língua Portuguesa, Matemática, Ciências, História e
  Geografia.
- **`scripts/enrich_comp.py`**: script para re-enriquecer o CSV de Computação
  automaticamente sempre que necessário (requer `BNCC_API_KEY` no `.env`).

### Alterado
- `server.py`: bloco de carga do `bncc_comp.csv` reescrito para ler
  `objeto_conhecimento`, `em_foco` e todos os campos `mf_*` do CSV.
- Docstring de `bncc_mapa_de_foco` atualizada para refletir a inclusão de
  Computação na cobertura da ferramenta.
- URLs do projeto atualizadas para o fork `linsj-vanessa/bncc-mcp`.
- `.gitignore`: ignora `.env` e `.env.*` (segredos e variáveis de ambiente).

## [0.2.1] - 2026-07-24

### Corrigido
- Habilidades do Ensino Médio (`bncc_em.csv`) cujo enunciado trazia texto
  extraído **além da própria habilidade** — rodapés de página, cabeçalhos de
  área, blocos de comentário e marcadores de nota de rodapé. 76 habilidades
  reprocessadas contra o PDF oficial da BNCC-EM; nenhuma passa de ~800
  caracteres (antes, casos com dezenas de milhares). Corrigido também um
  artefato de hifenização ("pe la" → "pela") em EM13LP26.


## [0.2.0] - 2026-06-09

### Adicionado
- Dataset de **Computação** (complemento à BNCC, anexo ao Parecer CNE/CEB
  nº 2/2022): 141 habilidades (`bncc_comp.csv`) — 11 Educação Infantil,
  104 Ensino Fundamental, 26 Ensino Médio — com o campo `eixo` (Pensamento
  Computacional, Mundo Digital, Cultura Digital). Acervo total: 1717
  habilidades. Fonte: computacional.com.br (Prof. Christian Brackmann /
  IFFAR, CC BY-NC-SA 4.0) — ver `ATTRIBUTION.md`.

## [0.1.0] - 2026-05-29

### Adicionado
- Servidor MCP da BNCC com 5 tools: `bncc_lookup`, `bncc_buscar`,
  `bncc_listar`, `bncc_mapa_de_foco`, `bncc_estatisticas`.
- 1576 habilidades (1304 Ensino Fundamental, 93 Educação Infantil,
  179 Ensino Médio).
- Unidade temática + objeto de conhecimento em 100% das habilidades EF.
- Camada do Mapa de Foco (Instituto Reúna) para 396 habilidades selecionadas.
- Empacotamento instalável (`pip install`), console script `bncc-mcp`.
