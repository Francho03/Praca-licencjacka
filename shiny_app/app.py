from shiny import App, render, ui, reactive
import geopandas as gpd
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from scipy.stats import pearsonr, spearmanr, shapiro, normaltest
import io
from datetime import date
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import probplot
import statsmodels.api as sm

# Wczytanie pliku GeoJSON
poland_gdf = gpd.read_file("poland.counties.json")
poland_gdf.columns = poland_gdf.columns.str.strip()
poland_gdf = poland_gdf.rename(columns={'name': 'pow'})
poland_gdf['terc'] = poland_gdf['terc'].astype(str)
poland_gdf = poland_gdf[~poland_gdf.geometry.isna()].reset_index(drop=True)

# Wczytanie pliku GeoJSON z województwami
voivodeships_gdf = gpd.read_file("poland.voivodeships.json")
voivodeships_gdf.columns = voivodeships_gdf.columns.str.strip()
voivodeships_gdf = voivodeships_gdf.rename(columns={'name': 'woj'})
voivodeships_gdf['terc'] = voivodeships_gdf['terc'].astype(str)
voivodeships_gdf = voivodeships_gdf[~voivodeships_gdf.geometry.isna()].reset_index(drop=True)

# Wczytanie głównego zbioru danych dla korelacji
merged_df = pd.read_excel("Sprawozdanie_przemoc_2014_2023_korelacja.xlsx", dtype={"kod": str})
merged_df['teryt_4'] = merged_df['kod'].str[:4]

# Wczytanie danych w odsetkach
pct_df = pd.read_excel("Sprawozdanie_przemoc_2014_2023_odsetek_ludnosci.xlsx", dtype={"kod": str})
pct_df['teryt_4'] = pct_df['kod'].str[:4]

# Zmienne do wyboru
sprawozdanie_vars = [
    'liczba_proc_nk_a', 'liczba_proc_nk_c', 'rodziny_wszczete',
    'liczba_osob_ogol', 'liczba_osob_kobiety', 'liczba_osob_mezczyzni',
    'liczba_osob_dzieci'
]
indicators = [
    'odsetek_bezrobotnych_dlugotrwalych', 'wielkosc_wynagrodzenia',
    'odsetek_rozwodow', 'liczba_osob_na_1_izbe',
    'przecietna_powierzchnia_mieszkania_na_1_osobe'
]
sprawozdanie_vars_odsetki = ['odsetek_ogol', 'odsetek_kobiety', 'odsetek_mezczyzni', 'odsetek_dzieci']
sprawozdanie_vars1 =sprawozdanie_vars +sprawozdanie_vars_odsetki
# Zmienne do wyboru - tylko dane odsetkowe
sprawozdanie_vars_odsetki = ['odsetek_ogol', 'odsetek_kobiety', 'odsetek_mezczyzni', 'odsetek_dzieci']
indicators_odsetki = [
    'odsetek_bezrobotnych_dlugotrwalych', 'odsetek_rozwodow'
]

# Wszystkie zmienne odsetkowe
all_vars_odsetki = sprawozdanie_vars_odsetki + indicators
all_vars = sprawozdanie_vars + indicators
df = pd.merge(merged_df, pct_df, on=["rok", "kod", "teryt_4"], suffixes=('', '_pct'))

# Funkcja analyze_correlation_with_diagnostics
def analyze_correlation_with_diagnostics(x, y, alpha=0.05):
    results = {
        'n': len(x),
        'missing_values': x.isnull().sum() + y.isnull().sum(),
        'outliers_x': 0,
        'outliers_y': 0,
        'normality_x': None,
        'normality_y': None,
        'recommended_test': None,
        'pearson_r': None,
        'pearson_p': None,
        'spearman_rho': None,
        'spearman_p': None,
        'interpretation': []
    }
    
    valid_data = pd.DataFrame({'x': x, 'y': y}).dropna()
    if len(valid_data) < 3:
        results['interpretation'].append("Zbyt mało obserwacji do analizy")
        return results
    
    x_clean, y_clean = valid_data['x'], valid_data['y']
    
    def count_outliers(data):
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        return ((data < lower) | (data > upper)).sum()

    results['outliers_x'] = count_outliers(x_clean)
    results['outliers_y'] = count_outliers(y_clean)

    if len(x_clean) >= 8:
        try:
            if len(x_clean) <= 5000:
                stat_x, p_x = shapiro(x_clean)
                stat_y, p_y = shapiro(y_clean)
            else:
                stat_x, p_x = normaltest(x_clean)
                stat_y, p_y = normaltest(y_clean)
            results['normality_x'] = p_x
            results['normality_y'] = p_y
        except:
            results['normality_x'] = None
            results['normality_y'] = None

    x_std = x_clean.std()
    y_std = y_clean.std()

    if x_std == 0 or y_std == 0:
        results['interpretation'].append("Brak zmienności w jednej ze zmiennych")
        return results

    try:
        pearson_r, pearson_p = pearsonr(x_clean, y_clean)
        results['pearson_r'] = pearson_r
        results['pearson_p'] = pearson_p
    except:
        pass

    try:
        spearman_rho, spearman_p = spearmanr(x_clean, y_clean)
        results['spearman_rho'] = spearman_rho
        results['spearman_p'] = spearman_p
    except:
        pass

    normal_x = results['normality_x'] is not None and results['normality_x'] > alpha
    normal_y = results['normality_y'] is not None and results['normality_y'] > alpha
    few_outliers = results['outliers_x'] <= len(x_clean) * 0.05 and results['outliers_y'] <= len(y_clean) * 0.05

    if normal_x and normal_y and few_outliers and len(x_clean) >= 30:
        results['recommended_test'] = 'pearson'
        results['recommended_r'] = results['pearson_r']
        results['recommended_p'] = results['pearson_p']
        results['interpretation'].append("Rekomendacja: test Pearsona (dane normalne, mało wartości odstających)")
    else:
        results['recommended_test'] = 'spearman'
        results['recommended_r'] = results['spearman_rho']
        results['recommended_p'] = results['spearman_p']
        reasons = []
        if not (normal_x and normal_y):
            reasons.append("rozkład nienormalny")
        if not few_outliers:
            reasons.append("dużo wartości odstających")
        if len(x_clean) < 30:
            reasons.append("mała próbka")
        results['interpretation'].append(f"Rekomendacja: test Spearmana ({', '.join(reasons)})")

    r_value = abs(results['recommended_r']) if results['recommended_r'] is not None else 0
    if r_value < 0.1:
        strength = "bardzo słaby"
    elif r_value < 0.3:
        strength = "słaby"
    elif r_value < 0.5:
        strength = "umiarkowany"
    elif r_value < 0.7:
        strength = "silny"
    else:
        strength = "bardzo silny"

    results['interpretation'].append(f"Siła związku: {strength} (|r|={r_value:.3f})")

    if results['recommended_p'] is not None:
        if results['recommended_p'] < alpha:
            results['interpretation'].append(f"Związek istotny statystycznie (p={results['recommended_p']:.4f})")
        else:
            results['interpretation'].append(f"Związek nieistotny statystycznie (p={results['recommended_p']:.4f})")

    return results


# Function to calculate resztki by county
def calculate_resztki_by_county(model_type='model1'):
    """
    Calculate resztki from regression model by county
    model_type: 'model1' (without fixed effects) or 'model2' (with fixed effects)
    """
    # Prepare the data (same as in your regression code)
    merged_df = pd.read_excel("Sprawozdanie_przemoc_2014_2023_korelacja.xlsx", dtype={"kod": str})
    merged_df['teryt_4'] = merged_df['kod'].str[:4]
    
    pct_df = pd.read_excel("Sprawozdanie_przemoc_2014_2023_odsetek_ludnosci.xlsx", dtype={"kod": str})
    pct_df['teryt_4'] = pct_df['kod'].str[:4]
    
    dane_rel = pd.merge(merged_df, pct_df, on=["rok", "kod", "teryt_4"], suffixes=('', '_pct'))
    
    # List of columns that should be numeric
    numeric_columns = [
        'odsetek_ogol', 
        'odsetek_bezrobotnych_dlugotrwalych', 
        'wielkosc_wynagrodzenia', 
        'odsetek_rozwodow', 
        'liczba_osob_na_1_izbe', 
        'przecietna_powierzchnia_mieszkania_na_1_osobe', 
        'rok'
    ]
    
    # Convert each column to numeric, coercing errors to NaN
    for col in numeric_columns:
        dane_rel[col] = pd.to_numeric(dane_rel[col], errors='coerce')
    
    # Drop rows with NaN in numeric columns or 'kod'
    dane_rel = dane_rel.dropna(subset=numeric_columns + ['kod'])
    
    # Create y
    y = dane_rel['odsetek_ogol']
    
    # Prepare X variables
    X = dane_rel[['odsetek_bezrobotnych_dlugotrwalych', 'wielkosc_wynagrodzenia', 
                  'odsetek_rozwodow', 'liczba_osob_na_1_izbe', 
                  'przecietna_powierzchnia_mieszkania_na_1_osobe', 'rok']].copy()
    X['wielkosc_wynagrodzenia'] = X['wielkosc_wynagrodzenia'] / 1000
    
    if model_type == 'model1':
        # Model 1 (without fixed effects)
        X = sm.add_constant(X)
        X = X.astype(float)
        y = y.astype(float)
        model = sm.OLS(y, X).fit()
    else:
        # Model 2 (with fixed effects)
        kod_dummies = pd.get_dummies(dane_rel['kod'], prefix='kod', drop_first=True)
        X = pd.concat([X, kod_dummies], axis=1)
        X = sm.add_constant(X)
        X = X.astype(float)
        y = y.astype(float)
        model = sm.OLS(y, X).fit()
    
    # Calculate resztki
    resztki = model.resid
    
    # Create dataframe with resztki and county codes
    resztki_df = pd.DataFrame({
        'teryt_4': dane_rel['teryt_4'].values,
        'kod': dane_rel['kod'].values,
        'residual': resztki,
        'fitted_value': model.fittedvalues,
        'actual_value': y.values
    })
    
    # Aggregate resztki by county (teryt_4) - using mean residual
    county_resztki = resztki_df.groupby('teryt_4').agg({
        'residual': ['mean', 'std', 'count'],
        'fitted_value': 'mean',
        'actual_value': 'mean'
    }).round(4)
    
    # Flatten column names
    county_resztki.columns = ['_'.join(col).strip() for col in county_resztki.columns]
    county_resztki = county_resztki.reset_index()
    
    # Rename columns for clarity
    county_resztki = county_resztki.rename(columns={
        'residual_mean': 'mean_residual',
        'residual_std': 'std_residual',
        'residual_count': 'n_observations',
        'fitted_value_mean': 'mean_fitted',
        'actual_value_mean': 'mean_actual'
    })
    
    return county_resztki, model    

# Interfejs użytkownika z zakładkami
app_ui = ui.page_fluid(
    ui.tags.style("""
        body { 
            font-family: 'Arial', sans-serif; 
            background-color: #f4f7fa; 
            color: #2c3e50; 
        }
        h1, h2, h3 { 
            color: #2c3e50; 
        }
        .section { 
            padding: 20px; 
            background-color: #ffffff; 
            border-radius: 10px; 
            margin-bottom: 20px; 
            box-shadow: 0 4px 8px rgba(0,0,0,0.1); 
        }
        table { 
            border-collapse: collapse; 
            width: 100%; 
        }
        th, td { 
            border: 1px solid #e0e0e0; 
            padding: 10px; 
            text-align: left; 
        }
        th { 
            background-color: #f2f2f2; 
            font-weight: bold; 
        }
        .footer { 
            background-color: #ecf0f1; 
            padding: 20px; 
            text-align: center; 
            font-size: 14px; 
            color: #7f8c8d; 
            border-top: 1px solid #e0e0e0; 
            margin-top: 20px; 
        }
        /* Stylizacja paska zakładek */
        .nav-tabs { 
            margin-bottom: 30px; 
            border-bottom: 2px solid #e0e0e0; 
        }
        .nav-tabs .nav-item { 
            margin-right: 10px; 
        }
        .nav-tabs .nav-link { 
            background-color: #ffffff; 
            border: 1px solid #e0e0e0; 
            border-radius: 8px 8px 0 0; 
            padding: 12px 20px; 
            color: #2c3e50; 
            font-weight: 500; 
            transition: all 0.3s ease; 
            font-size: 16px; 
        }
        .nav-tabs .nav-link:hover { 
            background-color: #f0f4f8; 
            border-color: #d0d4d8; 
            color: #1a5276; 
        }
        .nav-tabs .nav-link.active { 
            background-color: #3498db; 
            border-color: #3498db; 
            color: #ffffff; 
            font-weight: bold; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.1); 
        }
        .nav-tabs .nav-link.active:hover { 
            background-color: #2980b9; 
            border-color: #2980b9; 
        }
        /* Styling for correlation interpretation */
        .correlation-interpretation {
            padding: 15px;
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-top: 15px;
            border-left: 4px solid #3498db;
        }
        .correlation-interpretation h4 {
            margin: 0 0 10px 0;
            color: #2c3e50;
            font-size: 18px;
            font-weight: bold;
        }
        .correlation-interpretation ul {
            list-style-type: none;
            padding: 0;
            margin: 0;
        }
        .correlation-interpretation li {
            padding: 8px 0;
            font-size: 14px;
            color: #2c3e50;
            position: relative;
            padding-left: 25px;
        }
        .correlation-interpretation li::before {
            content: '•';
            position: absolute;
            left: 0;
            color: #3498db;
            font-size: 20px;
            line-height: 20px;
        }
        .correlation-interpretation .highlight {
            font-weight: bold;
            color: #1a5276;
        }
        .correlation-interpretation .significant {
            color: #27ae60; /* Green for significant results */
        }
        .correlation-interpretation .insignificant {
            color: #e74c3c; /* Red for non-significant results */
        }
    """),
    ui.h1("Analiza przemocy domowej w Polsce na przestrzeni lat 2014-2023"),
    
    # Zakładki w pasku menu
    ui.navset_tab(
        ui.nav_panel(
            "Informacje",
            ui.div({"class": "section"},
                ui.h2(" Cel aplikacji"),
                ui.p("Aplikacja została stworzona jako interaktywna wizualizacja wyników pracy licencjackiej:"),
                ui.HTML("""
                    <p><strong>Franciszek Dębicki</strong><br>
                    <em>Analiza przemocy domowej w Polsce na poziomie powiatów w latach 2014–2023</em><br>
                    Promotor: dr Maciej Beręsewicz, prof. UEP<br>
                    Kierunek: Informatyka i ekonometria<br>
                    Specjalizacja: Analityka gospodarcza<br>
                    Uniwersytet Ekonomiczny w Poznaniu, 2025</p>
                """),
                ui.p("Główne cele aplikacji:"),
                ui.tags.ul(
                    ui.tags.li("Wizualizacja danych dotyczących przemocy domowej w Polsce na poziomie powiatów."),
                    ui.tags.li("Analiza zależności między przemocą a wybranymi czynnikami społeczno-ekonomicznymi."),
                    ui.tags.li("Ułatwienie interpretacji wyników za pomocą interaktywnych map, wykresów i modeli regresyjnych.")
                ),
                ui.h3("Pobierz pracę licencjacką"),
                ui.download_button("download_pdf", "Pobierz PDF pracy licencjackiej")


            )
        ),
        
        # Zakładka: Opis zmiennych
        ui.nav_panel(
            "Opis zmiennych",
            ui.div({"class": "section"},
                ui.h2("Opis zmiennych użytych w analizie"),
                ui.HTML("""
                    <table>
                        <tr><th>Nazwa zmiennej</th><th>Opis</th></tr>
                        <tr><td>woj</td><td>Województwo (jednostka administracyjna najwyższego szczebla)</td></tr>
                        <tr><td>pow</td><td>Powiat (jednostka administracyjna średniego szczebla)</td></tr>
                        <tr><td>keso</td><td>Kod KESO – identyfikator jednostki statystycznej</td></tr>
                        <tr><td>rok</td><td>Rok, którego dotyczą dane</td></tr>
                        <tr><td>liczba_proc_nk_a</td><td>Liczba formularzy 'Niebieska Karta - A' sporządzonych przez pracowników socjalnych</td></tr>
                        <tr><td>liczba_proc_nk_c</td><td>Liczba formularzy 'Niebieska Karta - C' sporządzonych przez członków zespołów interdyscyplinarnych lub powołanych grup roboczych</td></tr>
                        <tr><td>rodziny_wszczete</td><td>Liczba rodzin, wobec których wszczęto procedurę 'Niebieska Karta'</td></tr>
                        <tr><td>liczba_osob_ogol</td><td>Liczba osób ogółem dotkniętych przemocą w rodzinie</td></tr>
                        <tr><td>liczba_osob_kobiety</td><td>Liczba kobiet dotkniętych przemocą w rodzinie</td></tr>
                        <tr><td>liczba_osob_mezczyzni</td><td>Liczba mężczyzn dotkniętych przemocą w rodzinie</td></tr>
                        <tr><td>liczba_osob_dzieci</td><td>Liczba dzieci dotkniętych przemocą w rodzinie</td></tr>
                        <tr><td>odsetek_ogol</td><td>Liczba osób ogółem dotkniętych przemocą w rodzinie względem populacji w Polsce</td></tr>
                        <tr><td>odsetek_kobiety</td><td>Liczba kobiet dotkniętych przemocą w rodzinie względem populacji kobiet w Polsce</td></tr>
                        <tr><td>odsetek_mezczyzni</td><td>Liczba mężczyzn dotkniętych przemocą w rodzinie wzgledem populacji mężczyzn w Polsce</td></tr>
                        <tr><td>odsetek_dzieci</td><td>Liczba dzieci dotkniętych przemocą w rodzinie wzgledem populacji dzieci w Polsce</td></tr>
                        <tr><td>odsetek_bezrobotnych_dlugotrwalych</td><td>Udział osób bezrobotnych długotrwale w osobach bezrobotnych</td></tr>
                        <tr><td>wielkosc_wynagrodzenia</td><td>Przeciętne miesięczne wynagrodzenia brutto</td></tr>
                        <tr><td>odsetek_rozwodow</td><td>Udział małżeństw zakończonych rozwodem w małżeństwach ogołem</td></tr>
                        <tr><td>liczba_osob_na_1_izbe</td><td>Przeciętna liczba osób na 1 izbę</td></tr>
                        <tr><td>przecietna_powierzchnia_mieszkania_na_1_osobe</td><td>Przeciętna powierzchnia użytkowa mieszkania na 1 osobę</td></tr>
                    </table>
                """)
            )
        ),
        
        ui.nav_panel(
            "Mapy",
             ui.div({"class": "section"},
                    ui.h3("Mapa przemocy domowej w powiatach (dane bezwględne)"),
                    ui.p("Mapa wizualizuje rozkład liczbowy wskaźników przemocy domowej w polskich powiatach w okresie 2014–2023."),
                    ui.input_select("violence_var", "Zmienna przemocowa:", choices=sprawozdanie_vars),
                    ui.input_select("year", "Rok:", choices=sorted(merged_df['rok'].unique().astype(str))),
                    ui.output_ui("violence_map"),
                    ui.output_ui("violence_stats"),
                    # ui.download_button("download_violence_map", "Pobierz mapę przemocową")
                ),

             ui.div({"class": "section"},
                    ui.h3("Mapa przemocy domowej w powiatach (dane względne)"),
                    ui.p("Mapa przedstawia rozkład wskaźników przemocy domowej w polskich powiatach w okresie 2014–2023, wyrażone jako procent populacji."),
                    ui.input_select("pct_year", "Rok:", choices=sorted(pct_df['rok'].unique().astype(str))),
                    ui.input_select("pct_var", "Zmienna przemocowa (odsetek):", choices=sprawozdanie_vars_odsetki),
                    ui.output_ui("pct_map"),
                    ui.output_ui("pct_stats"),
                    # ui.download_button("download_pct_map", "Pobierz mapę odsetkową")
                )
                # ui.nav_panel("Korelacje",
                #     ui.h3("Mapa korelacji: Przemoc domowa z czynnikami społeczno-ekonomicznymi"),
                #     ui.p("Mapa prezentuje przestrzenną analizę korelacji między wskaźnikami przemocy domowej a czynnikami społeczno-ekonomicznymi w powiatach w okresie 2014–2023."),
                #     ui.input_select("var1", "Zmienna przemoc:", choices=sprawozdanie_vars, selected=sprawozdanie_vars[0]),
                #     ui.input_select("var2", "Zmienna korelująca:", choices=indicators, selected=indicators[0]),
                #     ui.input_numeric("alpha_level", "Poziom istotności α:", value=0.05, min=0.01, max=0.1, step=0.01),
                #     ui.output_ui("correlation_map"),
                #     ui.output_ui("map_stats")
                # )
            
        ),

        # Zakładka: Wykresy
        ui.nav_panel(
            "Trendy",
                ui.h2("Wykresy"),
                ui.div({"class": "section"},
                ui.h3("Wykres spaghetti dla danych bezwzględnych"),
                ui.p("Wykres spaghetti przedstawia trendy wskaźników przemocy domowej w powiatach w okresie 2014–2023, z możliwością wyróżnienia wybranego powiatu na tle średniej krajowej."),
                ui.input_select("spaghetti_var", "Zmienna dla spaghetti plot:", choices=sprawozdanie_vars, selected=sprawozdanie_vars[0]),
                ui.output_ui("spaghetti_plot"),
                ui.input_select("highlight_powiat", "Wyróżnij powiat:", choices=sorted(merged_df['pow'].unique())),
            ),
              ui.div({"class": "section"},  
                ui.h3("Wykres spaghetti dla danych względnych"),
                ui.p("Wykres spaghetti prezentuje trendy wskaźników przemocy domowej w powiatach w okresie 2014–2023, z możliwością wyróżnienia wybranego powiatu na tle średniej krajowej."),
                ui.input_select("spaghetti_var_pct", "Zmienna dla spaghetti plot:", choices=sprawozdanie_vars_odsetki, selected=sprawozdanie_vars_odsetki[0]),
                ui.output_ui("spaghetti_plot_pct"),
                ui.input_select("highlight_powiat_pct", "Wyróżnij powiat:", choices=sorted(pct_df['pow'].unique()))
            )
        ),
        # UI Panel
        ui.nav_panel(
            "Korelacja",
            ui.div({"class": "section"},
                ui.h2("Interaktywna analiza korelacji"),
                ui.input_select("corr_year", "Wybierz rok dla analizy dwóch zmiennych:", 
                               choices=sorted(merged_df['rok'].astype(str).unique())),
                ui.input_select("corr_var1", "Pierwsza zmienna:", 
                               choices=sprawozdanie_vars_odsetki),
                ui.input_select("corr_var2", "Druga zmienna:", 
                               choices=indicators),
                ui.input_numeric("corr_alpha", "Poziom istotności α:", 
                                value=0.05, min=0.01, max=0.1, step=0.01),
                ui.output_ui("correlation_scatter_plot"),
                ui.output_ui("correlation_interpretation"),
                # ui.h3("Macierz korelacji - dane odsetkowe"),
                # ui.input_select("matrix_year", "Wybierz rok dla macierzy korelacji:", 
                            #    choices=sorted(merged_df['rok'].astype(str).unique())),
                # ui.output_ui("correlation_matrix_plot")
            )
        ),

        ui.nav_panel(
            "Regresja",
            ui.div({"class": "section"},
                ui.h2("Analiza reszt modelu regresji"),
                ui.p("Mapa reszt pokazuje różnice między rzeczywistymi a przewidywanymi wartościami odsetka przemocy domowej. Czerwone obszary oznaczają, że model niedoszacowuje przemoc (reszty dodatnie), niebieskie - że przeszacowuje (reszty ujemne)."),

                ui.input_radio_buttons(
                    "model_type", 
                    "Wybierz model regresji:", 
                    choices={
                        "model1": "Model 1 (bez efektów stałych powiatowych)",
                        "model2": "Model 2 (z efektami stałymi powiatowymi)"
                    },
                    selected="model1"
                ),

                ui.output_ui("resztki_map"),
                ui.output_ui("resztki_stats"),

                ui.h3("Wykres diagnostyczny: Reszty vs Wartości dopasowane"),
                ui.p("Wykres diagnostyczny pomoaga ocenić założenia modelu. Punkty powinny być losowo rozproszone wokół linii y=0."),
                ui.output_ui("resztki_vs_fitted_plot"),

                # ui.download_button("download_resztki_map", "Pobierz mapę resztek")
            )
        ),        

        # Zakładka: Zbiór danych
        ui.nav_panel(
            "Zbiór danych",
            ui.div({"class": "section"},
                ui.h2("Zbiór danych"),
                ui.navset_card_underline(
                    ui.nav_panel("Data frame", ui.output_data_frame("frame")),
                    # ui.nav_panel("Diagnostyka korelacji", ui.output_ui("diagnostic_info")),
                    # ui.nav_panel("Szczegółowa diagnostyka", ui.output_data_frame("detailed_diagnostics")),
                    # ui.nav_panel("Debug Info", ui.output_text("debug_info"))
                )
            )
        )
    ),

        # Stopka
        ui.div({"class": "footer"},
            ui.HTML("""
                <p><strong>Autor:</strong> Franciszek Dębicki</p>
                <p>Student III roku Informatyki i Ekonometrii na Uniwersytecie Ekonomicznym w Poznaniu</p>
                <p><strong>Promotor:</strong> Dr Maciej Beręsewicz, prof. UEP</p>
                <p>Katedra Statystyki</p>
                <p><strong>Cel strony:</strong> Wizualizacja badań przemocy w ramach pracy licencjackiej</p>
                <p><a href="https://github.com/Francho03/Praca-licencjacka" target="_blank">GitHub</a></p>
            """)
        )
    )

# Logika serwera
def server(input, output, session):
    # Upewnienie się, że teryt_4 jest dostępne globalnie w merged_df
    merged_df['teryt_4'] = merged_df['kod'].str[:4]
    
    # Definicja funkcji pomocniczej
    def add_voivodeship_borders(fig, voivodeships_gdf):
        voivodeships_gdf['id'] = voivodeships_gdf.index.astype(str)
        for _, row in voivodeships_gdf.iterrows():
            geom = row.geometry
            if geom.geom_type == 'Polygon':
                coords = [geom.exterior.coords.xy]
            elif geom.geom_type == 'MultiPolygon':
                coords = [poly.exterior.coords.xy for poly in geom.geoms]
            else:
                continue
            for x, y in coords:
                fig.add_trace(go.Scattergeo(
                    lon=list(x),
                    lat=list(y),
                    mode='lines',
                    line=dict(width=2, color='black'),
                    hoverinfo='none',
                    showlegend=False
                ))
        return fig
    
    # Dane debugujące dla diagnostyki
    @reactive.Calc
    def debug_data():
        poland_teryt = set(poland_gdf['terc'])
        merged_teryt = set(merged_df['teryt_4'])
        only_in_poland = poland_teryt - merged_teryt
        only_in_merged = merged_teryt - poland_teryt
        corr_df = correlation_by_county()
        corr_teryt = set(corr_df['teryt_4'])
        with_corr = corr_teryt.intersection(poland_teryt)
        
        return {
            "poland_count": len(poland_gdf),
            "merged_count": len(merged_df),
            "poland_teryt_count": len(poland_teryt),
            "merged_teryt_count": len(merged_teryt),
            "corr_teryt_count": len(corr_teryt),
            "teryt_with_corr_and_geom": len(with_corr),
            "only_in_poland": sorted(list(only_in_poland)),
            "only_in_merged": sorted(list(only_in_merged)),
            "sample_teryt_poland": sorted(list(poland_teryt))[:10],
            "sample_teryt_merged": sorted(list(merged_teryt))[:10],
            "sample_teryt_corr": sorted(list(corr_teryt))[:10]
        }
    
    # Funkcja do obliczania korelacji
    @reactive.Calc
    def correlation_by_county():
        results = []
        alpha = input.alpha_level()
        for teryt_4 in merged_df['teryt_4'].unique():
            subset = merged_df[merged_df['teryt_4'] == teryt_4]
            if len(subset) < 3:
                continue
            x = subset[input.var1()]
            y = subset[input.var2()]
            analysis = analyze_correlation_with_diagnostics(x, y, alpha)
            if analysis['recommended_r'] is not None:
                results.append({
                    "teryt_4": teryt_4,
                    "correlation": analysis['recommended_r'],
                    "p_value": analysis['recommended_p'],
                    "test_type": analysis['recommended_test'],
                    "n": analysis['n'],
                    "outliers_total": analysis['outliers_x'] + analysis['outliers_y'],
                    "outliers_x": analysis['outliers_x'],
                    "outliers_y": analysis['outliers_y'],
                    "normality_x_p": analysis['normality_x'],
                    "normality_y_p": analysis['normality_y'],
                    "pearson_r": analysis['pearson_r'],
                    "pearson_p": analysis['pearson_p'],
                    "spearman_rho": analysis['spearman_rho'],
                    "spearman_p": analysis['spearman_p'],
                    "interpretation": "; ".join(analysis['interpretation']),
                    "significant": analysis['recommended_p'] < alpha if analysis['recommended_p'] is not None else False
                })
        return pd.DataFrame(results)
    
    # Mapa korelacji
    @output
    @render.ui
    def correlation_map():
        corr_df = correlation_by_county()
        merged_map = poland_gdf.merge(corr_df, left_on='terc', right_on='teryt_4', how='left')
        merged_map['id'] = merged_map.index.astype(str)
        fig = px.choropleth(
            merged_map,
            geojson=merged_map.geometry.__geo_interface__,
            locations='id',
            color="correlation",
            hover_name="pow",
            color_continuous_scale="RdBu",
            range_color=[-1, 1],
            labels={'correlation': 'Korelacja'}
        )
        fig = add_voivodeship_borders(fig, voivodeships_gdf)
        fig.update_geos(
            fitbounds="locations",
            visible=False,
            projection_type="mercator",
            lataxis_range=[49, 55],
            lonaxis_range=[14, 24]
        )
        fig.update_layout(
            margin={"r": 0, "t": 50, "l": 0, "b": 0},
            title=f"Korelacja: {input.var1()} vs {input.var2()}"
        )
        return ui.HTML(pio.to_html(fig, full_html=False, include_plotlyjs="cdn"))
        
    # Ulepszone statystyki mapy
    @output
    @render.ui
    def map_stats():
        corr_df = correlation_by_county()
        powiats_with_corr = len(corr_df)
        total_powiats = len(poland_gdf)
        
        if not corr_df.empty:
            avg_corr = corr_df['correlation'].mean()
            min_corr = corr_df['correlation'].min()
            max_corr = corr_df['correlation'].max()
            pos_corr = (corr_df['correlation'] > 0).sum()
            neg_corr = (corr_df['correlation'] < 0).sum()
            pearson_count = (corr_df['test_type'] == 'pearson').sum()
            spearman_count = (corr_df['test_type'] == 'spearman').sum()
            significant_count = corr_df['significant'].sum()
            avg_n = corr_df['n'].mean()
            avg_outliers = corr_df['outliers_total'].mean()
            
            stats_html = f"""
            <div style="padding: 10px; background-color: #f8f9fa; border-radius: 5px; margin-top: 10px;">
                <h4>Statystyki mapy korelacji</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div>
                        <h5>Podstawowe statystyki</h5>
                        <p>Powiaty z danymi: {powiats_with_corr} z {total_powiats} ({powiats_with_corr/total_powiats:.1%})</p>
                        <p>Średnia korelacja: {avg_corr:.3f}</p>
                        <p>Zakres: {min_corr:.3f} do {max_corr:.3f}</p>
                        <p>Korelacje dodatnie: {pos_corr}, ujemne: {neg_corr}</p>
                        <p>Istotne statystycznie: {significant_count} ({significant_count/powiats_with_corr:.1%})</p>
                    </div>
                    <div>
                        <h5>Diagnostyka testów</h5>
                        <p>Testy Pearsona: {pearson_count}</p>
                        <p>Testy Spearmana: {spearman_count}</p>
                        <p>Średnia wielkość próbki: {avg_n:.1f}</p>
                        <p>Średnia liczba outlierów: {avg_outliers:.1f}</p>
                    </div>
                </div>
            </div>
            """
        else:
            stats_html = """
            <div style="padding: 10px; background-color: #f8f9fa; border-radius: 5px; margin-top: 10px;">
                <h4>Statystyki mapy</h4>
                <p>Brak danych korelacji dla wybranych zmiennych.</p>
            </div>
            """
        return ui.HTML(stats_html)

    # Diagnostyka korelacji
    @output
    @render.ui
    def diagnostic_info():
        corr_df = correlation_by_county()
        if not corr_df.empty:
            normal_x_count = (corr_df['normality_x_p'] > input.alpha_level()).sum() if 'normality_x_p' in corr_df.columns else 0
            normal_y_count = (corr_df['normality_y_p'] > input.alpha_level()).sum() if 'normality_y_p' in corr_df.columns else 0
            high_outliers = (corr_df['outliers_total'] > corr_df['n'] * 0.1).sum()
            both_tests = corr_df.dropna(subset=['pearson_r', 'spearman_rho'])
            if len(both_tests) > 0:
                correlation_agreement = both_tests.apply(
                    lambda row: (row['pearson_r'] > 0) == (row['spearman_rho'] > 0), axis=1
                ).mean()
            else:
                correlation_agreement = np.nan
            
            html = f"""
            <div style="padding: 15px; background-color: #e9ecef; border-radius: 8px;">
                <h4>Szczegółowa diagnostyka testów korelacji</h4>
                <div style="margin-bottom: 15px;">
                    <h5>Założenia testów</h5>
                    <p>Zmienna X - rozkład normalny: {normal_x_count} z {len(corr_df)} powiatów</p>
                    <p>Zmienna Y - rozkład normalny: {normal_y_count} z {len(corr_df)} powiatów</p>
                    <p>Wysokie outlier rate (>10%): {high_outliers} powiatów</p>
                </div>
                <div style="margin-bottom: 15px;">
                    <h5>Wybór testów</h5>
                    <p>Test Pearsona: {(corr_df['test_type'] == 'pearson').sum()} powiatów</p>
                    <p>Test Spearmana: {(corr_df['test_type'] == 'spearman').sum()} powiatów</p>
                </div>
                <div>
                    <h5>Jakość wyników</h5>
                    <p>Zgodność kierunku korelacji (Pearson vs Spearman): {correlation_agreement:.1%}</p>
                    <p>Mediana wielkości próbki: {corr_df['n'].median():.0f}</p>
                    <p>Zakres wielkości próbek: {corr_df['n'].min():.0f} - {corr_df['n'].max():.0f}</p>
                </div>
            </div>
            """
            return ui.HTML(html)
        else:
            return ui.HTML("<p>Brak danych do diagnostyki.</p>")

    # Szczegółowe dane diagnostyczne
    @output
    @render.data_frame
    def detailed_diagnostics():
        corr_df = correlation_by_county()
        if not corr_df.empty:
            display_cols = [
                'teryt_4', 'test_type', 'correlation', 'p_value', 'significant', 
                'n', 'outliers_total', 'normality_x_p', 'normality_y_p'
            ]
            available_cols = [col for col in display_cols if col in corr_df.columns]
            return corr_df[available_cols].round(4)
        else:
            return pd.DataFrame()

    # Informacje debugujące
    @output
    @render.text
    def debug_info():
        debug = debug_data()
        output = [
            f"GeoJSON records: {debug['poland_count']}",
            f"Merged data records: {debug['merged_count']}",
            f"Unique teryt in GeoJSON: {debug['poland_teryt_count']}",
            f"Unique teryt in merged data: {debug['merged_teryt_count']}",
            f"Teryt with correlation data: {debug['corr_teryt_count']}",
            f"Teryt with both correlation and geometry: {debug['teryt_with_corr_and_geom']}",
            "\nSample teryt in GeoJSON:",
            ", ".join(debug['sample_teryt_poland']),
            "\nSample teryt in merged data:",
            ", ".join(debug['sample_teryt_merged']),
            "\nSample teryt with correlation:",
            ", ".join(debug['sample_teryt_corr']),
            "\nTeryt only in GeoJSON (first 10):",
            ", ".join(debug['only_in_poland'][:10]) + ("..." if len(debug['only_in_poland']) > 10 else ""),
            "\nTeryt only in merged data (first 10):",
            ", ".join(debug['only_in_merged'][:10]) + ("..." if len(debug['only_in_merged']) > 10 else "")
        ]
        return "\n".join(output)

    # Spaghetti plot dla zmiennych przemocy
    @output
    @render.ui
    def spaghetti_plot():
        column_to_plot = input.spaghetti_var()
        highlight = input.highlight_powiat()
        dane = merged_df.copy()
        mean_values = dane.groupby('rok')[column_to_plot].mean().reset_index()
        fig = go.Figure()
        for teryt_4 in dane['teryt_4'].unique():
            data_powiat = dane[dane['teryt_4'] == teryt_4]
            pow_name = data_powiat['pow'].iloc[0] + f" ({teryt_4})"
            fig.add_trace(go.Scatter(
                x=data_powiat['rok'],
                y=data_powiat[column_to_plot],
                mode='lines',
                line=dict(
                    color='red' if data_powiat['pow'].iloc[0] == highlight else 'black',
                    width=3 if data_powiat['pow'].iloc[0] == highlight else 1
                ),
                opacity=1.0 if data_powiat['pow'].iloc[0] == highlight else 0.2,
                name=pow_name,
                hoverinfo='name+y'
            ))
        fig.add_trace(go.Scatter(
            x=mean_values['rok'],
            y=mean_values[column_to_plot],
            mode='lines',
            name='Średnia',
            line=dict(color='blue', width=3, dash='dash'),
            hoverinfo='name+y'
        ))
        fig.update_layout(
            title=f'Spaghetti Plot - {column_to_plot}',
            xaxis_title='Rok',
            yaxis_title=f'Wartość: {column_to_plot}',
            yaxis_type='log',
            hovermode='closest',
            legend_title='Powiaty'
        )
        return ui.HTML(pio.to_html(fig, full_html=False, include_plotlyjs="cdn"))

    # Spaghetti plot dla zmiennych odsetkowych
    @output
    @render.ui
    def spaghetti_plot_pct():
        column_to_plot = input.spaghetti_var_pct()
        highlight = input.highlight_powiat_pct()
        dane = pct_df.copy()
        mean_values = dane.groupby('rok')[column_to_plot].mean().reset_index()
        fig = go.Figure()
        for teryt_4 in dane['teryt_4'].unique():
            data_powiat = dane[dane['teryt_4'] == teryt_4]
            pow_name = data_powiat['pow'].iloc[0] + f" ({teryt_4})"
            fig.add_trace(go.Scatter(
                x=data_powiat['rok'],
                y=data_powiat[column_to_plot],
                mode='lines',
                line=dict(
                    color='red' if data_powiat['pow'].iloc[0] == highlight else 'black',
                    width=3 if data_powiat['pow'].iloc[0] == highlight else 1
                ),
                opacity=1.0 if data_powiat['pow'].iloc[0] == highlight else 0.2,
                name=pow_name,
                hoverinfo='name+y'
            ))
        fig.add_trace(go.Scatter(
            x=mean_values['rok'],
            y=mean_values[column_to_plot],
            mode='lines',
            name='Średnia',
            line=dict(color='blue', width=3, dash='dash'),
            hoverinfo='name+y'
        ))
        fig.update_layout(
            title=f'Spaghetti Plot - {column_to_plot} (odsetek)',
            xaxis_title='Rok',
            yaxis_title=f'Wartość: {column_to_plot} (%)',
            yaxis_type='linear',
            hovermode='closest',
            legend_title='Powiaty'
        )
        return ui.HTML(pio.to_html(fig, full_html=False, include_plotlyjs="cdn"))

    # Filtrowanie danych dla mapy przemocowej
    @reactive.Calc
    def filtered_data():
        year = int(input.year())
        return merged_df[merged_df['rok'] == year]

    # Mapa danych przemocowych z obsługą braku danych
    @output
    @render.ui
    def violence_map():
        data_year = filtered_data()
        var = input.violence_var()
        year = int(input.year())
        if year == 2014 and var in ['liczba_osob_kobiety', 'liczba_osob_mezczyzni', 'liczba_osob_dzieci']:
            return ui.HTML(f"<p>Brak danych dla zmiennej {var} w roku 2014.</p>")

        merged_map = poland_gdf.merge(data_year[['teryt_4', var]], left_on='terc', right_on='teryt_4', how='left')
        merged_map['id'] = merged_map.index.astype(str)
        fig = px.choropleth(
            merged_map,
            geojson=merged_map.geometry.__geo_interface__,
            locations='id',
            color=var,
            hover_name="pow",
            color_continuous_scale="Reds",
            range_color=[merged_map[var].min(), merged_map[var].max()],
            labels={var: var}
        )
        fig = add_voivodeship_borders(fig, voivodeships_gdf)
        fig.update_geos(
            fitbounds="locations",
            visible=False,
            projection_type="mercator",
            lataxis_range=[49, 55],
            lonaxis_range=[14, 24]
        )
        fig.update_layout(
            margin={"r": 0, "t": 50, "l": 0, "b": 0},
            title=f"{var} w roku {year}"
        )
        return ui.HTML(pio.to_html(fig, full_html=False, include_plotlyjs="cdn"))

    # Statystyki dla mapy przemocowej
    @output
    @render.ui
    def violence_stats():
        data_year = filtered_data()
        var = input.violence_var()
        year = int(input.year())
        if year == 2014 and var in ['liczba_osob_kobiety', 'liczba_osob_mezczyzni', 'liczba_osob_dzieci']:
            return ui.HTML("<p>Brak statystyk – dane niedostępne dla roku 2014.</p>")
        
        avg_value = data_year[var].mean()
        sum_value = data_year[var].sum()
        avg_over_years = merged_df[merged_df[var].notnull()].groupby('rok')[var].mean().mean()
        avg_poland_over_years = merged_df[merged_df[var].notnull()].groupby('rok')[var].sum().mean()
        
        return ui.HTML(f"""
            <div style="padding: 10px; background-color: #f8f9fa; border-radius: 5px;">
                <h4>Statystyki</h4>
                <p>Liczba powiatów: {data_year['teryt_4'].nunique()}</p>
                <p>Średnia wartość dla powiatów w roku {year}: {avg_value:.2f}</p>
                <p>Średnia wartość dla powiatów z lat 2014–2023: {avg_over_years:.2f}</p>
                <p>Suma dla całej Polski w roku {year}: {sum_value:.0f}</p>
                <p>Średnia wartość dla Polski z lat 2014–2023: {avg_poland_over_years:.0f}</p>
            </div>
        """)

    # Pobieranie mapy przemocowej
    @render.download(filename="violence_map.png")
    def download_violence_map():
        data_year = filtered_data()
        var = input.violence_var()
        year = int(input.year())
        if year == 2014 and var in ['liczba_osob_kobiety', 'liczba_osob_mezczyzni', 'liczba_osob_dzieci']:
            return
        merged_map = poland_gdf.merge(data_year[['teryt_4', var]], left_on='terc', right_on='teryt_4', how='left')
        merged_map['id'] = merged_map.index.astype(str)
        fig = px.choropleth(
            merged_map,
            geojson=merged_map.geometry.__geo_interface__,
            locations='id',
            color=var,
            hover_name="pow",
            color_continuous_scale="Reds",
            range_color=[merged_df[var].min(), merged_df[var].max()],
            labels={var: var}
        )
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(title=f"{var} w roku {year}")
        with io.BytesIO() as buf:
            fig.write_image(buf, format="png")
            yield buf.getvalue()

    # Filtrowanie danych dla mapy odsetkowej
    @reactive.Calc
    def filtered_pct_data():
        year = int(input.pct_year())
        return pct_df[pct_df['rok'] == year]

    # Mapa odsetków przemocy z obsługą braku danych
    @output
    @render.ui
    def pct_map():
        data_year = filtered_pct_data()
        var = input.pct_var()
        year = int(input.pct_year())
        if year == 2014 and var in ['odsetek_kobiety', 'odsetek_mezczyzni', 'odsetek_dzieci']:
            return ui.HTML(f"<p>Brak danych dla zmiennej {var} w roku 2014.</p>")

        merged_map = poland_gdf.merge(data_year[['teryt_4', var]], left_on='terc', right_on='teryt_4', how='left')
        merged_map['id'] = merged_map.index.astype(str)
        fig = px.choropleth(
            merged_map,
            geojson=merged_map.geometry.__geo_interface__,
            locations='id',
            color=var,
            hover_name="pow",
            color_continuous_scale="Reds",
            range_color=[data_year[var].min(), data_year[var].max()],
            labels={var: f"{var} (%)"}
        )
        fig = add_voivodeship_borders(fig, voivodeships_gdf)
        fig.update_geos(
            fitbounds="locations",
            visible=False,
            projection_type="mercator",
            lataxis_range=[49, 55],
            lonaxis_range=[14, 24]
        )
        fig.update_layout(
            margin={"r": 0, "t": 50, "l": 0, "b": 0},
            title=f"{var} (%) w roku {year}"
        )
        return ui.HTML(pio.to_html(fig, full_html=False, include_plotlyjs="cdn"))

    # Statystyki dla mapy odsetkowej
    @output
    @render.ui
    def pct_stats():
        data_year = filtered_pct_data()
        var = input.pct_var()
        year = int(input.pct_year())
        if year == 2014 and var in ['odsetek_kobiety', 'odsetek_mezczyzni', 'odsetek_dzieci']:
            return ui.HTML("<p>Brak statystyk – dane niedostępne dla roku 2014.</p>")
        
        if var == 'odsetek_ogol':
            affected_population = (data_year['odsetek_ogol'] * data_year['liczba_ludnosci'] / 100).sum()
            total_population = data_year['liczba_ludnosci'].sum()
        elif var == 'odsetek_kobiety':
            affected_population = (data_year['odsetek_kobiety'] * data_year['liczba_ludnosci_kobiety'] / 100).sum()
            total_population = data_year['liczba_ludnosci_kobiety'].sum()
        elif var == 'odsetek_mezczyzni':
            affected_population = (data_year['odsetek_mezczyzni'] * data_year['liczba_ludnosci_mezczyzni'] / 100).sum()
            total_population = data_year['liczba_ludnosci_mezczyzni'].sum()
        elif var == 'odsetek_dzieci':
            affected_population = (data_year['odsetek_dzieci'] * data_year['liczba_dzieci'] / 100).sum()
            total_population = data_year['liczba_dzieci'].sum()
        
        avg_value = data_year[var].mean()
        percent_value = (affected_population / total_population * 100) if total_population > 0 else 0
        avg_over_years = pct_df[pct_df[var].notnull()].groupby('rok').apply(
            lambda x: (x[var] * x['liczba_ludnosci'] / 100).sum() / x['liczba_ludnosci'].sum() * 100
            if var == 'odsetek_ogol' and x['liczba_ludnosci'].sum() > 0 else
            (x[var] * x['liczba_ludnosci_kobiety'] / 100).sum() / x['liczba_ludnosci_kobiety'].sum() * 100
            if var == 'odsetek_kobiety' and x['liczba_ludnosci_kobiety'].sum() > 0 else
            (x[var] * x['liczba_ludnosci_mezczyzni'] / 100).sum() / x['liczba_ludnosci_mezczyzni'].sum() * 100
            if var == 'odsetek_mezczyzni' and x['liczba_ludnosci_mezczyzni'].sum() > 0 else
            (x[var] * x['liczba_dzieci'] / 100).sum() / x['liczba_dzieci'].sum() * 100
            if var == 'odsetek_dzieci' and x['liczba_dzieci'].sum() > 0 else 0
        ).mean()
        
        return ui.HTML(f"""
            <div style="padding: 10px; background-color: #f8f9fa; border-radius: 5px;">
                <h4>Statystyki</h4>
                <p>Liczba powiatów: {data_year['teryt_4'].nunique()}</p>
                <p>Średni odsetek w powiecie w roku {year}: {avg_value:.2f}%</p>
                <p>Odsetek dla Polski w roku {year}: {percent_value:.2f}%</p>
                <p>Średni odsetek dla Polski z lat 2014–2023: {avg_over_years:.2f}%</p>
            </div>
        """)

    # Pobieranie mapy odsetkowej
    @render.download(filename="pct_map.png")
    def download_pct_map():
        data_year = filtered_pct_data()
        var = input.pct_var()
        year = int(input.pct_year())
        if year == 2014 and var in ['odsetek_kobiety', 'odsetek_mezczyzni', 'odsetek_dzieci']:
            return
        merged_map = poland_gdf.merge(data_year[['teryt_4', var]], left_on='terc', right_on='teryt_4', how='left')
        merged_map['id'] = merged_map.index.astype(str)
        fig = px.choropleth(
            merged_map,
            geojson=merged_map.geometry.__geo_interface__,
            locations='id',
            color=var,
            hover_name="pow",
            color_continuous_scale="Reds",
            range_color=[pct_df[var].min(), pct_df[var].max()],
            labels={var: f"{var} (%)"}
        )
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(title=f"{var} (%) w roku {year}")
        with io.BytesIO() as buf:
            fig.write_image(buf, format="png")
            yield buf.getvalue()

    # Podgląd danych
    @reactive.calc
    def dat():
        infile = Path("Sprawozdanie_przemoc_2014_2023_powiaty.xlsx")
        return pd.read_excel(infile)

    @render.data_frame
    def frame():
        return dat()

    @render.table
    def table():
        return dat()

    @render.download(filename="Sprawozdanie_przemoc_2014_2023_powiaty.csv")
    def download_csv():
        csv_bytes = merged_df.to_csv(index=False).encode("utf-8")
        yield csv_bytes


# Funkcje renderujące
    @output
    @render.ui
    def correlation_scatter_plot():
        year = int(input.corr_year())
        var1 = input.corr_var1()
        var2 = input.corr_var2()
        alpha = input.corr_alpha()

        subset = df[df['rok'] == year]

        # Sprawdzenie czy zmienne istnieją w danych
        if var1 not in subset.columns or var2 not in subset.columns:
            return ui.HTML("<p>Wybrane zmienne nie są dostępne dla tego roku.</p>")

        x = subset[var1].dropna()
        y = subset[var2].dropna()

        # Utworzenie wspólnego indeksu dla obu zmiennych
        common_idx = x.index.intersection(y.index)
        x = x.loc[common_idx]
        y = y.loc[common_idx]

        if len(x) < 3:
            return ui.HTML("<p>Zbyt mało danych do analizy korelacji.</p>")

        result = analyze_correlation_with_diagnostics(x, y, alpha)

        # Wykres rozrzutu bez linii trendu
        scatter_data = pd.DataFrame({var1: x, var2: y})

        fig = px.scatter(
            scatter_data, 
            x=var1, 
            y=var2, 
            title=f"Wykres rozrzutu: {var1} vs {var2} (Rok {year})",
            labels={
                var1: f"{var1} (%)",
                var2: f"{var2} (%)"
            }
        )

        # Stylizacja punktów podobna do przykładu
        fig.update_traces(
            marker=dict(
                size=5,
                color='black',
                symbol='circle-open',
                line=dict(width=1, color='black'),
                opacity=0.9
            )
        )

        # Dodanie linii regresji y=x
        min_val = min(x.min(), y.min())
        max_val = max(x.max(), y.max())
        
        fig.add_trace(
            go.Scatter(
                x=[min_val, max_val],
                y=[min_val, max_val],
                mode='lines',
                line=dict(color='red', width=2, dash='dash'),
                name='y = x',
                showlegend=True
            )
        )

        # Dodanie informacji o korelacji do tytułu
        corr_coef = result.get('correlation', 0)
        fig.update_layout(
            title=f"Wykres rozrzutu: {var1} vs {var2} - Rok {year}",
            xaxis_title=f"{var1} (%)",
            yaxis_title=f"{var2} (%)",
            showlegend=True,
            plot_bgcolor='white',
            paper_bgcolor='white',
            # Ustawienia dla bardziej kwadratowego wykresu
            width=600,
            height=600,
            xaxis=dict(
                showgrid=True,
                gridcolor='lightgray',
                gridwidth=0.5,
                zeroline=True,
                zerolinecolor='gray',
                zerolinewidth=1,
                # Zapewnienie równych zakresów osi
                range=[min_val - (max_val - min_val) * 0.05, max_val + (max_val - min_val) * 0.05],
                scaleanchor="y",
                scaleratio=1
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='lightgray',
                gridwidth=0.5,
                zeroline=True,
                zerolinecolor='gray',
                zerolinewidth=1,
                # Zapewnienie równych zakresów osi
                range=[min_val - (max_val - min_val) * 0.05, max_val + (max_val - min_val) * 0.05]
            )
        )

        html = pio.to_html(fig, full_html=False, include_plotlyjs="cdn")
        return ui.HTML(html)

    @output
    @render.ui
    def correlation_interpretation():
        year = int(input.corr_year())
        var1 = input.corr_var1()
        var2 = input.corr_var2()
        alpha = input.corr_alpha()

        subset = df[df['rok'] == year]

        if var1 not in subset.columns or var2 not in subset.columns:
            return ui.HTML("<p>Wybrane zmienne nie są dostępne dla tego roku.</p>")

        x = subset[var1].dropna()
        y = subset[var2].dropna()

        common_idx = x.index.intersection(y.index)
        x = x.loc[common_idx]
        y = y.loc[common_idx]

        if len(x) < 3:
            return ui.HTML("<p>Zbyt mało danych do interpretacji.</p>")

        result = analyze_correlation_with_diagnostics(x, y, alpha)

        interpretation_items = []
        for item in result['interpretation']:
            if "istotny statystycznie" in item.lower():
                item_class = "significant"
            elif "nieistotny statystycznie" in item.lower():
                item_class = "insignificant"
            else:
                item_class = ""
            if item.startswith("Siła związku") or item.startswith("Rekomendacja"):
                item_class += " highlight" if item_class else "highlight"
            interpretation_items.append(f'<li class="{item_class}">{item}</li>')

        html = f"""
        <div class="correlation-interpretation">
            <h4>Interpretacja korelacji ({var1} vs {var2}, Rok {year})</h4>
            <ul>
                {''.join(interpretation_items)}
            </ul>
            <p><strong>Liczba obserwacji:</strong> {len(x)}</p>
        </div>
        """
        return ui.HTML(html)

    # Reaktywna funkcja obliczająca macierz korelacji dla danych odsetkowych
    @reactive.Calc
    def correlation_matrix():
        year = int(input.matrix_year())
        subset = df[df['rok'] == year]

        # Tylko dostępne zmienne odsetkowe
        available_vars = [var for var in all_vars_odsetki if var in subset.columns]

        if len(available_vars) < 2:
            return None

        corr_data = subset[available_vars].select_dtypes(include=[np.number])

        # Usunięcie kolumn bez wariancji
        corr_data = corr_data.loc[:, corr_data.std() > 0]

        if corr_data.shape[1] < 2:
            return None

        return corr_data.corr()

    # Renderowanie macierzy korelacji
    @output
    @render.ui
    def correlation_matrix_plot():
        corr_matrix = correlation_matrix()
        if corr_matrix is None:
            return ui.HTML("<p>Brak wystarczających danych odsetkowych do wyświetlenia macierzy korelacji dla wybranego roku.</p>")

        fig = px.imshow(
            corr_matrix,
            labels=dict(color="Współczynnik korelacji"),
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            color_continuous_scale="RdBu",
            zmin=-1,
            zmax=1,
            text_auto=".3f",
            aspect="auto"
        )

        fig.update_layout(
            title=f"Macierz korelacji danych odsetkowych - rok {input.matrix_year()}",
            width=700,
            height=700,
            xaxis={'side': 'bottom'},
            yaxis={'side': 'left'}
        )

        # Poprawa czytelności etykiet
        fig.update_xaxes(tickangle=45)
        fig.update_yaxes(tickangle=0)

        return ui.HTML(pio.to_html(fig, full_html=False, include_plotlyjs="cdn"))


    @output
    @render.ui
    def resztki_map():
        # Get model type from input
        model_type = input.model_type()

        # Calculate resztki by county
        resztki_df, model = calculate_resztki_by_county(model_type)

        # Merge with geographical data
        merged_map = poland_gdf.merge(resztki_df, left_on='terc', right_on='teryt_4', how='left')
        merged_map['id'] = merged_map.index.astype(str)

        # Create choropleth map
        fig = px.choropleth(
            merged_map,
            geojson=merged_map.geometry.__geo_interface__,
            locations='id',
            color="mean_residual",
            hover_name="pow",
            hover_data={
                'mean_residual': ':.4f',
                'std_residual': ':.4f', 
                'n_observations': True,
                'mean_actual': ':.4f',
                'mean_fitted': ':.4f'
            },
            color_continuous_scale="RdBu_r",  # Reversed RdBu so red = positive resztki
            range_color=None,  # Auto-scale based on data
            labels={
                'mean_residual': 'Średnia reszt',
                'std_residual': 'Odchylenie Std reszt',
                'n_observations': 'Liczba Obserwacji',
                'mean_actual': 'Średnia Wartość Rzeczywista',
                'mean_fitted': 'Średnia Wartość Dopasowana'
            }
        )

        # Add voivodeship borders
        fig = add_voivodeship_borders(fig, voivodeships_gdf)

        # Update map layout
        fig.update_geos(
            fitbounds="locations",
            visible=False,
            projection_type="mercator",
            lataxis_range=[49, 55],
            lonaxis_range=[14, 24]
        )

        model_name = "Model 1 (bez efektów stałych)" if model_type == 'model1' else "Model 2 (z efektami stałymi)"
        fig.update_layout(
            margin={"r": 0, "t": 50, "l": 0, "b": 0},
            title=f"Reszty modelu regresji - {model_name}",
            coloraxis_colorbar=dict(
                title="Średnia reszt<br>(Rzeczywiste - Dopasowane)"
            )
        )

        return ui.HTML(pio.to_html(fig, full_html=False, include_plotlyjs="cdn"))

    # Add download handler for resztki map
    @render.download(filename="residuals_map.html")
    def download_resztki_map():
        model_type = input.model_type()
        resztki_df, model = calculate_resztki_by_county(model_type)

        # Create the same map as in resztki_map()
        merged_map = poland_gdf.merge(resztki_df, left_on='terc', right_on='teryt_4', how='left')
        merged_map['id'] = merged_map.index.astype(str)

        fig = px.choropleth(
            merged_map,
            geojson=merged_map.geometry.__geo_interface__,
            locations='id',
            color="mean_residual",
            hover_name="pow",
            hover_data={
                'mean_residual': ':.4f',
                'std_residual': ':.4f', 
                'n_observations': True,
                'mean_actual': ':.4f',
                'mean_fitted': ':.4f'
            },
            color_continuous_scale="RdBu_r",
            range_color=None,
            labels={
                'mean_residual': 'Średnia reszt',
                'std_residual': 'Odchylenie Std reszt',
                'n_observations': 'Liczba Obserwacji',
                'mean_actual': 'Średnia Wartość Rzeczywista',
                'mean_fitted': 'Średnia Wartość Dopasowana'
            }
        )

        fig = add_voivodeship_borders(fig, voivodeships_gdf)
        fig.update_geos(
            fitbounds="locations",
            visible=False,
            projection_type="mercator",
            lataxis_range=[49, 55],
            lonaxis_range=[14, 24]
        )

        model_name = "Model 1 (bez efektów stałych)" if model_type == 'model1' else "Model 2 (z efektami stałymi)"
        fig.update_layout(
            margin={"r": 0, "t": 50, "l": 0, "b": 0},
            title=f"Reszty modelu regresji - {model_name}",
            coloraxis_colorbar=dict(
                title="Średnia reszt<br>(Rzeczywiste - Dopasowane)"
            )
        )

        return pio.to_html(fig, full_html=True, include_plotlyjs="cdn")

    # Function to display resztki statistics
    @output
    @render.ui  
    def resztki_stats():
        model_type = input.model_type()
        resztki_df, model = calculate_resztki_by_county(model_type)

        # Calculate overall statistics
        total_counties = len(resztki_df)
        total_counties_with_geo = len(poland_gdf)

        if not resztki_df.empty:
            overall_mean_residual = resztki_df['mean_residual'].mean()
            overall_std_residual = resztki_df['mean_residual'].std()
            min_residual = resztki_df['mean_residual'].min()
            max_residual = resztki_df['mean_residual'].max()

            # Count positive and negative resztki
            positive_resztki = (resztki_df['mean_residual'] > 0).sum()
            negative_resztki = (resztki_df['mean_residual'] < 0).sum()

            # Model fit statistics
            r_squared = model.rsquared
            adj_r_squared = model.rsquared_adj
            rmse = np.sqrt(model.mse_resid)

            # Average observations per county
            avg_obs_per_county = resztki_df['n_observations'].mean()
            total_observations = resztki_df['n_observations'].sum()

            model_name = "Model 1 (bez efektów stałych)" if model_type == 'model1' else "Model 2 (z efektami stałymi)"

            stats_html = f"""
            <div style="padding: 10px; background-color: #f8f9fa; border-radius: 5px; margin-top: 10px;">
                <h4>Statystyki reszt - {model_name}</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div>
                        <h5>Reszty według powiatów</h5>
                        <p>Powiaty z danymi: {total_counties} z {total_counties_with_geo}</p>
                        <p>Średnia reszt: {overall_mean_residual:.4f}</p>
                        <p>Odchylenie std: {overall_std_residual:.4f}</p>
                        <p>Zakres: {min_residual:.4f} do {max_residual:.4f}</p>
                        <p>Reszty dodatnie: {positive_resztki}, ujemne: {negative_resztki}</p>
                        <p>Średnio obserwacji na powiat: {avg_obs_per_county:.1f}</p>
                    </div>
                    <div>
                        <h5>Dopasowanie modelu</h5>
                        <p>R-squared: {r_squared:.4f}</p>
                        <p>Adjusted R-squared: {adj_r_squared:.4f}</p>
                        <p>RMSE: {rmse:.4f}</p>
                        <p>Całkowita liczba obserwacji: {total_observations}</p>
                        <p style="margin-top: 15px; font-size: 0.9em; color: #666;">
                            <strong>Interpretacja:</strong><br>
                            • Reszty dodatnie (czerwone): model niedoszacowuje<br>
                            • Reszty ujemne (niebieskie): model przeszacowuje<br>
                            • Reszty bliskie 0: dobre dopasowanie modelu
                        </p>
                    </div>
                </div>
            </div>
            """
        else:
            stats_html = """
            <div style="padding: 10px; background-color: #f8f9fa; border-radius: 5px; margin-top: 10px;">
                <h4>Statystyki reszt</h4>
                <p>Brak danych reszt dla wybranego modelu.</p>
            </div>
            """

        return ui.HTML(stats_html)

    # Additional function to create resztki vs fitted plot
    @output
    @render.ui
    def resztki_vs_fitted_plot():
        model_type = input.model_type()
        resztki_df, model = calculate_resztki_by_county(model_type)

        # Create scatter plot of resztki vs fitted values
        fig = px.scatter(
            resztki_df, 
            x='mean_fitted', 
            y='mean_residual',
            hover_data=['teryt_4', 'n_observations'],
            labels={
                'mean_fitted': 'Średnie Wartości Dopasowane',
                'mean_residual': 'Średnia reszt'
            },
            title='Reszty vs Wartości Dopasowane (według powiatów)'
        )

        # Add horizontal line at y=0
        fig.add_hline(y=0, line_dash="dash", line_color="red", opacity=0.7)

        fig.update_layout(
            margin={"r": 0, "t": 50, "l": 0, "b": 0},
            height=400
        )

        return ui.HTML(pio.to_html(fig, full_html=False, include_plotlyjs="cdn"))

    @output
    @render.download(filename="Praca_licencjacka.pdf")
    def download_pdf():
        path = "Praca_licencjacka.pdf"
        with open(path, "rb") as f:
            yield f.read()


app = App(app_ui, server)