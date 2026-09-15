import os

# Configura tema Dracula e parâmetros do GIF antes de qualquer import do gifos
os.environ["GIFOS_GENERAL_COLOR_SCHEME"] = "dracula"
os.environ["GIFOS_GENERAL_FPS"] = "20"
os.environ["GIFOS_GENERAL_LOOP_COUNT"] = "1"

import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import gifos
from gifos.utils.schemas.github_user_stats import GithubUserStats
from gifos.utils.schemas.github_user_rank import GithubUserRank

# Configuração de Google Fonts
FONTS_DIR = Path("./.fonts")
FONT_LOGO_PATH = FONTS_DIR / "Silkscreen-Regular.ttf"
FONT_TERMINAL_PATH = FONTS_DIR / "FiraCode-Regular.ttf"

GOOGLE_FONTS = {
    FONT_LOGO_PATH: "https://raw.githubusercontent.com/google/fonts/main/ofl/silkscreen/Silkscreen-Regular.ttf",
    FONT_TERMINAL_PATH: "https://raw.githubusercontent.com/google/fonts/main/ofl/firacode/FiraCode%5Bwght%5D.ttf",
}

USERNAME = "araujosemacento"
TIMEZONE = "America/Fortaleza"


def ensure_fonts():
    """Garante o download automático das fontes do Google Fonts para cache local."""
    FONTS_DIR.mkdir(parents=True, exist_ok=True)
    for font_path, url in GOOGLE_FONTS.items():
        if not font_path.exists():
            print(f"INFO: Baixando fonte do Google Fonts: {font_path.name}...")
            urllib.request.urlretrieve(url, font_path)
            print(f"INFO: {font_path.name} pronta para uso!")


def get_user_stats(username: str, ignore_repos: list = None) -> GithubUserStats:
    """Busca as estatísticas do GitHub com fallback seguro para execuções locais sem GITHUB_TOKEN."""
    if os.getenv("GITHUB_TOKEN"):
        try:
            return gifos.utils.fetch_github_stats(username, ignore_repos or [])
        except Exception as e:
            print(f"WARN: Erro ao buscar dados com GITHUB_TOKEN ({e}). Usando fallback.")

    print("INFO: GITHUB_TOKEN não encontrado no ambiente. Usando dados padrão para pré-visualização.")
    return GithubUserStats(
        account_name="G. Melo",
        total_followers=9,
        total_stargazers=8,
        total_issues=1,
        total_commits_all_time=440,
        total_commits_last_year=117,
        total_pull_requests_made=6,
        total_pull_requests_merged=3,
        pull_requests_merge_percentage=50.0,
        total_pull_requests_reviewed=0,
        total_repo_contributions=1,
        languages_sorted=[
            ("JavaScript", 71.93),
            ("HTML", 22.65),
            ("Svelte", 1.91),
            ("TypeScript", 1.29),
            ("Python", 1.19),
            ("CSS", 0.28),
        ],
        user_rank=GithubUserRank(level="C+", percentile=84.61),
    )


def main():
    ensure_fonts()

    t = gifos.Terminal(1280, 820, 15, 15, str(FONT_TERMINAL_PATH), 20)
    t.set_prompt(f"\x1b[91m{USERNAME}\x1b[0m@\x1b[93mreadme\x1b[97m:\x1b[92m~\x1b[97m$ \x1b[0m")

    t.gen_text("", 1, count=20)
    t.toggle_show_cursor(False)
    year_now = datetime.now(ZoneInfo(TIMEZONE)).strftime("%Y")
    t.gen_text("Modular BIOS v1.0.11", 1)
    t.gen_text(f"Copyright (C) {year_now}, \x1b[31mGabriel Melo\x1b[0m", 2)
    t.gen_text("\x1b[94mGitHub Profile ReadMe Terminal, Rev 1011\x1b[0m", 4)
    t.gen_text("Suzuma(tm) CPU - 1.68 THz", 6)
    t.gen_text(
        "Press \x1b[94mDEL\x1b[0m or \x1b[94mF2\x1b[0m to enter UEFI BIOS Setting",
        t.num_rows,
    )
    for i in range(0, 131072, 6554):  # 16G Memory
        t.delete_row(7)
        if i < 30000:
            t.gen_text(
                f"Memory Test: {i}", 7, count=2, contin=True
            )
        else:
            t.gen_text(f"Memory Test: {i}", 7, contin=True)
    t.delete_row(7)
    t.gen_text("Memory Test: 16GB OK", 7, count=10, contin=True)
    t.gen_text("", 11, count=10, contin=True)

    t.clear_frame()
    t.gen_text("Initiating Boot Sequence ", 1, contin=True)
    t.gen_typing_text(".....", 1, contin=True)
    t.gen_text("\x1b[96m", 1, count=0, contin=True)

    # Logo com Silkscreen (Google Fonts) com centralização
    orig_xpad = t._Terminal__xpad
    orig_ypad = t._Terminal__ypad
    t.set_font(str(FONT_LOGO_PATH), 72)
    os_logo_text = "GABRIEL MELO"

    logo_bbox = t._Terminal__font.getbbox(os_logo_text)
    logo_w = logo_bbox[2] - logo_bbox[0]
    logo_h = logo_bbox[3] - logo_bbox[1]
    t._Terminal__xpad = int((t._Terminal__width - logo_w) / 2 - logo_bbox[0])
    t._Terminal__ypad = int((t._Terminal__height - logo_h) / 2 - logo_bbox[1])
    t.num_rows = 1
    t.num_cols = len(os_logo_text)
    t._Terminal__col_in_row = {1: 1}

    effect_lines = gifos.effects.text_scramble_effect_lines(
        os_logo_text, 3, include_special=False
    )
    for i in range(len(effect_lines)):
        t.delete_row(1)
        t.gen_text(effect_lines[i], 1, 1)

    t._Terminal__xpad = orig_xpad
    t._Terminal__ypad = orig_ypad
    t.set_font(str(FONT_TERMINAL_PATH), 18)
    t.clear_frame()
    t.clone_frame(5)
    t.toggle_show_cursor(False)
    t.gen_text("\x1b[93mREADME OS v1.0.11 (tty1)\x1b[0m", 1, count=5)
    t.gen_text("login: ", 3, count=5)
    t.toggle_show_cursor(True)
    t.gen_typing_text(USERNAME, 3, contin=True)
    t.gen_text("", 4, count=5)
    t.toggle_show_cursor(False)
    t.gen_text("password: ", 4, count=5)
    t.toggle_show_cursor(True)
    t.gen_typing_text("***********", 4, contin=True)
    t.toggle_show_cursor(False)
    time_now = datetime.now(ZoneInfo(TIMEZONE)).strftime(
        "%a %b %d %I:%M:%S %p %Z %Y"
    )
    t.gen_text(f"Last login: {time_now} on tty1", 6)

    t.gen_prompt(7, count=5)
    prompt_col = t.curr_col
    t.toggle_show_cursor(True)
    t.gen_typing_text("\x1b[91mclea", 7, contin=True)
    t.delete_row(7, prompt_col)
    t.gen_text("\x1b[92mclear\x1b[0m", 7, count=3, contin=True)

    ignore_repos = []
    git_user_details = get_user_stats(USERNAME, ignore_repos)
    user_age = gifos.utils.calc_age(29, 8, 2002)

    t.clear_frame()
    top_languages = [lang[0] for lang in git_user_details.languages_sorted]

    # Tux Big ASCII art
    tux_lines = [
        r"                  \x1b[97m.88888888:.\x1b[0m",
        r"                 \x1b[97m88888888.88888.\x1b[0m",
        r"               \x1b[97m.8888888888888888.\x1b[0m",
        r"               \x1b[97m888888888888888888\x1b[0m",
        r"               \x1b[97m88' _`88'_  `88888\x1b[0m",
        r"               \x1b[97m88 88 88 88  88888\x1b[0m",
        r"               \x1b[97m88_88_::_88_:88888\x1b[0m",
        r"               \x1b[97m88\x1b[93m:::,::,:::::\x1b[97m8888\x1b[0m",
        r"               \x1b[97m88\x1b[93m`:::::::::'`\x1b[97m8888\x1b[0m",
        r"              \x1b[97m.88  \x1b[93m`::::'    \x1b[97m8:88.\x1b[0m",
        r"             \x1b[97m8888            `8:888.\x1b[0m",
        r"           \x1b[97m.8888'             `888888.\x1b[0m",
        r"          \x1b[97m.8888:..  .::.  ...:'8888888:.\x1b[0m",
        r"         \x1b[97m.8888.'     :'     `'::`88:88888\x1b[0m",
        r"        \x1b[97m.8888        '         `.888:8888.\x1b[0m",
        r"       \x1b[97m888:8         .           888:88888\x1b[0m",
        r"     \x1b[97m.888:88        .:           888:88888:\x1b[0m",
        r"     \x1b[97m8888888.       ::           88:888888\x1b[0m",
        r"     \x1b[97m`\x1b[93m.::.\x1b[97m888.      ::          .88888888\x1b[0m",
        r"    \x1b[93m.::::::.\x1b[97m888.    ::         :\x1b[93m::`\x1b[97m8888\x1b[93m'.:.\x1b[0m",
        r"   \x1b[93m::::::::::.\x1b[97m888   '         .:\x1b[93m:::::::::::\x1b[0m",
        r"   \x1b[93m::::::::::::.\x1b[97m8    '      .:8\x1b[93m::::::::::::.\x1b[0m",
        r"  \x1b[93m.::::::::::::::\x1b[97m.        .:888\x1b[93m:::::::::::::\x1b[0m",
        r"  \x1b[93m:::::::::::::::\x1b[97m88:.__..:88888\x1b[93m:::::::::::'\x1b[0m",
        r"   \x1b[93m`'.:::::::::::\x1b[97m88888888888.88\x1b[93m:::::::::'\x1b[0m",
        r"         \x1b[93m`':::_:\x1b[97m' -- '' -'-' `'\x1b[93m:_::::'`\x1b[0m",
    ]
    tux_art = "\n".join(tux_lines)

    top_tier = max(1, round(100 - git_user_details.user_rank.percentile))

    user_details_lines = f"""
    \x1b[30;105m{USERNAME}@GitHub\x1b[0m
    ----------------------
    \x1b[96mOS:\x1b[0m     \x1b[93mWeb, Linux, IoT\x1b[0m
    \x1b[96mHost:\x1b[0m   \x1b[93mUFC #SMD\x1b[0m
    \x1b[96mKernel:\x1b[0m \x1b[93mDeveloper\x1b[0m
    \x1b[96mUptime:\x1b[0m \x1b[93m{user_age.years} years, {user_age.months} months, {user_age.days} days\x1b[0m
    \x1b[96mIDE:\x1b[0m    \x1b[93mVSCode, PyCharm\x1b[0m

    \x1b[30;105mContact:\x1b[0m
    ----------------------
    \x1b[96mEmail:\x1b[0m     \x1b[93mgabrielmeloentries@gmail.com\x1b[0m
    \x1b[96mLinkedIn:\x1b[0m  \x1b[93maraujosemacento\x1b[0m

    \x1b[30;105mGitHub Stats:\x1b[0m
    ----------------------
    \x1b[96mTotal Commits:\x1b[0m \x1b[93m{git_user_details.total_commits_all_time}+ ({git_user_details.total_commits_last_year} em {int(year_now) - 1})\x1b[0m
    \x1b[96mRanking:\x1b[0m       \x1b[93mTop {top_tier}% do GitHub\x1b[0m
    \x1b[96mTotal Stars:\x1b[0m   \x1b[93m{git_user_details.total_stargazers}\x1b[0m
    \x1b[96mFollowers:\x1b[0m     \x1b[93m{git_user_details.total_followers}\x1b[0m
    \x1b[96mTop Langs:\x1b[0m     \x1b[93m{', '.join(top_languages[:5])}\x1b[0m
"""


    t.gen_prompt(1)
    prompt_col = t.curr_col
    t.clone_frame(10)
    t.toggle_show_cursor(True)
    t.gen_typing_text("\x1b[91mfetch.s", 1, contin=True)
    t.delete_row(1, prompt_col)
    t.gen_text("\x1b[92mfetch.sh\x1b[0m", 1, contin=True)
    t.gen_typing_text(f" -u {USERNAME}", 1, contin=True)

    t.toggle_show_cursor(False)
    t.gen_text(tux_art, 2, 4)
    t.gen_text(user_details_lines, 2, 50, count=5, contin=True)

    t.toggle_show_cursor(True)
    prompt_row = t.num_rows
    t.gen_prompt(prompt_row)
    t.gen_typing_text(
        "\x1b[92m# Obrigado pela visita! Tenha um otimo dia :D\x1b[0m",
        prompt_row,
        contin=True,
    )
    t.gen_text("", prompt_row, count=120, contin=True)

    t.gen_gif()

    readme_file_content = rf"""<div align="center">
<picture>
    <source media="(prefers-color-scheme: dark)" srcset="./output.gif">
    <source media="(prefers-color-scheme: light)" srcset="./output.gif">
    <img alt="GIFOS" src="output.gif">
</picture>

<picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/{USERNAME}/{USERNAME}/output/github-contribution-grid-snake-dark.gif">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/{USERNAME}/{USERNAME}/output/github-contribution-grid-snake.gif">
    <img alt="github-contribution-grid-snake" src="https://raw.githubusercontent.com/{USERNAME}/{USERNAME}/output/github-contribution-grid-snake.gif">
</picture>
</div>

## Sobre mim

#### Quem sou eu
```bash
{USERNAME}@readme:~$ whoami
```
- {user_age.years} anos, natural de Fortaleza - Ceará, Brasil.
- Graduando em **Sistemas e Mídias Digitais** pela Universidade Federal do Ceará (**UFC**).
- Foco de atuação em desenvolvimento **Front-End**, com experiência **FullStack** e **Sistemas Embarcados**.

#### Contatos
```bash
{USERNAME}@readme:~$ contact --list
```
<ul>
<li>
  <a href="https://github.com/araujosemacento" target="_blank">
    <img src="https://img.shields.io/badge/GitHub-araujosemacento-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub" />
  </a>
</li>
<li>
  <a href="https://linkedin.com/in/araujosemacento" target="_blank">
    <img src="https://img.shields.io/badge/LinkedIn-araujosemacento-0A66C2?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn" />
  </a>
</li>
<li>
  <a href="mailto:gabrielmeloentries@gmail.com">
    <img src="https://img.shields.io/badge/Email-gabrielmeloentries%40gmail.com-D14836?style=flat-square&logo=gmail&logoColor=white" alt="Email" />
  </a>
</li>
</ul>

#### Tech Stack
```bash
{USERNAME}@readme:~$ techstack --table
```
| Categoria | Tecnologias |
| :--- | :--- |
| **Front-End** | <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/svelte/svelte-original.svg" alt="Svelte" title="Svelte" width="28" height="28" /> &nbsp; <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg" alt="React" title="React" width="28" height="28" /> &nbsp; <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nextjs/nextjs-original.svg" alt="Next.js" title="Next.js" width="28" height="28" /> &nbsp; <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-original.svg" alt="TypeScript" title="TypeScript" width="28" height="28" /> &nbsp; <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/tailwindcss/tailwindcss-original.svg" alt="TailwindCSS" title="TailwindCSS" width="28" height="28" /> |
| **Back-End** | <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" alt="Python" title="Python" width="28" height="28" /> &nbsp; <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nodejs/nodejs-original.svg" alt="Node.js" title="Node.js" width="28" height="28" /> &nbsp; <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/java/java-original.svg" alt="Java" title="Java" width="28" height="28" /> |
| **Banco de Dados** | <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" alt="PostgreSQL" title="PostgreSQL" width="28" height="28" /> &nbsp; <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mysql/mysql-original.svg" alt="MySQL" title="MySQL" width="28" height="28" /> &nbsp; <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/sqlite/sqlite-original.svg" alt="SQLite" title="SQLite" width="28" height="28" /> &nbsp; <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/firebase/firebase-plain.svg" alt="Firebase" title="Firebase" width="28" height="28" /> |
| **Ferramentas & Habilidades** | <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/git/git-original.svg" alt="Git" title="Git" width="28" height="28" /> &nbsp; <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/githubactions/githubactions-original.svg" alt="GitHub Actions" title="GitHub Actions" width="28" height="28" /> &nbsp; <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg" alt="Docker" title="Docker" width="28" height="28" /> &nbsp; <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linux/linux-original.svg" alt="Linux" title="Linux" width="28" height="28" /> &nbsp; <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/figma/figma-original.svg" alt="Figma" title="Figma" width="28" height="28" /> &nbsp; <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/arduino/arduino-original.svg" alt="Arduino" title="Arduino" width="28" height="28" /> |

<details>
  <summary><b>Visualizar tecnologias por extenso</b></summary>

| Categoria | Tecnologias |
| :--- | :--- |
| **Front-End** | <ul><li>Svelte</li><li>React</li><li>Next.js</li><li>TypeScript</li><li>TailwindCSS</li></ul> |
| **Back-End** | <ul><li>Python</li><li>Node.js</li><li>Java</li></ul> |
| **Banco de Dados** | <ul><li>PostgreSQL</li><li>MySQL</li><li>SQLite</li><li>Firebase</li></ul> |
| **Ferramentas & Habilidades** | <ul><li>Git</li><li>GitHub Actions</li><li>Docker</li><li>Linux</li><li>Figma</li><li>Arduino</li></ul> |

</details>

<p align="center">
  <sub>We love <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/fedora/fedora-original.svg" alt="Fedora Linux" width="10" height="10" /> in this household</sub>
</p>
"""
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_file_content)
        print("INFO: README.md file generated")


if __name__ == "__main__":
    main()
