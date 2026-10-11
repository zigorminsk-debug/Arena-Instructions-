# -*- coding: utf-8 -*-
"""v1.6: случай пустого репозитория (нет кнопки Add file) + последовательная нумерация рисунков."""
import re

OLD2NEW = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 13, 11: 14, 12: 15, 13: 16, 14: 19, 15: 11, 16: 12, 17: 17, 18: 18}

INSERT_RU = '''    m.p("Если галочку README поставить забыли, репозиторий создастся пустым: на странице не "
        "будет кнопки Add file, а вместо списка файлов появится блок «Quick setup» (рис. 10). "
        "Это не ошибка — нажмите синюю ссылку «uploading an existing file» («загрузить "
        "существующий файл»): откроется то же окно загрузки, а после первого коммита кнопка "
        "Add file появится.")
    m.shot("shots/gh_empty.png", "https://github.com/",
           "Рис. 10. Пустой репозиторий: кнопки Add file ещё нет. Нажмите ссылку «uploading an "
           "existing file» — она откроет окно загрузки и создаст первый коммит. Скриншот "
           "реального репозитория на github.com.")
'''

CALLOUT_RU = '''    m.callout("warn", "Нет кнопки Add file?",
              "Значит, репозиторий пустой — в нём нет ни одного коммита. Нажмите ссылку "
              "«uploading an existing file» в блоке Quick setup (см. рис. 10) или создайте "
              "README прямо на сайте: кнопка «creating a new file».")
'''

INSERT_PL = '''    m.p("Jeśli zapomnisz zaznaczyć README, repozytorium utworzy się puste: na stronie nie "
        "będzie przycisku Add file, a zamiast listy plików pojawi się blok „Quick setup” "
        "(rys. 10). To nie błąd — kliknij niebieskie łącze „uploading an existing file” "
        "(„wgraj istniejący plik”): otworzy się to samo okno wgrywania, a po pierwszym "
        "commicie pojawi się przycisk Add file.")
    m.shot("shots/gh_empty.png", "https://github.com/",
           "Rys. 10. Puste repozytorium: przycisku Add file jeszcze nie ma. Kliknij łącze "
           "„uploading an existing file” — otworzy okno wgrywania i utworzy pierwszy commit. "
           "Zrzut prawdziwego repozytorium na github.com.")
'''

CALLOUT_PL = '''    m.callout("warn", "Nie ma przycisku Add file?",
              "Znaczy to, że repozytorium jest puste — nie ma w nim żadnego commitu. Kliknij "
              "łącze „uploading an existing file” w bloku Quick setup (zob. rys. 10) albo "
              "utwórz README na stronie: przycisk „creating a new file”.")
'''


def renum(src):
    def repl(mo):
        n = int(mo.group(2))
        return "%s%d" % (mo.group(1), OLD2NEW.get(n, n))
    # двухпроходная замена через временные метки, чтобы 15->11 не попало под 11->14
    def repl1(mo):
        n = int(mo.group(2))
        return "%s@@%d@@" % (mo.group(1), n)
    src = re.sub(r"((?:Рис|рис|Rys|rys)\.\s)(\d+)", repl1, src)
    src = re.sub(r"@@(\d+)@@", lambda mo: str(OLD2NEW[int(mo.group(1))]), src)
    return src


def patch(path, marker_shot9, marker_callout3):
    src = open(path, encoding="utf-8").read()
    src = renum(src)
    insert = INSERT_RU if path == "content.py" else INSERT_PL
    callout = CALLOUT_RU if path == "content.py" else CALLOUT_PL
    assert src.count(marker_shot9) == 1, path
    src = src.replace(marker_shot9, marker_shot9 + "\n" + insert, 1)
    assert src.count(marker_callout3) == 1, path
    src = src.replace(marker_callout3, callout + marker_callout3, 1)
    open(path, "w", encoding="utf-8").write(src)
    print("patched", path)


patch("content.py",
      '           "Рис. 9. Готовый репозиторий (скриншот docs.github.com): ветка main, первый коммит Initial commit и файл README.md в списке.")',
      '    m.callout("warn", "Word и Excel не загружаются в чат Arena",')
patch("content_pl.py",
      '           "Rys. 9. Gotowe repozytorium (zrzut z docs.github.com): gałąź main, pierwszy commit Initial commit i plik README.md na liście.")',
      '    m.callout("warn", "Word i Excel nie wgrywają się do czatu Arena",')
