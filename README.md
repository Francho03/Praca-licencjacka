## Proces Generowania Danych (Data Generating Process) dla Sprawozdanie_przemoc_2014_2023

### 1. Źródła Danych
Zbiór danych został opracowany poprzez integrację wielu raportów obejmujących lata 2014-2023. Główne źródła to oficjalne raporty statystyczne dotyczące przypadków przemocy domowej w Polsce. Raporty te zostały zebrane z instytucji rządowych(MEiN, MKiDN, MOPR, MSW, MZ, OPS, PCPR, WPS) odpowiedzialnych za monitorowanie przypadków przemocy domowej i wdrażanie procedury "Niebieska Karta".

### 2. Ładowanie Danych
Dane zostały zapisane w wielu plikach typu Excel, z których każdy odpowiadał innym latom i sekcjom raportów. Biblioteka `pandas` została użyta do załadowania i przetworzenia danych. Wybrane zostały konkretne arkusze zawierające istotne informacje, z których następnie zostały wyseleckjonowane konkretne kolumn wykorzystane w dalszej analizie.

```python
import pandas as pd

# Ładowanie przykładowego raportu z 2018 roku
Procedura_A_2018 = pd.read_excel("Sprawozdanie_przemoc_2018.xls", 
                                 sheet_name="Część 15", 
                                 skiprows=14, 
                                 na_values=['-', 'X'], 
                                 header=None, 
                                 names=column_names_procedura_A)
```

### 3. Czyszczenie Danych
Znaki zastępcze ('-', 'X') zostały zastąpione wartościami `NaN`. Kolumna `keso` została przekonwertowana na format `string` dla spójności. Jednostki administracyjne klasyfikowane jako "ROPS" (Regionalne Ośrodki Polityki Społecznej) zostały usunięte ze względu na to, że zawierały tylko i wyłacznie braki danych i nie były spójne z pozostałymi arkuszami.

```python
Procedura_A_2018['keso'] = Procedura_A_2018['keso'].astype(str)
Liczba_osob_2018 = Liczba_osob_2018[Liczba_osob_2018["typ_jednostki"] != "ROPS"]
```

### 4. Wybór Kolumn
Zbiór danych został uporządkowany, aby skupić się na kluczowych statystykach proceduralnych i demograficznych. 

```python
Procedura_A_2018 = Procedura_A_2018.iloc[:, [1,2,3,4,5,6,7]]
Liczba_osob_2018 = Liczba_osob_2018.iloc[:, [1,2,3,4,5,6,]+list(range(7,11))]

# Zmiana nazw kluczowych kolumn demograficznych
Liczba_osob_2018["Liczba_osob_ogol"] = Liczba_osob_2018["ogol_gmina"]
Liczba_osob_2018["Liczba_osob_kobiety"] = Liczba_osob_2018["kobiety_gmina"]
Liczba_osob_2018["Liczba_osob_mezczyzni"] = Liczba_osob_2018["mezczyzni_gmina"]
Liczba_osob_2018["Liczba_osob_dzieci"] = Liczba_osob_2018["dzieci_gmina"]

Liczba_osob_2018 = Liczba_osob_2018.drop(columns=["ogol_pow","kobiety_pow","mezczyzni_pow","dzieci_pow", 
                                                   "ogol_gmina","kobiety_gmina","mezczyzni_gmina","dzieci_gmina"])
```

### 5. Łączenie Danych
Dane z różnych źródeł w ramach każdego roku zostały połączone.

```python
Sprawozdanie_przemoc_2018 = Podzial_administracyjny_2018
Sprawozdanie_przemoc_2018 = pd.merge(Sprawozdanie_przemoc_2018, Procedura_A_2018, on=merge_columns, how='outer')
Sprawozdanie_przemoc_2018 = pd.merge(Sprawozdanie_przemoc_2018, Liczba_osob_2018, on=merge_columns, how='outer')
Sprawozdanie_przemoc_2018.sort_values(by="LP", inplace=True)
Sprawozdanie_przemoc_2018.reset_index(drop=True, inplace=True)
Sprawozdanie_przemoc_2018["rok"] = 2018
```

Po przetworzeniu danych dla każdego roku, wszystkie zbiory danych zostały połączone w jeden kompleksowy zbiór.

```python
def polacz(*datasets):
    return pd.concat(datasets, ignore_index=True)

Sprawozdanie_przemoc_2014_2020 = polacz(
    Sprawozdanie_przemoc_2020,
    Sprawozdanie_przemoc_2019,
    Sprawozdanie_przemoc_2018,
    Sprawozdanie_przemoc_2017,
    Sprawozdanie_przemoc_2016,
    Sprawozdanie_przemoc_2015,
    Sprawozdanie_przemoc_2014
)


Sprawozdanie_przemoc_2014_2023 = polacz(
   Sprawozdanie_przemoc_2023,
   Sprawozdanie_przemoc_2022,
   Sprawozdanie_przemoc_2021,
   Sprawozdanie_przemoc_2014_2020,
)
```


### 6. Ostateczna Struktura Danych i Kolumny Wyjściowe
Ostateczny zbiór danych zawiera uporządkowane rekordy obejmujące lata (2014–2023), umożliwiające analizę trendów przemocy domowej w Polsce.

#### Kolumny Administracyjne:
- **lp** – Numer porządkowy.
- **woj** – Województwo.
- **pow** – Powiat.
- **gm** – Gmina.
- **typ_gm** – Typ gminy.
- **typ_jednostki** – Klasyfikacja jednostki raportującej.
- **keso** – KOD Elementu Struktury Organizacyjnej.

#### Statystyki Proceduralne:
- **liczba_proc_NK_A** – Liczba formularzy „Niebieska Karta - A”.
- **rodziny_objete** – Liczba rodzin objętych procedurą 'Niebieskie Karty' 
- **rodziny_wszczete** – Liczba rodzin, wobec których wszczęto procedurę 'Niebieskie Karty' w danym roku sprawozdawczym.

#### Statystyki Demograficzne:
- **liczba_osob_ogol** – Łączna liczba osób dotkniętych przemocą.
- **liczba_osob_kobiety** – Liczba kobiet dotkniętych przemocą.
- **liczba_osob_mezczyzni** – Liczba mężczyzn dotkniętych przemocą.
- **liczba_osob_dzieci** – Liczba dzieci dotkniętych przemocą.

#### Wymiar Czasowy:
- **rok** – Rok, w którym dane zostały zebrane.

### 7. Format Wyjściowy
Ostateczny zbiór danych został zapisany w formacie Excel do dalszej analizy.

```python
Sprawozdanie_przemoc_2014_2020.to_excel("Sprawozdanie_przemoc_2014_2023.xlsx", index=False)
