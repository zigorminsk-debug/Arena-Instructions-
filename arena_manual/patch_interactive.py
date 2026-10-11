# -*- coding: utf-8 -*-
"""v1.5: интерактивный PDF — кликабельные скриншоты и ссылки + описание в начале."""

A = '<a href="%s" color="#1d4ed8"><u>%s</u></a>'

URL_BY_FILE = {
    "arena_attach": "https://arena.ai/agent",
    "arena_chatbar": "https://arena.ai/agent",
    "arena_connect": "https://arena.ai/agent",
    "arena_feedback": "https://arena.ai/agent",
    "arena_manage": "https://arena.ai/agent",
    "arena_toggle": "https://arena.ai/agent",
    "arena_workspace": "https://arena.ai/agent",
    "gh_new": "https://github.com/new",
    "gh_create": "https://github.com/new",
    "gh_files": "https://github.com/",
    "gh_upload": "https://github.com/",
    "gh_merge": "https://github.com/pulls",
}

INTRO_RU = '''    # ---------------------------------------------------------- 0. ИНТЕРАКТИВ
    m.h1("Как пользоваться этой инструкцией", "s0")
    m.lead("Этот документ — интерактивный: ссылки в нём кликабельны. Нажмите на синюю "
           "подчёркнутую ссылку или на любой скриншот — и PDF-просмотрщик откроет в браузере "
           "нужную страницу: раздел Arena или страницу GitHub.")
    m.ul([
        "<b>Скриншоты — это кнопки.</b> Каждый скриншот ведёт туда, где он сделан: скриншоты "
        "Arena открывают Agent Mode (arena.ai/agent), скриншоты GitHub — соответствующую "
        "страницу сайта.",
        "<b>Ссылка «открыть страницу ↗» под картинкой</b> — тот же адрес текстом: удобно, если "
        "клик не сработал.",
        "<b>Оглавление кликабельно</b>: клик по главе переносит к ней; вернуться можно кнопкой "
        "«Назад» в просмотрщике PDF.",
        "<b>Синие ссылки в тексте</b> открывают внешние страницы: справку, создание репозитория, "
        "ваши Pull Request'ы.",
    ])
    m.table(
        ["Ссылка", "Куда ведёт", "Зачем нужна"],
        [
            ["<a href=\\"https://arena.ai/agent\\" color=\\"#1d4ed8\\"><u>arena.ai/agent</u></a>",
             "Agent Mode на Arena",
             "Главная рабочая страница: диалог, Workspace, подключения"],
            ["<a href=\\"https://help.arena.ai\\" color=\\"#1d4ed8\\"><u>help.arena.ai</u></a>",
             "Справочный центр Arena", "Официальные ответы, как всё устроено"],
            ["<a href=\\"https://github.com/\\" color=\\"#1d4ed8\\"><u>github.com</u></a>",
             "Ваш GitHub", "Ваши репозитории и файлы"],
            ["<a href=\\"https://github.com/new\\" color=\\"#1d4ed8\\"><u>github.com/new</u></a>",
             "Форма создания репозитория",
             "Шаг из главы 15: создать «шкаф» для документов"],
            ["<a href=\\"https://github.com/pulls\\" color=\\"#1d4ed8\\"><u>github.com/pulls</u></a>",
             "Ваши Pull Request'ы", "Сюда агент приносит результат на согласование"],
        ],
        widths=[1.2, 1.5, 2.4],
    )
    m.callout("info", "Если ссылка не открывается",
              "Кликабельные ссылки работают в PDF-просмотрщиках: браузеры Chrome и Edge, Adobe "
              "Acrobat, «Просмотр» на macOS. В печатной копии все адреса видны текстом — их можно "
              "ввести вручную.")
'''

INTRO_PL = '''    # ---------------------------------------------------------- 0. INTERAKTYW
    m.h1("Jak korzystać z tej instrukcji", "s0")
    m.lead("Ten dokument jest interaktywny: łącza w nim są klikalne. Kliknij niebieskie "
           "podkreślone łącze lub dowolny zrzut ekranu — przeglądarka PDF otworzy potrzebną "
           "stronę: sekcję Arena albo stronę GitHuba.")
    m.ul([
        "<b>Zrzuty ekranu to przyciski.</b> Każdy zrzut prowadzi tam, gdzie go zrobiono: zrzuty "
        "Arena otwierają Agent Mode (arena.ai/agent), zrzuty GitHuba — odpowiednią stronę "
        "serwisu.",
        "<b>Łącze „otwórz stronę ↗” pod obrazkiem</b> to ten sam adres w formie tekstu: "
        "wygodne, gdy klik nie zadziała.",
        "<b>Spis treści jest klikalny</b>: kliknięcie rozdziału przenosi do niego; powrót — "
        "przyciskiem „Wstecz” w przeglądarce PDF.",
        "<b>Niebieskie łącza w tekście</b> otwierają strony zewnętrzne: pomoc, tworzenie "
        "repozytorium, Twoje Pull Requesty.",
    ])
    m.table(
        ["Łącze", "Dokąd prowadzi", "Do czego służy"],
        [
            ["<a href=\\"https://arena.ai/agent\\" color=\\"#1d4ed8\\"><u>arena.ai/agent</u></a>",
             "Agent Mode na Arena",
             "Główna strona robocza: dialog, Workspace, połączenia"],
            ["<a href=\\"https://help.arena.ai\\" color=\\"#1d4ed8\\"><u>help.arena.ai</u></a>",
             "Centrum pomocy Arena", "Oficjalne odpowiedzi, jak wszystko działa"],
            ["<a href=\\"https://github.com/\\" color=\\"#1d4ed8\\"><u>github.com</u></a>",
             "Twój GitHub", "Twoje repozytoria i pliki"],
            ["<a href=\\"https://github.com/new\\" color=\\"#1d4ed8\\"><u>github.com/new</u></a>",
             "Formularz tworzenia repozytorium",
             "Krok z rozdziału 15: utworzyć „szafę” na dokumenty"],
            ["<a href=\\"https://github.com/pulls\\" color=\\"#1d4ed8\\"><u>github.com/pulls</u></a>",
             "Twoje Pull Requesty", "Tu agent przynosi wynik do akceptacji"],
        ],
        widths=[1.2, 1.5, 2.4],
    )
    m.callout("info", "Gdy łącze się nie otwiera",
              "Klikalne łącza działają w przeglądarkach PDF: Chrome, Edge, Adobe Acrobat, "
              "Podgląd na macOS. W wydruku wszystkie adresy zostają w tekście — można je wpisać "
              "ręcznie.")
'''

INLINE_RU = [
    ('Откройте <b>https://arena.ai/agent</b> напрямую.',
     'Откройте ' + A % ("https://arena.ai/agent", "arena.ai/agent") + ' напрямую.'),
    ('бесплатный аккаунт на GitHub (github.com) и аккаунт в Arena',
     'бесплатный аккаунт на GitHub (' + A % ("https://github.com/", "github.com") + ') и аккаунт в Arena'),
    ('Зайдите на github.com и войдите в аккаунт.',
     'Зайдите на ' + A % ("https://github.com/", "github.com") + ' и войдите в аккаунт.'),
    ('Откройте ваш репозиторий на github.com и зайдите в нужную папку',
     'Откройте ваш репозиторий на ' + A % ("https://github.com/", "github.com") + ' и зайдите в нужную папку'),
    ('Откройте Arena в режиме Agent Mode (arena.ai/agent).',
     'Откройте Arena в режиме Agent Mode (' + A % ("https://arena.ai/agent", "arena.ai/agent") + ').'),
]

INLINE_PL = [
    ('Otwórz bezpośrednio <b>https://arena.ai/agent</b>.',
     'Otwórz bezpośrednio ' + A % ("https://arena.ai/agent", "arena.ai/agent") + '.'),
    ('darmowe konto na GitHubie (github.com) i konto',
     'darmowe konto na GitHubie (' + A % ("https://github.com/", "github.com") + ') i konto'),
    ('Wejdź na github.com i zaloguj się na konto.',
     'Wejdź na ' + A % ("https://github.com/", "github.com") + ' i zaloguj się na konto.'),
    ('Otwórz swoje repozytorium na github.com i wejdź do potrzebnego folderu',
     'Otwórz swoje repozytorium na ' + A % ("https://github.com/", "github.com") + ' i wejdź do potrzebnego folderu'),
    ('Otwórz Arena w trybie Agent Mode (arena.ai/agent).',
     'Otwórz Arena w trybie Agent Mode (' + A % ("https://arena.ai/agent", "arena.ai/agent") + ').'),
]


def patch(path, intro, marker, inline):
    src = open(path, encoding="utf-8").read()
    assert marker in src, path
    src = src.replace(marker, intro + marker, 1)
    n = 0
    for fname, url in URL_BY_FILE.items():
        old = 'm.shot("shots/%s.png",' % fname
        cnt = src.count(old)
        if cnt:
            src = src.replace(old, 'm.shot("shots/%s.png", "%s",' % (fname, url))
            n += cnt
    assert n == 18, (path, n)
    for old, new in inline:
        assert src.count(old) == 1, (path, old[:50])
        src = src.replace(old, new, 1)
    open(path, "w", encoding="utf-8").write(src)
    print("patched", path, "intro + 18 urls + %d inline links" % len(inline))


patch("content.py", INTRO_RU,
      "    # ---------------------------------------------------------- 1. ОБЗОР", INLINE_RU)
patch("content_pl.py", INTRO_PL,
      "    # ---------------------------------------------------------- 1. PRZEGLĄD", INLINE_PL)
