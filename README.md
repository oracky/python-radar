# Projekt z Fizyki Ogólnej - Michał Oracki
# Radar
## Instrukcja uruchomienia 
<br/>

1. Utworzyć wirtualne środowisko: 

```bash
python -m venv venv
```

2. Aktywacja środowiska wirtualnego: 

Windows:
```bash
venv\Scripts\activate
``` 
Linux:
```bash
source venv/bin/activate
``` 
3. Instalacja wymaganych bibliotek (arcade): 
```bash
pip install -r requirements.txt
``` 
4. Uruchomienie programu: 
```bash
python main.py
``` 
<br/>

## Opis
<br/>
Projekt testowany na Windowsie, Python 3.10, wersja biblioteki arcade: 2.6.15
<br/>
Program symuluje działanie radaru. Radar wykrywa obiekty znajdujące się w jego obszarze działania. Reszta obiektów oraz ich poruszanie się na żywo można podglądać na minimapie w dolnym prawym rogu. Program umożliwia konfigurację radaru oraz obiektów na mapie.  
<br/>
<br/>

### Dodanie nowych obiektów na mapę
W celu dodania nowych obiektów należy użyć suwaka z napisem ```Number of objects``` (wartości od 0 do 20) i wybrać ilość obiektów do wygenerowania, a następnie nacisnąć przycisk ```Generate new moving objects```. 

<br/>

### Zmiana prędkości radaru 
W celu zmiany prędkości radaru należy użyć suwaka z napisem ```Radar speed``` (wartości od 0 do 100%, gdzie 50% to przeskalowana domyślna wartość z configu - plik simulation/config.py). 

<br/>

### Zmiana prędkości obiektów
W celu zmiany prędkości obiektów należy użyć suwaka z napisem ```Objects speed``` (wartości od 0 do 100%, gdzie 50% to przeskalowana domyślna wartość z configu - plik simulation/config.py). 

<br/>

### Zmiana kąta obserwacji radaru
W celu zmiany kąta obserwacji radaru należy użyć suwaka z napisem ```Radar range``` (wartości od 0 do 100%, gdzie 50% to przeskalowana domyślna wartość z configu - plik simulation/config.py).

<br/>

### Niestandardowe zmiany 
W celu innych niestandardowych zmian należy zmodyfikować plik konfiguracyjny - simulation/config.py.
