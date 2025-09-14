# Calendarize

-   Nositelj: doc. dr. sc. Nikola Tanković
-   Asistent: mag. inf. Luka Blašković
-   Kolegij: Raspodijeljeni sustavi
-   Studij: Diplomski stduij Računarstva
-   Student: Romeo Dombaj

----------

## Opis projekta

Calendarize je web aplikacija koja služi kao alat za rezerviranje termina. Nakon što admin izradi svoje termine, korisnici uz pomoć imena i emaila mogu rezervirati iste termine. Zadatak je bio stvoriti distributivni sustav, što ova aplikacija i prikazuje na način da povezuje više samostalnih mikroservisa koji se mogu skalirati ovisno o potrebama.

Aplikacija demonstrira kako se pomoću arhitekture mikroservisa može izgraditi skalabilan i fleksibilan sustav za rezervaciju termina. Korištenjem modernih tehnologija poput FastAPI-ja za backend, Reacta za frontend, DynamoDB-a za bazu podataka te NGINX-a kao reverse proxyja postignuta je modularnost i jednostavnije održavanje aplikacije.


## Tehnologije

-   **Frontend**: React
-   **Backend**: Python (FastAPI)
-   **Baza podataka**: DynamoDB


## Struktura sustava

Aplikacija se sastoji od pet servisa:
-   **main app service** – serviranje frontenda, gateway komunikacije frontenda
-   **user service** – registracija i autentikacija korisnika
-   **booking service** – upravljanje terminima (rezerviranje)
-   **notification service** – upravljanje obavijestima
-   **email service** – slanje i bilježenje e-mailova
