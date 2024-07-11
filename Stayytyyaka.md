# Rozdział pierwszy: Wprowadzenie do statystyki przestrzennej.

1.1 Metody analiz przestrzennych- podstawowe definicje i pojęcia
Analizy przestrzenne:
Analizy pionowe- różne informacje, ten sam obszar
Analizy poziome- ta sama informacja, inne obszary


Zapytanie do bazy
Pomiaru
Przekształcenia: Buforowanie i ponowna klasyfikacja wg atrybutów

Interpolacja przesztrzenna- ma na celu okresleni wartosci pewenj w zmiennej w punkcie w którym ona nie była mierzona
1.2 Informacje przestrzenne- klasyfikacja, pomiar zmiennych
Pytania najczęściej zadawane przez badaczy dotyczą:
charakteru występowania zjawiska tzn ustalenia czy dane zjawisko ma w przestrzeni charakter regularny, losowy lub klastrowy.
prawidłowości przestrzennych wykazywanych przez obiekty lub zjawiska
rozproszenia lub skupienia podobnych wartości badanej zmiennej 
skorelowanie badanej zmiennej  z innymi zmiennymi na danym obszarze
niezależności różnych wartości zmiennej, ,, przyciągania się” lub ,,odpychania się” podobnych wartości zmiennej badanej 
zmian w przestrzennym rozkładzie zmiennych
Dane zlokalizowane:
zbiór znaków 
zbiór słów
Dane Statystyczne:
Klasyfikacja wg źródeł informacji
informacje naturalne(geograficzne)
Dane geograficzne:
Dane rastrowe- opisane za pomocą siatki 
Dane wektorowe - opisane za pomocą współrzędnych
społeczno ekonomiczne
Dane infrastrukturalne - łączą dane geograficzne i społeczno ekonomiczne, najczęściej są to informacje o wielkości i położeniu obiektów w postaci infrastruktury( np rzeki,kanały drogi)
Klasyfikacja wg typów informacji
informacje otrzymane na podstawie różnego rodzaju pomiarów topograficznych:
Dane powierzchniowe - ciągła zmienność informacji otrzymywana na podstawie ocen i informacji przestrzennych gromadzonych w terenie.- metoda interpolacji obszarowej
Dane obszarowe- dane dyskretne - pochodzą z pewnej powierzchni geograficznej dla badanych obiektów, wykazują autokorelacja przestrzenna i heterogeniczności.
Dane punktowe - odnoszą się do badanych zjawisk, które się zrealizowały. Mają tendencję do tworzenia skupisk dlatego trzeba je testować. 
Dane przestrzenno- czasowe- wykorzystują dane o wymiarze czasowym i przestrzennym.

Rodzaje metryk:

Przestrzeń euklidesowa- umożliwia dobre przybliżenie odległości przestrzennych w przypadku dużych wielkości. Płaskość wyznaczanych odległości.
na układzie współrzędnych 


Metryka manhattan:

Metryka sferyczna:


1.3 Jakość danych przestrzennych

Siedem cech dotyczących jakości danych przestrzennych:
pochodzenie- skąd pochodzą dane, kiedy zostały pozyskane i jak?
zgodność- brak wewnętrznej sprzeczności
kompleksowość- spełnienia przez zbiór danych deklarowanych wytycznych
dokładność semantyczna- wyraża wierności z jaką zbiór danych odpowiadający przyjętemu modelowi danych przestrzennych odtwarza dziedzinę problemu
dokładność czasowa- aktualność danych do wymagań
dokładność pozycyjna-dokładność współrzędnych punktów
dokładność atrybutu-prawidłowość określenia atrybutów

1,4 Niepewność w danych przestrzennych

Głównym źródłem niepewności jest sposób zdefiniowania badanych obiektów w przestrzeni.

Dobrze zdefiniowany obiekt - możno go wydzielić z innych obiektów.

Rodzaje błędów niepewności przy dobrze zdefiniowanym obiekcie:
pomiarowe
klasyfikacji
wynikające z generalizacji przestrzeni
popełniane podczas wprowadzania danych
powstałe w wyniku upływu czasu 
powstałe podczas przetwarzania danych
wynikajce z fakt ze atrybutu czy polozenie obiektow w przestrzeni nie są pewne i mogą być określone jedynie z pewnym prawdopodobieństwem
Obiekty słabo zdefiniowany - nieokreślony i niejednorodność.
Nieokreśloność:
własności- wynika z braku wyraźnych granic obiektu
atrybutów- wynika z braku jednoznacznych kryteriów klasyfikacji.- Teoria zbiorów rozmytych
Niejednorodność- problem przyporządkowania obiektu do określonej klasy w sytuacji gdy w systemach klasyfikacji występują różne kryteria służące do określenia tej samej klasy.
niezgodność -teoria Dempstera-Shafera(DST) i model danych częściowo wyspecyfikowany
niespecyficzność-teoria zbiorów rozmytych

1.5 Reprezentatywności próby w badaniach przestrzennych.

Próba reprezentatywna powinna spełniać:
Nieobecność czynników selektywnych- brak stronniczej selekcji, rozwiązanie: losowy dobór jednostek do próby.
Miniatura populacji generalnej- rozkład cech stanowi idealne odwzorowanie rozkładu cech w populacji.
Typowość– wysoka częstość występowania pewnych cech w badanej populacji.
Pokrycie różnorodności populacji-  włączenie do próbki przedstawicieli wszystkich podgrup.
Metody pobierania próbki losowej:
Metoda dobór prostej próby losowej
Metoda warstwowa próba losowa 
Metoda próba systematyczna 
Metoda warstwowej, systematycznej próby nieliniowej



