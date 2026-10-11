# -*- coding: utf-8 -*-
"""v1.7: скрин формы с галочкой README и кнопкой Create repository + раздел 15.10
(переименовать / перенести / удалить репозиторий)."""
import re

SHOT9_RU = '''    m.shot("shots/gh_readme.png", "https://github.com/new",
           "Рис. 9. Низ формы создания (скриншот формы на github.com): поставьте галочку "
           "«Add a README file» и нажмите зелёную кнопку «Create repository» — тогда "
           "репозиторий создастся не пустым и кнопка Add file появится сразу.")
'''
SHOT9_PL = '''    m.shot("shots/gh_readme.png", "https://github.com/new",
           "Rys. 9. Dół formularza tworzenia (zrzut formularza na github.com): zaznacz "
           "„Add a README file” i kliknij zielony przycisk „Create repository” — wtedy "
           "repozytorium nie będzie puste i przycisk Add file pojawi się od razu.")
'''

MGR_RU = '''
    m.h2("15.10. Управление репозиторием: переименовать, перенести, удалить", "sn-mgr")
    m.p("Всё управление репозиторием живёт в его настройках: в шапке репозитория нажмите вкладку "
        "Settings (рис. 21). Откроется страница General: сверху — поле имени, внизу — блок "
        "«Danger Zone» с опасными действиями.")
    m.shot("shots/gh_settings.png", "https://github.com/",
           "Рис. 21. Шапка репозитория: вкладка Settings обведена — через неё вход в настройки "
           "(скриншот из официальной документации docs.github.com).")
    m.h3("Переименовать")
    m.ol([
        "Settings → самое верхнее поле Repository name («имя репозитория»).",
        "Впишите новое имя и нажмите кнопку Rename рядом с полем.",
        "Старые ссылки на репозиторий продолжат работать: GitHub сам перенаправляет на новое имя.",
    ])
    m.h3("Перенести в другой аккаунт или организацию")
    m.ol([
        "Settings → прокрутите вниз до блока Danger Zone (рис. 22).",
        "Строка Transfer ownership («передача владения») → кнопка Transfer.",
        "Укажите нового владельца и подтвердите. Репозиторий переедет вместе со всеми файлами "
        "и историей.",
    ])
    m.h3("Удалить")
    m.ol([
        "Danger Zone → строка Delete this repository → кнопка Delete this repository.",
        "В окне подтверждения нажмите «I want to delete this repository», прочитайте "
        "предупреждения и впишите имя репозитория.",
        "Репозиторий удалится вместе со всеми файлами. Часть удалённых репозиториев можно "
        "восстановить в течение 90 дней, но считайте, что удаление необратимо.",
    ])
    m.shot("shots/gh_danger.png", "https://github.com/",
           "Рис. 22. Блок Danger Zone внизу страницы Settings: Transfer — перенести репозиторий "
           "другому владельцу, Delete this repository — удалить (скриншот github.com).")
    m.callout("bad", "Удаляйте, только если уверены",
              "После удаления агент потеряет доступ к файлам, а ваши документы исчезнут из "
              "репозитория. Сначала скачайте всё ценное на компьютер. Если репозиторий просто "
              "мешает — переименуйте или перенесите его, а не удаляйте.")
'''

MGR_PL = '''
    m.h2("15.10. Zarządzanie repozytorium: zmienić nazwę, przenieść, usunąć", "sn-mgr")
    m.p("Całe zarządzanie repozytorium mieszka w jego ustawieniach: w nagłówku repozytorium "
        "kliknij zakładkę Settings (rys. 21). Otworzy się strona General: u góry — pole nazwy, "
        "na dole — blok „Danger Zone” z niebezpiecznymi akcjami.")
    m.shot("shots/gh_settings.png", "https://github.com/",
           "Rys. 21. Nagłówek repozytorium: zakładka Settings obwiedziona — tędy wchodzisz w "
           "ustawienia (zrzut z oficjalnej dokumentacji docs.github.com).")
    m.h3("Zmienić nazwę")
    m.ol([
        "Settings → najwyżej położone pole Repository name („nazwa repozytorium”).",
        "Wpisz nową nazwę i kliknij przycisk Rename obok pola.",
        "Stare łącza do repozytorium będą działać: GitHub sam przekierowuje na nową nazwę.",
    ])
    m.h3("Przenieść na inne konto lub organizację")
    m.ol([
        "Settings → przewiń na dół do bloku Danger Zone (rys. 22).",
        "Wiersz Transfer ownership („przeniesienie własności”) → przycisk Transfer.",
        "Wskaż nowego właściciela i potwierdź. Repozytorium pojedzie razem ze wszystkimi "
        "plikami i historią.",
    ])
    m.h3("Usunąć")
    m.ol([
        "Danger Zone → wiersz Delete this repository → przycisk Delete this repository.",
        "W oknie potwierdzenia kliknij „I want to delete this repository”, przeczytaj "
        "ostrzeżenia i wpisz nazwę repozytorium.",
        "Repozytorium usunie się razem ze wszystkimi plikami. Część usuniętych repozytoriów "
        "można przywrócić w ciągu 90 dni, ale zakładaj, że usunięcie jest nieodwracalne.",
    ])
    m.shot("shots/gh_danger.png", "https://github.com/",
           "Rys. 22. Blok Danger Zone na dole strony Settings: Transfer — przenieś repozytorium "
           "innemu właścicielowi, Delete this repository — usuń (zrzut github.com).")
    m.callout("bad", "Usuwaj tylko, gdy jesteś pewien",
              "Po usunięciu agent straci dostęp do plików, a Twoje dokumenty znikną z "
              "repozytorium. Najpierw pobierz wszystko, co cenne, na komputer. Jeśli "
              "repozytorium po prostu przeszkadza — zmień nazwę albo przenieś je, nie usuwaj.")
'''

OLD_STEPS_RU = '''        "Поставьте галочку Add a README file — так папка создастся не пустой.",
        "Нажмите зелёную кнопку Create repository — рис. 8.",'''
NEW_STEPS_RU = '''        "Внизу формы поставьте галочку Add a README file («добавить файл README») и нажмите "
        "зелёную кнопку Create repository («создать репозиторий») — папка создастся не пустой, "
        "и кнопка Add file появится сразу (рис. 9).",'''

OLD_STEPS_PL = '''        "Zaznacz Add a README file — dzięki temu folder nie utworzy się pusty.",
        "Kliknij zielony przycisk Create repository — rys. 8.",'''
NEW_STEPS_PL = '''        "Na dole formularza zaznacz Add a README file („dodaj plik README”) i kliknij zielony "
        "przycisk Create repository („utwórz repozytorium”) — folder nie będzie pusty, a "
        "przycisk Add file pojawi się od razu (rys. 9).",'''


def renum(src):
    src = re.sub(r"((?:Рис|рис|Rys|rys)\.\s)(\d+)",
                 lambda mo: mo.group(1) + "@@%d@@" % int(mo.group(2)), src)
    return re.sub(r"@@(\d+)@@",
                  lambda mo: str(int(mo.group(1)) + 1) if 9 <= int(mo.group(1)) <= 19 else mo.group(1),
                  src)


def patch(path, shot9, mgr, marker8, marker16, old_steps=None, new_steps=None):
    src = open(path, encoding="utf-8").read()
    src = renum(src)
    if old_steps:
        assert src.count(old_steps) == 1, path
        src = src.replace(old_steps, new_steps, 1)
    assert src.count(marker8) == 1, path
    src = src.replace(marker8, marker8 + "\n" + shot9, 1)
    assert src.count(marker16) == 1, path
    src = src.replace(marker16, mgr + "\n" + marker16, 1)
    open(path, "w", encoding="utf-8").write(src)
    print("patched", path)


patch("content.py", SHOT9_RU, MGR_RU,
      '             "Рис. 8. Форма создания репозитория (скриншот docs.github.com): Owner — владелец аккаунта, Repository name — имя репозитория; зелёная надпись «is available» — имя свободно.")',
      '    m.h1("16. Глоссарий: простые слова вместо терминов", "gl")',
      OLD_STEPS_RU, NEW_STEPS_RU)

patch("content_pl.py", SHOT9_PL, MGR_PL,
      '             "Rys. 8. Formularz tworzenia repozytorium (zrzut z docs.github.com): Owner — właściciel konta, Repository name — nazwa repozytorium; zielony napis „is available” — nazwa jest wolna.")',
      '    m.h1("16. Słowniczek: proste słowa zamiast terminów", "gl")',
      OLD_STEPS_PL, NEW_STEPS_PL)
