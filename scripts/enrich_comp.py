# -*- coding: utf-8 -*-
"""Enriquece bncc_comp.csv com objeto_conhecimento curado.

O complemento de Computação à BNCC (Parecer CNE/CEB nº 2/2022) não possui
objeto_conhecimento definido oficialmente nem na API bncc.api.br. Este script
aplica um mapeamento curado — derivado do conteúdo de cada habilidade e da
estrutura dos três eixos — para preencher o campo, deixando Computação em
pé de igualdade com os demais componentes no servidor MCP.

Uso:
    python scripts/enrich_comp.py

Não requer chave de API; opera somente sobre o CSV local.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
COMP_CSV = ROOT / "bncc_mcp" / "data" / "bncc_comp.csv"

# ---------------------------------------------------------------------------
# Mapeamento curado: codigo → (eixo_em, objeto_conhecimento)
#
# eixo_em: eixo para habilidades do Ensino Médio (campo vazio no CSV original)
# objeto_conhecimento: agrupamento temático dentro do eixo
# ---------------------------------------------------------------------------

MAPEAMENTO: dict[str, tuple[str, str]] = {
    # ── Educação Infantil ────────────────────────────────────────────────────
    "EI03CO01": ("", "Reconhecimento de Padrões"),
    "EI03CO02": ("", "Algoritmos"),
    "EI03CO03": ("", "Algoritmos"),
    "EI03CO04": ("", "Algoritmos"),
    "EI03CO05": ("", "Algoritmos"),
    "EI03CO06": ("", "Lógica"),
    "EI03CO07": ("", "Hardware e Dispositivos"),
    "EI03CO08": ("", "Hardware e Dispositivos"),
    "EI03CO09": ("", "Hardware e Dispositivos"),
    "EI03CO10": ("", "Cidadania e Ética Digital"),
    "EI03CO11": ("", "Cidadania e Ética Digital"),

    # ── Ensino Fundamental – 1º ano ──────────────────────────────────────────
    "EF01CO01": ("", "Reconhecimento de Padrões"),
    "EF01CO02": ("", "Algoritmos"),
    "EF01CO03": ("", "Algoritmos"),
    "EF01CO04": ("", "Dados e Representação"),
    "EF01CO05": ("", "Dados e Representação"),
    "EF01CO06": ("", "Criação Digital"),
    "EF01CO07": ("", "Segurança e Privacidade Pessoal"),

    # ── Ensino Fundamental – 2º ano ──────────────────────────────────────────
    "EF02CO01": ("", "Reconhecimento de Padrões"),
    "EF02CO02": ("", "Algoritmos"),
    "EF02CO03": ("", "Hardware e Dispositivos"),
    "EF02CO04": ("", "Hardware e Dispositivos"),
    "EF02CO05": ("", "Criação Digital"),
    "EF02CO06": ("", "Segurança e Privacidade Pessoal"),

    # ── Ensino Fundamental – 3º ano ──────────────────────────────────────────
    "EF03CO01": ("", "Lógica"),
    "EF03CO02": ("", "Algoritmos"),
    "EF03CO03": ("", "Decomposição e Abstração"),
    "EF03CO04": ("", "Dados e Representação"),
    "EF03CO05": ("", "Dados e Representação"),
    "EF03CO06": ("", "Hardware e Dispositivos"),
    "EF03CO07": ("", "Criação Digital"),
    "EF03CO08": ("", "Criação Digital"),
    "EF03CO09": ("", "Segurança e Privacidade Pessoal"),

    # ── Ensino Fundamental – 4º ano ──────────────────────────────────────────
    "EF04CO01": ("", "Estruturas de Dados"),
    "EF04CO02": ("", "Estruturas de Dados"),
    "EF04CO03": ("", "Algoritmos"),
    "EF04CO04": ("", "Dados e Representação"),
    "EF04CO05": ("", "Dados e Representação"),
    "EF04CO06": ("", "Criação Digital"),
    "EF04CO07": ("", "Cidadania e Ética Digital"),
    "EF04CO08": ("", "Cidadania e Ética Digital"),

    # ── Ensino Fundamental – 5º ano ──────────────────────────────────────────
    "EF05CO01": ("", "Estruturas de Dados"),
    "EF05CO02": ("", "Estruturas de Dados"),
    "EF05CO03": ("", "Lógica"),
    "EF05CO04": ("", "Algoritmos"),
    "EF05CO05": ("", "Hardware e Dispositivos"),
    "EF05CO06": ("", "Dados e Representação"),
    "EF05CO07": ("", "Software e Sistemas Operacionais"),
    "EF05CO08": ("", "Cidadania e Ética Digital"),
    "EF05CO09": ("", "Cidadania e Ética Digital"),
    "EF05CO10": ("", "Impacto Social da Tecnologia"),
    "EF05CO11": ("", "Criação Digital"),

    # ── Ensino Fundamental – Anos Iniciais (1º–5º, habilidades integradoras) ─
    "EF15CO01": ("", "Estruturas de Dados"),
    "EF15CO02": ("", "Algoritmos"),
    "EF15CO03": ("", "Lógica"),
    "EF15CO04": ("", "Decomposição e Abstração"),
    "EF15CO05": ("", "Dados e Representação"),
    "EF15CO06": ("", "Hardware e Dispositivos"),
    "EF15CO07": ("", "Software e Sistemas Operacionais"),
    "EF15CO08": ("", "Criação Digital"),
    "EF15CO09": ("", "Cidadania e Ética Digital"),

    # ── Ensino Fundamental – 6º ano ──────────────────────────────────────────
    "EF06CO01": ("", "Estruturas de Dados"),
    "EF06CO02": ("", "Algoritmos e Programação"),
    "EF06CO03": ("", "Algoritmos e Programação"),
    "EF06CO04": ("", "Decomposição e Abstração"),
    "EF06CO05": ("", "Algoritmos e Programação"),
    "EF06CO06": ("", "Algoritmos e Programação"),
    "EF06CO07": ("", "Redes e Internet"),
    "EF06CO08": ("", "Dados e Representação"),
    "EF06CO09": ("", "Cidadania e Ética Digital"),
    "EF06CO10": ("", "Impacto Social da Tecnologia"),

    # ── Ensino Fundamental – 7º ano ──────────────────────────────────────────
    "EF07CO01": ("", "Estruturas de Dados"),
    "EF07CO02": ("", "Algoritmos e Programação"),
    "EF07CO03": ("", "Algoritmos e Programação"),
    "EF07CO04": ("", "Estruturas de Dados"),
    "EF07CO05": ("", "Decomposição e Abstração"),
    "EF07CO06": ("", "Redes e Internet"),
    "EF07CO07": ("", "Segurança Digital"),
    "EF07CO08": ("", "Cidadania e Ética Digital"),
    "EF07CO09": ("", "Cidadania e Ética Digital"),
    "EF07CO10": ("", "Impacto Social da Tecnologia"),
    "EF07CO11": ("", "Criação Digital"),

    # ── Ensino Fundamental – 8º ano ──────────────────────────────────────────
    "EF08CO01": ("", "Algoritmos e Programação"),
    "EF08CO02": ("", "Estruturas de Dados"),
    "EF08CO03": ("", "Algoritmos e Programação"),
    "EF08CO04": ("", "Algoritmos e Programação"),
    "EF08CO05": ("", "Redes e Internet"),
    "EF08CO06": ("", "Redes e Internet"),
    "EF08CO07": ("", "Cidadania e Ética Digital"),
    "EF08CO08": ("", "Segurança e Privacidade Pessoal"),
    "EF08CO09": ("", "Cidadania e Ética Digital"),
    "EF08CO10": ("", "Segurança e Privacidade Pessoal"),
    "EF08CO11": ("", "Cidadania e Ética Digital"),

    # ── Ensino Fundamental – 9º ano ──────────────────────────────────────────
    "EF09CO01": ("", "Estruturas de Dados"),
    "EF09CO02": ("", "Algoritmos e Programação"),
    "EF09CO03": ("", "Algoritmos e Programação"),
    "EF09CO04": ("", "Segurança Digital"),
    "EF09CO05": ("", "Segurança Digital"),
    "EF09CO06": ("", "Impacto Social da Tecnologia"),
    "EF09CO07": ("", "Impacto Social da Tecnologia"),
    "EF09CO08": ("", "Impacto Social da Tecnologia"),
    "EF09CO09": ("", "Cidadania e Ética Digital"),
    "EF09CO10": ("", "Cidadania e Ética Digital"),

    # ── Ensino Fundamental – Anos Finais (6º–9º, habilidades integradoras) ───
    "EF69CO01": ("", "Estruturas de Dados"),
    "EF69CO02": ("", "Algoritmos e Programação"),
    "EF69CO03": ("", "Algoritmos e Programação"),
    "EF69CO04": ("", "Decomposição e Abstração"),
    "EF69CO05": ("", "Algoritmos e Programação"),
    "EF69CO06": ("", "Algoritmos e Programação"),
    "EF69CO07": ("", "Redes e Internet"),
    "EF69CO08": ("", "Dados e Representação"),
    "EF69CO09": ("", "Redes e Internet"),
    "EF69CO10": ("", "Redes e Internet"),
    "EF69CO11": ("", "Cidadania e Ética Digital"),
    "EF69CO12": ("", "Impacto Social da Tecnologia"),

    # ── Ensino Médio ─────────────────────────────────────────────────────────
    # O CSV não possui campo eixo para o EM; preenchemos aqui.
    "EM13CO01": ("Pensamento Computacional", "Algoritmos e Programação"),
    "EM13CO02": ("Pensamento Computacional", "Decomposição e Abstração"),
    "EM13CO03": ("Pensamento Computacional", "Algoritmos e Programação"),
    "EM13CO04": ("Pensamento Computacional", "Decomposição e Abstração"),
    "EM13CO05": ("Pensamento Computacional", "Decomposição e Abstração"),
    "EM13CO06": ("Mundo Digital",            "Software e Sistemas Operacionais"),
    "EM13CO07": ("Mundo Digital",            "Redes e Internet"),
    "EM13CO08": ("Mundo Digital",            "Segurança Digital"),
    "EM13CO09": ("Mundo Digital",            "Impacto Social da Tecnologia"),
    "EM13CO10": ("Mundo Digital",            "Inteligência Artificial e Ciência de Dados"),
    "EM13CO11": ("Mundo Digital",            "Inteligência Artificial e Ciência de Dados"),
    "EM13CO12": ("Mundo Digital",            "Inteligência Artificial e Ciência de Dados"),
    "EM13CO13": ("Mundo Digital",            "Inteligência Artificial e Ciência de Dados"),
    "EM13CO14": ("Cultura Digital",          "Cidadania e Ética Digital"),
    "EM13CO15": ("Cultura Digital",          "Impacto Social da Tecnologia"),
    "EM13CO16": ("Cultura Digital",          "Criação Digital"),
    "EM13CO17": ("Cultura Digital",          "Criação Digital"),
    "EM13CO18": ("Cultura Digital",          "Criação Digital"),
    "EM13CO19": ("Cultura Digital",          "Criação Digital"),
    "EM13CO20": ("Cultura Digital",          "Criação Digital"),
    "EM13CO21": ("Cultura Digital",          "Criação Digital"),
    "EM13CO22": ("Cultura Digital",          "Criação Digital"),
    "EM13CO23": ("Cultura Digital",          "Impacto Social da Tecnologia"),
    "EM13CO24": ("Cultura Digital",          "Impacto Social da Tecnologia"),
    "EM13CO25": ("Cultura Digital",          "Cidadania e Ética Digital"),
    "EM13CO26": ("Cultura Digital",          "Cidadania e Ética Digital"),
}

# Colunas adicionadas ao CSV
NOVAS_COLUNAS = [
    "objeto_conhecimento",
    "em_foco",
    "mf_classificacao",
    "mf_conhecimento_previo",
    "mf_objetivos",
    "mf_competencias",
    "mf_habilidades_relacionadas",
    "mf_comentarios",
]


def main() -> None:
    with open(COMP_CSV, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)

    # Garante que as novas colunas existem no cabeçalho
    for col in NOVAS_COLUNAS:
        if col not in fieldnames:
            fieldnames.append(col)
            for row in rows:
                row.setdefault(col, "")

    total = len(rows)
    preenchidos = 0

    for row in rows:
        codigo = row.get("codigo", "").strip()
        if codigo not in MAPEAMENTO:
            print(f"[AVISO] {codigo} não está no mapeamento — pulando", file=sys.stderr)
            continue

        eixo_em, obj_con = MAPEAMENTO[codigo]

        # Preenche eixo para habilidades do EM (campo vazio no CSV original)
        if eixo_em and not row.get("eixo", "").strip():
            row["eixo"] = eixo_em
            # unidade_tematica espelha o eixo (mesma convenção do EF)
            row["unidade_tematica"] = eixo_em

        row["objeto_conhecimento"] = obj_con
        preenchidos += 1

    with open(COMP_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    print(f"CSV atualizado: {COMP_CSV}")
    print(f"objeto_conhecimento preenchido: {preenchidos}/{total} habilidades")

    # Resumo por objeto_conhecimento
    from collections import Counter
    contagem = Counter(MAPEAMENTO[r.get("codigo", "")] [1]
                       for r in rows if r.get("codigo") in MAPEAMENTO)
    print("\nDistribuição por objeto_conhecimento:")
    for obj, n in sorted(contagem.items(), key=lambda x: -x[1]):
        print(f"  {n:3}  {obj}")


if __name__ == "__main__":
    main()
