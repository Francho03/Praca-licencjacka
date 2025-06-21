# Analiza przemocy domowej w Polsce (2014–2023)

## Opis projektu

Repozytorium zawiera kod źródłowy wykorzystany w pracy licencjackiej, której celem było:

- Stworzenie ustrukturyzowanego i przygotowanego do analizy zbioru danych dotyczących przemocy domowej w Polsce na poziomie **gmin** i **powiatów**.
- Przeprowadzenie **analizy zależności** między przemocą domową a wybranymi czynnikami społeczno-ekonomicznymi, wybranymi na podstawie przeglądu literatury naukowej.
- Opracowanie **interaktywnej aplikacji internetowej** do wizualizacji wyników i dalszej eksploracji danych.

## Dane źródłowe

Dane pochodzą ze **Sprawozdań z realizacji Krajowego Programu Przeciwdziałania Przemocy w Rodzinie** opracowywanych przez **Ministerstwo Rodziny, Pracy i Polityki Społecznej** w latach 2014–2023.

Przygotowany zbiór danych został opublikowany w Repozytorium Otwartych Danych (RepOD):

🔗 [Dostęp do danych w RepOD](https://repod.icm.edu.pl/dataset.xhtml?persistentId=doi:10.18150/RX5M06)

## Zawartość repozytorium

W repozytorium znajdują się:

- Skrypty w języku **Python** (głównie z użyciem biblioteki `pandas`) służące do:
  - czyszczenia i łączenia danych,
  - agregacji i przekształceń na poziomie gmin i powiatów,
  - przeprowadzania analiz statystycznych (korelacje Spearmana, regresja liniowa),
  - przygotowania danych do wizualizacji.
- Kod aplikacji internetowej zbudowanej przy użyciu **Shiny for Python**.
- Wykresy i mapy (kartogramy) przedstawiające przestrzenne i czasowe zróżnicowanie przemocy domowej w Polsce.

## Aplikacja internetowa

Do eksploracji wyników analizy stworzona została interaktywna aplikacja webowa dostępna publicznie:

🌐 [Zobacz aplikację Shiny for Python](https://qcklyh-franciszek-d0bicki.shinyapps.io/my-python-project/)

Aplikacja umożliwia:

- przeglądanie kartogramów przedstawiających skalę przemocy domowej na poziomie powiatów,
- analizę trendów przemocy w czasie,
- eksplorację danych w podziale demograficznym (kobiety, mężczyźni, dzieci).

## Wnioski z analizy

- **Korelacje Spearmana** nie wykazały silnych zależności pomiędzy przemocą domową a analizowanymi czynnikami społeczno-ekonomicznymi.
- **Modele regresji liniowej**, szczególnie te z uwzględnieniem efektów stałych dla powiatów, wykazały istotne statystycznie zależności dla niektórych zmiennych.
- Uzyskane wyniki wskazują na potrzebę dalszych badań z większą szczegółowością przestrzenną i uwzględnieniem dodatkowych zmiennych kontekstowych.

## Wymagania

- Python 3.9+
- Pakiety: `pandas`, `statsmodels`, `plotly`, `shiny` i inne (szczegóły w `requirements.txt`)

## Licencja

Projekt udostępniany jest na licencji MIT. Dane opublikowane w RepOD podlegają własnej licencji wskazanej na stronie zbioru danych.
