# Rozdział pierwszy: Wprowadzenie do statystyki przestrzennej.

## 1.1 Metody analiz przestrzennych- podstawowe definicje i pojęcia
Analizy przestrzenne:
* Analizy pionowe- różne informacje, ten sam obszar
* Analizy poziome- ta sama informacja, inne obszary


* Zapytanie do bazy
* Pomiaru
* Przekształcenia: Buforowanie i ponowna klasyfikacja wg atrybutów

Interpolacja przesztrzenna- ma na celu okresleni wartosci pewenj w zmiennej w punkcie w którym ona nie była mierzona
## 1.2 Informacje przestrzenne- klasyfikacja, pomiar zmiennych
### Pytania najczęściej zadawane przez badaczy dotyczą:
1. charakteru występowania zjawiska tzn ustalenia czy dane zjawisko ma w przestrzeni charakter regularny, losowy lub klastrowy.
2. prawidłowości przestrzennych wykazywanych przez obiekty lub zjawiska
3. rozproszenia lub skupienia podobnych wartości badanej zmiennej 
4. skorelowanie badanej zmiennej  z innymi zmiennymi na danym obszarze
5. niezależności różnych wartości zmiennej, ,, przyciągania się” lub ,,odpychania się” podobnych wartości zmiennej badanej 
6. zmian w przestrzennym rozkładzie zmiennych
### Dane zlokalizowane:
1.  zbiór znaków 
2. zbiór słów
3. Dane Statystyczne:
* Klasyfikacja wg źródeł informacji
1.  informacje naturalne(geograficzne)
  * Dane geograficzne:
- Dane rastrowe- opisane za pomocą siatki 
- Dane wektorowe - opisane za pomocą współrzędnych
2. społeczno ekonomiczne
* Dane infrastrukturalne - łączą dane geograficzne i społeczno ekonomiczne, najczęściej są to informacje o wielkości i położeniu obiektów w postaci infrastruktury( np rzeki,kanały drogi)
* Klasyfikacja wg typów informacji
1. informacje otrzymane na podstawie różnego rodzaju pomiarów topograficznych:
1. Dane powierzchniowe - ciągła zmienność informacji otrzymywana na podstawie ocen i informacji przestrzennych gromadzonych w terenie.- metoda interpolacji obszarowej
1. Dane obszarowe- dane dyskretne - pochodzą z pewnej powierzchni geograficznej dla badanych obiektów, wykazują autokorelacja przestrzenna i heterogeniczności.
1. Dane punktowe - odnoszą się do badanych zjawisk, które się zrealizowały. Mają tendencję do tworzenia skupisk dlatego trzeba je testować. 
1. Dane przestrzenno- czasowe- wykorzystują dane o wymiarze czasowym i przestrzennym.

#### Rodzaje metryk:

1. Przestrzeń euklidesowa- umożliwia dobre przybliżenie odległości przestrzennych w przypadku dużych wielkości. Płaskość wyznaczanych odległości.
na układzie współrzędnych 
![Zrzut ekranu 2024-07-11 130514](https://github.com/user-attachments/assets/93c40e8a-80bb-4d60-ad63-5af944881ec0 "euklides")


2. Metryka manhattan:


![Zrzut ekranu 2024-07-11 130710](https://github.com/user-attachments/assets/32aaafbb-dedb-426f-b0f9-0f5c8213e063 "manhattan")

4. Metryka sferyczna:

![Zrzut ekranu 2024-07-11 130734](https://github.com/user-attachments/assets/c0699494-5e6d-4e55-912e-17beb0ce35c7 "ortodroma")

## 1.3 Jakość danych przestrzennych

Siedem cech dotyczących jakości danych przestrzennych:
1. pochodzenie- skąd pochodzą dane, kiedy zostały pozyskane i jak?
1. zgodność- brak wewnętrznej sprzeczności
1. kompleksowość- spełnienia przez zbiór danych deklarowanych wytycznych
1. dokładność semantyczna- wyraża wierności z jaką zbiór danych odpowiadający przyjętemu modelowi danych przestrzennych odtwarza dziedzinę problemu
1. dokładność czasowa- aktualność danych do wymagań
1. dokładność pozycyjna-dokładność współrzędnych punktów
1. dokładność atrybutu-prawidłowość określenia atrybutów

## 1.4 Niepewność w danych przestrzennych

Głównym źródłem niepewności jest sposób zdefiniowania badanych obiektów w przestrzeni.

### Dobrze zdefiniowany obiekt - można go wydzielić z innych obiektów.

#### Rodzaje błędów niepewności przy dobrze zdefiniowanym obiekcie:
1. pomiarowe
1. klasyfikacji
1. wynikające z generalizacji przestrzeni
1. popełniane podczas wprowadzania danych
1. powstałe w wyniku upływu czasu 
1. powstałe podczas przetwarzania danych
1. wynikajce z fakt ze atrybutu czy polozenie obiektow w przestrzeni nie są pewne i mogą być określone jedynie z pewnym prawdopodobieństwem
### Obiekty słabo zdefiniowany - nieokreślony i niejednorodność.
##### Nieokreśloność:
* własności- wynika z braku wyraźnych granic obiektu
* atrybutów- wynika z braku jednoznacznych kryteriów klasyfikacji.- Teoria zbiorów rozmytych
#### Niejednorodność- problem przyporządkowania obiektu do określonej klasy w sytuacji gdy w systemach klasyfikacji występują różne kryteria służące do określenia tej samej klasy.
* niezgodność -teoria Dempstera-Shafera(DST) i model danych częściowo wyspecyfikowany
* niespecyficzność-teoria zbiorów rozmytych

## 1.5 Reprezentatywności próby w badaniach przestrzennych.

#### Próba reprezentatywna powinna spełniać:
1. Nieobecność czynników selektywnych- brak stronniczej selekcji, rozwiązanie: losowy dobór jednostek do próby.
1. Miniatura populacji generalnej- rozkład cech stanowi idealne odwzorowanie rozkładu cech w populacji.
1. Typowość– wysoka częstość występowania pewnych cech w badanej populacji.
1. Pokrycie różnorodności populacji-  włączenie do próbki przedstawicieli wszystkich podgrup.
#### Metody pobierania próbki losowej:
1. Metoda dobór prostej próby losowej
1. Metoda warstwowa próba losowa 
1. Metoda próba systematyczna 
1. Metoda warstwowej, systematycznej próby nieliniowej

# Rozdział drugi: Geneza i rozwój metod statystyki przestrzennej.
## 2.1 Statystyka przestrzenna jako dziedzina analizy przestrzennej
Statystyczna analiza danych przestrzennych:
1. ekonometria przestrzenna - specyfikacja, estymacja i weryfikacja modeli uwzględniających aspekt przestrzenny.
2. statystyka przestrzenna - opiera na się na analizie danych
### Trzy główne nurty metodologiczne w statystyce przestrzennej:
####  1.analiza danych punktowych: 
##### w jaki sposób obiekty są rozmieszczane w przestrzeni:
 * losowo-(na rozmieszczenie nie wpływa żaden czynnik)
 * regularnie-(świadome rozmieszczenie obiektów w nienaturalny sposób)
 * klastrowo-( na rozmieszczeni wplywa czynnik)
##### Warunki konieczne do przeprowadzenia analizy danych punktowych:
1. znajomość długości i szerokości współrzędnych geograficznych punktó nanoszonych na mapę
2. wcześniejsze określenie powierzchni badanego obszaru
3. dane punktowe powinny stanowić kompletny zbiór, a nie jedynie próbę
4. istnienie rzeczywistej zależności między obiektami analizowane obszaru a punktami nanoszonymi na mapę
   
#### 2. geostatystyka - optymalizacja szacowanych parametrów geologicznych
#### 3. metody analizy danych obszarowych i i punktowych atrybutowych
## 2.2 Rozwój metod statystyki przestrzennej
Autokorelacja przestrzenna- występowanie jednego zjawiska w jednej jednostce przestrzennej powoduje zmniejszanie się bądź zwiększanie się tego zjawiska w jednostkach sąsiednich. 

## 2.3 Powiązanie statystyki przestrzennej z innymi dziedzinami
### 2.3.1 Statystyka przestrzenna a  tradycyjna statystyka
Statystyka klasyczna zakłada, że elementy próby są dobierane niezależnie, natomiast statystyka przestrzenna nie może spełnić tego założenia(Prawo Toblera)

### 2.3.2 Statystyka przestrzenna a geografia 
#### Przestrzeń geograficzna - jest główną cechą, która odróżnia tradycjne dane statystyczne od danych przestrzennych.
##### Można podzielić ją na:
* przestrzeń społeczno-ekonomiczną
* przestrzeń społeczną
### 2.3.3 Statystka przestrzenna a ekonometria przestrzenna. 
#### Trzy zasady modelowania statystycznego:
1. qproksymacja funkcji(regresja przestrzenna) dopasowującej do zbioru wejściowych danych przestrzennych zależności analitycznej wyrażonej wzorem matematycznym
2. klasyfikacja, czyli przypisanie zaobserwowanych przypadków do określonej liczby klas kategorii reprezentowanych przez zmnienne wyjsciowe
3. wykrywanie regularności istotnych cech w danych wejściowych bez znajomości wzorców

#### Statystyka przestrzenna opiera się na podejściu data driven
#### Ekonometria przestrzenna opiera się na podejściumodel driven 
# Rozdział trzeci: Dane przestrzenne-podstawowe zagadnienia
## 3.1 Klasyfikacja i własności danych przestrzennych
#### Cztery rodzaje danych przestrzennych wg Cressie:
1. Dane obszarowe - charakteryzujące się skokową zmniennościa- jest określony
2. Dane powierzchniowe- określane poprzez ciągłą zmienność na podstawie funkcji odległości- jest określony
3. Dane punktowe - reprezentują wartości zmiennych mające charakter puunktów w przestreni georgaficznej- pole losowe
5. Obszary przestrzenne - wartości zmiennych mające charakter obiektów o określonym zasięgu przestrzennym- pole losowe
#### Efekty pierwszego rzędu - odnoszą się do zmian wartości średnej danej zmiennej w określonej przestrzeni. - Trafycyjna regresja
#### Efekty drugiego rzędu- odnoszą się do przestrzennych zależności pomiędzy jednostkami. Zachodzi efekt sąsiedztwa. - techniki analizy biorące pod uwagę kowiariancję w danych generujących efekty lokalne.
#### Współzależność przestrzenna - natężenie pewnych zjawisk przenosi się a obiektu na inne obszary sąsiednie. = Prawo Toblera = autokorelacja przestrzenna. 
#### Heterogeniczność przestrzenna(odwzorowanie stacjonarności w szeregach czasowych) - brak stałości struktur rozmieszcenia wartości badanych cech.
#### Błąd ekologiczny - różnica pomiędzy wartością statystyki dla pojedynczego obiektu estymowanej za pomocą zbiorowości a wartością statystyki szacowanej na podstawie jednsotek.
#### Błąd atomistyczny - odwrotność błędu ekologicznego
#### Problem zmiennej jednsotki odniesienia - błąd wynikający z faktu, że zjawisko o charakterze punktowym jest analizowane za pomocą danych zagregowanych. - szczególny przypadek błedu ekologicznego.
### 3.1.1 Dane obszarowe
-miejsce na wzór strona 52!!!
#### Główne techniki analizy danych obszarowych:
1. przestrzenna średnia ruchoma
2. estymacja jądra
3. przestrzenna autokorelacja
4. przestrzenna korelacja i regresja
### 3.1.2 Dane powierzchniowe

