#!/usr/bin/env python3
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).parent
OUT = ROOT / "leanprover-community-zh.pdf"

SOURCES = [
    "data/presentation.md",
    "data/what_is.md",
    "templates/get_started.md",
    "templates/learn.md",
    "templates/glossary.md",
    "templates/did_you_prove_it.md",
    "templates/mwe.md",
    "templates/cite.md",
    "templates/latex.md",
    "templates/theories.md",
    "templates/theories/naturals.md",
    "templates/theories/sets.md",
    "templates/theories/linear_algebra.md",
    "templates/theories/topology.md",
    "templates/theories/category_theory.md",
    "templates/extras/calc.md",
    "templates/extras/congr.md",
    "templates/extras/conv.md",
    "templates/extras/simp.md",
    "templates/extras/speedup.md",
    "templates/extras/well_founded_recursion.md",
    "templates/extras/tactic_writing.md",
    "templates/extras/pitfalls.md",
    "templates/contribute/index.md",
    "templates/contribute/values.md",
    "templates/contribute/how-to-contribute.md",
    "templates/contribute/git.md",
    "templates/contribute/naming.md",
    "templates/contribute/style.md",
    "templates/contribute/doc.md",
    "templates/contribute/commit.md",
    "templates/contribute/pr-review.md",
    "templates/contribute/tags_and_branches.md",
    "templates/community_guidelines.md",
    "templates/teaching/index.md",
    "templates/teaching/resources.md",
    "templates/teaching/practices.md",
]


def strip_jinja(text: str) -> str:
    text = re.sub(r"{%\s*raw\s*%}", "", text)
    text = re.sub(r"{%\s*endraw\s*%}", "", text)
    text = re.sub(r"{%\s*markdown\s*%}", "", text)
    text = re.sub(r"{%\s*endmarkdown\s*%}", "", text)
    text = re.sub(r"{%.*?%}", "", text, flags=re.S)
    text = re.sub(r"{{\s*([^{}|]+?)\s*}}", r"`\1`", text)
    text = text.replace(r"$\TeX$", "TeX")
    text = text.replace(r"$\LaTeX$", "LaTeX")
    text = text.replace(r"\begin{align}", r"\begin{aligned}")
    text = text.replace(r"\end{align}", r"\end{aligned}")
    return text


def available_font_families() -> set[str]:
    try:
        completed = subprocess.run(
            ["fc-list", ":", "family"],
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            errors="ignore",
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return set()
    families: set[str] = set()
    for line in completed.stdout.splitlines():
        for family in line.split(","):
            family = family.strip().replace("\\-", "-")
            if family:
                families.add(family)
    return families


def choose_font(candidates: list[str], default: str) -> str:
    families = available_font_families()
    for candidate in candidates:
        if candidate in families:
            return candidate
    return default


def main() -> int:
    cjk_font = choose_font(
        [
            "Noto Serif CJK SC",
            "Source Han Serif SC",
            "SimSun",
            "NSimSun",
            "Microsoft YaHei",
            "Noto Serif SC",
        ],
        "Noto Serif SC",
    )
    main_font = choose_font(["Noto Serif", "Times New Roman"], cjk_font)
    mono_font = choose_font(["Noto Sans Mono", "Consolas"], "Noto Sans Mono")
    combined = [
        "---",
        "title: Lean 社区文档",
        "documentclass: ctexbook",
        "geometry: margin=2.5cm",
        "---",
        "",
    ]
    for src in SOURCES:
        path = ROOT / src
        text = path.read_text(encoding="utf-8")
        text = strip_jinja(text)
        combined.extend(["", f"<!-- source: {src} -->", "", text.strip(), ""])

    tmp = ROOT / "build" / "leanprover-community-zh.md"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text("\n".join(combined), encoding="utf-8", newline="\n")
    header = ROOT / "build" / "leanprover-community-zh-header.tex"
    header.write_text(
        "\n".join(
            [
                r"\newcommand{\lt}{<}",
                r"\newcommand{\gt}{>}",
                r"\newcommand{\N}{\mathbb{N}}",
                r"\newcommand{\Z}{\mathbb{Z}}",
                r"\newcommand{\Q}{\mathbb{Q}}",
                r"\newcommand{\R}{\mathbb{R}}",
                r"\newcommand{\C}{\mathbb{C}}",
            ]
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    cmd = [
        "pandoc",
        str(tmp),
        "--from",
        "markdown+tex_math_dollars-raw_tex",
        "--include-in-header",
        str(header),
        "--pdf-engine=xelatex",
        "-V",
        f"CJKmainfont={cjk_font}",
        "-V",
        f"mainfont={main_font}",
        "-V",
        f"monofont={mono_font}",
        "-o",
        str(OUT),
    ]
    subprocess.run(cmd, cwd=ROOT, check=True)
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
