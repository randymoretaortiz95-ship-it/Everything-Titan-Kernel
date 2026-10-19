# Everything Titan Kernel: Verificatore Fisico e 28 Principi di Progetto

**Titan Research Labs** · Release V2.0 (revisione tecnica, ottobre 2026) · Licenza MIT

Uno strumento aperto e gratuito per controllare in pochi secondi se un calcolo è coerente con la fisica, e una raccolta di 28 principi di progetto con lo stato di verifica dichiarato per ciascuno.

## A cosa serve
Molte decisioni su ambiente, agricoltura, salute e infrastrutture partono da un calcolo. Un errore di unità o un bilancio che non torna è facile da evitare se lo si controlla subito. Il **Verificatore Fisico** (`index.html`) fa tre controlli, interamente nel tuo browser, senza installare nulla e senza che i dati lascino il tuo dispositivo:

1. **Coerenza dimensionale:** le unità di un'equazione tornano? (SI: m, kg, s, A, K, mol, cd)
2. **Bilancio di conservazione:** ingressi, uscite e accumulo di massa o energia tornano entro una tolleranza ε?
3. **Plausibilità fisica:** rendimenti ≤ 100%, temperature sopra lo zero assoluto, probabilità tra 0 e 1, grandezze non negative.

È un controllo di buon senso: serve a trovare errori evitabili, non a dimostrare che un risultato sia corretto. È disponibile in italiano, inglese e spagnolo.

## Perché esiste
L'obiettivo è modesto e concreto: rendere più accessibile il ragionamento quantitativo e ridurre gli errori evitabili nei calcoli che informano decisioni su ambiente, agricoltura, sostenibilità e infrastrutture. La speranza è che altre persone lo usino, lo critichino e lo migliorino.

## Per chi è
- **Studenti e docenti** di fisica, ingegneria e scienze ambientali: per verificare esercizi e costruire esempi didattici.
- **Ingegneri, tecnici, agronomi e tecnici ambientali:** per un controllo preliminare di unità e bilanci (acqua, umidità, flussi, energia) prima di un dimensionamento.
- **Ricercatori e sviluppatori di modelli e simulazioni:** per rivedere i 28 principi, estendere i test e proporre correzioni.
- **Chi usa assistenti AI per calcoli e programmazione:** un controllo a valle, indipendente dall'AI, sulle grandezze fisiche prodotte.
- **Laboratori, aziende e persone interessate a collaborare:** per validare i modelli con dati reali (sensori, serre, magazzini, impianti).
- **Ambito sanitario:** i modelli di questo repository non sono strumenti clinici. Qualunque uso in sanità richiede partner clinici e validazione.

## Cosa contiene
| Percorso | Contenuto |
|---|---|
| `index.html` | Verificatore Fisico (IT/EN/ES), pagina unica senza dipendenze |
| `kernel/versione_corretta_28_principi.txt` | I 28 principi: formula, nota e stato |
| `kernel/titan_kernel_28.json` | Gli stessi dati in forma strutturata |
| `benchmarks/verifica_numerica_kernel.py` | Verifica numerica di 15 principi (NumPy, zlib) |

## Come provarlo
- **Online:** apri la pagina pubblicata con GitHub Pages (vedi il link nel riquadro "About" del repository).
- **In locale:** scarica `index.html` e aprilo nel browser.
- **Benchmark:** `pip install numpy` e poi `python benchmarks/verifica_numerica_kernel.py`.

## Stato di verifica e limiti
Nessuna voce è stata validata con dati sperimentali. Gli stati sono: *Noto* (risultato standard), *Modello* (relazione empirica da tarare), *Corretto* (enunciato originale rettificato), *Da validare* (ipotesi non ancora verificata). Quindici principi sono stati controllati numericamente; la voce 27 è illustrata su dati sintetici. I modelli non sono strumenti clinici né di sicurezza.

## Come contribuire
Ogni contributo è benvenuto, anche piccolo:
1. **Revisione critica** dei 28 principi: errori, riferimenti bibliografici, casi limite.
2. **Dati reali** per validare i modelli, anche pochi (umidità in uno stoccaggio, portate, temperature).
3. **Nuovi controlli** per il Verificatore: altre unità, funzioni, bilanci (energia, carica, specie chimiche).
4. **Traduzioni e accessibilità** (altre lingue, lettori di schermo, uso da telefono).
5. **Test e benchmark**, in particolare per la voce 27 (controllo di conservazione sugli output di un'AI).

Apri una *Issue* per discutere un'idea o una *Pull Request* per proporre una modifica. Vedi `CONTRIBUTING.md`.

## Licenza
MIT. Puoi usare, copiare e modificare il materiale, mantenendo l'avviso di copyright.

---

## English summary
An open, free tool that checks in seconds whether a calculation is physically consistent (units, conservation balances, plausibility), running entirely in your browser (`index.html`, IT/EN/ES), plus 28 design principles with their verification status declared. It is a sanity check, not a proof. Aimed at students, engineers, environmental and agricultural technicians, researchers, developers and anyone using AI assistants for calculations. Nothing here has been validated with experimental data yet: contributions, critical review and real data are welcome. Not a clinical or safety tool. MIT license.

## Resumen en español
Una herramienta abierta y gratuita que comprueba en segundos si un cálculo es físicamente coherente (unidades, balances de conservación, plausibilidad), y funciona por completo en tu navegador (`index.html`, IT/EN/ES), junto con 28 principios de diseño con su estado de verificación declarado. Es una comprobación de sentido común, no una demostración. Dirigida a estudiantes, ingenieros, técnicos ambientales y agrícolas, investigadores, desarrolladores y a quien use asistentes de IA para calcular. Nada de esto se ha validado aún con datos experimentales: se agradecen revisiones críticas, datos reales y contribuciones. No es una herramienta clínica ni de seguridad. Licencia MIT.
