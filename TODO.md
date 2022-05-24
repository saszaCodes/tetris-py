1. Szkielet serwera
   - wielowątkowy
   - obsługa wysyłania - wystawiona funkcja pozwalająca wysyłać z określoną częstotliwością (NOPE, to jednak na wyższym poziomie)
   - dodatkowo funkcja pozwalająca przestać wysyłać
   - dodatkowo może funkcja pozwalająca wysłać x razy + częstotliwość?
   - jak vsmp - obsługa udp pod spodem, osobno obsługa na poziomie pakietów
   - timeout będzie w górnej warstwie robiony
   - na razie niech printuje wszystko co przychodzi
2. Parser pakietów w obie strony
3. Serwer potrafi obsłużyć (wystawić na wyższy poziom oraz zarządzić na wyższym poziomie, w tym wysyłaniem z różną częstotliwością) pakiety
4. Klient potrafi obsłużyć pakiety
5. Klient obsługuje pakiety po kliknięciu guzika
6. Parser potrafi obsłużyć dane gry


7. Podział main na tetris_engine, engine_loops, engine_engine_sounds, engine_blocks, tetris_utils
8. Zmiana na dictionary w constants
9. Podział socket_handlera (parsera?) na common, client i server
10. Serwer ma nie rozumieć danych gry
11. Parser umie przetłumaczyć obiekt game data na tablicę tablic
12. Klient potrafi obsłużyć dane 
13. Wysyłanie i odbieranie danych przez klienta


### PYTANIA
1. Co to `scapy`, chyba coś ciekawego