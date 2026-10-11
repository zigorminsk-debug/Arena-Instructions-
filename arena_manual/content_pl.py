# -*- coding: utf-8 -*-
"""Treść instrukcji Arena Agent Mode — wersja polska."""
from reportlab.lib.units import mm
from reportlab.platypus import NextPageTemplate, PageBreak, Spacer

from builder import INK, Paragraph, S, Table, TableStyle


def ParagraphStyle_tmp(size, leading, color, bold=False):
    from reportlab.lib.styles import ParagraphStyle
    return ParagraphStyle("tmp", fontName="DJ-Bold" if bold else "DJ",
                          fontSize=size, leading=leading, textColor=color)


def cover_flow(meta):
    out = []
    out.append(Spacer(1, 16 * mm))
    out.append(Paragraph('<font color="#8fb0ff"><b>ARENA.AI &nbsp;·&nbsp; AGENT MODE</b></font>',
                         ParagraphStyle_tmp(11, 15, "#cfe0ff")))
    out.append(Spacer(1, 4 * mm))
    out.append(Paragraph('<b>Szczegółowa instrukcja<br/>pracy z AI Arena</b>',
                         ParagraphStyle_tmp(30, 36, "#ffffff", bold=True)))
    out.append(Spacer(1, 6 * mm))
    out.append(Paragraph("Jak zbudowana jest platforma, jak agent współpracuje z usługami "
                         "zewnętrznymi i konektorami oraz jak pracować z dokumentami, plikami "
                         "i innymi treściami",
                         ParagraphStyle_tmp(12, 17, "#c8d3e6")))
    out.append(Spacer(1, 12 * mm))
    data = [
        [Paragraph('<b>Co w środku</b>', S["cell"]),
         Paragraph("16 rozdziałów: tryby, przestrzeń robocza, pliki i dokumenty, narzędzia "
                   "agenta, konektory i usługi (GitHub, Google i inne), prompty, kontrola "
                   "jakości, bezpieczeństwo, awarie, ściągawka, start krok po kroku dla "
                   "nowicjusza z obrazkami i słowniczek prostym językiem", S["cell"])],
        [Paragraph('<b>Dla kogo</b>', S["cell"]),
         Paragraph("Dla użytkowników Agent Mode, deweloperów, analityków, autorów dokumentów "
                   "i wszystkich, którzy budują wieloetapowe procesy pracy w Arena", S["cell"])],
        [Paragraph('<b>Aktualność</b>', S["cell"]),
         Paragraph(meta["version"] + ". Centrum pomocy i blog Arena często się zmieniają — "
                   "szczegóły porównuj z interfejsem", S["cell"])],
    ]
    tbl = Table(data, colWidths=[32 * mm, 138 * mm], hAlign="LEFT")
    tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEABOVE", (0, 0), (-1, 0), 0.8, INK),
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, INK),
        ("LINEBELOW", (0, 0), (-1, -2), 0.3, INK),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    out.append(tbl)
    out.append(NextPageTemplate("Body"))
    out.append(PageBreak())
    return out


def build(m, meta):
    # ---------------------------------------------------------- 0. INTERAKTYW
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
            ["<a href=\"https://arena.ai/agent\" color=\"#1d4ed8\"><u>arena.ai/agent</u></a>",
             "Agent Mode na Arena",
             "Główna strona robocza: dialog, Workspace, połączenia"],
            ["<a href=\"https://help.arena.ai\" color=\"#1d4ed8\"><u>help.arena.ai</u></a>",
             "Centrum pomocy Arena", "Oficjalne odpowiedzi, jak wszystko działa"],
            ["<a href=\"https://github.com/\" color=\"#1d4ed8\"><u>github.com</u></a>",
             "Twój GitHub", "Twoje repozytoria i pliki"],
            ["<a href=\"https://github.com/new\" color=\"#1d4ed8\"><u>github.com/new</u></a>",
             "Formularz tworzenia repozytorium",
             "Krok z rozdziału 15: utworzyć „szafę” na dokumenty"],
            ["<a href=\"https://github.com/pulls\" color=\"#1d4ed8\"><u>github.com/pulls</u></a>",
             "Twoje Pull Requesty", "Tu agent przynosi wynik do akceptacji"],
        ],
        widths=[1.2, 1.5, 2.4],
    )
    m.callout("info", "Gdy łącze się nie otwiera",
              "Klikalne łącza działają w przeglądarkach PDF: Chrome, Edge, Adobe Acrobat, "
              "Podgląd na macOS. W wydruku wszystkie adresy zostają w tekście — można je wpisać "
              "ręcznie.")
    # ---------------------------------------------------------- 1. PRZEGLĄD
    m.h1("1. Czym jest Arena i jak działa Agent Mode", "s1")
    m.lead("Arena (arena.ai) to platforma oceny modeli AI oraz środowisko pracy dla zadań "
           "agentowych. Znana jest z leaderboardów budowanych na głosach ludzi oraz z trybów "
           "porównywania odpowiedzi. Agent Mode to osobna powierzchnia: jeden model otrzymuje "
           "zadanie, narzędzia i piaskownicę i realizuje je od początku do końca.")

    m.h2("1.1. Kluczowa idea", "s1-1")
    m.p("W zwykłym czacie złożone zadanie trzeba dzielić na dziesiątki promptów i ręcznie "
        "przenosić wyniki między oknami. W Agent Mode cel formułujesz raz: agent sam układa "
        "plan, wywołuje narzędzia, tworzy i poprawia pliki, sprawdza wynik i w razie potrzeby "
        "zadaje pytania doprecyzowujące. Oficjalne centrum pomocy opisuje to jako "
        "„autonomiczne budowanie planu i realizację wieloetapowego procesu pracy w jednym "
        "przebiegu”.")
    m.p("Warto rozumieć model odpowiedzialności: to <b>nadzorowana autonomia</b>. Agent może "
        "czytać strony internetowe, wykonywać polecenia w powłoce, instalować pakiety i "
        "zapisywać pliki. Twoją rolą jest postawienie zadania, kontrola kroków pośrednich "
        "i odbiór wyniku.")

    m.h2("1.2. Jak wejść do Agent Mode", "s1-2")
    m.ol([
        "Otwórz bezpośrednio <a href=\"https://arena.ai/agent\" color=\"#1d4ed8\"><u>arena.ai/agent</u></a>.",
        "Albo na stronie głównej Arena kliknij rozwijane menu w lewym górnym rogu i przełącz "
        "się z Battle Mode na <b>Agent Mode</b>.",
        "W razie potrzeby podłącz usługi (np. GitHub) w panelu połączeń przed wysłaniem "
        "pierwszego promptu — agent od razu dostanie potrzebny kontekst.",
        "Sformułuj zadanie w pasku wprowadzania, załącz pliki i kliknij strzałkę wysyłania.",
    ])

    m.h2("1.3. Kiedy który tryb wybrać", "s1-3")
    m.table(
        ["Tryb", "Do czego", "Kiedy nie jest potrzebny"],
        [
            ["<b>Agent Mode</b>",
             "Wieloetapowe zadania: strony i aplikacje, głęboka analiza, raporty, "
             "przetwarzanie dokumentów i danych, praca z repozytorium",
             "Proste pytanie faktograficzne lub jedna poprawka tekstu — szybciej i taniej "
             "w czacie"],
            ["<b>Battle Mode</b>",
             "Porównanie dwóch anonimowych modeli i głosowanie na lepszą odpowiedź",
             "Gdy potrzebny jest konkretny wynik, a nie porównanie"],
            ["<b>Direct / Side-by-Side</b>",
             "Punktowe zapytania do wybranego modelu lub równoległe porównanie",
             "Gdy wymagana jest długa praca z plikami"],
            ["<b>Code Arena</b>",
             "Aplikacje webowe: frontend, a w wariancie Fullstack — bazy danych, "
             "uwierzytelnianie, integracje zewnętrzne i wdrożenia",
             "Gdy praca toczy się w istniejącym repozytorium — tam wygodniejszy jest Agent "
             "Mode z GitHubem"],
            ["<b>Image / Video Arena</b>",
             "Generowanie i porównywanie obrazów i wideo, edycja grafik",
             "Gdy obrazek jest tylko ilustracją wewnątrz dużego dokumentu"],
        ],
        widths=[1.1, 2.6, 2.0],
    )

    m.h2("1.4. Co widać, a czego nie", "s1-4")
    m.p("Każda nowa sesja Agent Mode jest wykonywana przez dedykowany model orkiestratora, "
        "wybierany losowo spośród modeli z agentowego leaderboarda. W odróżnieniu od Battle "
        "Mode nazwa modelu nie jest ujawniana: tak Arena zbiera uczciwą statystykę na "
        "realnych zadaniach. W trakcie rozmowy model pozostaje ten sam, ale jeśli odpowiedź "
        "grozi zepsuciem sesji, system może automatycznie przełączyć się na inny — dlatego "
        "czasem zachowanie agenta delikatnie zmienia się w obrębie jednego czatu.")
    m.callout("info", "Co daje leaderboard Agent Arena",
              "Orkiestratory są rankowane według pięciu sygnałów: potwierdzony sukces "
              "zadania, stosunek pochwał do skarg, sterowność (na ile trafnie model poprawia "
              "wynik po Twojej uwadze), odzyskiwanie po nieudanej komendzie bash oraz "
              "halucynacje narzędzi. Ocena końcowa to „czysta poprawa” względem średniego "
              "modelu. Praktyczny sens: Twoje oceny i uwagi to nie tylko informacja "
              "zwrotna, ale też dane, na których budowany jest ranking.")

    m.shot("shots/arena_attach.png", "https://arena.ai/agent",
             "Rys. 1. Prawdziwy ekran Agent Mode (zrzut z oficjalnego centrum pomocy help.arena.ai). Po lewej — lista kroków agenta: „Searched the web” — szukał w internecie, „Fetched / Read” — pobrał i przeczytał stronę; po prawej — panel Workspace (przestrzeń robocza) z plikami sesji.")

    # ---------------------------------------------------------- 2. INTERFEJS
    m.h1("2. Interfejs i przestrzeń robocza", "s2")
    m.lead("Ekran Agent Mode dzieli się na dialog po lewej i panel roboczy po prawej. Dialog "
           "to historia kroków agenta; panel to, co utworzył i jak się to zmieniało.")

    m.h2("2.1. Główne strefy ekranu", "s2-1")
    m.table(
        ["Strefa", "Co robi", "Jak korzystać"],
        [
            ["<b>Pasek wprowadzania</b>",
             "Prompt, załączniki, wysłanie zadania",
             "Przycisk „+” — załącz plik; można po prostu wkleić plik ze schowka; strzałka — "
             "uruchom"],
            ["<b>Lista kroków</b>",
             "Pokazuje plan agenta, wywołania narzędzi, komendy i ich wyniki",
             "Rozwijaj kroki, aby zrozumieć, co dokładnie zostało zrobione i gdzie jest błąd"],
            ["<b>Workspace</b>",
             "Pliki sesji: to, co wgrałeś i co stworzył agent",
             "Otwieraj plik w podglądzie, pobieraj wynik"],
            ["<b>Diff</b>",
             "Zmiany kodu linia po linii, z podświetlaniem składni",
             "Przełącznik między „ostatni ruch” a „cała gałąź”"],
            ["<b>Checks</b>",
             "Status automatycznych kontroli commitów i PR: przechodzi / nie przeszło / w toku",
             "Sprawdzaj przed mergem, żeby nie wciągnąć zepsutego builda"],
            ["<b>Podgląd portu</b>",
             "Żywy podgląd serwera uruchomionego w piaskownicy",
             "Poproś agenta „pokaż podgląd” — podniesie serwer deweloperski i odda link"],
            ["<b>Połączenia</b>",
             "Usługi, do których agent ma dostęp (np. GitHub)",
             "Włączaj i wyłączaj przełącznikiem dla konkretnego czatu"],
        ],
        widths=[1.0, 1.7, 2.4],
    )

    m.h2("2.2. Piaskownica: czym jest fizycznie", "s2-2")
    m.p("Agent Mode działa w izolowanym środowisku w chmurze — nie na Twoim komputerze. Agent "
        "ma pełnoprawną powłokę Linuksa: czyta i zapisuje pliki, instaluje pakiety, uruchamia "
        "skrypty, testy i serwery, sprawdza wyniki i poprawia błędy. To bezpieczniejsze niż "
        "uruchamianie lokalne, ale oznacza też główną zasadę: <b>to, co zostało w "
        "piaskownicy, trzeba stamtąd zabrać</b> — pobrać archiwum albo wysłać do repozytorium.")
    m.ul([
        "<b>Część trwała</b> — pliki w katalogu domowym sesji. Przeżywają kolejną replikę: do "
        "projektu można wrócić i kontynuować.",
        "<b>Nie jest zapisywane</b> — zainstalowane pakiety, cache buildów, uruchomione "
        "procesy, historia powłoki. W nowej wiadomości otoczenie podnosi się od nowa, więc "
        "agent w razie potrzeby reinstaluje zależności.",
        "<b>Długie procesy</b> (serwery deweloperskie, watchery) uruchamiane są jako procesy "
        "w tle, a nie zwykłą komendą: dzięki temu działają między replikami, a Ty widzisz "
        "żywy podgląd.",
    ])

    m.h2("2.3. Cykl życia zadania", "s2-3")
    m.p("Typowy cykl wygląda tak: formułujesz cel, agent układa plan, wywołuje narzędzia, "
        "odkłada wynik do pliku, sprawdza go i oddaje Tobie. Dalej cykl powtarza się tyle "
        "razy, ile trzeba: „kontynuuj”, „przerób tabelę”, „dodaj rozdział”. Po zakończeniu "
        "Arena zaproponuje pozostawienie informacji zwrotnej lub wybór „kontynuuj pracę”.")
    m.shot("shots/arena_feedback.png", "https://arena.ai/agent",
             "Rys. 2. Finał cyklu zadania (zrzut z help.arena.ai): pytanie „Was this task successful?” — „czy zadanie zakończyło się sukcesem?”. Odpowiedzi: Yes — tak, No — nie, Keep working — pracuj dalej.")

    # ---------------------------------------------------------- 3. PLIKI
    m.h1("3. Pliki: wgrywanie, przechowywanie, odbiór wyniku", "s3")
    m.lead("Pliki to główny sposób przekazania agentowi kontekstu i główny sposób odebrania "
           "wyniku. Tu opisane są obsługiwane formaty, mechanika i pułapki.")

    m.h2("3.1. Jak wgrać plik", "s3-1")
    m.ol([
        "Kliknij ikonę <b>„+”</b> w pasku wprowadzania i wybierz plik na urządzeniu.",
        "Albo <b>skopiuj i wklej</b> plik bezpośrednio w pole wprowadzania.",
        "Plik pojawi się w prompcie przed wysłaniem — upewnij się, że załączone jest "
        "dokładnie to, co trzeba.",
        "Wyślij prompt wraz z krótkim opisem zadania: „przeanalizuj”, „przetłumacz”, "
        "„zbierz raport z tych danych”.",
    ])
    m.callout("warn", "Przełączanie areny przy wgrywaniu obrazka",
              "Jeśli wgrywasz obraz w Text Arena, platforma automatycznie przełączy Cię do "
              "Image Arena: zakłada, że chcesz edytować grafikę, a nie tylko pokazać ją "
              "modelowi. Aby wrócić do zwykłego promptu z kontekstem wizualnym, wyjdź z "
              "Image Arena.")

    m.h2("3.2. Obsługiwane formaty wgrywania", "s3-2")
    m.table(
        ["Tryb", "Obsługiwane typy"],
        [
            ["<b>Agent Mode</b>",
             "PNG, WebP, JPEG, GIF, PDF, TXT, Markdown, CSV, HTML, XML, CSS, JavaScript, JSON"],
            ["<b>Battle Mode</b>",
             "PNG, JPEG, WebP, PDF"],
            ["<b>Przez GitHub</b>",
             "Dowolne pliki repozytorium: agent pracuje na klonie i nie jest ograniczony "
             "listą wgrywania"],
        ],
        widths=[1.0, 3.4],
    )
    m.p("Jeśli potrzebny format nie jest obsługiwany przy wgrywaniu (np. DOCX, XLSX, PPTX "
        "albo archiwum), są dwie drogi obejścia: położyć plik w podłączonym repozytorium "
        "i poprosić agenta, aby wziął go stamtąd, albo wyeksportować dane do obsługiwanego "
        "formatu (CSV, JSON, TXT, Markdown).")

    m.h2("3.3. Jak agent obchodzi się z Twoimi plikami", "s3-3")
    m.p("Wgrany plik trafia do przestrzeni roboczej sesji, a dalej agent wybiera sposób pracy "
        "według typu treści:")
    m.ul([
        "<b>Obrazy</b> — ogląda bezpośrednio jako kontekst wizualny: opisuje, porównuje, "
        "używa jako referencji do generacji.",
        "<b>PDF</b> — czyta po stronach; przy dużej objętości wyciąga tekst narzędziami w "
        "piaskownicy i pracuje na tekście, a nie na „obrazku strony”.",
        "<b>Tabele (CSV)</b> — ładuje do środowiska analizy i liczy: grupowania, "
        "podsumowania, filtry, wykresy.",
        "<b>Tekst, Markdown, HTML, CSS, JS, JSON, XML</b> — czyta i poprawia jak kod lub "
        "znaczniki, może wykonać i sprawdzić.",
        "<b>Duże pliki</b> — czyta fragmentami przez powłokę (po stronach, po zakresach "
        "linii, po szukaniu), żeby nie tracić kontekstu.",
    ])

    m.h2("3.4. Jak odebrać wynik", "s3-4")
    m.table(
        ["Scenariusz", "Jak uzyskać pliki", "Ograniczenia"],
        [
            ["Repozytorium niepodłączone",
             "Panel <b>Workspace</b> po prawej → przycisk <b>Download</b> → archiwum ZIP "
             "z plikami sesji",
             "Archiwum trzeba pobrać przed zakończeniem pracy z czatem"],
            ["Sesja „zepsuła się”, ale pliki są potrzebne",
             "Dodaj <b>/download-workspace</b> na końcu URL tej sesji Agent Mode — pobiorą "
             "się ostatnie pliki przestrzeni roboczej",
             "To droga zapasowa; oddaje tylko to, co leży w workspace"],
            ["Podłączony GitHub",
             "ZIP nie jest tworzony: agent commituje zmiany do gałęzi roboczej i otwiera "
             "Pull Request. Sprawdzasz w <b>Diff</b>, mergujesz lub pobierasz gałąź",
             "Jeden PR na sesję; po merge lub zamknięciu PR sesja nie może już pushować"],
        ],
        widths=[1.0, 2.2, 1.8],
    )
    m.callout("bad", "Główna pułapka: pliki po merge",
              "Gdy tylko Pull Request zostanie zmergowany lub zamknięty, sesja traci "
              "możliwość wysyłania zmian na GitHub. Wszystko, co agent stworzy potem, "
              "zostanie tylko wewnątrz czatu: nie da się tego wypchnąć, pobrać ani "
              "przenieść do nowej sesji. Najpierw upewnij się, że wszystko jest wysłane, "
              "i dopiero potem merguj; do nowej pracy zakładaj nową sesję.")
    m.shot("shots/arena_workspace.png", "https://arena.ai/agent",
             "Rys. 3. Panel Workspace po prawej (zrzut z help.arena.ai): tu leżą pliki sesji — zarówno wgrane, jak i utworzone przez agenta. Ikona strzałki w dół w nagłówku panelu pobiera wynik.")

    # ---------------------------------------------------------- 4. DOKUMENTY
    m.h1("4. Praca z dokumentami i treściami tekstowymi", "s4")
    m.lead("Dokumenty to najczęstszy przypadek użycia Agent Mode: rozebrać plik wejściowy, "
           "złożyć nowy, przełożyć jeden format na inny. Rozdział opisuje, jak działa to "
           "w praktyce.")

    m.h2("4.1. Czytanie dokumentów wejściowych", "s4-1")
    m.table(
        ["Typ", "Co potrafi agent", "Jak prosić"],
        [
            ["PDF",
             "Wydobyć tekst i strukturę, znaleźć potrzebne sekcje, zrobić streszczenie, "
             "złożyć tabelę porównawczą z kilku dokumentów",
             "„Wyciągnij z PDF wymagania wobec wykonawcy i przedstaw tabelą”"],
            ["DOCX",
             "Przeczytać przez bibliotekę parsowania Worda, wydobyć tekst, tabele i "
             "strukturę nagłówków",
             "Plik musi być dostępny w sesji: wgraj obsługiwany eksport albo połóż plik "
             "w repozytorium"],
            ["XLSX / CSV",
             "Wczytać arkusze, sprawdzić typy danych, policzyć agregaty, znaleźć anomalie, "
             "zbudować wykresy",
             "„Sprawdź plik pod kątem duplikatów i braków, pokaż top-10 po przychodzie”"],
            ["PPTX",
             "Rozebrać slajdy i tekst, przygotować strukturę nowej prezentacji",
             "„Złóż z raportu prezentację na 10 slajdów”"],
            ["Obrazy i skany",
             "Przeczytać jako obraz; w razie potrzeby rozpoznać tekst",
             "„Przetłumacz tekst ze skanu do Markdown”"],
            ["Kod i konfiguracje",
             "Przeczytać, wyjaśnić, zrefaktorzyć, pokryć testami, uruchomić",
             "„Znajdź, gdzie gubi się autoryzacja, i napraw”"],
        ],
        widths=[0.8, 2.0, 1.6],
    )

    m.h2("4.2. Tworzenie dokumentów: o jaki format prosić", "s4-2")
    m.p("Agent umie składać dokumenty programowo, dlatego format wyniku wybierasz sam. "
        "Praktyczna zasada: <b>proś o nowoczesne formaty OOXML</b> — DOCX, XLSX, PPTX. To "
        "właśnie one poprawnie otwierają się w podglądzie Arena i w pakietach biurowych; "
        "przestarzałe DOC i PPT nie wyświetlą się w aplikacji i pobiorą się jako zwykłe "
        "pliki.")
    m.table(
        ["Potrzebujesz", "Proś o format", "Dlaczego"],
        [
            ["Raport, umowa, regulamin", "<b>DOCX</b> lub Markdown",
             "DOCX edytuje się w Wordzie i pokazuje w podglądzie"],
            ["Tabele, sprawozdawczość, dane", "<b>XLSX</b> (w razie potrzeby CSV)",
             "Formuły, arkusze, formatowanie; CSV — do eksportu do innych systemów"],
            ["Prezentacja", "<b>PPTX</b>", "Otwiera się w PowerPoincie i w podglądzie Arena"],
            ["Wersja końcowa „do druku”", "<b>PDF</b>",
             "Utrwala skład; pilnuj, by dla polskich znaków użyto czcionki z ich obsługą"],
            ["Artykuł, README, baza wiedzy", "<b>Markdown</b>",
             "Lekki, wersjonowany w gicie, konwertowalny do czegokolwiek"],
            ["Landing, dashboard, prototyp", "<b>HTML</b> (lub projekt + serwer deweloperski)",
             "Można obejrzeć na żywo w podglądzie portu"],
            ["Schematy i ilustracje", "<b>SVG</b> lub PNG",
             "SVG osadza się w HTML i skaluje bez strat"],
        ],
        widths=[1.2, 1.1, 2.1],
    )

    m.h2("4.3. Podgląd plików i jego ograniczenia", "s4-3")
    m.p("Gdy agent kończy plik, otwiera go w przeglądarce Arena. Formaty z bogatym "
        "podglądem: tekst i kod, Markdown, HTML, SVG, obrazy, audio, wideo, PDF, CSV oraz "
        "dokumenty Office (DOCX, XLSX, PPTX). Cała reszta jest oferowana do pobrania.")
    m.p("Podgląd renderuje się w izolowanej ramce iframe bez dostępu do sieci. Dlatego "
        "zewnętrzne czcionki, style, obrazki i biblioteki z CDN wewnątrz HTML nie załadują "
        "się w podglądzie — strona wyświetli się uproszczono. Sam pobrany plik działa przy "
        "tym pełnoprawnie w przeglądarce. Jeśli potrzebny jest podgląd „jak w życiu”, "
        "poproś agenta o osadzenie stylów i grafiki wewnątrz pliku albo o podniesienie "
        "lokalnego serwera i oddanie linku.")
    m.callout("warn", "Polskie znaki w PDF",
              "Przy generowaniu PDF z kodu potrzebna jest czcionka z obsługą polskich "
              "znaków (np. rodzina DejaVu). Bez tego zamiast liter z ogonkami pojawiają się "
              "kwadraty lub puste miejsca. Dobry nawyk — poprosić agenta, by po zbudowaniu "
              "otworzył PDF i upewnił się, że tekst się czyta.")

    m.h2("4.4. Techniki pracy z dużymi dokumentami", "s4-4")
    m.ul([
        "<b>Najpierw struktura, potem detale.</b> Poproś o spis treści lub listę sekcji — "
        "łatwiej wybrać, co czytać w całości.",
        "<b>Drobij zadanie.</b> Jeden przebieg — jeden cel: najpierw streszczenie, potem "
        "tabela, potem oprawa. Tak ginie mniej detali.",
        "<b>Proś o kontrole.</b> „Przelicz sumy z danych źródłowych i pokaż rozbieżności” — "
        "taniej niż szukać błędu w gotowym raporcie.",
        "<b>Utrwalaj źródła.</b> Przy zadaniach analitycznych proś o listę linków i dat przy "
        "każdym stwierdzeniu.",
        "<b>Zapisuj rzeczy pośrednie.</b> Szkic w Markdownie lub CSV w przestrzeni roboczej "
        "przeżywa sesję i przyspiesza kolejną iterację.",
    ])
    m.shot("shots/arena_attach.png", "https://arena.ai/agent",
             "Rys. 4. Analiza dokumentu na żywo (zrzut z help.arena.ai): agent „Thought” — pomyślał, „Searched / Fetched / Read” — znalazł i przeczytał źródło, a wynik zapisze do pliku w Workspace.")

    # ---------------------------------------------------------- 5. NARZĘDZIA
    m.h1("5. Narzędzia agenta: co potrafi", "s5")
    m.lead("Możliwości Agent Mode określa zestaw narzędzi. Zrozumienie tego zestawu pomaga "
           "formułować zadania tak, by agent użył właściwego narzędzia za pierwszym razem.")

    m.h2("5.1. Zestaw podstawowy", "s5-1")
    m.table(
        ["Narzędzie", "Co robi", "Typowe zapytanie"],
        [
            ["<b>Powłoka (bash)</b>",
             "Wykonuje komendy: instalacja pakietów, uruchamianie skryptów, testy, build, "
             "obróbka plików",
             "„Zainstaluj zależności i przepuść testy, pokaż wynik”"],
            ["<b>Operacje na plikach</b>",
             "Tworzy, czyta, poprawia pliki; składa projekty z wielu plików",
             "„Złóż raport do jednego pliku i otwórz go”"],
            ["<b>Wyszukiwarka webowa</b>",
             "Szuka aktualnych informacji i zwraca źródła",
             "„Znajdź aktualne cenniki i przedstaw tabelą z linkami”"],
            ["<b>Czytanie stron</b>",
             "Pobiera tekst konkretnej strony lub dokumentu spod URL, w tym PDF",
             "„Przeczytaj tę stronę dokumentacji i streść wymagania”"],
            ["<b>Generowanie obrazów</b>",
             "Tworzy ilustracje, logotypy, makiety; umie edytować istniejące grafiki",
             "„Zrób okładkę raportu w stonowanych niebieskich barwach”"],
            ["<b>Mowa (TTS)</b>",
             "Czyta tekst na głos: najpierw wybierany jest głos, potem syntezowany plik "
             "audio",
             "„Czytaj wstęp głosem lektora”"],
            ["<b>Szukanie obrazów</b>",
             "Znajduje grafiki w sieci i zapisuje je w przestrzeni roboczej",
             "„Dobierz trzy fotografie do slajdów”"],
            ["<b>Pytania doprecyzowujące</b>",
             "Zadaje pytania z wariantami odpowiedzi, jeśli zadanie jest niejednoznaczne",
             "Odpowiadaj na nie — to mocniej wpływa na wynik niż długi prompt"],
            ["<b>Procesy w tle</b>",
             "Uruchamia serwery deweloperskie i długie zadania, oddaje żywy podgląd",
             "„Podnieś stronę lokalnie i pokaż podgląd”"],
            ["<b>Konektory</b>",
             "Podłączają usługi zewnętrzne i dają agentowi ich narzędzia",
             "„Weź zadania z naszego trackera i złóż raport” (jeśli usługa jest podłączona)"],
        ],
        widths=[1.0, 2.0, 1.8],
    )

    m.h2("5.2. Powłoka: co wolno, a na co nie liczyć", "s5-2")
    m.ul([
        "<b>Wolno:</b> instalować pakiety, uruchamiać testy i lintery, konwertować formaty, "
        "liczyć dane, podnosić serwery, pracować z gitem.",
        "<b>Nie licz na to, że:</b> zainstalowane pakiety i uruchomione procesy przeniosą "
        "się do następnej wiadomości — otoczenie podnosi się od nowa.",
        "<b>Długie komendy</b> (serwer deweloperski, watcher, build) uruchamiaj procesem "
        "w tle, inaczej komenda po prostu urwie się po limicie czasu.",
        "<b>Sieć jest dostępna</b> do instalacji zależności i zapytań do API, ale podgląd "
        "w przeglądarce działa przez proxy platformy — serwer musi nasłuchiwać na "
        "wszystkich interfejsach, a nie tylko na adresie lokalnym.",
    ])

    m.h2("5.3. Badanie w internecie", "s5-3")
    m.p("Przy zadaniach „znajdź i zrozum” agent łączy szukanie i czytanie stron: szuka "
        "źródeł, otwiera trafne, wydobywa fakty i składa wynik z linkami. Przydatne "
        "doprecyzowania w prompcie: okres („z ostatniego roku”), typ źródeł („oficjalna "
        "dokumentacja, nie blogi”), głębokość („krótkie streszczenie” albo „rozbiór "
        "z cytatami”), format wyniku (tabela, lista, raport).")

    m.h2("5.4. Obrazy i dźwięk", "s5-4")
    m.p("Generowanie obrazów tworzy jeden samodzielny plik na wywołanie. Jeśli nie masz "
        "pewności co do stylu, poproś o warianty: agent pokaże kilka osobnych kandydatów, "
        "a Ty wybierzesz jeden — dalej praca pójdzie z nim. Poprawki („zrób jaśniejsze "
        "tło”, „dodaj tekst”) robi się na wybranym obrazie.")
    m.p("Udźwiękowienie działa w dwóch krokach: najpierw dobierany jest głos (dostajesz do "
        "odsłuchu dwa warianty i wybierasz), potem syntezowane jest audio. Syntezowana jest "
        "tylko mowa — śpiew jest niedostępny. Długie teksty dzielone są na fragmenty po "
        "zdaniach.")

    # ---------------------------------------------------------- 6. USŁUGI
    m.h1("6. Jak Arena współpracuje z usługami zewnętrznymi", "s6")
    m.lead("Łączność ze światem zewnętrznym idzie trzema drogami: konektory (autoryzowany "
           "dostęp do usługi), bezpośredni dostęp do sieci z piaskownicy oraz "
           "wyspecjalizowane areny. Poniżej — mechanika każdej drogi.")

    m.h2("6.1. Czym jest konektor", "s6-1")
    m.p("Konektor to autoryzowane podłączenie do konkretnej usługi. Daje agentowi zestaw "
        "narzędzi tej usługi: przeczytać Twoje dane, utworzyć rekord, wysłać wiadomość, "
        "otworzyć zadanie. Autoryzacja przechodzi przez OAuth po stronie usługi, dlatego "
        "hasła agentowi nie przekazujesz, a zakres dostępu określasz sam na ekranie "
        "potwierdzenia.")
    m.ol([
        "<b>Podłącz usługę</b> w panelu połączeń — otworzy się okno autoryzacji usługi.",
        "<b>Ogranicz dostęp</b>: tam, gdzie usługa na to pozwala, wybieraj konkretne "
        "zasoby (np. poszczególne repozytoria, a nie wszystkie naraz).",
        "<b>Włącz przełącznik</b> usługi dla konkretnego czatu: połączenie może istnieć, "
        "ale być wyłączone dla bieżącej sesji.",
        "<b>Poproś agenta</b> o wykonanie działania. Sam określi potrzebną usługę, załaduje "
        "jej narzędzia i wykona operację.",
    ])

    m.h2("6.2. Stany połączenia", "s6-2")
    m.table(
        ["Stan", "Co oznacza", "Co zrobić"],
        [
            ["<b>Nie podłączono</b>", "Nie autoryzowałeś tej usługi",
             "Podłącz ją w panelu połączeń"],
            ["<b>Podłączono, ale wyłączono</b>",
             "Usługa jest autoryzowana, ale odłączona dla bieżącego czatu",
             "Włącz przełącznik usługi w tej rozmowie"],
            ["<b>Włączono</b>", "Narzędzia usługi są dostępne dla agenta",
             "Formułuj zadanie — agent wywoła je sam"],
            ["<b>Błąd dostępu</b>",
             "Token wygasł, uprawnienia cofnięto albo usługa jest niedostępna",
             "Podłącz usługę ponownie; przy ponownym podłączeniu zwykle wystarczy "
             "reautoryzacja, lista zasobów się zachowuje"],
        ],
        widths=[1.1, 1.7, 1.9],
    )
    m.shot("shots/arena_toggle.png", "https://arena.ai/agent",
             "Rys. 5. Menu Connections (połączenia) w pasku wprowadzania (zrzut z help.arena.ai): usługa GitHub jest podłączona i włączona zielonym przełącznikiem dla tego czatu.")

    m.h2("6.3. Zasady pracy konektorów, które warto znać", "s6-3")
    m.ul([
        "<b>Narzędzia dogrywają się na żądanie.</b> Agent najpierw patrzy, jakie narzędzia "
        "daje usługa, i dopiero potem je wywołuje. Dlatego pierwsze zapytanie do nowej "
        "usługi trwa trochę dłużej.",
        "<b>Jedna usługa — jeden czat.</b> Połączenie włącza się i wyłącza na poziomie "
        "rozmowy: tak kontrolujesz, do czego jest dostęp w konkretnym zadaniu.",
        "<b>Identyfikatory biorą się z realnych danych.</b> Aby utworzyć zadanie, stronę "
        "czy wiadomość, agent najpierw pobiera listę dostępnych obiektów i używa "
        "identyfikatorów stamtąd. Nie wymyśla identyfikatorów — dlatego czasem najpierw "
        "wykonuje się „lista”, a dopiero potem „utwórz”.",
        "<b>Działania wykonują się w Twoim imieniu.</b> Wszystko, co agent robi w usłudze, "
        "wygląda jak Twoje działanie i podlega Twoim uprawnieniom: czego nie widzisz Ty, "
        "nie zobaczy też agent.",
        "<b>Odłączenie jest odwracalne.</b> Jeśli odłączysz usługę i podłączysz ponownie, "
        "zwykle wystarczy ponowna autoryzacja — wybrane zasoby się zachowują.",
    ])

    m.h2("6.4. Bezpośredni dostęp do sieci z piaskownicy", "s6-5")
    m.p("Oprócz konektorów agent ma zwykły dostęp sieciowy z powłoki: może instalować "
        "pakiety z publicznych rejestrów, zwracać się do otwartych API, pobierać dane "
        "i dokumenty. To roboczy sposób podłączenia usługi, dla której nie ma gotowego "
        "konektora.")
    m.code([
        "# schemat pracy z dowolnym API z piaskownicy",
        "export MY_TOKEN=&lt;wartość&gt;        # sekret zadaje się jako zmienna, nie w prompcie",
        "curl -s -H \"Authorization: Bearer $MY_TOKEN\" https://api.example.com/v1/items",
        "python3 -c \"import requests, json; ...\"   # albo pełnoprawny skrypt z parsem odpowiedzi",
    ], "Przykład: zwrócenie się do zewnętrznego API bez konektora")
    m.callout("bad", "Sekrety i tokeny",
              "Nie wklejaj kluczy API, haseł i tokenów do tekstu promptu: dialog to nie "
              "magazyn sekretów. Jeśli bez klucza się nie obejdzie, przekazuj go jako "
              "zmienną środowiskową albo przez mechanizm, który udostępnia usługa, i cofnij "
              "klucz po zakończeniu pracy.")

    m.h2("6.5. Inne powierzchnie Areny", "s6-7")
    m.table(
        ["Powierzchnia", "Co daje", "Jak włączyć"],
        [
            ["<b>Code Arena (Fullstack)</b>",
             "Aplikacje z bazą danych, uwierzytelnianiem, integracjami zewnętrznymi "
             "i wdrożeniem",
             "Wybór trybu Code Arena; wygodne do prototypów od zera"],
            ["<b>Image Arena</b>",
             "Generowanie i porównywanie obrazów, edycja wgranych grafik",
             "Włącza się automatycznie przy wgrywaniu obrazu w Text Arena"],
            ["<b>Video Arena</b>", "Generowanie wideo", "Wybór trybu Video Arena"],
            ["<b>Auto-Mode</b>", "Automatyczny wybór modalności pod zadanie",
             "Funkcja eksperymentalna, włączana w menu trybów"],
            ["<b>Wybór konkretnego modelu</b>",
             "Praca z wybranym modelem zamiast losowej pary",
             "Selektor modeli; w Agent Mode model orkiestratora nie jest ujawniany"],
        ],
        widths=[1.1, 2.1, 1.8],
    )

    # ---------------------------------------------------------- 7. KONEKTORY
    m.h1("7. Konektory szczegółowo: GitHub, Google i inne usługi", "scon")
    m.lead("Konektory to sposób, w jaki Arena daje agentowi dostęp do usług zewnętrznych. "
           "Poniżej — szczegółowe instrukcje dla każdego z nich: do czego służy, jak się go "
           "podłącza, jak przebiega praca i o czym pamiętać. Dokładny zestaw konektorów "
           "zależy od konta i wersji: źródłem prawdy jest panel połączeń.")

    m.h2("7.1. GitHub — kod i repozytoria", "scon-gh")
    m.p("GitHub to flagowe podłączenie Agent Mode: czat zamienia się w środowisko "
        "deweloperskie pracujące wprost na Twoim kodzie. Agent czyta repozytorium, poprawia "
        "pliki, uruchamia testy, commituje zmiany i otwiera Pull Requesty; Ty zajmujesz się "
        "review i mergem.")
    m.table(
        ["Do czego służy", "Co dostajesz na wyjściu"],
        [
            ["Naprawa błędów w istniejącym projekcie",
             "PR z poprawką, opisem przyczyny i zielonymi Checks"],
            ["Nowe funkcje i refaktoring",
             "Zmiany w gałęzi roboczej, diff do review, testy"],
            ["Aktualizacja zależności i audyt CI",
             "Zaktualizowane manifesty i raport o tym, co się zepsuło"],
            ["Review kodu przed mergem",
             "Lista ryzyk i braków w testach dla otwartego PR"],
            ["Prototypy na realnym kodzie",
             "Działająca funkcjonalność w Twoim repozytorium, a nie w czacie"],
        ],
        widths=[1.6, 2.8],
    )
    m.h3("Podłączanie")
    m.ol([
        "Włącz konektor GitHub w Agent Mode.",
        "Przejdź autoryzację GitHub (OAuth) — Arena dostanie dostęp do Twojego konta.",
        "Kliknij <b>Manage repositories</b> i wybierz organizacje i repozytoria, do których "
        "dajesz dostęp.",
        "Upewnij się, że przełącznik GitHub jest włączony właśnie w tym czacie.",
        "Wybierz repozytorium i gałąź, potem opisz zadanie.",
    ])
    m.h3("Jak przebiega praca")
    m.p("Na początku sesji Arena klonuje wybrane repozytorium do piaskownicy: agent bada "
        "i poprawia kod na izolowanej kopii. Wszystkie zmiany pokazują się w panelu "
        "<b>Diff</b> — można oglądać tylko ostatni ruch agenta albo całą gałąź, "
        "z podświetlaniem składni. Panel <b>Checks</b> pokazuje status automatycznych "
        "kontroli commitów i PR: przechodzi, padło albo jeszcze się wykonuje. Agent sam "
        "wykonuje commit, push i utworzenie Pull Requesta; Ty zajmujesz się review "
        "i mergem.")
    m.shot("shots/arena_manage.png", "https://arena.ai/agent",
             "Rys. 6. Wybór repozytorium po włączeniu GitHuba (zrzut z help.arena.ai): „Select a repository” — wybierz repozytorium, „Branch” — gałąź, kółko zębate po prawej — zarządzanie połączeniami.")
    m.h3("Scenariusze i prompty")
    m.table(
        ["Scenariusz", "Prompt"],
        [
            ["Naprawić błąd",
             "„W repozytorium X w gałęzi main napraw błąd Z. Uruchom testy, pokaż wynik "
             "i otwórz PR z opisem przyczyny.”"],
            ["Dodać funkcję",
             "„Dodaj endpoint /report z miesięcznym podsumowaniem. Pokryj testami, nie "
             "ruszaj konfiguracji, otwórz PR.”"],
            ["Zaktualizować zależności",
             "„Zaktualizuj zależności, przepuść build i testy, sporządź raport: co się "
             "zmieniło i co się zepsuło.”"],
            ["Zrobić review",
             "„Obejrzyj ostatni otwarty PR: wylistuj ryzyka i braki w testach.”"],
        ],
        widths=[1.0, 3.4],
    )
    m.h3("Ograniczenia")
    m.ul([
        "<b>Jeden Pull Request na sesję.</b> Kilka PR z jednego czatu na razie nie jest "
        "obsługiwane: dziel dużą pracę na sesje.",
        "<b>ZIP się nie pobiera.</b> Jeśli repozytorium jest podłączone, wynik idzie na "
        "GitHub, nie do archiwum.",
        "<b>Po merge nie można pushować.</b> Pliki utworzone po merge lub zamknięciu PR "
        "zostaną tylko w czacie.",
        "<b>Repozytorium musi istnieć.</b> Utworzyć projekt od zera i wypchnąć go pierwszym "
        "commitem nadal musisz Ty; dalej agent przejmuje pracę.",
        "<b>Kod wykonuje się w chmurze,</b> a nie na Twoim komputerze: lokalnego środowiska "
        "nie rusza.",
        "<b>Odłączenie jest odwracalne.</b> Przy ponownym podłączeniu GitHuba wystarczy "
        "reautoryzacja — lista repozytoriów się zachowuje.",
    ])

    m.h2("7.2. Google — dokumenty, pliki, poczta, kalendarz", "scon-g")
    m.p("Jeśli w Twojej wersji dostępny jest konektor Google, daje on agentowi dostęp do "
        "usług Twojego konta: Drive, Dokumenty, Arkusze, Gmail, Kalendarz. Wszystkie "
        "działania wykonują się w Twoim imieniu i tylko w uprawnieniach, które zatwierdziłeś "
        "na ekranie OAuth.")
    m.table(
        ["Usługa", "Do czego służy", "Przykładowy prompt"],
        [
            ["Drive", "Pliki źródłowe i wyniki: raporty, eksporty, prezentacje",
             "„Odłóż gotowy raport do folderu Raporty na Drive”"],
            ["Dokumenty", "Teksty: regulaminy, notatki ze spotkań, wersje robocze",
             "„Złóż z konspektu dokument projektu i dodaj wstęp”"],
            ["Arkusze", "Dane i obliczenia: odczyt arkuszy, agregaty, nowe wiersze",
             "„Policz w tabeli sumy po miesiącach i dodaj arkusz podsumowania”"],
            ["Gmail", "Kontekst korespondencji i wysyłka wyniku",
             "„Szkicuj odpowiedź do klienta na ostatni e-mail”"],
            ["Kalendarz", "Harmonogram, spotkania, przypomnienia",
             "„Znajdź wolny slot na sync w tym tygodniu i utwórz spotkanie”"],
        ],
        widths=[0.7, 1.9, 1.8],
    )
    m.h3("Podłączanie")
    m.ol([
        "Otwórz panel połączeń i wybierz Google.",
        "Przejdź OAuth Google i wybierz konto, do którego dajesz dostęp.",
        "Na ekranie uprawnień zatwierdź tylko potrzebne zakresy (np. odczyt Drive i edycja "
        "Dokumentów); nie potwierdzaj niczego „na zapas”.",
        "Włącz przełącznik Google w potrzebnym czacie.",
        "Zacznij od zapytania testowego: „pokaż 10 ostatnich plików na Drive” — tak "
        "upewnisz się, że dostęp działa, zanim dasz zadanie bojowe.",
    ])
    m.h3("Jak przebiega praca")
    m.p("Praca zaczyna się od „listy i szukania”: agent znajduje potrzebne obiekty — pliki, "
        "e-maile, spotkania — po realnych identyfikatorach, a potem działa: czyta, tworzy, "
        "aktualizuje. Wynik pojawia się w Twoim Google: dokument na Drive, e-mail "
        "w wysłanych, wydarzenie w kalendarzu. Po zadaniu sprawdź, co dokładnie powstało.")
    m.h3("O czym pamiętać")
    m.ul([
        "Działania są widoczne dla otoczenia jako Twoje: e-mail wysłany przez agenta jest "
        "wysłany z Twojego konta.",
        "Dostęp cofniesz w każdej chwili w ustawieniach konta Google (sekcja bezpieczeństwa "
        "i dostępu stron trzecich); nowe zapytania po tym ustają.",
        "Poufne foldery i skrzynki trzymaj poza przyznanymi zakresami.",
        "Jeśli konektora nie ma na liście panelu — w tej wersji jest niedostępny: dane "
        "z Drive możesz przekazać przez wgranie pliku albo przez repozytorium.",
    ])

    m.h2("7.3. Inne połączenia: trackery, komunikatory, bazy wiedzy", "scon-other")
    m.p("Oprócz GitHuba i Google, zależnie od wersji konta, mogą być dostępne konektory do "
        "usług roboczych: baz wiedzy, trackerów zadań, komunikatorów, magazynów plików, "
        "analityki. Logika jest ta sama: OAuth → wybór zasobów → przełącznik na czat → "
        "narzędzia na żądanie.")
    m.table(
        ["Grupa", "Do czego służy", "Przykład zadania"],
        [
            ["Kod i repozytoria",
             "Praca na realnym kodzie: czytanie, poprawki, gałęzie, PR",
             "Naprawić błąd, dodać funkcję, zaktualizować zależności (w Arena to GitHub)"],
            ["Dokumenty i bazy wiedzy",
             "Czytać materiały wewnętrzne i publikować wyniki",
             "Złożyć regulamin z rozproszonych notatek, opublikować raport"],
            ["Zadania i projekty",
             "Brać zadania do pracy i raportować status",
             "Sporządzić raport sprintu, rozłożyć backlog po priorytetach"],
            ["Komunikatory i poczta",
             "Zbierać kontekst dyskusji i wysyłać wynik",
             "Streszczenie korespondencji z tygodnia, rozsyłka ogłoszenia"],
            ["Magazyny plików",
             "Brać źródła i odkładać wynik",
             "Obrobić eksport, rozłożyć pliki po folderach"],
            ["Analityka i dane",
             "Zapytania do metryk produktowych i biznesowych",
             "Sprawdzić hipotezę na danych, złożyć raport dashboardowy"],
        ],
        widths=[1.0, 1.8, 2.2],
    )
    m.callout("info", "Jak sprawdzić, co jest dostępne akurat dla Ciebie",
              "Zapytaj agenta wprost: „Które usługi są podłączone do tego czatu?” Odpowie "
              "według listy połączeń, nie według domysłów. Jeśli potrzebna usługa nie jest "
              "podłączona — agent to powie i zaproponuje podłączenie, a nie będzie imitować "
              "pracy.")

    m.h2("7.4. Dobór konektora do zadania", "scon-pick")
    m.table(
        ["Zadanie", "Co podłączyć"],
        [
            ["Naprawić kod lub dodać funkcję w projekcie", "GitHub"],
            ["Złożyć raport z firmowych plików i odłożyć wynik do wspólnego folderu",
             "Google Drive / Dokumenty (jeśli dostępne) albo magazyn plików"],
            ["Pobrać zadania do pracy i zaktualizować statusy", "Tracker zadań (jeśli dostępny)"],
            ["Rozesłać wynik zespołowi lub klientowi", "Poczta lub komunikator"],
            ["Opublikować instrukcję w bazie wiedzy", "Baza wiedzy (Notion i podobne)"],
            ["Usługi nie ma w panelu, ale jest otwarte API",
             "Bezpośredni dostęp do sieci z piaskownicy (rozdział 6.4)"],
        ],
        widths=[2.6, 1.8],
    )

    # ---------------------------------------------------------- 8. PROMPTY
    m.h1("8. Jak stawiać zadania agentowi", "s7")
    m.lead("Jakość wyniku w Agent Mode niemal w całości określa sformułowanie. Poniżej — "
           "robocze techniki sprawdzone na realnych zadaniach.")

    m.h2("8.1. Formuła dobrego promptu", "s7-1")
    m.code([
        "CEL:       co ma powstać na wyjściu (artefakt, nie proces)",
        "KONTEKST:  kto jest odbiorcą, jakie dane i pliki są załączone, jakie ograniczenia",
        "FORMAT:    DOCX / XLSX / PDF / Markdown / HTML, struktura, objętość, język",
        "KRYTERIA:  po czym poznać, że zadanie jest wykonane (liczby, kontrole, źródła)",
        "GRANICE:   czego nie robić (nie ruszać plików X, nie zmieniać stylu)",
    ], "Szablon stawiania zadania")

    m.h2("8.2. Gotowe sformułowania", "s7-2")
    m.table(
        ["Zadanie", "Sformułowanie"],
        [
            ["Rozbiór dokumentu",
             "„Przeczytaj załączony PDF. Złóż streszczenie na 1 stronę w DOCX: cel, "
             "kluczowe ryzyka, terminy, odpowiedzialni. Wszystkie cytaty — z numerami "
             "stron.”"],
            ["Analiza danych",
             "„Wczytaj CSV. Sprawdź braki i duplikaty, policz dynamikę po miesiącach, "
             "znajdź top-10 kategorii. Wynik — XLSX z arkuszami: Dane, Podsumowanie, "
             "Wykresy.”"],
            ["Raport z badaniem",
             "„Zbierz przegląd rynku z ostatnich 12 miesięcy: tylko oficjalne źródła "
             "i duże redakcje. Format — Markdown, przy każdym stwierdzeniu link i data. "
             "Osobnym blokiem — czego nie udało się sprawdzić.”"],
            ["Poprawka kodu",
             "„W repozytorium X w gałęzi Y napraw błąd Z. Uruchom testy i pokaż wynik. "
             "Nie ruszaj plików konfiguracyjnych. Otwórz PR z opisem przyczyny.”"],
            ["Dokument „pod klucz”",
             "„Zrób instrukcję dla nowych pracowników w DOCX: sekcje, zaślepki zrzutów "
             "ekranu, tabela częstych błędów, checklista pierwszego dnia. Objętość 8–12 "
             "stron, ton neutralny.”"],
        ],
        widths=[1.0, 3.4],
    )

    m.h2("8.3. Pytania doprecyzowujące i korekta", "s7-3")
    m.p("Jeśli zadanie jest niejednoznaczne, agent zada pytania z wariantami odpowiedzi. "
        "Odpowiadaj na nie — to najtańszy sposób trafić w wynik za pierwszym podejściem. "
        "Jeśli wynik nie ten, koryguj konkretnie: „tabelę w orientacji poziomej”, "
        "„usuń rozdział 3”, „źródła tylko z lat 2025–2026”. Ogólne uwagi („zrób lepiej”) "
        "prawie zawsze dają rozmyty wynik.")
    m.callout("ok", "Zasada jednego zadania na wiadomość",
              "Jedna wiadomość — jeden cel. Kilka niezależnych celów w jednym prompcie "
              "rozmywa uwagę agenta; lepsze są kolejne repliki albo osobne sesje. Związane "
              "podzadania w obrębie jednego celu formułuj odwrotnie razem — tak agent "
              "złoży je w jeden spójny artefakt.")

    m.h2("8.4. Sesje równoległe", "s7-4")
    m.p("Związane, ale niezależne zadania wygodnie rozkładać na osobne czaty: każdy ma "
        "swoją piaskownicę, swój zestaw plików i swoją historię. Tak łatwiej śledzić postęp "
        "i nie mieszać kontekstu. W obrębie jednej sesji agent umie wykonywać niezależne "
        "kroki równolegle — np. jednocześnie generować kilka plików.")

    m.h2("8.5. Limity, archiwizacja, porządek w historii", "s7-5")
    m.ul([
        "<b>Kredyty.</b> Konto ma dzienny bilans użycia: pierwszy prompt uruchamia "
        "24-godzinny okres, w którym kredyty się zużywają. Przy zbliżaniu się do limitu "
        "pojawi się wskaźnik w pasku wprowadzania, przy wyczerpaniu — wiadomość "
        "z odliczaniem do odnowienia. Korzystanie z Battle Mode w Text Arena i Code Arena "
        "nie liczy się do dziennego bilansu.",
        "<b>Długie sesje.</b> Rozmowa może iść setki ruchów; żeby zmieścić się w kontekście, "
        "stara część historii może być ściskana do streszczenia. Krytyczne detale trzymaj "
        "w plikach przestrzeni roboczej, nie tylko w korespondencji.",
        "<b>Zatrzymanie.</b> Wykonanie można przerwać i skorygować zadanie, nie tracąc "
        "utworzonych plików.",
        "<b>Porządek.</b> Czaty można archiwizować i usuwać; przestrzeń robocza jest "
        "przypisana do sesji, więc cenne pliki warto od razu pobierać albo wysyłać do "
        "repozytorium.",
    ])

    # ---------------------------------------------------------- 9. JAKOŚĆ
    m.h1("9. Kontrola wyniku: jak odbierać pracę", "s8")
    m.lead("Agent potrafi oddać ładnie sformatowany, ale błędny wynik. Odbiór to Twoja "
           "strefa odpowiedzialności i da się go sformalizować w kilka kontroli.")

    m.h2("9.1. Czego wymagać od agenta", "s8-1")
    m.ol([
        "<b>Uruchomienia standardowej kontroli.</b> Testy projektu, build, linter, typy — "
        "to, czym sprawdzany jest właśnie ten kod. Proś wprost: „przepuść testy i pokaż "
        "wynik”.",
        "<b>Nazwanej ścieżki kontroli.</b> Normalna odpowiedź to „uruchomiono funkcję X, "
        "zwróciła Y”. Kontrola, która nie przechodzi przez zmieniony kod, niczego nie "
        "potwierdza: kontrola składni albo skrypt-„sobowtór” realnej logiki się nie "
        "liczą.",
        "<b>Uczciwych luk.</b> Jeśli nie da się sprawdzić (brak dostępu, brak danych), "
        "agent powinien powiedzieć to wprost i zaznaczyć niesprawdzone — a nie podawać "
        "domysł tonem faktu.",
        "<b>Zgodności z oczekiwaniami.</b> Czysty kod powrotu to nie oznaka sukcesu: jeśli "
        "zamiast 40 linii wyszło 39 albo wartość czyta się jako „fałsz”, to właśnie jest "
        "wynik, który trzeba naprawić.",
    ])

    m.h2("9.2. Checklista odbioru", "s8-2")
    m.table(
        ["Kontrola", "Jak się upewnić"],
        [
            ["Artefakt istnieje", "Plik otwiera się w podglądzie albo leży w Workspace"],
            ["Format jest właściwy", "DOCX/XLSX/PPTX się otwierają; PDF się czyta, polskie znaki są na miejscu"],
            ["Treść odpowiada zadaniu", "Porównaj strukturę z promptem: sekcje, objętość, język"],
            ["Liczby przeliczone", "Poproś o przeliczenie sum z danych źródłowych i pokazanie rozbieżności"],
            ["Źródła podane", "Przy każdym zewnętrznym fakcie — link i data"],
            ["Kod działa", "Testy/build uruchomione, wynik pokazany, w Checks brak czerwonych"],
            ["Wynik zapisany", "ZIP pobrany albo zmiany wypchnięte do gałęzi przed merge"],
        ],
        widths=[1.2, 3.2],
    )
    m.callout("ok", "Przydatny nawyk",
              "Kończ zadanie frazą: „Pokaż, co dokładnie sprawdziłeś i co zostało "
              "niesprawdzone”. To jedna linijka w prompcie, która wyraźnie podnosi "
              "rzetelność końcowego raportu.")

    # ---------------------------------------------------------- 10. OGRANICZENIA
    m.h1("10. Ograniczenia, bezpieczeństwo, prywatność", "s9")

    m.h2("10.1. Granice techniczne", "s9-1")
    m.ul([
        "Praca idzie w piaskownicy w chmurze: lokalne pliki Twojego komputera są "
        "niedostępne, jeśli sam ich nie wgrałeś.",
        "Zainstalowane pakiety i procesy w tle nie przeżywają następnej wiadomości; "
        "zachowują się tylko pliki katalogu roboczego.",
        "Obsługiwane typy wgrywania ogranicza lista z rozdziału 3.2; cała reszta — przez "
        "repozytorium lub konwersję.",
        "Przy podłączonym repozytorium — jeden PR na sesję i brak możliwości pusha po "
        "merge.",
        "Podgląd działa bez sieci: zewnętrzne zasoby wewnątrz HTML się w nim nie ładują.",
        "Model orkiestratora nie jest ujawniany i może się zmienić wewnątrz sesji przy "
        "ryzyku awarii.",
    ])

    m.h2("10.2. Czego nie oddawać agentowi", "s9-2")
    m.ul([
        "Haseł, kluczy API, tokenów, kluczy prywatnych i certyfikatów.",
        "Danych osobowych klientów, dokumentacji medycznej i bankowej bez konieczności.",
        "Materiałów objętych NDA, jeśli polityka Twojej organizacji na to nie pozwala.",
        "Pełnego dostępu do wszystkich repozytoriów organizacji — dawaj dostęp punktowo, "
        "na konkretne projekty.",
    ])
    m.p("Zasada minimalnego dostępu działa i tu: podłączaj tylko te usługi, które są "
        "potrzebne do zadania, i tylko te zasoby wewnątrz usługi, które się do niego "
        "odnoszą. Odłączyć konektor można w każdej chwili; cofnięcie dostępu po stronie "
        "usługi zatrzymuje nowe zapytania, ale nie cofa już pobranych danych.")

    m.h2("10.3. Zarządzanie danymi sesji", "s9-3")
    m.ul([
        "Czaty można archiwizować i usuwać; usunięcie kasuje też historię korespondencji.",
        "Pliki przestrzeni roboczej są przypisane do sesji — pobieraj wynik od razu.",
        "Twoje oceny, pochwały i uwagi są wykorzystywane do budowy leaderboarda Agent "
        "Arena.",
    ])

    # ---------------------------------------------------------- 11. AWARIE
    m.h1("11. Typowe awarie i co robić", "s10")
    m.table(
        ["Objaw", "Przyczyna", "Działanie"],
        [
            ["Plik się nie wgrywa",
             "Format spoza obsługiwanej listy",
             "Skonwertuj do PDF, TXT, MD, CSV, JSON albo połóż plik w repozytorium"],
            ["Wgranie obrazka zabrało Cię do Image Arena",
             "Automatyczne przełączenie modalności",
             "Wyjdź z Image Arena, by wrócić do tekstowego promptu"],
            ["Brak przycisku Download",
             "Do sesji podłączone jest repozytorium GitHub",
             "Wynik idzie do PR; albo dodaj /download-workspace do URL"],
            ["Pliki utworzone, ale się nie pobierają",
             "PR już zmergowany lub zamknięty",
             "Załóż nową sesję i powtórz potrzebną część pracy"],
            ["Komenda urywa się w połowie",
             "Długi proces uruchomiony zwykłą komendą",
             "Poproś o uruchomienie go procesem w tle i oddanie podglądu"],
            ["Zależności „zniknęły”",
             "Otoczenie jest odtwarzane między wiadomościami",
             "Poproś o reinstalację zależności albo dodaj instalację do skryptu builda"],
            ["Podgląd strony jest pusty",
             "Serwer nasłuchuje tylko adresu lokalnego albo blokuje zewnętrzny origin",
             "Poproś o przywiązanie serwera do wszystkich interfejsów i dopuszczenie "
             "originu podglądu"],
            ["W PDF zamiast polskich znaków kwadraty",
             "Czcionka bez obsługi polskich znaków",
             "Poproś o przebudowanie PDF czcionką obsługującą polskie znaki"],
            ["Agent mówi, że usługi nie ma",
             "Konektor niepodłączony lub wyłączony dla tego czatu",
             "Podłącz usługę i włącz jej przełącznik w bieżącej rozmowie"],
            ["Wynik wygląda wiarygodnie, ale liczby się nie zgadzają",
             "Kontrola nie była uruchamiana albo nie pokrywała zmian",
             "Zażądaj uruchomienia standardowej kontroli i pokazania faktycznego wyniku"],
            ["Skończyły się kredyty",
             "Dzienny bilans wyczerpany",
             "Poczekaj na odnowienie według odliczania; porównywanie w Battle Mode nie "
             "zużywa kredytów"],
        ],
        widths=[1.2, 1.5, 1.9],
    )

    # ---------------------------------------------------------- 12. FAQ
    m.h1("12. Krótkie odpowiedzi na częste pytania", "s11")
    m.table(
        ["Pytanie", "Odpowiedź"],
        [
            ["Czy można wybrać model w Agent Mode?",
             "Nie: orkiestrator wybierany jest losowo i nie jest ujawniany. Wybór modelu "
             "jest dostępny w innych trybach Areny."],
            ["Czy agent pracuje na moim komputerze?",
             "Nie, wszystko wykonuje się w piaskownicy w chmurze. Lokalnie dostajesz tylko "
             "pobrane pliki albo gałąź w repozytorium."],
            ["Ile plików można wgrać naraz?",
             "Ograniczenie wiąże się z formatem i rozmiarem; duże zestawy wygodniej "
             "przekazywać przez repozytorium albo archiwum w obsługiwanym formacie."],
            ["Czy można kontynuować pracę jutro?",
             "Tak, pliki katalogu roboczego zachowują się w ramach sesji. Ale cenny wynik "
             "pewniej pobrać albo wypchnąć od razu."],
            ["Co zrobić, jeśli sesja „zawiesiła się”?",
             "Zatrzymaj wykonanie i wyślij doprecyzowanie. Jeśli interfejs jest "
             "niedostępny, pliki i tak da się zabrać przez /download-workspace w URL."],
            ["Czy Agent Mode nadaje się do prostego pytania?",
             "Nie. Do jednorazowych pytań szybsze i oszczędniejsze są Battle, Direct lub "
             "Side-by-Side."],
            ["Po czym poznać, że zadanie jest wykonane?",
             "Po artefakcie i po kontroli: plik jest na miejscu, format właściwy, kontrola "
             "uruchomiona, a jej wynik zgodny z oczekiwaniami."],
        ],
        widths=[1.3, 3.1],
    )

    # ---------------------------------------------------------- 13. ŚCIĄGAWKA
    m.h1("13. Ściągawka: sesja w 8 krokach", "s12")
    m.ol([
        "<b>Określ artefakt.</b> Co ma leżeć w rękach na końcu: DOCX, XLSX, PDF, strona, "
        "gałąź z PR.",
        "<b>Podłącz potrzebne.</b> GitHub albo inna usługa — przed pierwszym promptem, "
        "z minimalnym zakresem dostępu.",
        "<b>Załącz kontekst.</b> Pliki, linki, ograniczenia — wszystko, co wpływa na "
        "wynik.",
        "<b>Sformułuj zadanie</b> według schematu: cel, kontekst, format, kryteria, "
        "granice.",
        "<b>Odpowiedz na pytania doprecyzowujące</b> — to tańsze niż przerabianie.",
        "<b>Sprawdź według checklisty</b> z rozdziału 9: format, treść, liczby, źródła, "
        "uruchomiona kontrola.",
        "<b>Skoryguj punktowo</b> i poproś o ponowne sprawdzenie zmienionego.",
        "<b>Odbierz wynik</b> — pobierz archiwum albo upewnij się, że zmiany są "
        "wypchnięte przed merge.",
    ])

    # ---------------------------------------------------------- 14. ŹRÓDŁA
    m.h1("14. Źródła i zastrzeżenie o aktualności", "s13")
    m.p("Instrukcja zebrana " + meta["version"] + " na podstawie oficjalnych materiałów "
        "Areny:")
    m.ul([
        "Centrum pomocy Arena, „How to use Agent Mode on Arena” — uruchamianie trybu, "
        "obsługiwane formaty wgrywania, przestrzeń robocza, /download-workspace, "
        "leaderboard Agent Arena i metodologia oceny.",
        "Centrum pomocy Arena, „How to use coding in Agent Mode” — podłączanie GitHuba, "
        "wybór repozytoriów, panel Diff, okno Checks, jeden PR na sesję.",
        "Centrum pomocy Arena, „How to Upload Files into Arena” — sposoby wgrywania, "
        "obsługiwane typy per tryb, automatyczne przełączanie do Image Arena.",
        "Centrum pomocy Arena, „How to understand Arena's Credit System” — dzienny "
        "bilans kredytów, wskaźnik limitu, wyjątek dla Battle Mode.",
        "Blog Arena, „Coding in Agent Mode: From Idea to Shipping with GitHub” oraz "
        "„Empowering Users to Get More Done With Agent Mode” — architektura pracy "
        "z repozytoriami, piaskownica, podgląd portów.",
    ])
    m.callout("warn", "Zastrzeżenie",
              "Opisy narzędzi i procesów pracy w rozdziałach 5–9 opierają się na "
              "zachowaniu Agent Mode w bieżącej wersji platformy i na praktyce pracy "
              "z agentem; konkretne nazwy przycisków i skład konektorów porównuj "
              "z interfejsem swojego konta — produkt aktualizuje się często i detale "
              "mogą się różnić.")


    # ---------------------------------------------------------- 15. NOWICJUSZ
    m.h1("15. Krok po kroku dla nowicjusza: dokumenty, programy i autobudowa przez GitHub", "sn")
    m.lead("Ten rozdział to trasa „od zera” do wyniku: agent sam robi dokumenty Word i Excel "
           "i odkłada je do Twojej internetowej szafki; tam też automatycznie budują się "
           "Twoje programy na Windowsa i Androida. Bez trudnych słów: każde niejasne słowo "
           "wyjaśnia słowniczek (rozdział 16). Po prostu idź po krokach i porównuj z "
           "obrazkami.")

    m.h2("15.1. Co będzie potrzebne i jak to w ogóle działa", "sn-1")
    m.p("Potrzebne są dwie rzeczy: darmowe konto na GitHubie (<a href=\"https://github.com/\" color=\"#1d4ed8\"><u>github.com</u></a>) i konto "
        "w Arena. Niczego nie trzeba instalować na komputerze.")
    m.p("Wyobraź sobie, że GitHub to Twoja osobista szafka na pliki w internecie. Arena "
        "dostaje od Ciebie klucz do szafki (to właśnie „podłączenie”), robi dokumenty "
        "i odkłada je do właściwych folderów. W każdej chwili otwierasz szafkę "
        "z komputera lub telefonu i zabierasz gotowe pliki.")
    m.ul([
        "Na końcu masz foldery „Activity” (akcje marketingowe) i „TP” (propozycje "
        "techniczne), w których leżą gotowe dokumenty Word i tabele Excel.",
        "Każdy dokument — z historią: widać, kiedy powstał i co się w nim zmieniało.",
        "Nic nie ginie: pliki mieszkają w Twojej „szafce”, a nie w korespondencji.",
    ])

    m.h2("15.2. Krok 1. Tworzymy „szafkę” — repozytorium na GitHubie", "sn-2")
    m.p("Repozytorium to po prostu folder w internecie. Tworzymy go raz:")
    m.ol([
        "Wejdź na <a href=\"https://github.com/\" color=\"#1d4ed8\"><u>github.com</u></a> i zaloguj się na konto.",
        "Kliknij znaczek „+” w prawym górnym rogu i wybierz New repository (albo zielony "
        "przycisk na stronie głównej) — rys. 7.",
        "W pole Repository name wpisz nazwę literami łacińskimi, bez spacji: na przykład "
        "moje-dokumenty.",
        "Wybierz Private — wtedy folder widzisz tylko Ty.",
        "Na dole formularza zaznacz Add a README file („dodaj plik README”) i kliknij zielony "
        "przycisk Create repository („utwórz repozytorium”) — folder nie będzie pusty, a "
        "przycisk Add file pojawi się od razu (rys. 9).",
    ])
    m.shot("shots/gh_new.png", "https://github.com/new",
             "Rys. 7. GitHub, menu „+” w nagłówku strony (zrzut z oficjalnej dokumentacji docs.github.com): punkt New repository — „nowe repozytorium” — obwiedziony.")
    m.shot("shots/gh_create.png", "https://github.com/new",
             "Rys. 8. Formularz tworzenia repozytorium (zrzut z docs.github.com): Owner — właściciel konta, Repository name — nazwa repozytorium; zielony napis „is available” — nazwa jest wolna.")
    m.shot("shots/gh_readme.png", "https://github.com/new",
           "Rys. 9. Dół formularza tworzenia (zrzut formularza na github.com): zaznacz "
           "„Add a README file” i kliknij zielony przycisk „Create repository” — wtedy "
           "repozytorium nie będzie puste i przycisk Add file pojawi się od razu.")

    m.p("Po utworzeniu zobaczysz stronę nowego folderu (rys. 10). Na razie jest w nim "
        "jeden plik README — to „metka” folderu. Foldery activity, tp i shablony agent "
        "utworzy sam, gdy dostanie pierwsze zadanie.")
    m.shot("shots/gh_files.png", "https://github.com/",
             "Rys. 10. Gotowe repozytorium (zrzut z docs.github.com): gałąź main, pierwszy commit Initial commit i plik README.md na liście.")
    m.p("Jeśli zapomnisz zaznaczyć README, repozytorium utworzy się puste: na stronie nie "
        "będzie przycisku Add file, a zamiast listy plików pojawi się blok „Quick setup” "
        "(rys. 11). To nie błąd — kliknij niebieskie łącze „uploading an existing file” "
        "(„wgraj istniejący plik”): otworzy się to samo okno wgrywania, a po pierwszym "
        "commicie pojawi się przycisk Add file.")
    m.shot("shots/gh_empty.png", "https://github.com/",
           "Rys. 11. Puste repozytorium: przycisku Add file jeszcze nie ma. Kliknij łącze "
           "„uploading an existing file” — otworzy okno wgrywania i utworzy pierwszy commit. "
           "Zrzut prawdziwego repozytorium na github.com.")

    m.callout("ok", "Nazwa — bez spacji i polskich znaków",
              "Dobre nazwy: moje-dokumenty, docs-activity, tp-baza. Złe: „Moje "
              "dokumenty”, „dokumenty 2026”. Litery łacińskie i myślnik to "
              "najpewniejszy wariant.")


    m.h2("15.3. Krok 2. Wgrywamy Twoje dokumenty do repozytorium", "sn-up")
    m.p("Żeby agent robił dokumenty według Twoich wzorów, wzory trzeba odłożyć do "
        "„szafki”. Pliki wgrywają się do repozytorium prosto w przeglądarce — żadnych "
        "programów nie trzeba:")
    m.ol([
        "Otwórz swoje repozytorium na <a href=\"https://github.com/\" color=\"#1d4ed8\"><u>github.com</u></a> i wejdź do potrzebnego folderu "
        "(np. shablony). Jeśli folderu jeszcze nie ma — najprościej poprosić agenta "
        "w Arena: „utwórz w repozytorium foldery shablony, activity i tp”.",
        "Wewnątrz folderu kliknij przycisk Add file i wybierz Upload files — rys. 12.",
        "Przeciągnij swój plik Worda lub Excela do okna, które się otworzy (albo kliknij "
        "„choose your files” i wybierz go na komputerze). Poczekaj, aż pasek wgrywania "
        "dojdzie do końca — rys. 13.",
        "Kliknij zielony przycisk Commit changes — plik zapisze się w folderze.",
        "Powtórz dla każdego wzoru: aktywnosc.docx, tp.docx, budzet.xlsx.",
    ])
    m.shot("shots/gh_upload.png", "https://github.com/",
             "Rys. 12. Przycisk Add file na stronie repozytorium (zrzut z docs.github.com): w rozwiniętym menu punkt Upload files — „wgraj pliki” — obwiedziony.")
    m.shot("shots/gh_files.png", "https://github.com/",
             "Rys. 13. Wynik wgrania (zrzut z docs.github.com): po kliknięciu Commit changes plik pojawia się na liście repozytorium, u góry — ostatni commit.")
    m.callout("warn", "Nie ma przycisku Add file?",
              "Znaczy to, że repozytorium jest puste — nie ma w nim żadnego commitu. Kliknij "
              "łącze „uploading an existing file” w bloku Quick setup (zob. rys. 11) albo "
              "utwórz README na stronie: przycisk „creating a new file”.")
    m.callout("warn", "Word i Excel nie wgrywają się do czatu Arena",
              "Czat przyjmuje obrazki, PDF, teksty i tabele CSV. Dlatego DOCX i XLSX "
              "pewniej odkładać do repozytorium przez GitHuba, jak wyżej. Agent potem "
              "weźmie szablony wprost z repozytorium.")
    m.callout("ok", "Co wgrać do repozytorium",
              "Twoje bieżące wzory: „Activity” z Waszą czapką i logiem, szablon TP, "
              "tabelę budżetu. Agent skopiuje oprawę ze wzoru i wszystkie nowe dokumenty "
              "będą wyglądać znajomo dla Ciebie.")

    m.h2("15.4. Krok 3. Podłączamy GitHuba do Arena", "sn-3")
    m.ol([
        "Otwórz Arena w trybie Agent Mode (<a href=\"https://arena.ai/agent\" color=\"#1d4ed8\"><u>arena.ai/agent</u></a>).",
        "Znajdź panel połączeń i kliknij Connect naprzeciw GitHuba — rys. 14, krok 1.",
        "Otworzy się okno GitHuba: zaloguj się i kliknij przycisk zgody na dostęp "
        "(Authorize). Hasło do GitHuba nie jest przekazywane agentowi — zgodę można "
        "cofnąć jednym kliknięciem.",
        "Wróć do Arena i kliknij Manage repositories: zaznacz haczykiem swoje "
        "repozytorium i zapisz — rys. 15, krok 1.",
        "W samym czacie włącz przełącznik GitHub — rys. 15, krok 2. Bez przełącznika "
        "agent nie widzi „szafki”, nawet jeśli wszystko jest podłączone.",
    ])
    m.shot("shots/arena_connect.png", "https://arena.ai/agent",
             "Rys. 14. Menu Connections w Arena (zrzut z help.arena.ai): wiersz GitHub z ikoną strzałki — kliknięcie otwiera autoryzację na GitHubie.")
    m.shot("shots/arena_toggle.png", "https://arena.ai/agent",
             "Rys. 15. Ta sama lista Connections (zrzut z help.arena.ai): zielony przełącznik po prawej stronie GitHuba włącza dostęp dla bieżącego czatu.")
    m.callout("warn", "Jeśli przycisku GitHub nie ma na liście",
              "Znaczy, że w tej wersji konta podłączenie jest niedostępne. Wtedy gotowe "
              "pliki można zabierać archiwum z panelu Workspace (rozdział 3.4) — schemat "
              "pracy ten sam, po prostu bez „szafki”.")

    m.h2("15.5. Krok 4. Pierwsze zadanie: dokument Word", "sn-4")
    m.p("Teraz napisz w czacie zadanie jak koledze. Im konkretniej, tym lepszy wynik:")
    m.code([
        "Zrób dokument Word „Activity na marzec”.",
        "Co ma być w środku: cel akcji, budżet, kalendarz działań po tygodniach.",
        "Zapisz plik w folderze activity pod nazwą aktywnosc-mart.docx.",
    ], "Przykład zadania — wklej w czat i popraw pod siebie")
    m.p("Agent zrobi plik, pokaże go Tobie i otworzy Pull Request — to „wniosek "
        "o zapisanie” w Twoim repozytorium (rys. 16 i 16). Tobie zostaje obejrzeć "
        "i kliknąć Merge — po tym plik na zawsze leży w „szafce”.")
    m.shot("shots/arena_chatbar.png", "https://arena.ai/agent",
             "Rys. 16. Pasek wprowadzania Agent Mode (zrzut z help.arena.ai): treść zadania prostymi słowami, przycisk Add files — „dołącz pliki” (obwiedziony), strzałka po prawej — start.")
    m.shot("shots/gh_merge.png", "https://github.com/pulls",
             "Rys. 17. Strona Pull Request na GitHubie (zrzut z docs.github.com): zielony przycisk Merge pull request — „scal zmiany z główną gałęzią”; strzałka obok rozwija sposoby scalenia.")
    m.callout("info", "Merge to po prostu przycisk „zapisz”",
              "Nie bój się słowa: Merge odkłada gotowy plik do Twojego folderu. Dopóki "
              "nie klikniesz Merge, plik nigdzie się nie ruszy i nikomu nie przeszkodzi.")

    m.h2("15.6. Krok 5. Tabela Excel — tak samo", "sn-5")
    m.p("Dla Excela wszystko jest tak samo, zmienia się tylko tekst zadania:")
    m.code([
        "Zrób tabelę Excel „Budżet Activity na marzec”.",
        "Kolumny: Pozycja, Kwota, Komentarz.",
        "Wiersze: materiały promo, reklama w social mediach, praca grafika.",
        "Na dole — wiersz „Razem” z sumą. Zapisz w activity/budzet-mart.xlsx.",
    ], "Przykład zadania na tabelę")
    m.p("Agent sam policzy „Razem” i odłoży plik .xlsx do folderu. Otwiera się zwykłym "
        "programem Excel.")

    m.h2("15.7. Krok 6. Ustawiamy przepływ: Activity i TP według Twojego wzoru", "sn-6")
    m.p("Żeby dokumenty za każdym razem wyglądały tak, jak przyjęto u Was, raz odłóż do "
        "repozytorium swoje wzory — szablony. Dalej agent będzie je wypełniał, a nie "
        "wymyślał oprawę od zera:")
    m.ol([
        "Utwórz w repozytorium folder shablony (przyciskiem Add file na GitHubie albo "
        "prosząc agenta).",
        "Odłóż tam swoje wzory: shablony/aktywnosc.docx, shablony/tp.docx, "
        "shablony/budzet.xlsx.",
        "W każdym zadaniu pisz: „zrób według wzoru shablony/...”.",
    ])
    m.code([
        "moje-dokumenty/",
        "  shablony/      <- Twoje wzory (odkładasz raz)",
        "  activity/      <- gotowe „Activity”",
        "  tp/            <- gotowe TP",
    ], "Jak będą rozłożone foldery w repozytorium")
    m.code([
        "Weź wzór shablony/aktywnosc.docx i wypełnij danymi:",
        "akcja — „Wiosenna wyprzedaż”, terminy — 1–31 marca, budżet — 5000 zł.",
        "Gotowy plik zapisz w folderze activity pod nazwą aktywnosc-2026-03.docx.",
        "Otwórz Pull Request.",
    ], "Szablon zadania na „Activity” — podstaw swoje dane")
    m.p("Dla TP — to samo: „Weź wzór shablony/tp.docx, wypełnij na produkt…, zapisz "
        "w tp/…”. Jeśli w Twojej firmie „Activity” i TP nazywają się i wyglądają "
        "inaczej — schemat się nie zmienia: wzór jest Twój, agent wypełnia.")
    m.callout("ok", "Im dokładniejszy wzór, tym dokładniejszy wynik",
              "Jeśli we wzorze są Wasze logo, nagłówek i formy tabel — gotowy dokument "
              "je odziedziczy. Agent nie będzie wymyślał oprawy na nowo.")


    m.h2("15.8. Krok 7. Gdzie i jak zabierać gotowy wynik", "sn-get")
    m.p("Gotowe dokumenty mieszkają w dwóch miejscach: na stałe — w repozytorium, "
        "tymczasowo — w panelu Arena. Zabieraj tak, jak wygodniej:")
    m.table(
        ["Gdzie zabrać", "Jak", "Kiedy wygodnie"],
        [
            ["Z repozytorium na GitHubie",
             "Otwórz folder (activity lub tp), kliknij w wiersz pliku, na otwartej "
             "stronie kliknij przycisk Download ze strzałką — rys. 18",
             "Prawie zawsze: to Twoje stałe przechowalisko"],
            ["Z Arena (panel Workspace)",
             "Po prawej otwórz panel plików: klik w plik otwiera podgląd, przycisk "
             "„pobierz” zabiera plik, a przycisk Download pakuje całą przestrzeń "
             "roboczą do ZIP — rys. 19",
             "Gdy plik jest potrzebny od razu, bez otwierania GitHuba"],
            ["Sposób awaryjny",
             "Dodaj /download-workspace na końcu adresu czatu Arena — pliki przestrzeni "
             "roboczej pobiorą się archiwum",
             "Gdy czat „zepsuł się” i panel nie otwiera"],
        ],
        widths=[1.0, 2.2, 1.5],
    )
    m.shot("shots/gh_files.png", "https://github.com/",
             "Rys. 18. Pobieranie z repozytorium (zrzut z docs.github.com): kliknięcie pliku na liście otwiera jego stronę z przyciskiem pobrania na komputer.")
    m.shot("shots/arena_workspace.png", "https://arena.ai/agent",
             "Rys. 19. Panel Workspace w Arena (zrzut z help.arena.ai): pliki sesji bez GitHuba — kliknięcie otwiera podgląd, ikona w nagłówku pobiera wszystko.")
    m.p("Pobrany plik otwiera się na komputerze jak zwykle: .docx — w Wordzie, .xlsx — "
        "w Excelu. Jeśli agent otworzył Pull Request, a Ty jeszcze nie kliknąłeś Merge — "
        "plik już można zabrać z Workspace albo ze strony PR (zakładka Files changed). "
        "Po Merge leży w repozytorium.")
    m.callout("info", "Gdzie co leży",
              "Repozytorium to szafka: pliki przechowują się na stałe i są widoczne z każdego urządzenia. Workspace to blat roboczy: żyje, dopóki otwarty jest czat. Dlatego zasada jest prosta: cenne dokumenty wysyłaj do repozytorium (czyli klikaj Merge), a brudnopisy mogą zostać w czacie.")  # placeholder replaced below

    m.h2("15.9. Błędy nowicjusza i jak je naprawiać", "sn-7")
    m.table(
        ["Co się stało", "Dlaczego", "Co zrobić"],
        [
            ["Agent mówi, że nie widzi GitHuba",
             "W czacie wyłączony jest przełącznik GitHub",
             "Włącz przełącznik (rys. 15, krok 2) i powtórz zadanie"],
            ["Plik utworzył się „nie tam”",
             "W zadaniu nie podano folderu",
             "Podawaj folder i nazwę pliku w każdym zadaniu albo poproś: „przenieś plik "
             "do activity”"],
            ["Poprosiłeś o kolejny dokument, a agent „zapomniał”",
             "Poprzedni Pull Request jest już zamknięty lub zmergowany",
             "Zacznij nowy czat do nowej pracy — to normalne"],
            ["Czekam na archiwum ZIP, a go nie ma",
             "Przy podłączonym GitHubie pliki idą do repozytorium",
             "Otwórz repozytorium i pobieraj pliki stamtąd (rys. 20)"],
            ["Dokument ładny, ale „nie o tym”",
             "Zadanie było ogólne: „zrób ładnie”",
             "Wypunktuj sekcje dokumentu i daj wzór"],
        ],
        widths=[1.3, 1.5, 1.9],
    )
    m.shot("shots/gh_files.png", "https://github.com/",
             "Rys. 20. Pliki w repozytorium (zrzut z docs.github.com): kliknięcie nazwy pliku (README.md obwiedziony) otwiera jego stronę — stamtąd plik się pobiera.")

    # ---------------------------------------------------------- 16. SŁOWNICZEK

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


    m.h2("15.11. Z czego pisze się programy na Windows: języki z plusami i minusami", "sn-lang")
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
            ["<b>Go</b>",
             "Składa się do jednego .exe bez zbędnych bibliotek; bardzo szybka budowa; prosta "
             "i ścisła składnia",
             "Brak wbudowanej biblioteki okien: interfejs tylko z zewnętrznych bibliotek "
             "(Fyne, Walk); mniej materiałów nauki niż po Pythonie",
             "Szybkie narzędzia, serwisy i programy sieciowe; do okien — nie pierwszy wybór"],
            ["<b>Rust</b>",
             "Szybkość jak w C++; kompilator nie przepuszcza błędów pamięci — programy "
             "niezawodne",
             "Jeden z najtrudniejszych języków w nauce; pierwsza budowa i konfiguracja "
             "zajmują czas",
             "Dla tych, którzy już trochę programują i chcą maksymalnej niezawodności"],
            ["<b>Java</b>",
             "Jeden program działa i na Windowsie, i na innych systemach; dużo materiałów "
             "naukowych",
             "Wymaga zainstalowanej Javy na komputerze; standardowe okna (Swing) wyglądają "
             "staroświecko",
             "Studentom i celującym w duże firmowe systemy"],
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


    m.h1("16. Słowniczek: proste słowa zamiast terminów", "gl")
    m.lead("Krótki słowniczek: co oznaczają słowa, które spotykasz w Arena i na GitHubie.")
    m.table(
        ["Słowo", "Prostymi słowami"],
        [
            ["Repozytorium", "Folder na pliki w internecie — Twoja „szafka” na GitHubie"],
            ["GitHub", "Serwis, w którym mieszkają takie foldery; darmowy do użytku osobistego"],
            ["Commit", "„Zfotografował” zmianę pliku — została zapisana w historii"],
            ["Push", "Wysłał zapisaną zmianę do folderu w internecie"],
            ["Pull Request (PR)", "Wniosek „odłóż moje zmiany do foldera”. Czeka na Twój przycisk Merge"],
            ["Merge", "Przycisk „zapisz ostatecznie”. Po nim plik leży w folderze"],
            ["Diff", "Podświetlenie tego, co dokładnie się zmieniło: jakie pliki i wiersze doszły"],
            ["Checks", "Automatyczne kontrole zmiany: zielone — wszystko w porządku"],
            ["Gałąź (branch)", "Brudnopis folderu: można zmieniać, nie ruszając głównej wersji"],
            ["Piaskownica", "Osobny „brudny komputer” agenta w internecie, gdzie pracuje bezpiecznie"],
            ["Konektor", "Klucz-dostęp do usługi (np. GitHuba), który wydajesz agentowi"],
            ["OAuth", "Okno „zezwolić na dostęp?” po stronie usługi. Hasło nie jest pokazywane agentowi"],
            ["Prompt", "Twoja wiadomość-zadanie w czacie"],
            ["Workspace", "Panel plików bieżącego czatu w Arena"],
            ["DOCX / XLSX", "Pliki Worda / Excela"],
            ["ZIP", "Archiwum: kilka plików jednym „pudełkiem” do pobrania"],
            ["Szablon", "Twój wzór dokumentu, według którego agent robi nowe"],
        ],
        widths=[1.0, 3.4],
    )
