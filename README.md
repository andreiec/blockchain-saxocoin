## Introducere

Saxocoin-ul este o criptomonedă dezvoltată pe propriul Blockchain realizat în Python (Flask + MySQL). Implementarea acestuia este una relativ simplă întrucât arhitectura este reprezentată de nimic mai mult decât de 2 clase (Block și Blockchain) și o platforma web pentru a realiza tranzacții și a cumpăra moneda (plus integrarea procesului de minat și hashing).


## Clasele

Pentru realizarea aplicației am folosit 2 clase de bază - Block și Blockchain.

### Clasa Block

Această clasă are 4 variabile (data, number, previous_hash și nounce) și o singură metodă (hash), care returnează hash-ul block-ului.

- “Data” reprezintă conținutul Block-ului (în cazul acesta tranzacția de sub forma “sender>receiver>amount”, ex. “andrei>liviu>10”)
- “Number” reprezintă numărul de ordine al block-ului în chain
- “Prevoius_hash” reprezintă hash-ul block-ului de dinainte
- “Nounce” reprezintă un număr “random” ce are ca scop facilitarea mineritului astfel încât hash-ul să conțină un număr minim de zerouri


### Clasa Blockchain

Această clasă are două variabile (difficulty și chain) și 4 singură metode (add, remove, mine, checkvalid).

- Variabila “difficulty” reglementează numărul de zerouri necesari pe care hash-ul unui block trebuie să le aibă astfel încât el să fie valid.
- Variabila “chain” reprezintă nimic mai mult decât lista de block-uri din blockchain
- Metodele “add” și “remove” sunt destul de self explanatory
- Metoda “mine” primește un block drept argument și iterează prin diverse “nounce” pentru a putea găsi un hash care să fie cel puțin egal cu dificultatea.
- Metoda “checkvalid” verifică hash-urile fiecărui block din chain și spune dacă blockchainul este valid sau nu.


## Tranzacții

Tranzacțiile dintre utilizatori sunt realizate prin crearea unui Block cu datele aferente sub formatul “user1>user2>amount”, după care, programul minează acel Block pentru a-l putea valida și a-l putea salva în baza de date (funcțiile aferente sunt ‘send_coins’ și ‘transfer’. Astfel, balanța unui utilizator este realizată prin iterarea tuturor block-urile, iar daca utilizatorul este la stânga primului “>” din datele block-ului înseamnă că trebuie scăzut din balanță valoarea și vice-versa dacă se află la dreapta primului “>”.


## Minat

Minatul este realizat de către back-end prin algoritmul de hash-ing SHA256 care generează un hash de 64 valori. Procesul de minat este influențat de dificultatea blockchain-ul deoarece un blockchain cu o dificultate mai mare necesită mai multă putere de computație pentru a găsi un hash cu zerourile necesare.
Funcția care se ocupa de mining se numește “mine”, aferentă clasei Blockchain. Această funcție operează pe un “while True” până când un hash valid este găsit (schimbând de fiecare dată nounce-ul).


## Comunicarea cu baza de date

Comunicarea cu tabelele create în MySQL este realizată prin câteva funcții ajutătoare din fișierul “sqlhelpers.py”. Aceste funcții mimează operațiile de CRUD pentru a nu încurca cod de Python cu cod de SQL.
