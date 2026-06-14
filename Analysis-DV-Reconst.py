import math #import biblio math

import numpy as np #import biblio dla wiekszych obliczen

#import matplotlib dla vizualizacji danych,oraz pyplota, modula dla bezposredniego kierowania wykresem
import matplotlib.pyplot as plt

#import cyfrowy projekt w ktorym pozniej zapiszemy przemiany stanu qubitu az do go pomiaru
from qiskit import QuantumCircuit

#import lokalnego silnika fizyki kwantowej (zastępuje fizyczny procesor IBM)
from qiskit_aer import AerSimulator



#wporadzenie nowej funkcji prawdop_na_kat ze zmienna (parametrem) prawdop_jedn,
#do ktorej pozniej beda przypisane wartosci prawdopodobienstwa, z ktorych potem bedziemy wyliczac kat
def prawdop_na_kat(prawdop_jedn):
    #korzystajac ze sfery Blocha oraz wzoru na przeliczenie kata obrotu wyrazonego w radianach,
    #majac prawdopodobienstwo(prawdop_jedn), przeksztalcamy standardowy wzor do wyszukiwania wektora dla bramki ry
    #ry - Rotation around Y-axis. ta bramka jest kluczowa,
    #poniewaz to ona przyjmuje kat wylacznie w radianach (od 0 do "pi"), i obraca wektor do gory (blizej zera)
    #lub do dolu (blizej jedynki) po "powierzchni sfery Blocha"
    #i akurat ten kat wskazuje prawdopodobienstwo czy qubit w czasie mierzenia bedzie zerem czy raczej jedynka
    return 2 * math.asin(math.sqrt(prawdop_jedn))
#range - funkcja generujaca liczby w zakresie (start from(zaczac od 5)) (loop until(zatrzymac sie przed 96)) (w takim kroku),
#lub w prostym parametrze range(start, stop, step)
#x/100.0 - musimy miec w liczby w postaci ulamkowej,
#poniewaz prawdopodobienstwo wyraza sie w ulamkach od 0.0 do 1.0, pelnych liczb byc nie moze
#petla for bierze liczbe z zakresu range i przypisuje ja tymczasowo do zmiennej x

#lista wszystkich mozliwych ulamkow (19)
prawdopodobienstwo = [x/100.0 for x in range(5, 96, 5)]

simulator = AerSimulator() #wlaczenie symulatora kwantowego
print("====== FAZA PIERWSZA: ANALIZA DANYCH ======")

#inicjalizacja zmiennych stanowych, pierwsza wartosc (0 lub 1) dla wektora K, a druga dla L,
#uwzgledniamy punkty skrajne (00 oraz 11) od ktorych zaleza stany 01 oraz 10
pozycja_max_wydajnosci = None #zmienna na wspolrzendne wektorow K i L,
#przy ktorych system wykazuje najwyzsza wydajnosc 00 (K i L dzialaja)
#wprowadzamy None, poniewaz na poczatku wartosc jest pusta, i jest tylko jak rezerwa miejsca,
# dopiero pojawia tam sie wartosci po uruchamieniu petli

#procentowy wynik dla stanu 00 w podanym punkcie wspolrzednych K i L
#przechowuje najwyzszy rekord, ktory sluzy jako punkt odniesienia do porownan, w instrukcji warunkowej if
wart_max_wydajnosci = -1

pozycja_max_obciazenia = None #zmienna na wspolrzendne wektorow K i L,
#przy ktorych system wykazuje najwyzsze obciazenie 11 (K i L nie dzialaja)

#procentowy wynik dla stanu 11 w podanym punkcie wspolrzednych K i L
#przechowuje najwyzszy rekord, ktory sluzy jako punkt odniesienia do porownan, w instrukcji warunkowej if
wart_max_obciazenia = -1

#ten pasywny rejestr wart_max_ otrzymuje maksymalne prawdopodobienstwo wystapienia 00 lub 11 (w zaleznosci od rejestru)
#w pewnym punkcie, a potem porownuje kolejne wartosci do tej ktora juz jest przechowywana w rejestrze, zeby
#odnalezc najwieksza, zaczynamy od -1 ze wzgledu na charakter wartosci (od 0% do 100%)

licznik_stanow_granicznych = 0 #licznik dni o w ktorych wydajnosc (prawdopodobienstwo o stan 00) wynosi okolo 50%

#rejestry dla wspolrzednych wektorow K i L oraz je cztery stany, 00, 01, 10, 11

K_wspolrzedna = []
L_wspolrzedna = []
#w kazdym rejestrze stanow po obliczeniu procentow, bedziemy korzystali z tych wartosci
#zeby wskazac nasycenie kropek na wykresie koncowym
stan_00 = []
stan_01 = []
stan_10 = []
stan_11 = []

#*zmienna iteracyjna - zmienia swoja wartosc przy kazdym powtorzeniu petli for
#dopoki petla nie dobiegnie konca, pozostaje ze swoja wartoscia
for K_prawdop in prawdopodobienstwo: #wprowadzenie zmiennej iteracyjnej przez wyzej zaznaczona liste 19 ulamkow
    for L_prawdop in prawdopodobienstwo: #petla wewnatrz zewnetrznej petli K
        #dla kazdej wartosci K_prawdop, L_prawdop przechodzi przez caly rejestr prawdopodobienstwo
        #z tego wynika ze dla kazdej z 19 wartosci K_prawdop, istnieja 19 wartosci L_prawdop
        #wiec 19*19 = 361 wynik
        circuit = QuantumCircuit(2, 2) #wprowadzenie matrycy z dwoma kubitami i bitami
        #dla kazdego z 361 wynikow, za kazdym iterowaniem czyszcac obwody zeby one sie nie mieszaly
        #wskazakismy tez twa tory, dla K i dla L

        # prawdop_na_kat(K_prawdop) wziety ulamek ze zmiennej K_prawdop, jest zmieniany przez funkcje prawdop_na_kat
        # i przeksztalcony ze zwyklej liczby dziesietnej na radiany (sfera Blocha)
        # circuit.ry(), ry, rotation along the y-axis znaczy ze kat 0, oznacza wychylenie pionowe zero,
        # wiec kubit sto procent wynosi 0, a jezeli kat wychylenia np. 2, to znaczy ze prawdopodobienstwo
        # zostalo "obrocono" o 2 radiany od gory w dol
        # O i 1 na koncu uwazano za dwa rownolegle tory wskazane jeszcze w circuit, sa niezalezne w pewnej mierze
        # i dlatego wprowadzane sa osobnie, 0 i 1 sa wylacznie tylko dla tego zeby wskazac,
        # ze te obliczenia katow w radianach sa rozne i zachodza w roznych przestrzeniach
        circuit.ry(prawdop_na_kat(K_prawdop), 0)
        circuit.ry(prawdop_na_kat(L_prawdop), 1)


        #moment w ktorym przepisujemy kubit, jako bit zwykly, dla toru pierwszego K
        #zarowno jak dla toru drugiego L
        circuit.measure(0, 0)
        circuit.measure(1, 1)

        shots = 100000 #ilosc prob na kazdy dowolny punkt,
        #sprawdzajac prawdopodobienstwo wystapienia 00, 01, 10, 11 w kazdym z 361 punktow

        #simulator.run() - to fukcja ktora uruchamia obwod circuit "shots" razy,
        #i wykonuje symulacje "shots" razy dla kazdego z 361 punktow
        #zapisujemy .result() na koncu zeby fizyczna pamiec Ram miala czas na spokojne przeliczenie
        #wszystkich wartosci, poniewaz jezeli usuniemy to .result() to,
        #simulator.run(circuit, shots=shots), ta linia ktora wykonuje sie w nanosekundzie,
        #(to znaczy ze python momentalnie ja uruchamia do C++) nie bedzie mogla fizycznie
        #przejsc przez wszystkie 100000 shots w jedna nanosekunde w ktorej python uruchomil ta funkcje
        #wiec czekamy dopoki RAM pamiec fizycznie zachowa wszystkie te 100000 shots dla kazdego z 361 punktow
        wynik = simulator.run(circuit, shots=shots).result()

        counts = wynik.get_counts() #.get_counts() to sorter,
        #ktory liczy ile z 100000 razy wystapily stany 00, 01, 10, 11 w calym obwodzie wynik
        #nawiasy sa potrzebne dla dodatkowych instrukcji
        #a samo .get_counts() jest metoda obiektowa, ktora bedzie obslugiwac
        #surowe dane z obiektu wynik.

        #counts.get(00, 0) - znaczy ze ta funkcja szuka ilosci wystapien stanu '00',
        #a jesli go nie znajdzie to wpisuje zero, ze np, ani razu nie wystapil stan 00
        #na wszystkie 100000 obliczen (to tez moze sie zdarzyc)
        #sama w sobie metoda .get() wyciaga szukane wartosci, i jest metoda obiektowa
        #zatym dzielimy ilosc tych stanow przez ilosc wszystkich stanow 100000
        #w taki prosob uzyskujemy potrzebny ulamek ktory potem mnozymy razy 100 zeby uzyskac procenty
        #koncowy typ liczby - zmiennopozycyjny (n.p. 90.3; 15.6)
        p_00 = (counts.get('00', 0) / shots) * 100
        p_01 = (counts.get('01', 0) / shots) * 100
        p_10 = (counts.get('10', 0) / shots) * 100
        p_11 = (counts.get('11', 0) / shots) * 100

        #teraz wypelniamy puste listy K_wspolrzedna = [], L_wspolrzedna = [],
        # stan_00 = [], stan_01 = [], stan_10 = [], stan_11 = []
        #.append() to metoda ktora bierze wartosc aktualnej zmiennej K_prawdop z loopu for
        #i zapisuje ja na koniec (na poczatku pustej) listy K_wspolrzedna = []

        #potrzebujemy te listy(!) dla rysowania czterech wykresow,  dziala to tak:
        #matplotlib bierze wspolrzedne x(k) i y(l) i potem np.  do wykresu 00
        #przsypisuje kropke o takim nasyceniu o jakim jest prawdopodobienstwo wywolania stanu 00
        #akurat w tych wspolrzednych wsrod wszystkich 100000 prob ktore zostaly zrobione
        #dla kazdej kropki (kombinacji) x (k) i y (l), kropek takich, w kazdym z
        #czterech wykresow bedzie 361
        K_wspolrzedna.append(K_prawdop)
        L_wspolrzedna.append(L_prawdop) #dla L to samo

        # to samo robimy tez dla list z wartosciami 00 i t.p.
        # tylko musimy z powrotem podzielic przez setke, zeby uzyskac ulamek
        # i pozniej wykorzystac to dla wskazania nasycenia kropek na wykresie
        stan_00.append(p_00 / 100)
        stan_01.append(p_01 / 100)
        stan_10.append(p_10 / 100)
        stan_11.append(p_11 / 100)

        #teraz wypisujemy wszystkie te wyniki (procenty (prawdopodobienstwa stanow) dla kazdego punktu),
        #robimy je widoczne dla lepszego zrozumienia zachowania danych
        #uzywamy f-stringa ktory wskazuje ze w cudzyslowach beda nie tylko slowa ale i zmienne,
        #ktore beda sie zmienialy przy kazdym wydruku danych
        #{K_prawdop} bierzemy zmienna K_prawdop (wspolrzedne wektoru K) i
        #{K_prawdop:.2f} oznacza ze mozemy zapisac liczbe wylacznie na dwa miejsca po przecinku
        #f to skrot do float, ktory pozwala na zapisania liczb dziesietnych i t.p.
        #{p_00:5.1f}, bierzemy prawdobopobienstwo stanu 00 i
        #wyswietlamy liczbe z jednym miejscem po przecinku
        #oraz rezerwujemy dla tego wyniku 5 miejsc zeby tabela wygladala lakonicznie
        #i nie rozjechala sie w przypadku kiedy wystapi 0.3% dla jednego ukladu wspolrzednych
        #a dla drugiego 10.5%
        print(f"Wektory: K - {K_prawdop:.2f} | L - {L_prawdop:.2f} |"
              f" 00: {p_00:5.1f}% | "
              f" 01: {p_01:5.1f}% | "
              f" 10: {p_10:5.1f}% | "
              f" 11: {p_11:5.1f}% | ")

        #oto teraz tu wprowadzamy dwie petly if zeby odnalezc:
        #gdzie (na ktorych wspolrzednych x (k - K_wspolrzedna) i y (l - L_wspolrzedna))
        #i o ile (jakie najwyzsze prawdopodobienstwo) bedzie najwyzsza (00) oraz najgorsza (11) wydajnosc systemu
        #dla obu wektorow
        #ten loop if za kazdym razem strawdza czy nowa liczba jest wieksza od starej
        #na poczatku wart_max_wydajnosci jest -1, wiec program ruszy
        #wartosci p_## (n.p. 0.00 (punkt skrajny)) sa mniejsze od 1 ale wieksze od -1, dlatego musielismy zapisac -1
        #zeby wyeliminowac jakiekolwiek zaburzenie w przypadku uzyskania 0.00
        if p_00 > wart_max_wydajnosci:
            wart_max_wydajnosci = p_00 #przypisujemy nowa wartosc, zamiast starej
            pozycja_max_wydajnosci = (K_prawdop, L_prawdop) #zapisujemy to
            #gdzie uzyskalismy ta nowa wartosc

        #to samo robimy dla drugiego punktu skrajnego - 11
        #notatka: K_prawdop to pojedyncza wartosc, a K_wspolrzedna - to cala lista wszystkich wspolrzednych
        #(nazwy sa troche mylace, moj blad)

        if p_11 > wart_max_obciazenia:
            wart_max_obciazenia = p_11
            pozycja_max_obciazenia = (K_prawdop, L_prawdop)

        #wprowadzamy punkty_graniczne, gdzie szansa na stan 00 jest niemal taka sama jak na stan 11

        if 45.0 <= p_00 <= 55.0:
            licznik_stanow_granicznych += 1 #przy pojawieniu takiego stanu,
            #licznik rosnie o jeden

print ("====== FAZA DRUGA: PODSUMOWANIE ANALIZY DANYCH ======")
#len() - dlugosc listy; napisalismy prawdopodobienstwo dwa razy
#poniewaz mamy dwa wektory i dla kazdego scenariusza sa dwa wektory
print(f"Liczba przeanalizowanych scenariuszy: {len(prawdopodobienstwo) * len(prawdopodobienstwo)} scenariuszy")
#.1f piszemy ze wzgledu na utrate precyzji liczb zmiennopozycyjnych
#zeby nie bylo czegos takiego jak 29.300000000001%, a 29.3%
print(f"Maksymalna wydajnosc systemu - stan(00): {wart_max_wydajnosci:.1f}% w wektorach K/L: {pozycja_max_wydajnosci}")
print(f"Maksymalne obciazenie systemu - stan(11): {wart_max_obciazenia:.1f}% w wektorach K/L: {pozycja_max_obciazenia}")
print(f"Suma stanow granicznych: {licznik_stanow_granicznych}")
print("------------------------------------------------------------------")

#\n - linija odstepu
print("\nGeneruja sie Wykresy... Sprawdz wyskakujace okno")

#fig - figura, axes - wykresy;
#subplots (2, 2), jak w matryce, najpierw liczba rzedow (nrows), a potem liczba kolumn (ncols)
#to wskazuje ze bedziemy mieli caly dashboard podzielony na (2*2) cztery czesci
#1 - ile cwiartek, 2 - jakiego rozmiaru, plt.subplots zwraca dwie wartosci
#figsize=(12, 11) - rozmiar wyskakujacego okna, ktore potem dzielimy na 4
#plt.subplots - funkcja ktora naraz zwraca dwie wartosci, wiec mamy dwie zmienne ze spacja
fig, axes = plt.subplots(2, 2, figsize=(12, 11))

#axes[0, 0] - pracujemy z wykresem w gornej lewej czesci (jak w matryce)
#rzad zerowy, kolumna zerowa
#.scatter() - rysujemy kropki, w tym:
#przekazujemy dla kazdej kropki wspolrzedne (K/L_wspolrzedna), color, nasycenie (lista - stan_00), wielkosc, kontur
axes[0, 0].scatter(K_wspolrzedna, L_wspolrzedna, c='green', s=45, alpha=stan_00)
#.set_title/x/ylabel - podpisy dla czytelnosci wykresu
axes[0, 0].set_title("Wykres 00. Wyniki prawdopodobienstwa")
axes[0, 0].set_xlabel("Operational Factor K")
axes[0, 0].set_ylabel("Operational Factor L")
#.grid - siatka kropkowa ':' na tle wykresu, o przezroczystosci 0.5
axes[0, 0].grid(True, linestyle=':', alpha=0.5)

axes[0, 1].scatter(K_wspolrzedna, L_wspolrzedna, c='orange', s=45, alpha=stan_01)
axes[0, 1].set_title("Wykres 01. Wyniki prawdopodobienstwa")
axes[0, 1].set_xlabel("Operational Factor K")
axes[0, 1].set_ylabel("Operational Factor L")
axes[0, 1].grid(True, linestyle=':', alpha=0.5)

axes[1, 0].scatter(K_wspolrzedna, L_wspolrzedna, c='blue', s=45, alpha=stan_10)
axes[1, 0].set_title("Wykres 10. Wyniki prawdopodobienstwa")
axes[1, 0].set_xlabel("Operational Factor K")
axes[1, 0].set_ylabel("Operational Factor L")
axes[1, 0].grid(True, linestyle=':', alpha=0.5)

axes[1, 1].scatter(K_wspolrzedna, L_wspolrzedna, c='red', s=45, alpha=stan_11)
axes[1, 1].set_title("Wykres 11. Wyniki prawdopodobienstwa")
axes[1, 1].set_xlabel("Operational Factor K")
axes[1, 1].set_ylabel("Operational Factor L")
axes[1, 1].grid(True, linestyle=':', alpha=0.5)

plt.tight_layout() #zeby wykresy jeden na drugi nie najechal, i wygladaly elegansko
plt.show() #wyswietl wykres


























