import os
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Configura tema Dracula e parâmetros do GIF por padrão
os.environ.setdefault("GIFOS_GENERAL_COLOR_SCHEME", "dracula")
os.environ.setdefault("GIFOS_GENERAL_FPS", "20")
os.environ.setdefault("GIFOS_GENERAL_LOOP_COUNT", "1")

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

    # Terminal ampliado para acomodar inicialização com fonte 18 e restante com fonte 16
    t = gifos.Terminal(1150, 820, 15, 15, str(FONT_TERMINAL_PATH), 18)
    t.set_prompt(f"\x1b[0;91m{USERNAME}\x1b[0m@\x1b[0;93mreadme\x1b[0;97m:\x1b[0;92m~\x1b[0;97m$ \x1b[0m")

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

    # Logo com Silkscreen (Google Fonts)
    t.set_font(str(FONT_LOGO_PATH), 64)
    os_logo_text = "GABRIEL MELO"
    mid_row = (t.num_rows + 1) // 2
    mid_col = (t.num_cols - len(os_logo_text) + 1) // 2
    effect_lines = gifos.effects.text_scramble_effect_lines(
        os_logo_text, 3, include_special=False
    )
    for i in range(len(effect_lines)):
        t.delete_row(mid_row + 1)
        t.gen_text(effect_lines[i], mid_row + 1, mid_col + 1)

    # Retorna ao terminal com Fira Code
    t.set_font(str(FONT_TERMINAL_PATH), 16)
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
    \x1b[96mOS:\x1b[0m     \x1b[93mWeb, Android, Arduino\x1b[0m
    \x1b[96mHost:\x1b[0m   \x1b[93mUFC #SMD\x1b[0m
    \x1b[96mKernel:\x1b[0m \x1b[93mDeveloper\x1b[0m
    \x1b[96mUptime:\x1b[0m \x1b[93m{user_age.years} years, {user_age.months} months, {user_age.days} days\x1b[0m
    \x1b[96mIDE:\x1b[0m    \x1b[93mVSCode, Pycharm, Android Studio\x1b[0m

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
    \x1b[96mTop Langs:\x1b[0m     \x1b[93m{', '.join(top_languages[:6])}\x1b[0m
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
    # Renderiza o Tux Big e as informações lado a lado
    t.gen_text(tux_art, 2, 1)
    t.gen_text(user_details_lines, 2, 47, count=5, contin=True)

    t.toggle_show_cursor(True)
    t.gen_prompt(28)
    t.gen_typing_text(
        "\x1b[92m# Obrigado pela visita! Tenha um otimo dia :D\x1b[0m",
        28,
        contin=True,
    )
    t.gen_text("", 28, count=120, contin=True)

    t.gen_gif()

    readme_file_content = rf"""<div align="center">
<picture>
    <source media="(prefers-color-scheme: dark)" srcset="./output.gif">
    <source media="(prefers-color-scheme: light)" srcset="./output.gif">
    <img alt="GIFOS" src="output.gif">
</picture>

<br><br>

<details>
<summary><b>🔍 Mais detalhes / About Me</b></summary>
<br>

### 👨‍💻 Sobre mim
- 🎓 Graduando em **Sistemas e Mídias Digitais** pela Universidade Federal do Ceará (**UFC**).
- 🔬 Bolsista de suporte e pesquisa no laboratório **LEAD** (UECE & Dell Technologies).
- 🚀 Foco em desenvolvimento **FullStack** e sistemas embarcados.

### 🌐 Redes & Contato
- 💼 **LinkedIn:** [araujosemacento](https://linkedin.com/in/araujosemacento)
- 📸 **Instagram:** [@araujo.sem.acento](https://instagram.com/araujo.sem.acento)
- ✉️ **Email:** [araujosemacento@alu.ufc.br](mailto:araujosemacento@alu.ufc.br)

### 🛠️ Principais Tecnologias
- **Linguagens:** Python, TypeScript, JavaScript, Kotlin, Java, C
- **Front-End:** React, Svelte, Astro, Next.js, TailwindCSS
- **Back-End:** FastAPI, Django, Flask, Node.js
- **Bancos de Dados:** PostgreSQL, MySQL, MongoDB, Firebase
- **Dev Tools:** Git, Docker, Linux, PyCharm, VSCode

</details>
</div>
"""
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_file_content)
        print("INFO: README.md file generated")


if __name__ == "__main__":
    main()
