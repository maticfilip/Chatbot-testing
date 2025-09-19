# Testiranje učinkovitosti i točnosti chatbota  
**Za Raiffesein Bank testiranje, pozicija Junior developer za chatbot tim**  
*Filip Matić*  

---

## Uvod  

Testiranje se provodi u svrhu provjeravanja točnosti prepoznavanja namjere korisnika (*intent*) na osnovu njegovog upita, odnosno unosa korisnika. Testiranjem su provjerene osnovne metrike poput **točnosti** (omjer točnih odgovora i ukupnog broja pitanja) i **povjerenja modela (confidence)**.  

Chatbot za testiranje ima **10 namjera** (*intenta*), koje bi trebao prepoznati iz korisničkog upita.  

Intenti:  
- `radno_vrijeme`  
- `ulaznice`  
- `adresa`  
- `danas_izložbe`  
- `kafic`  
- `toaleti`  
- `pristupacnost`  
- `parking`  
- `clanstvo`  
- `kontakt`  

Za svaki intent su predloženi primjeri za koje bi chatbot trebao sigurno pogoditi namjeru, odnosno odgovor. Za svaki intent postoji samo jedan točan odgovor.  

---

## Okruženje  

Testiranje je provedeno lokalno, u **Python virtualnom okruženju** napravljenom na temelju priložene `.env.example` datoteke.  

Za testiranje je pripremljeno **92 test case-a**. Test caseovi su napisani tako da testiraju sposobnost prepoznati točan intent u uvjetima kada upiti nisu optimalno napisani, odnosno da simuliraju svakodnevnu situaciju gdje korisnik ne zna kako treba optimalno formulirati pitanje za unos.  

Napisani test caseovi su priloženi uz izvještaj, a njihova namjera je bila testirati različite vrste upita:  
- Točni upiti  
- Upiti s neformalnim govorom  
- Upiti s greškama u tipkanju  
- Upiti s gramatičkim/pravopisnim greškama  
- Upiti bez specijalnih znakova č,ć,š,ž,đ  

---

## Testni slučajevi  

Za svaki test case je poslan upit API-u, te su iz njegovog odgovora izvučeni podaci potrebni za testiranje točnosti chatbota.  

Primjer formata testnog slučaja:  

test_ID | unos | ocekivani_intent
T1 | "Koje radno vrijeme?" | radno_vrijeme
T2 | "Kad radite?" | radno_vrijeme


Osim sposobnosti bota da prepozna intent, napisani upiti su zamišljeni tako da ispitaju sljedeće sposobnosti:  
- Jezična varijabilnost  
- Kontekstualno razumijevanje  
- Fallback odgovore  
- Ponašanje u slučaju negativnih testova  

Za testiranje su ponuđene dvije opcije: **Selenium** i **REST**.  
- Selenium je opcija koja može pokriti više sadržaja i brže to uraditi.  
- REST je odabran jer je prikladniji za **programerski pristup** i kodersku prirodu pozicije.  

---

## Korištene funkcije  

Kod je pisan u lokalnom Python virtualnom okruženju, koristeći **REST API**.  

Osnovne funkcije:  
- Čitanje CSV testnih slučajeva  
- Slanje poruka API-u  
- Provjera rezultata  
- Izračun statistike  
- Spremanje rezultata u CSV  

Korištene datoteke:  
- `test_cases.csv` → svi upiti za testiranje  
- `tocni_odgovori.csv` → upiti priloženi uz popis namjera, korišteni za računanje prosjeka i mediana *confidence-a*  

---

## Rezultati  

Cijeli kod se vrtio 3 minute i 53 sekunde, što je posljedica prolazaka kroz sve upite za testiranje iz dvije tablice.  

Što se tiče podataka iz **tocni_odgovori**, prosjek i median su dosta niski.  
- Median confidence = **0.2**  
- Prosjek = **0.13**  

Za daljnju klasifikaciju testnih upita korišten je median confidence.  

Od 92 testnih upita, njih 54 je zadovoljilo, odnosno točno pogodilo namjeru korisnika, što nam daje **__% točnosti**.  

👉 Unatoč niskom median confidence-u, čak 81 upit je ispod mediana, ali dio njih i dalje daje točan intent.  
👉 43 upita (tj. 46.7%) imaju nizak prag sigurnosti, ali svejedno pogađaju točan intent.  

➡️ Zaključak: **razina confidence-a nije bila metrika koju smo mogli uzeti u obzir za točnost klasifikacije.**  
Točnost je određena isključivo usporedbom točnog i predviđenog intenta.  

---

## Analiza rezultata  

Pregledom **38 pogrešnih predviđanja**, greške se mogu podijeliti na:  

1. **Jezična varijabilnost** – bot ne prepoznaje strane jezike ni neformalne uvedenice.  
2. **Greške u unosu** – tipfeleri često stvaraju probleme (5/10 primjera nije prepoznato).  
3. **Neformalni govor** – problemi kod nejasnih izraza (npr. “U koliko otvarate?” → bot misli da je riječ o cijenama).  
4. **Dvosmislenost pitanja** – npr. “Koliko je za parking?” → bot to klasificira kao cijene ulaznica.  
5. **Upiti bez specijalnih znakova** – uglavnom prepoznaje, ali gubi kod ključnih riječi (npr. “izlozbe”).  
6. **Fallback** – bot nema fallback opciju; odgovara nečim nevezanim umjesto generičnim odgovorom tipa: *“Nisam Vas razumio, molim ponovite pitanje.”*  
7. **Kontekstualno razumijevanje** – bot ne pamti prošla pitanja. Npr.:  
   - Pitanje: “Imate li parking?” → točno.  
   - Sljedeće: “Koliko košta?” → pogrešno, misli na ulaznice.  

---

## Zaključak  

Postoji više slabih strana bota na kojima bi se trebalo/moglo poraditi:  
- Dodatno treniranje modela za prepoznavanje ključnih riječi i konteksta.  
- Bilingualnost (npr. hrvatski + engleski) zbog turista.  
- **Fallback odgovori**: jednostavna implementacija generičnog odgovora ispod određenog praga sigurnosti.  
- **Kontekstualno razumijevanje**: dodavanje memorije konverzacije ili RNN/LSTM modela koji pamte niz pitanja.  

Rekurentne neuronske mreže (RNN/LSTM) često se koriste kod botova s LLM-ovima jer mogu obraditi cijelu povijest razgovora u stvarnom vremenu.  

---
