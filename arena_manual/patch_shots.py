# -*- coding: utf-8 -*-
"""v1.4: заменяем все нарисованные схемы/мокапы на реальные скриншоты с сайтов."""

SH = "shots/%s.png"

RU = [
    # (старый вызов, файл скриншота, новая подпись)
    ('''    m.figure(dg.diagram_architecture(),
             "Рис. 1. Общая схема: пользователь → оркестратор → инструменты и песочница → внешние сервисы")''',
     "arena_attach",
     "Рис. 1. Настоящий экран Agent Mode (скриншот из официального справочного центра "
     "help.arena.ai). Слева — лента шагов агента: «Searched the web» — поискал в интернете, "
     "«Fetched / Read» — скачал и прочитал страницу; справа — панель Workspace (рабочее "
     "пространство) с файлами сессии."),
    ('    m.figure(dg.diagram_loop(), "Рис. 2. Цикл задачи в Agent Mode")',
     "arena_feedback",
     "Рис. 2. Финал цикла задачи (скриншот help.arena.ai): вопрос «Was this task successful?» — "
     "«задача выполнена успешно?». Ответы: Yes — да, No — нет, Keep working — «продолжай работу»."),
    ('    m.figure(dg.diagram_files(), "Рис. 3. Путь файла: загрузка → рабочее пространство → результат")',
     "arena_workspace",
     "Рис. 3. Панель Workspace справа (скриншот help.arena.ai): здесь лежат файлы сессии — и "
     "загруженные, и созданные агентом. Значок стрелки вниз в шапке панели скачивает результат."),
    ('''    m.figure(dg.diagram_docs(),
             "Рис. 4. Конвейер документов: вход → разбор в песочнице → выход в нужном формате")''',
     "arena_attach",
     "Рис. 4. Разбор входящего документа вживую (скриншот help.arena.ai): агент «Thought» — "
     "подумал, «Searched / Fetched / Read» — нашёл и прочитал источник, результат соберёт в файл "
     "в Workspace."),
    ('''    m.figure(dg.diagram_connector_states(),
             "Рис. 5. Жизненный цикл подключения сервиса к сессии")''',
     "arena_toggle",
     "Рис. 5. Меню Connections (подключения) в строке ввода (скриншот help.arena.ai): сервис "
     "GitHub подключён и включён зелёным тумблером для этого чата."),
    ('    m.figure(dg.diagram_github(), "Рис. 6. Рабочий цикл Agent Mode с GitHub")',
     "arena_manage",
     "Рис. 6. Выбор репозитория после включения GitHub (скриншот help.arena.ai): «Select a "
     "repository» — выбрать репозиторий, «Branch» — ветка, шестерёнка справа — управление "
     "подключениями."),
    ('    m.figure(nf.fig_n1(), "Рис. 7. Где находится кнопка создания репозитория")',
     "gh_new",
     "Рис. 7. GitHub, меню «+» в шапке сайта (скриншот из официальной документации "
     "docs.github.com): пункт New repository — «новый репозиторий» — обведён."),
    ('    m.figure(nf.fig_n2(), "Рис. 8. Форма создания: имя, приватность, галочка README и кнопка Create repository")',
     "gh_create",
     "Рис. 8. Форма создания репозитория (скриншот docs.github.com): Owner — владелец аккаунта, "
     "Repository name — имя репозитория; зелёная надпись «is available» — имя свободно."),
    ('    m.figure(nf.fig_n3(), "Рис. 9. Готовый репозиторий: сюда агент будет класть документы")',
     "gh_files",
     "Рис. 9. Готовый репозиторий (скриншот docs.github.com): ветка main, первый коммит Initial "
     "commit и файл README.md в списке."),
    ('    m.figure(nf.fig_n4(), "Рис. 10. Панель подключений Arena: кнопка Connect и управление репозиториями")',
     "arena_connect",
     "Рис. 10. Меню Connections в Arena (скриншот help.arena.ai): строка GitHub со значком "
     "стрелки — клик открывает авторизацию на GitHub."),
    ('    m.figure(nf.fig_n5(), "Рис. 11. Выбираем репозиторий галочкой и включаем тумблер в чате")',
     "arena_toggle",
     "Рис. 11. Тот же список Connections (скриншот help.arena.ai): зелёный тумблер справа от "
     "GitHub включает доступ для текущего чата."),
    ('    m.figure(nf.fig_n6(), "Рис. 12. Вы пишете задачу простыми словами — агент делает файл")',
     "arena_chatbar",
     "Рис. 12. Строка ввода Agent Mode (скриншот help.arena.ai): текст задачи простыми словами, "
     "кнопка Add files — «прикрепить файлы» (обведена), стрелка справа — запуск."),
    ('    m.figure(nf.fig_n7(), "Рис. 13. Pull Request: проверки пройдены — нажимаем Merge (или скачиваем файлы себе)")',
     "gh_merge",
     "Рис. 13. Страница Pull Request на GitHub (скриншот docs.github.com): зелёная кнопка Merge "
     "pull request — «слить изменения в основную ветку»; стрелка рядом раскрывает способы слияния."),
    ('    m.figure(nf.fig_n8(), "Рис. 14. Готовые документы в репозитории: клик по файлу — и он скачивается")',
     "gh_files",
     "Рис. 14. Файлы в репозитории (скриншот docs.github.com): клик по имени файла (README.md "
     "обведён) открывает его страницу — оттуда файл скачивается."),
    ('    m.figure(nf.fig_n9(), "Рис. 15. Папка на GitHub: кнопка Add file → пункт Upload files")',
     "gh_upload",
     "Рис. 15. Кнопка Add file на странице репозитория (скриншот docs.github.com): в раскрывшемся "
     "меню пункт Upload files — «загрузить файлы» — обведён."),
    ('    m.figure(nf.fig_n10(), "Рис. 16. Перетащите файл, дождитесь загрузки и нажмите Commit changes")',
     "gh_files",
     "Рис. 16. Результат загрузки (скриншот docs.github.com): после кнопки Commit changes файл "
     "появляется в списке репозитория, сверху — последний коммит."),
    ('    m.figure(nf.fig_n11(), "Рис. 17. Скачивание из репозитория: клик по файлу, затем кнопка Download")',
     "gh_files",
     "Рис. 17. Скачивание из репозитория (скриншот docs.github.com): клик по файлу в списке "
     "открывает его страницу с кнопкой загрузки на компьютер."),
    ('    m.figure(nf.fig_n12(), "Рис. 18. Панель Workspace в Arena: просмотр и скачивание без GitHub")',
     "arena_workspace",
     "Рис. 18. Панель Workspace в Arena (скриншот help.arena.ai): файлы сессии без GitHub — клик "
     "открывает предпросмотр, значок в шапке скачивает всё."),
]

PL = [
    ('''    m.figure(dg.diagram_architecture(),
             "Rys. 1. Schemat ogólny: użytkownik → orkiestrator → narzędzia i piaskownica → usługi zewnętrzne")''',
     "arena_attach",
     "Rys. 1. Prawdziwy ekran Agent Mode (zrzut z oficjalnego centrum pomocy help.arena.ai). Po "
     "lewej — lista kroków agenta: „Searched the web” — szukał w internecie, „Fetched / Read” — "
     "pobrał i przeczytał stronę; po prawej — panel Workspace (przestrzeń robocza) z plikami sesji."),
    ('    m.figure(dg.diagram_loop(), "Rys. 2. Cykl zadania w Agent Mode")',
     "arena_feedback",
     "Rys. 2. Finał cyklu zadania (zrzut z help.arena.ai): pytanie „Was this task successful?” — "
     "„czy zadanie zakończyło się sukcesem?”. Odpowiedzi: Yes — tak, No — nie, Keep working — "
     "pracuj dalej."),
    ('    m.figure(dg.diagram_files(), "Rys. 3. Droga pliku: wgranie → przestrzeń robocza → wynik")',
     "arena_workspace",
     "Rys. 3. Panel Workspace po prawej (zrzut z help.arena.ai): tu leżą pliki sesji — zarówno "
     "wgrane, jak i utworzone przez agenta. Ikona strzałki w dół w nagłówku panelu pobiera wynik."),
    ('''    m.figure(dg.diagram_docs(),
             "Rys. 4. Potok dokumentów: wejście → analiza w piaskownicy → wyjście w żądanym formacie")''',
     "arena_attach",
     "Rys. 4. Analiza dokumentu na żywo (zrzut z help.arena.ai): agent „Thought” — pomyślał, "
     "„Searched / Fetched / Read” — znalazł i przeczytał źródło, a wynik zapisze do pliku w "
     "Workspace."),
    ('''    m.figure(dg.diagram_connector_states(),
             "Rys. 5. Cykl życia podłączenia usługi do sesji")''',
     "arena_toggle",
     "Rys. 5. Menu Connections (połączenia) w pasku wprowadzania (zrzut z help.arena.ai): usługa "
     "GitHub jest podłączona i włączona zielonym przełącznikiem dla tego czatu."),
    ('    m.figure(dg.diagram_github(), "Rys. 6. Roboczy cykl Agent Mode z GitHubem")',
     "arena_manage",
     "Rys. 6. Wybór repozytorium po włączeniu GitHuba (zrzut z help.arena.ai): „Select a "
     "repository” — wybierz repozytorium, „Branch” — gałąź, kółko zębate po prawej — zarządzanie "
     "połączeniami."),
    ('    m.figure(nf.fig_n1(), "Rys. 7. Gdzie znajduje się przycisk tworzenia repozytorium")',
     "gh_new",
     "Rys. 7. GitHub, menu „+” w nagłówku strony (zrzut z oficjalnej dokumentacji "
     "docs.github.com): punkt New repository — „nowe repozytorium” — obwiedziony."),
    ('    m.figure(nf.fig_n2(), "Rys. 8. Formularz tworzenia: nazwa, prywatność, haczyk README i przycisk Create repository")',
     "gh_create",
     "Rys. 8. Formularz tworzenia repozytorium (zrzut z docs.github.com): Owner — właściciel "
     "konta, Repository name — nazwa repozytorium; zielony napis „is available” — nazwa jest "
     "wolna."),
    ('    m.figure(nf.fig_n3(), "Rys. 9. Gotowe repozytorium: tu agent będzie odkładać dokumenty")',
     "gh_files",
     "Rys. 9. Gotowe repozytorium (zrzut z docs.github.com): gałąź main, pierwszy commit Initial "
     "commit i plik README.md na liście."),
    ('    m.figure(nf.fig_n4(), "Rys. 10. Panel połączeń Arena: przycisk Connect i zarządzanie repozytoriami")',
     "arena_connect",
     "Rys. 10. Menu Connections w Arena (zrzut z help.arena.ai): wiersz GitHub z ikoną strzałki — "
     "kliknięcie otwiera autoryzację na GitHubie."),
    ('    m.figure(nf.fig_n5(), "Rys. 11. Zaznaczamy repozytorium haczykiem i włączamy przełącznik w czacie")',
     "arena_toggle",
     "Rys. 11. Ta sama lista Connections (zrzut z help.arena.ai): zielony przełącznik po prawej "
     "stronie GitHuba włącza dostęp dla bieżącego czatu."),
    ('    m.figure(nf.fig_n6(), "Rys. 12. Piszesz zadanie prostymi słowami — agent robi plik")',
     "arena_chatbar",
     "Rys. 12. Pasek wprowadzania Agent Mode (zrzut z help.arena.ai): treść zadania prostymi "
     "słowami, przycisk Add files — „dołącz pliki” (obwiedziony), strzałka po prawej — start."),
    ('    m.figure(nf.fig_n7(), "Rys. 13. Pull Request: kontrole przeszły — klikamy Merge (albo pobieramy pliki sobie)")',
     "gh_merge",
     "Rys. 13. Strona Pull Request na GitHubie (zrzut z docs.github.com): zielony przycisk Merge "
     "pull request — „scal zmiany z główną gałęzią”; strzałka obok rozwija sposoby scalenia."),
    ('    m.figure(nf.fig_n8(), "Rys. 14. Gotowe dokumenty w repozytorium: klik w plik — i się pobiera")',
     "gh_files",
     "Rys. 14. Pliki w repozytorium (zrzut z docs.github.com): kliknięcie nazwy pliku (README.md "
     "obwiedziony) otwiera jego stronę — stamtąd plik się pobiera."),
    ('    m.figure(nf.fig_n9(), "Rys. 15. Folder na GitHubie: przycisk Add file → punkt Upload files")',
     "gh_upload",
     "Rys. 15. Przycisk Add file na stronie repozytorium (zrzut z docs.github.com): w rozwiniętym "
     "menu punkt Upload files — „wgraj pliki” — obwiedziony."),
    ('    m.figure(nf.fig_n10(), "Rys. 16. Przeciągnij plik, poczekaj na wgranie i kliknij Commit changes")',
     "gh_files",
     "Rys. 16. Wynik wgrania (zrzut z docs.github.com): po kliknięciu Commit changes plik pojawia "
     "się na liście repozytorium, u góry — ostatni commit."),
    ('    m.figure(nf.fig_n11(), "Rys. 17. Pobieranie z repozytorium: klik w plik, potem przycisk Download")',
     "gh_files",
     "Rys. 17. Pobieranie z repozytorium (zrzut z docs.github.com): kliknięcie pliku na liście "
     "otwiera jego stronę z przyciskiem pobrania na komputer."),
    ('    m.figure(nf.fig_n12(), "Rys. 18. Panel Workspace w Arena: podgląd i pobieranie bez GitHuba")',
     "arena_workspace",
     "Rys. 18. Panel Workspace w Arena (zrzut z help.arena.ai): pliki sesji bez GitHuba — "
     "kliknięcie otwiera podgląd, ikona w nagłówku pobiera wszystko."),
]


def patch(path, items, imp_old):
    src = open(path, encoding="utf-8").read()
    assert imp_old in src, path
    src = src.replace(imp_old, "", 1)
    for old, fname, cap in items:
        assert src.count(old) == 1, (path, old[:60])
        new = '    m.shot("%s",\n             "%s")' % (SH % fname, cap)
        src = src.replace(old, new, 1)
    open(path, "w", encoding="utf-8").write(src)
    print("patched", path, len(items), "shots")


patch("content.py", RU, "import diagrams as dg\nimport figs_novice as nf\n")
patch("content_pl.py", PL, "import diagrams_pl as dg\nimport figs_novice_pl as nf\n")
