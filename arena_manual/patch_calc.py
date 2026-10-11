# -*- coding: utf-8 -*-
"""v1.10: разделы 15.11-15.13 переписаны: языки для Windows (+/-), промты для Arena
с примером калькулятора (Windows и Android), команды сборки и Actions с автообновлением."""

RU = '''    m.h2("15.11. Из чего пишут программы для Windows: языки с плюсами и минусами", "sn-lang")
    m.p("Одну и ту же программу можно написать на разных языках. Вот основные пути — со всеми "
        "«за» и «против», чтобы вы осознанно выбрали, о чём просить Arena:")
    m.table(
        ["Язык", "Плюсы", "Минусы", "Кому подходит"],
        [
            ["<b>Python</b>",
             "Самый лёгкий старт; код читается как текст; тысячи библиотек; .exe собирается "
             "одной командой PyInstaller",
             "Работает медленнее собранных языков; .exe весит несколько мегабайт",
             "Новичкам и для любых утилит — наш выбор в примерах ниже"],
            ["<b>C# (.NET)</b>",
             "«Родной» язык Windows; красивые окна (WinForms/WPF); высокая скорость",
             "Больше учиться; сборка чуть сложнее, чем у Python",
             "Тем, кто хочет расти в программирование под Windows"],
            ["<b>C++</b>",
             "Максимальная скорость и контроль над системой",
             "Самый сложный; ручная работа с памятью; для первой программы избыточен",
             "Игры, драйверы, быстрые движки — не для старта"],
            ["<b>JavaScript (Electron)</b>",
             "Интерфейс как у сайта; одна программа работает и на Windows, и на других "
             "системах",
             "Программа «тяжёлая»: внутри целый браузер; ест много памяти",
             "Когда нужен красивый интерфейс: мессенджеры, редакторы"],
        ],
        widths=[0.8, 1.7, 1.5, 1.4],
    )
    m.callout("ok", "Что выбрать новичку",
              "Python: меньше всего кода, простейшие команды, а для Android тот же Python с "
              "библиотекой Kivy — не придётся учить второй язык. Все примеры и промты ниже — "
              "на Python.")

    m.h2("15.12. Пример: калькулятор для Windows и Android — пишем промты для Arena", "sn-calc")
    m.p("Код можно вообще не писать самому: вы описываете калькулятор словами в промте, а "
        "Arena пишет код, кладёт файлы в ваш репозиторий и открывает Pull Request. Ниже — "
        "готовые промты: скопируйте, вставьте в строку ввода и не забудьте подключить "
        "репозиторий (раздел 15.4).")
    m.code([
        "Напиши калькулятор для Windows на Python (tkinter): кнопки с цифрами 0-9,",
        "операции + - * /, кнопка «=» считает результат, кнопка «C» сбрасывает.",
        "Окно — как у обычного калькулятора: экран сверху, кнопки сеткой 4x4.",
        "Положи файл calc_win.py в корень репозитория, проверь синтаксис и сделай коммит.",
    ], "Промт для Arena — калькулятор для Windows (скопируйте и вставьте)")
    m.p("Агент положит в репозиторий примерно такой файл — это и есть пример готового "
        "калькулятора для Windows:")
    m.code([
        "# calc_win.py - калькулятор для Windows",
        "import tkinter as tk",
        "",
        "def press(ch):",
        '    if ch == "C":',
        '        scr.set("0"); return',
        '    if ch == "=":',
        "        try:",
        '            scr.set(str(eval(scr.get().replace("x", "*"))))',
        "        except Exception:",
        '            scr.set("ошибка")',
        "        return",
        '    scr.set(ch if scr.get() == "0" else scr.get() + ch)',
        "",
        "root = tk.Tk()",
        'root.title("Калькулятор")',
        'scr = tk.StringVar(value="0")',
        'tk.Label(root, textvariable=scr, font=("Arial", 18),',
        '         anchor="e").grid(column=0, row=0, columnspan=4,',
        '                          sticky="we", padx=6, pady=6)',
        'keys = ["7", "8", "9", "/", "4", "5", "6", "x", "1", "2",',
        '        "3", "-", "0", ".", "C", "+", "="]',
        "for i, k in enumerate(keys):",
        "    tk.Button(root, text=k, width=5,",
        "              command=lambda c=k: press(c)).grid(",
        "        column=i % 4, row=1 + i // 4, padx=3, pady=3)",
        "root.mainloop()",
    ], "calc_win.py — что агент напишет по промту")
    m.code([
        "Напиши калькулятор для Android на Python (Kivy): экран с выражением и результатом,",
        "кнопки 0-9, операции + - * /, «=» считает, «C» сбрасывает, сетка 4x4.",
        "Положи файл main.py в корень репозитория и создай buildozer.spec",
        "с названием приложения «Калькулятор». Проверь синтаксис и сделай коммит.",
    ], "Промт для Arena — калькулятор для Android (скопируйте и вставьте)")
    m.p("Для Android агент сделает файл main.py — тот же подход: экран сверху, кнопки сеткой:")
    m.code([
        "# main.py - калькулятор для Android",
        "from kivy.app import App",
        "from kivy.uix.boxlayout import BoxLayout",
        "from kivy.uix.gridlayout import GridLayout",
        "from kivy.uix.button import Button",
        "from kivy.uix.label import Label",
        "",
        "class CalcApp(App):",
        "    def build(self):",
        '        self.expr = ""',
        '        root = BoxLayout(orientation="vertical")',
        '        self.scr = Label(text="0", font_size=40, size_hint_y=0.25)',
        "        root.add_widget(self.scr)",
        "        grid = GridLayout(cols=4, spacing=4, padding=4)",
        '        for k in ["7", "8", "9", "/", "4", "5", "6", "*",',
        '                  "1", "2", "3", "-", "0", ".", "C", "+", "="]:',
        "            b = Button(text=k, font_size=26)",
        "            b.bind(on_press=lambda btn: self.press(btn.text))",
        "            grid.add_widget(b)",
        "        root.add_widget(grid)",
        "        return root",
        "",
        "    def press(self, ch):",
        '        if ch == "C":',
        '            self.expr = ""',
        '        elif ch == "=":',
        "            try:",
        "                self.expr = str(eval(self.expr))",
        "            except Exception:",
        '                self.expr = "ошибка"',
        "        else:",
        "            self.expr += ch",
        '        self.scr.text = self.expr or "0"',
        "",
        "CalcApp().run()",
    ], "main.py — калькулятор для Android (Kivy)")
    m.callout("info", "Как правильно просить Arena",
              "Один промт — одна программа. Указывайте: язык (Python), что за кнопки и "
              "операции, имя файла и куда положить в репозитории, и финал «проверь и сделай "
              "коммит». Если результат не понравился — пишите «переделай: …» тем же чатом.")

    m.h2("15.13. Сборка на GitHub: команды и Actions с автообновлением", "sn-ci")
    m.p("GitHub Actions — встроенная «фабрика»: один файл настройки в репозитории, и GitHub "
        "при каждом пуше сам собирает .exe и .apk и обновляет релиз — у вас всегда свежие "
        "файлы без единой команды на своём компьютере.")
    m.ol([
        "В репозитории нажмите Add file → Create new file.",
        "В поле имени впишите .github/workflows/build.yml — папки создадутся сами.",
        "Вставьте текст ниже и нажмите Commit changes.",
        "Готово: каждый пуш в main запускает сборку и обновляет релиз с тегом latest.",
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
        "          pyinstaller --onefile --windowed calc_win.py",
        "      - name: Artifact",
        "        uses: actions/upload-artifact@v4",
        "        with:",
        "          name: calc-exe",
        "          path: dist/calc_win.exe",
        "      - name: Auto release",
        "        uses: softprops/action-gh-release@v2",
        "        with:",
        "          tag_name: latest",
        "          files: dist/calc_win.exe",
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
        "          buildozer -v android debug",
        "      - name: Artifact",
        "        uses: actions/upload-artifact@v4",
        "        with:",
        "          name: calc-apk",
        "          path: bin/*.apk",
        "      - name: Auto release",
        "        uses: softprops/action-gh-release@v2",
        "        with:",
        "          tag_name: latest",
        "          files: bin/*.apk",
    ], "Файл .github/workflows/build.yml — вставьте как есть")
    m.p("Если захотите собрать .exe у себя на компьютере (не обязательно), команды такие "
        "(терминал: Win+R → cmd; командой cd перейдите в папку с файлом):")
    m.code([
        "pip install pyinstaller",
        "pyinstaller --onefile --windowed calc_win.py",
        "dir dist",
    ], "Локальная сборка .exe: готовый файл появится в папке dist")
    m.shot("shots/gh_actions_tab.png", "https://github.com/",
           "Рис. 23. Вкладка Actions в шапке репозитория (обведена): здесь видно, как идут "
           "сборки (скриншот из официальной документации docs.github.com).")
    m.shot("shots/gh_actions_run.png", "https://github.com/",
           "Рис. 24. Страница запуска сборки: слева jobs windows и android, справа — шаги и "
           "логи; зелёная галочка — сборка готова (скриншот docs.github.com).")
    m.p("Как работает автообновление: шаг «Auto release» кладёт свежие файлы в релиз с тегом "
        "latest — при каждой сборке он перезаписывается, поэтому на странице Releases всегда "
        "лежат самые новые калькулятор.exe и калькулятор.apk. Скачали — установили — "
        "пользуетесь; после следующего пуша там будет новая версия.")
    m.p("Где забирать готовые файлы: вкладка Actions (рис. 23) → клик по запуску → внизу блок "
        "Artifacts (calc-exe, calc-apk); либо страница Releases справа на главной "
        "репозитория. Красный крест у запуска — ошибка: откройте запуск и читайте логи, чаще "
        "всего это опечатка в имени файла.")
    m.callout("ok", "Раскладка файлов в репозитории",
              "calc_win.py, main.py и buildozer.spec — в корне; файл сборки — строго "
              ".github/workflows/build.yml. Если положите код в папку — поправьте пути в "
              "build.yml.")
'''

PL = '''    m.h2("15.11. Z czego pisze się programy na Windows: języki z plusami i minusami", "sn-lang")
    m.p("Ten sam program można napisać w różnych językach. Oto główne drogi — ze wszystkimi "
        "„za” i „przeciw”, żebyś świadomie wybrał, o co prosić Arenę:")
    m.table(
        ["Język", "Plusy", "Minusy", "Dla kogo"],
        [
            ["<b>Python</b>",
             "Najłatwiejszy start; kod czyta się jak tekst; tysiące bibliotek; .exe składa się "
             "jedną komendą PyInstaller",
             "Działa wolniej niż języki kompilowane; .exe waży kilka megabajtów",
             "Nowicjuszom i do wszelkich narzędzi — nasz wybór w przykładach poniżej"],
            ["<b>C# (.NET)</b>",
             "„Rodzimy” język Windowsa; ładne okna (WinForms/WPF); wysoka szybkość",
             "Więcej nauki; budowa nieco trudniejsza niż w Pythonie",
             "Dla chcących rosnąć w programowanie pod Windowsa"],
            ["<b>C++</b>",
             "Maksymalna szybkość i kontrola nad systemem",
             "Najtrudniejszy; ręczna praca z pamięcią; na pierwszy program nadmiarowy",
             "Gry, sterowniki, szybkie silniki — nie na start"],
            ["<b>JavaScript (Electron)</b>",
             "Interfejs jak strona; jeden program działa i na Windowsie, i na innych "
             "systemach",
             "Program „ciężki”: w środku cała przeglądarka; je dużo pamięci",
             "Gdy potrzebny ładny interfejs: komunikatory, edytory"],
        ],
        widths=[0.8, 1.7, 1.5, 1.4],
    )
    m.callout("ok", "Co wybrać jako nowicjusz",
              "Python: najmniej kodu, najprostsze komendy, a na Androida ten sam Python z "
              "biblioteką Kivy — nie trzeba uczyć się drugiego języka. Wszystkie przykłady i "
              "prompty poniżej — w Pythonie.")

    m.h2("15.12. Przykład: kalkulator na Windowsa i Androida — piszemy prompty do Areny", "sn-calc")
    m.p("Kodu w ogóle nie trzeba pisać samemu: opisujesz kalkulator słowami w prompcie, a Arena "
        "pisze kod, odkłada pliki do Twojego repozytorium i otwiera Pull Request. Poniżej — "
        "gotowe prompty: skopiuj, wklej w pasek wprowadzania i nie zapomnij podłączyć "
        "repozytorium (rozdział 15.4).")
    m.code([
        "Napisz kalkulator na Windowsa w Pythonie (tkinter): przyciski z cyframi 0-9,",
        "działania + - * /, przycisk „=” liczy wynik, przycisk „C” kasuje.",
        "Okno — jak w zwykłym kalkulatorze: ekran u góry, przyciski siatką 4x4.",
        "Połóż plik calc_win.py w korzeniu repozytorium, sprawdź składnię i zrób commit.",
    ], "Prompt do Areny — kalkulator na Windowsa (skopiuj i wklej)")
    m.p("Agent położy do repozytorium mniej więcej taki plik — to właśnie przykład gotowego "
        "kalkulatora na Windowsa:")
    m.code([
        "# calc_win.py - kalkulator na Windowsa",
        "import tkinter as tk",
        "",
        "def press(ch):",
        '    if ch == "C":',
        '        scr.set("0"); return',
        '    if ch == "=":',
        "        try:",
        '            scr.set(str(eval(scr.get().replace("x", "*"))))',
        "        except Exception:",
        '            scr.set("blad")',
        "        return",
        '    scr.set(ch if scr.get() == "0" else scr.get() + ch)',
        "",
        "root = tk.Tk()",
        'root.title("Kalkulator")',
        'scr = tk.StringVar(value="0")',
        'tk.Label(root, textvariable=scr, font=("Arial", 18),',
        '         anchor="e").grid(column=0, row=0, columnspan=4,',
        '                          sticky="we", padx=6, pady=6)',
        'keys = ["7", "8", "9", "/", "4", "5", "6", "x", "1", "2",',
        '        "3", "-", "0", ".", "C", "+", "="]',
        "for i, k in enumerate(keys):",
        "    tk.Button(root, text=k, width=5,",
        "              command=lambda c=k: press(c)).grid(",
        "        column=i % 4, row=1 + i // 4, padx=3, pady=3)",
        "root.mainloop()",
    ], "calc_win.py — co agent napisze z promptu")
    m.code([
        "Napisz kalkulator na Androida w Pythonie (Kivy): ekran z wyrażeniem i wynikiem,",
        "przyciski 0-9, działania + - * /, „=” liczy, „C” kasuje, siatka 4x4.",
        "Połóż plik main.py w korzeniu repozytorium i utwórz buildozer.spec",
        "z nazwą aplikacji „Kalkulator”. Sprawdź składnię i zrób commit.",
    ], "Prompt do Areny — kalkulator na Androida (skopiuj i wklej)")
    m.p("Na Androida agent zrobi plik main.py — to samo podejście: ekran u góry, przyciski "
        "siatką:")
    m.code([
        "# main.py - kalkulator na Androida",
        "from kivy.app import App",
        "from kivy.uix.boxlayout import BoxLayout",
        "from kivy.uix.gridlayout import GridLayout",
        "from kivy.uix.button import Button",
        "from kivy.uix.label import Label",
        "",
        "class CalcApp(App):",
        "    def build(self):",
        '        self.expr = ""',
        '        root = BoxLayout(orientation="vertical")',
        '        self.scr = Label(text="0", font_size=40, size_hint_y=0.25)',
        "        root.add_widget(self.scr)",
        "        grid = GridLayout(cols=4, spacing=4, padding=4)",
        '        for k in ["7", "8", "9", "/", "4", "5", "6", "*",',
        '                  "1", "2", "3", "-", "0", ".", "C", "+", "="]:',
        "            b = Button(text=k, font_size=26)",
        "            b.bind(on_press=lambda btn: self.press(btn.text))",
        "            grid.add_widget(b)",
        "        root.add_widget(grid)",
        "        return root",
        "",
        "    def press(self, ch):",
        '        if ch == "C":',
        '            self.expr = ""',
        '        elif ch == "=":',
        "            try:",
        "                self.expr = str(eval(self.expr))",
        "            except Exception:",
        '                self.expr = "blad"',
        "        else:",
        "            self.expr += ch",
        '        self.scr.text = self.expr or "0"',
        "",
        "CalcApp().run()",
    ], "main.py — kalkulator na Androida (Kivy)")
    m.callout("info", "Jak poprawnie prosić Arenę",
              "Jeden prompt — jeden program. Podawaj: język (Python), jakie przyciski i "
              "działania, nazwę pliku i gdzie położyć w repozytorium, oraz finał „sprawdź i "
              "zrób commit”. Jeśli wynik się nie spodoba — pisz „przerób: …” w tym samym "
              "czacie.")

    m.h2("15.13. Budowa na GitHubie: komendy i Actions z autoodświeżaniem", "sn-ci")
    m.p("GitHub Actions to wbudowana „fabryka”: jeden plik ustawień w repozytorium, a GitHub "
        "przy każdym pushu sam buduje .exe i .apk i odświeża release — masz zawsze świeże "
        "pliki bez jednej komendy na swoim komputerze.")
    m.ol([
        "W repozytorium kliknij Add file → Create new file.",
        "W pole nazwy wpisz .github/workflows/build.yml — foldery utworzą się same.",
        "Wklej tekst poniżej i kliknij Commit changes.",
        "Gotowe: każdy push do main uruchamia budowę i odświeża release z tagiem latest.",
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
        "          pyinstaller --onefile --windowed calc_win.py",
        "      - name: Artifact",
        "        uses: actions/upload-artifact@v4",
        "        with:",
        "          name: calc-exe",
        "          path: dist/calc_win.exe",
        "      - name: Auto release",
        "        uses: softprops/action-gh-release@v2",
        "        with:",
        "          tag_name: latest",
        "          files: dist/calc_win.exe",
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
        "          buildozer -v android debug",
        "      - name: Artifact",
        "        uses: actions/upload-artifact@v4",
        "        with:",
        "          name: calc-apk",
        "          path: bin/*.apk",
        "      - name: Auto release",
        "        uses: softprops/action-gh-release@v2",
        "        with:",
        "          tag_name: latest",
        "          files: bin/*.apk",
    ], "Plik .github/workflows/build.yml — wklej jak jest")
    m.p("Jeśli zechcesz zbudować .exe u siebie na komputerze (nieobowiązkowe), komendy są "
        "takie (terminal: Win+R → cmd; komendą cd przejdź do folderu z plikiem):")
    m.code([
        "pip install pyinstaller",
        "pyinstaller --onefile --windowed calc_win.py",
        "dir dist",
    ], "Lokalna budowa .exe: gotowy plik pojawi się w folderze dist")
    m.shot("shots/gh_actions_tab.png", "https://github.com/",
           "Rys. 23. Zakładka Actions w nagłówku repozytorium (obwiedziona): tu widać, jak "
           "idą budowy (zrzut z oficjalnej dokumentacji docs.github.com).")
    m.shot("shots/gh_actions_run.png", "https://github.com/",
           "Rys. 24. Strona uruchomienia budowy: po lewej jobs windows i android, po prawej — "
           "kroki i logi; zielony haczyk — budowa gotowa (zrzut docs.github.com).")
    m.p("Jak działa autoodświeżanie: krok „Auto release” odkłada świeże pliki do release’a z "
        "tagiem latest — przy każdej budowie nadpisuje się, więc na stronie Releases zawsze "
        "leżą najnowsze kalkulator.exe i kalkulator.apk. Pobrałeś — zainstalowałeś — "
        "korzystasz; po następnym pushu będzie tam nowa wersja.")
    m.p("Gdzie zabierać gotowe pliki: zakładka Actions (rys. 23) → klik w uruchomienie → na "
        "dole blok Artifacts (calc-exe, calc-apk); albo strona Releases po prawej na głównej "
        "repozytorium. Czerwony krzyżyk przy uruchomieniu — błąd: otwórz uruchomienie i czytaj "
        "logi, najczęściej to literówka w nazwie pliku.")
    m.callout("ok", "Rozkład plików w repozytorium",
              "calc_win.py, main.py i buildozer.spec — w korzeniu; plik budowy — ściśle "
              ".github/workflows/build.yml. Jeśli położysz kod w folderze — popraw ścieżki w "
              "build.yml.")
'''


def patch(path, block, start, end):
    src = open(path, encoding="utf-8").read()
    i = src.index(start)
    j = src.index(end)
    src = src[:i] + block + "\n\n" + src[j:]
    open(path, "w", encoding="utf-8").write(src)
    print("patched", path)


patch("content.py", RU,
      '    m.h2("15.11.', '    m.h1("16. Глоссарий')
patch("content_pl.py", PL,
      '    m.h2("15.11.', '    m.h1("16. Słowniczek')
