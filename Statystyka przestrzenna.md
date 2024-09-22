# Rozdział pierwszy: Wprowadzenie do statystyki przestrzennej.

## 1.1 Metody analiz przestrzennych- podstawowe definicje i pojęcia
Analizy przestrzenne:
* Analizy pionowe- różne informacje, ten sam obszar
* Analizy poziome- ta sama informacja, inne obszary


* Zapytanie do bazy
* Pomiaru
* Przekształcenia: Buforowanie i ponowna klasyfikacja wg atrybutów

Interpolacja przesztrzenna- ma na celu okreslenie wartosci pewnej zmiennej w punkcie w którym ona nie była mierzona
## 1.2 Informacje przestrzenne- klasyfikacja, pomiar zmiennych
### Pytania najczęściej zadawane przez badaczy dotyczą:
1. Charakteru występowania zjawiska tzn ustalenia czy dane zjawisko ma w przestrzeni charakter regularny, losowy lub klastrowy.
2. Prawidłowości przestrzennych wykazywanych przez obiekty lub zjawiska
3. Rozproszenia lub skupienia podobnych wartości badanej zmiennej 
4. Skorelowanie badanej zmiennej  z innymi zmiennymi na danym obszarze
5. Niezależności różnych wartości zmiennej, ,, przyciągania się” lub ,,odpychania się” podobnych wartości zmiennej badanej 
6. Zmian w przestrzennym rozkładzie zmiennych
### Dane zlokalizowane:
1. Zbiór znaków 
2. Zbiór słów
3. Dane Statystyczne:
* Klasyfikacja wg źródeł informacji
1.  Informacje naturalne(geograficzne)
  * Dane geograficzne:
- Dane rastrowe- opisane za pomocą siatki 
- Dane wektorowe - opisane za pomocą współrzędnych
2. Społeczno ekonomiczne
* Dane infrastrukturalne - łączą dane geograficzne i społeczno ekonomiczne, najczęściej są to informacje o wielkości i położeniu obiektów w postaci infrastruktury( np rzeki,kanały drogi)
* Klasyfikacja wg typów informacji
1. Informacje otrzymane na podstawie różnego rodzaju pomiarów topograficznych:
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
1. Pochodzenie- skąd pochodzą dane, kiedy zostały pozyskane i jak?
1. Zgodność- brak wewnętrznej sprzeczności
1. Kompleksowość- spełnienia przez zbiór danych deklarowanych wytycznych
1. Dokładność semantyczna- wyraża wierności z jaką zbiór danych odpowiadający przyjętemu modelowi danych przestrzennych odtwarza dziedzinę problemu
1. Dokładność czasowa- aktualność danych do wymagań
1. Dokładność pozycyjna-dokładność współrzędnych punktów
1. Dokładność atrybutu-prawidłowość określenia atrybutów

## 1.4 Niepewność w danych przestrzennych

Głównym źródłem niepewności jest sposób zdefiniowania badanych obiektów w przestrzeni.

### Dobrze zdefiniowany obiekt - można go wydzielić z innych obiektów.

#### Rodzaje błędów niepewności przy dobrze zdefiniowanym obiekcie:
1. Pomiarowe
1. Klasyfikacji
1. Wynikające z generalizacji przestrzeni
1. Popełniane podczas wprowadzania danych
1. Powstałe w wyniku upływu czasu 
1. Powstałe podczas przetwarzania danych
1. Wynikajce z fakt ze atrybutu czy polozenie obiektow w przestrzeni nie są pewne i mogą być określone jedynie z pewnym prawdopodobieństwem
### Obiekty słabo zdefiniowany - nieokreślony i niejednorodność.
##### Nieokreśloność:
* Własności- wynika z braku wyraźnych granic obiektu
* Atrybutów- wynika z braku jednoznacznych kryteriów klasyfikacji.- Teoria zbiorów rozmytych
#### Niejednorodność- problem przyporządkowania obiektu do określonej klasy w sytuacji gdy w systemach klasyfikacji występują różne kryteria służące do określenia tej samej klasy.
* Niezgodność -teoria Dempstera-Shafera(DST) i model danych częściowo wyspecyfikowany
* Niespecyficzność-teoria zbiorów rozmytych

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
1. Ekonometria przestrzenna - specyfikacja, estymacja i weryfikacja modeli uwzględniających aspekt przestrzenny.
2. Statystyka przestrzenna - opiera na się na analizie danych
### Trzy główne nurty metodologiczne w statystyce przestrzennej:
####  1.Analiza danych punktowych: 
##### W jaki sposób obiekty są rozmieszczane w przestrzeni:
 * losowo-(na rozmieszczenie nie wpływa żaden czynnik)
 * regularnie-(świadome rozmieszczenie obiektów w nienaturalny sposób)
 * klastrowo-( na rozmieszczeni wplywa czynnik)
##### Warunki konieczne do przeprowadzenia analizy danych punktowych:
1. Znajomość długości i szerokości współrzędnych geograficznych punktó nanoszonych na mapę
2. Wcześniejsze określenie powierzchni badanego obszaru
3. Dane punktowe powinny stanowić kompletny zbiór, a nie jedynie próbę
4. Istnienie rzeczywistej zależności między obiektami analizowane obszaru a punktami nanoszonymi na mapę
   
#### 2. Geostatystyka - optymalizacja szacowanych parametrów geologicznych
#### 3. Metody analizy danych obszarowych i i punktowych atrybutowych
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
1. Aproksymacja funkcji(regresja przestrzenna) dopasowującej do zbioru wejściowych danych przestrzennych zależności analitycznej wyrażonej wzorem matematycznym
2. Klasyfikacja, czyli przypisanie zaobserwowanych przypadków do określonej liczby klas kategorii reprezentowanych przez zmnienne wyjsciowe
3. Wykrywanie regularności istotnych cech w danych wejściowych bez znajomości wzorców

#### Statystyka przestrzenna opiera się na podejściu data driven
#### Ekonometria przestrzenna opiera się na podejściumodel driven 
# Rozdział trzeci: Dane przestrzenne-podstawowe zagadnienia
## 3.1 Klasyfikacja i własności danych przestrzennych
#### Cztery rodzaje danych przestrzennych wg Cressie:
1. Dane obszarowe - charakteryzujące się skokową zmniennościa- jest określony
2. Dane powierzchniowe- określane poprzez ciągłą zmienność na podstawie funkcji odległości- jest określony
3. Dane punktowe - reprezentują wartości zmiennych mające charakter punktów w przestrzeni georgaficznej- pole losowe
5. Obszary przestrzenne - wartości zmiennych mające charakter obiektów o określonym zasięgu przestrzennym- pole losowe
#### Efekty pierwszego rzędu - odnoszą się do zmian wartości średnej danej zmiennej w określonej przestrzeni. - Tradycyjna regresja
#### Efekty drugiego rzędu- odnoszą się do przestrzennych zależności pomiędzy jednostkami. Zachodzi efekt sąsiedztwa. - techniki analizy biorące pod uwagę kowiariancję w danych generujących efekty lokalne.
#### Współzależność przestrzenna - natężenie pewnych zjawisk przenosi się z obiektu na inne obszary sąsiednie. = Prawo Toblera = autokorelacja przestrzenna. 
#### Heterogeniczność przestrzenna(odwzorowanie stacjonarności w szeregach czasowych) - brak stałości struktur rozmieszcenia wartości badanych cech.
#### Błąd ekologiczny - różnica pomiędzy wartością statystyki dla pojedynczego obiektu estymowanej za pomocą zbiorowości, a wartością statystyki szacowanej na podstawie jednsotek.
#### Błąd atomistyczny - odwrotność błędu ekologicznego
#### Problem zmiennej jednsotki odniesienia - błąd wynikający z faktu, że zjawisko o charakterze punktowym jest analizowane za pomocą danych zagregowanych. - szczególny przypadek błedu ekologicznego.
### 3.1.1 Dane obszarowe
-miejsce na wzór strona 52!!!
#### Główne techniki analizy danych obszarowych:
1. Przestrzenna średnia ruchoma
2. Estymacja jądra
3. Przestrzenna autokorelacja
4. Przestrzenna korelacja i regresja
### 3.1.2 Dane powierzchniowe
nieskończona liczba lokazlizacji si
#### Główne techniki analizy danych powierzchniowych
* przestrzenna średnia ruchoma
* analizy trendu powierzchniowego
* teselacje
* tringulacja/TIN
* wariogram/kowariogram/kriging
* analiza czynnikowa
* analiza skupień
* analiza kanoniczna
### 3.1.3 Dane punktowe
Dane punktowe bezatrybutowe- mają przypisane tylko współrzędne geograficzne
### 3.1.4  Dane przestrzenno-czasowe 
Macierz geograficzna Berrego
## 3.2 Wybrane problemy związane z agregacją danych przestrzennych
#### Problemy analizy danych zagregowanych:
1. Błąd ekologiczny
2. Różnice w wartościach miar statystyki opisowej ze względu na sposób podziału przestrzeni na obszary.
#### Alternatywą dla uniknięcia powyższych problemów jest wnioskowanie z danych indywidualnych przy czym wtedy może pojawić się błąd atomistyczny.

### 3.2.1 Problem MAUP i błąd ekoloniczny
#### Problem MAUP można podzielć na dwa problemy:
* problem stosowanej w analizie skali/poziomu agregacji- w zależności jaki poziom agregacji danych zostanie wykorzystany wyniki analizy tego samego zjawiska będą się różnić   
* problem sposobu podziału przestrzeni - zmiana wyników analizy  w zależnści od sposobu podziału przestrzeni geograficznej na obszary w ramach takiego samego stopnia agregacji danych.
##### Przykład 3.1 Efekt zmiany poziomu agregacji przestrzennej danych
![IMG20240716142643](https://github.com/user-attachments/assets/69d927c2-a23c-4f08-a586-7a1f1e0f8754)
##### Obserwacje:
###### Wzrosrt poziomu agregacji danych powoduje:
- redukcje wielkość odchylenia standardowego
- wzrost współczynnika korelacji liniowej 
###### Wnioski:
Efekt MAUP związany z przestrzenną agregacją danych jest statystycznie istotny.

##### Przykład 3.2 Efekt zzmiany sposobu podziału przestrzeni geograficznej.
1000 elementów losowo rozłożoną w przestrzeni geograficznej, a przestrzeń tą podzielono na 6 różnych sposobów, tak, że każdy z nich odzwierciedla ten sam poziom agregacji przestrzennej danych oraz dzieli  zbiór respondentów w sposob rozłączny i wyczerpujący.
W każdym podziale liczba poligonów wynosi 20, natomiast ich geometria jest inna.

![IMG20240716142643](https://github.com/user-attachments/assets/1e360137-e4d9-4863-883d-9994321f75cc)
#### Wyniki:
![image](https://github.com/user-attachments/assets/a6b2f887-a96e-4b58-8cb9-3f5729e9b6c9)
Jak widać średnia oraz odchylenie standardowe nie różnią się w sposób istotny statystycznie, natomiast współczynnik korelacji różni się już w sposób istotny.

Nieloswy rozkład zjawiska w przestrzeni geograficznej możę skutkować istotnym statystycznie efektem agregacji i zmainy podziału przestrzeni.


MAUP może być traktowany jako szczegółny przypadek błędu ekologicznego. 
W MAUP:                W Błędzi ekologicznym
efekt skali/agregacji----> błąd agregacji
sposób podziału przestrzeni---> błąd specyfikacji

### 3.2.2. Błąd atomistyczny
