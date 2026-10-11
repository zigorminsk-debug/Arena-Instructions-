# -*- coding: utf-8 -*-
"""v1.8: примеры программ для Windows и Android + автосборка GitHub Actions с автообновлением."""

RU = '''
    m.h2("15.11. Пример: программа для Windows (Python → .exe)", "sn-win")
    m.p("Самый простой и надёжный путь — язык Python и упаковщик PyInstaller: программа "
        "пишется одним файлом, а упаковщик собирает из неё обычный .exe, который запускается "
        "на любом Windows даже без установленного Python.")
    m.code([
        "# myapp.py — окошко с кнопкой",
        "import tkinter as tk",
        "",
        "def hello():",
        '    label["text"] = "Собрано на GitHub!"',
        "",
        "root = tk.Tk()",
        'root.title("Моя первая программа")',
        'root.geometry("320x140")',
        'tk.Button(root, text="Нажми", command=hello).pack(pady=10)',
        'label = tk.Label(root, text="")',
        "label.pack()",
        "root.mainloop()",
    ], "Файл myapp.py — положите его в корень репозитория")
    m.p("Проверить программу можно у себя на компьютере. Точные команды (терминал: Win+R, "
        "напишите cmd и Enter; затем командой cd перейдите в папку с файлом):")
    m.code([
        "pip install pyinstaller",
        "pyinstaller --onefile --windowed myapp.py",
        "dir dist",
    ], "Сборка .exe у себя: готовый файл появится в папке dist")
    m.ol([
        "Python ставится с python.org — при установке обязательно отметьте галочку "
        "«Add Python to PATH».",
        "После команды pyinstaller готовый myapp.exe лежит в папке dist — его можно "
        "отправить кому угодно.",
        "Но локальная сборка не обязательна: ниже GitHub будет собирать .exe сам на каждый "
        "пуш (раздел 15.13).",
    ])

    m.h2("15.12. Пример: приложение для Android (Python + Kivy → .apk)", "sn-and")
    m.p("Для Android самый короткий путь «в один файл» — Python с библиотекой Kivy и упаковщик "
        "Buildozer: из того же подхода получается установочный .apk для телефона.")
    m.code([
        "# main.py — кнопка и надпись на Android",
        "from kivy.app import App",
        "from kivy.uix.boxlayout import BoxLayout",
        "from kivy.uix.button import Button",
        "from kivy.uix.label import Label",
        "",
        "class MyApp(App):",
        "    def build(self):",
        '        box = BoxLayout(orientation="vertical")',
        '        self.label = Label(text="Привет, Android!")',
        '        btn = Button(text="Нажми меня", size_hint_y=0.4)',
        "        btn.bind(on_press=lambda *_: setattr(",
        '            self.label, "text", "Собрано на GitHub!"))',
        "        box.add_widget(self.label)",
        "        box.add_widget(btn)",
        "        return box",
        "",
        "MyApp().run()",
    ], "Файл main.py — тоже в корень репозитория")
    m.ol([
        "Команда buildozer init создаёт файл настроек buildozer.spec (имя приложения, версия).",
        "Команда buildozer android debug собирает .apk в папку bin (первый раз 10–15 минут).",
        "На Windows Buildozer локально не работает — это не проблема: .apk за вас соберёт "
        "GitHub Actions на своих серверах (раздел 15.13).",
    ])
    m.callout("warn", "Не пугайтесь слов «SDK» и «NDK»",
              "Это наборы инструментов Android, которые Buildozer скачивает сам во время "
              "первой сборки. Ваше участие не требуется — просто подождите.")

    m.h2("15.13. Автосборка на GitHub Actions и автообновление релиза", "sn-ci")
    m.p("GitHub Actions — встроенная «фабрика»: в репозиторий кладётся один файл настройки, и "
        "дальше GitHub при каждом пуше сам запускает сборку Windows- и Android-версий и "
        "обновляет релиз. Вы просто скачиваете свежие .exe и .apk со страницы Releases.")
    m.ol([
        "В репозитории нажмите Add file → Create new file.",
        "В поле имени впишите .github/workflows/build.yml — папки создадутся сами.",
        "Вставьте текст ниже и нажмите Commit changes.",
        "Готово: каждый пуш в main автоматически запускает сборку и обновляет релиз с тегом "
        "latest.",
    ])
    m.code([
        "name: build",
        "",
        "on:",
        "  push:",
        "    branches: [main]",
        "  workflow_dispatch:",
        "",
        "jobs:",
        "  windows:",
        "    runs-on: windows-latest",
        "    steps:",
        "      - uses: actions/checkout@v4",
        "      - uses: actions/setup-python@v5",
        "        with:",
        '          python-version: "3.12"',
        "      - name: Build EXE",
        "        run: |",
        "          pip install pyinstaller",
        "          pyinstaller --onefile --windowed myapp.py",
        "      - name: Artifact",
        "        uses: actions/upload-artifact@v4",
        "        with:",
        "          name: myapp-exe",
        "          path: dist/myapp.exe",
        "      - name: Auto release",
        "        uses: softprops/action-gh-release@v2",
        "        with:",
        "          tag_name: latest",
        "          files: dist/myapp.exe",
        "",
        "  android:",
        "    runs-on: ubuntu-latest",
        "    steps:",
        "      - uses: actions/checkout@v4",
        "      - uses: actions/setup-python@v5",
        "        with:",
        '          python-version: "3.12"',
        "      - name: Build APK",
        "        run: |",
        "          pip install buildozer cython",
        "          buildozer init || true",
        "          buildozer -v android debug",
        "      - name: Artifact",
        "        uses: actions/upload-artifact@v4",
        "        with:",
        "          name: myapp-apk",
        "          path: bin/*.apk",
        "      - name: Auto release",
        "        uses: softprops/action-gh-release@v2",
        "        with:",
        "          tag_name: latest",
        "          files: bin/*.apk",
    ], "Файл .github/workflows/build.yml — вставьте как есть")
    m.shot("shots/gh_actions_tab.png", "https://github.com/",
           "Рис. 23. Вкладка Actions в шапке репозитория (обведена): здесь видно, как идут "
           "сборки (скриншот из официальной документации docs.github.com).")
    m.shot("shots/gh_actions_run.png", "https://github.com/",
           "Рис. 24. Страница запуска сборки: слева_jobs windows и android, справа — шаги и "
           "логи; зелёная галочка — сборка готова (скриншот docs.github.com).")
    m.p("Как работает автообновление: шаг «Auto release» кладёт свежие файлы в релиз с тегом "
        "latest — этот релиз один и тот же при каждой сборке, поэтому на странице Releases "
        "всегда лежат самые новые .exe и .apk. Скачали — установили — пользуетесь; после "
        "следующего пуша там будет новая версия.")
    m.p("Где забирать готовые файлы: вкладка Actions (рис. 23) → клик по запуску → внизу блок "
        "Artifacts (myapp-exe, myapp-apk); либо страница Releases справа на главной "
        "репозитория. Красный крест у запуска — ошибка: откройте запуск и читайте логи, чаще "
        "всего это опечатка в имени файла.")
    m.callout("ok", "Раскладка файлов в репозитории",
              "myapp.py и main.py — в корне; buildozer.spec — в корне (создастся при первом "
              "запуске buildozer init); файл сборки — строго .github/workflows/build.yml. "
              "Если положите код в папку — поправьте пути в build.yml.")
'''

PL = '''
    m.h2("15.11. Przykład: program dla Windows (Python → .exe)", "sn-win")
    m.p("Najprostsza i najpewniejsza droga — język Python i pakowacz PyInstaller: program pisze "
        "się w jednym pliku, a pakowacz składa z niego zwykły .exe, który uruchamia się na "
        "każdym Windowsie nawet bez zainstalowanego Pythona.")
    m.code([
        "# myapp.py — okienko z przyciskiem",
        "import tkinter as tk",
        "",
        "def hello():",
        '    label["text"] = "Zbudowano na GitHubie!"',
        "",
        "root = tk.Tk()",
        'root.title("Mój pierwszy program")',
        'root.geometry("320x140")',
        'tk.Button(root, text="Naciśnij", command=hello).pack(pady=10)',
        'label = tk.Label(root, text="")',
        "label.pack()",
        "root.mainloop()",
    ], "Plik myapp.py — połóż go w korzeniu repozytorium")
    m.p("Program można sprawdzić u siebie na komputerze. Dokładne komendy (terminal: Win+R, "
        "wpisz cmd i Enter; potem komendą cd przejdź do folderu z plikiem):")
    m.code([
        "pip install pyinstaller",
        "pyinstaller --onefile --windowed myapp.py",
        "dir dist",
    ], "Budowa .exe u siebie: gotowy plik pojawi się w folderze dist")
    m.ol([
        "Python instaluje się z python.org — przy instalacji koniecznie zaznacz „Add Python "
        "to PATH”.",
        "Po komendzie pyinstaller gotowy myapp.exe leży w folderze dist — można go wysłać "
        "komukolwiek.",
        "Ale lokalna budowa nie jest obowiązkowa: poniżej GitHub będzie budować .exe sam przy "
        "każdym pushu (rozdział 15.13).",
    ])

    m.h2("15.12. Przykład: aplikacja na Androida (Python + Kivy → .apk)", "sn-and")
    m.p("Dla Androida najkrótsza droga „w jednym pliku” — Python z biblioteką Kivy i pakowacz "
        "Buildozer: z tego samego podejścia powstaje instalacyjny .apk na telefon.")
    m.code([
        "# main.py — przycisk i napis na Androidzie",
        "from kivy.app import App",
        "from kivy.uix.boxlayout import BoxLayout",
        "from kivy.uix.button import Button",
        "from kivy.uix.label import Label",
        "",
        "class MyApp(App):",
        "    def build(self):",
        '        box = BoxLayout(orientation="vertical")',
        '        self.label = Label(text="Cześć, Android!")',
        '        btn = Button(text="Naciśnij mnie", size_hint_y=0.4)',
        "        btn.bind(on_press=lambda *_: setattr(",
        '            self.label, "text", "Zbudowano na GitHubie!"))',
        "        box.add_widget(self.label)",
        "        box.add_widget(btn)",
        "        return box",
        "",
        "MyApp().run()",
    ], "Plik main.py — też do korzenia repozytorium")
    m.ol([
        "Komenda buildozer init tworzy plik ustawień buildozer.spec (nazwa aplikacji, wersja).",
        "Komenda buildozer android debug składa .apk do folderu bin (za pierwszym razem "
        "10–15 minut).",
        "Na Windowsie Buildozer lokalnie nie działa — to nie problem: .apk za Ciebie zbuduje "
        "GitHub Actions na swoich serwerach (rozdział 15.13).",
    ])
    m.callout("warn", "Nie przerażaj się słowami „SDK” i „NDK”",
              "To zestawy narzędzi Androida, które Buildozer pobiera sam podczas pierwszej "
              "budowy. Twój udział nie jest potrzebny — po prostu poczekaj.")

    m.h2("15.13. Autobudowa na GitHub Actions i autoodświeżanie release’a", "sn-ci")
    m.p("GitHub Actions to wbudowana „fabryka”: do repozytorium trafia jeden plik ustawień, a "
        "dalej GitHub przy każdym pushu sam uruchamia budowę wersji windowsowej i androidowej "
        "i odświeża release. Ty tylko pobierasz świeże .exe i .apk ze strony Releases.")
    m.ol([
        "W repozytorium kliknij Add file → Create new file.",
        "W pole nazwy wpisz .github/workflows/build.yml — foldery utworzą się same.",
        "Wklej tekst poniżej i kliknij Commit changes.",
        "Gotowe: każdy push do main automatycznie uruchamia budowę i odświeża release z "
        "tagiem latest.",
    ])
    m.code([
        "name: build",
        "",
        "on:",
        "  push:",
        "    branches: [main]",
        "  workflow_dispatch:",
        "",
        "jobs:",
        "  windows:",
        "    runs-on: windows-latest",
        "    steps:",
        "      - uses: actions/checkout@v4",
        "      - uses: actions/setup-python@v5",
        "        with:",
        '          python-version: "3.12"',
        "      - name: Build EXE",
        "        run: |",
        "          pip install pyinstaller",
        "          pyinstaller --onefile --windowed myapp.py",
        "      - name: Artifact",
        "        uses: actions/upload-artifact@v4",
        "        with:",
        "          name: myapp-exe",
        "          path: dist/myapp.exe",
        "      - name: Auto release",
        "        uses: softprops/action-gh-release@v2",
        "        with:",
        "          tag_name: latest",
        "          files: dist/myapp.exe",
        "",
        "  android:",
        "    runs-on: ubuntu-latest",
        "    steps:",
        "      - uses: actions/checkout@v4",
        "      - uses: actions/setup-python@v5",
        "        with:",
        '          python-version: "3.12"',
        "      - name: Build APK",
        "        run: |",
        "          pip install buildozer cython",
        "          buildozer init || true",
        "          buildozer -v android debug",
        "      - name: Artifact",
        "        uses: actions/upload-artifact@v4",
        "        with:",
        "          name: myapp-apk",
        "          path: bin/*.apk",
        "      - name: Auto release",
        "        uses: softprops/action-gh-release@v2",
        "        with:",
        "          tag_name: latest",
        "          files: bin/*.apk",
    ], "Plik .github/workflows/build.yml — wklej jak jest")
    m.shot("shots/gh_actions_tab.png", "https://github.com/",
           "Rys. 23. Zakładka Actions w nagłówku repozytorium (obwiedziona): tu widać, jak "
           "idą budowy (zrzut z oficjalnej dokumentacji docs.github.com).")
    m.shot("shots/gh_actions_run.png", "https://github.com/",
           "Rys. 24. Strona uruchomienia budowy: po lewej jobs windows i android, po prawej — "
           "kroki i logi; zielony haczyk — budowa gotowa (zrzut docs.github.com).")
    m.p("Jak działa autoodświeżanie: krok „Auto release” odkłada świeże pliki do release’a z "
        "tagiem latest — ten release jest ten sam przy każdej budowie, więc na stronie "
        "Releases zawsze leżą najnowsze .exe i .apk. Pobrałeś — zainstalowałeś — korzystasz; "
        "po następnym pushu będzie tam nowa wersja.")
    m.p("Gdzie zabierać gotowe pliki: zakładka Actions (rys. 23) → klik w uruchomienie → na "
        "dole blok Artifacts (myapp-exe, myapp-apk); albo strona Releases po prawej na "
        "głównej repozytorium. Czerwony krzyżyk przy uruchomieniu — błąd: otwórz uruchomienie "
        "i czytaj logi, najczęściej to literówka w nazwie pliku.")
    m.callout("ok", "Rozkład plików w repozytorium",
              "myapp.py i main.py — w korzeniu; buildozer.spec — w korzeniu (utworzy się przy "
              "pierwszym buildozer init); plik budowy — ściśle .github/workflows/build.yml. "
              "Jeśli położysz kod w folderze — popraw ścieżki w build.yml.")
'''


def patch(path, block, marker):
    src = open(path, encoding="utf-8").read()
    assert src.count(marker) == 1, path
    src = src.replace(marker, block + "\n" + marker, 1)
    open(path, "w", encoding="utf-8").write(src)
    print("patched", path)


patch("content.py", RU, '    m.h1("16. Глоссарий: простые слова вместо терминов", "gl")')
patch("content_pl.py", PL, '    m.h1("16. Słowniczek: proste słowa zamiast terminów", "gl")')
