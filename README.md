# smart-health
This is the repository for the health monitor system of Arkimede s.r.l . It uses a low cost [sensor](http://www.sca-shinyei.com/pdf/PPD42NS.pdf) and an [obdII bluetooth adapter](http://www.cartft.com/catalog/il/1859) to detect __temperature__, __pressure__ and __PM10__ in the air. It is economic, scalable, interoperable and open ;) . Try it!

Sorry, at this moment, only italian version :(

##Il progetto

* Il sistema è __economico__: è stato infatti realizzato con hardware a basso costo. Per effettuare le misurazioni sono stati scelti dei sistemi embedded facilmente reperibili sul mercato, dai costi molto contenuti che allo stesso tempo garantiscono buona capacità di elaborazione. Anche la scelta della sensoristica è stata rivolta a mantenere bassi i costi, i sensori di particolato sono purtroppo molto costosi. Il nostro approccio è stato quello di risparmiare sulla qualità dei sensori, pensando di migliorare la precisione della misurazione in un secondo momento attraverso una post elaborazione dei dati. Studi in letteratura hanno dimostrato come un elevato numero di sensori a basso costo, con opportune calibrazioni, possono garantire delle misurazioni paragonabili a quelle di un singolo sensore di alta qualità molto più costoso

* Il sistema è __scalabile__: la memorizzazione dei dati è distribuita attraverso filesystem HDFS permettendo così lo storing di grosse moli di dati. Quando i dati sono tanti, l’uso di un sistema di memorizzazione centralizzato può rappresentare il collo di bottiglia dell’intera infrastruttura. Inoltre, la distribuzione dei dati in un cluster di macchine, permette operazioni di post elaborazione distribuite molto efficaci e ampiamente utilizzate in ambito big data. Infine, i tempi di risposta del server di comunicazione sono stati studiati sotto diverse condizioni di carico, ottenendo anche in situazioni di stress buoni tempi di risposta.

* Il sistema sfrutta il paradigma RESTful, ciò garantisce un elevato livello di __interoperabilità__ tra le varie parti. Il server che permette la comunicazione e lo smistamento delle informazioni tra i livelli è di fatto un web service che fornisce la proprie funzionalità attraverso chiamate rest su protocollo http. Questa scelta lascia massima libertà sul linguaggio di
programmazione da utilizzare nell’implementazione di un’applicazione di terze parti che volesse interagire con il sistema; non si è legati a nessuna libreria di uno specifico linguaggio.

* Il sistema è in grado di pubblicare i dati raccolti in maniera automatica in formato __open data__ sullo store del Fi-lab. Il nostro sistema doveva infatti prevedere un metodo semplice per l’accesso ai dati da parte dei programmatori che avessero intenzione di sviluppare applicazioni di tipo ambientale. CKAN e il formato open data sono stati utilizzati proprio a
questo scopo. Il vantaggio nell’uso di CKAN è rappresentato dalla possibilità di accedere ai dati delle misurazioni attraverso semplici api. Sviluppatori di terze parti possono dunque utilizzare il sistema per le proprie
applicazioni come sorgente di dati ambientali.

* Il sistema fornisce un’ __interfaccia grafica__ per la consultazione delle misurazioni. I dati non sono accessibili solamente in formato open data per l’elaborazione automatica; attraverso un sistema innovativo di nome
Wirecloud i dati sono consultabili dagli utenti direttamente dal browser

##Struttura Dati
Il sistema utilizza il modello dei dati [NGSI](http://technical.openmobilealliance.org/Technical/release_program/docs/NGSI/V1_0-20120529-A/OMA-TS-NGSI_Context_Management-V1_0-20120529-A.pdf) (New Generation Service Interface)
L’entità più importante nel nostro sistema è il __Service__, questa entità rappresenta il singolo servizio. I servizi presenti in questo momento sulla piattaforma sono tre: uno per la misurazione di __temperatura__, uno per la __pressione__ e l'ultimo per la rilevazione del __particolato__. Il sistema, come già anticipato, prevede la possibilità di aggiungere nuovi servizi e meccanismi di discovery dei servizi per l'utente.

Di seguito sono riportati gli attributi dell'entità Service con una breve spiegazione:

1. __description__: una breve descrizione del servizio

2. __typeOfService__: stringa di testo che rappresenta il servizio

Successivamente abbiamo l'entità __Procedure__ che rappresenta il singolo sensore montato sul taxi, questi sono i suoi attributi:

1. __description__: una breve descrizione del sensore.

2. __model__: marca e modello del sensore

3. __type__: indica se il sensore è fisso o mobile

4. __datasheet__: link al datasheet del sensore

5. __observed_property__: proprietà fisica misurata dal sensore.

Per rappresentare il taxi esiste l'entità __Taxi__ con i seguenti attributi:

1. __ID_SERVICE__: id del servizio a cui partecipa il taxi

2. __procedure__: id del sensore montato sul taxi

3. __position__: posizione attuale occupata dal taxi

Infine abbiamo l'entità __Observations__ che rappresenta la singola osservazione effettuata dal sensore. Questi i suoi attributi:

1. __ID_SERVICE__: id del servizio a cui appartiene la misurazione

2. __date__: data della misurazione

3. __duration__: durata della misurazione

4. __server__: ip del server che contiene i dati dell'osservazione

5. __position__: posizione della misurazione

6. __observed_property__: proprietà fisica oggetto della misura

7. __procedure__: id del sensore che ha effettuato la misurazione

![Struttura dati](/doc/images/struttura_dati_definitivo_cut.png)

##Architettura
Il sistema è diviso in tre livelli:

* Il livello di __sensoristica__: appartengono a questo livello i dispositivi embedded e i sensori utilizzati per la raccolta dei dati, le operazioni a questo livello consistono fondamentalmente nella raccolta e nell'inoltro delle informazioni al livello superiore che avrà il compito di elaborarle. 

* Il livello di __backend__: a questo livello troviamo la logica di funzionamento del sistema, il compito del backend è quello di ricevere i dati dal livello inferiore e inoltrarli al sistema di memorizzazione permanente, passarli al livello superiore per l'interrogazione da parte degli utenti finali. Svolge dunque sia una funzione di comunicazione tra il livello di sensoristica e di interfaccia utente, sia di elaborazione e memorizzazione permanente dei dati.

* Il livello di __interfaccia utente__: come si può intuire facilmente, questo è il livello al quale accedono gli utenti, attraverso di esso è possibile consultare i dati in modo intuitivo. Questo livello nasconde i livelli inferiori e rappresenta quindi l'interfaccia del sistema verso l'utente finale.

![Livelli del sistema](/doc/images/livelli_sistema_cut.jpeg)

###Livello sensoristica
Il software che gestisce la componente di sensoristica è composto da tre script che girano direttamente sul dispositivo embedded (Linino o Raspberry): 

* __Obd.py__: legge i valori di temperatura e pressione dal dispositivo obd e li scrive su un file.

* __Shinyei.py__: legge i valori di PM10 dal sensore Shinyei e li scrive su un file.

* __Send_measures.py__: rileva un aggiornamento dei file e invia i nuovi dati ad Orion.

![Livello sensoristica](/doc/images/livello_sensoristica.png)

###Livello backend

Il secondo livello ha il compito di permettere la comunicazione tra l’applicazione produttrice dei dati (nel nostro caso il livello di sensoristica) e l’applicazione consumatrice (l’interfaccia grafica che si trova al terzo livello). I dati di temperatura, pressione e del particolato devono essere smistati dal primo al terzo livello e memorizzati per una futura consultazione o post elaborazione. Per svolgere questi compiti abbiamo utilizzato esclusivamente moduli sofware messi a disposizione dalla tecnologia Fi-ware, nello specifico:

* [__Orion__](http://catalogue.fiware.org/enablers/publishsubscribe-context-broker-orion-context-broker): è il modulo software centrale del livello di backend, ha il compito di ricevere le informazioni/misurazioni, di smistare i valori misurati alle applicazioni che ne hanno fatto richiesta attraverso sottoscrizioni, di inviare i dati a Cosmos/CKAN per una memorizzazione permanente.

* [__Cosmos__](http://catalogue.fiware.org/enablers/bigdata-analysis-cosmos): mette a disposizione un file-system distribuito in cui salvare i dati, il componente fa anche uso della tecnologia Hadoop MapReduce per una elaborazione efficiente dei dati su un cluster di macchine.

* [__CKAN__](http://ckan.org/): permette la pubblicazione e la consultazione di informazioni in formato open data. I dati raccolti dal sistema verranno quindi pubblicati sullo store del Fi-lab attraverso le api CKAN. I dati quindi potranno essere venduti o fruiti gratuitamente attraverso lo store.

* __subscriptionServer__: Il subscriptionServer svolge il ruolo di proxy tra Orion e i due sistemi di memorizzazione usati dal nostro sistema: Cosmos e CKAN. Orion non è in grado di memorizzare i dati a lungo termine; i valori degli attributi vengono sovrascritti ad ogni nuovo aggiornamento. Il subscriptionServer resta in ascolto per aggiornamenti sui dati, quando
riceva una notifica di update (nuove misurazioni) dal server Orion, invia il nuovo dato a Cosmos. Contemporaneamente il subscriptionServer si occuperà di salvare i dati su CKAN usando le api apposite

* __restServerHive__: Il compito del RestServerHive è quello di fare da proxy tra il LinearGraph e Cosmos: il LinearGraph richiede i dati al server, quest'ultimo effettua una query Hive su Cosmos e restituisce i dati al widget in un formato opportuno. I passaggi appena descritti risultano necessari in quanto le api NGSI di Wirecloud non mettono a disposizione delle procedure per contattare direttamente Cosmos. 

![Livello backend](/doc/images/livello_comunicazione_memorizzazione.png)
###Livello Interfaccia utente

L’ultima componente del sistema è l’interfaccia con l’utente, attraverso di essa è possibile selezionare il servizio d'interesse e visualizzare sulla mappa le entità che prendono parte al servizio selezionato. Nel caso specifico, cioè l’applicazione per la misurazione del particolato, l’utente visualizzerà sulla mappa i taxi che dispongono dei sensori e le zone della città in cui sono disponibili delle misurazioni. Per la realizzazione dell’interfaccia grafica abbiamo utilizzato Wirecloud (vedi paragrafo [sec:Wirecloud]) e implementato due nuovi widget per i nostri scopi: 

* __ServiceWidget__: mostra all’utente i servizi attivi e permette di selezionarne uno.

* __QueryWidget__: individua tutte le entità di un servizio e le inoltra alla mappa per la visualizzazione.

I widget e gli operatori già esistenti che utilizziamo sono i seguenti:

* __MapViewer__: mostra le entità di un servizio su una mappa.

* __LinearGraph__: mostra il grafico di una misurazione.

* __NgsiEntityToPoi__: usato per trasformare i dati in uscita dal QueryWidget in un formato adatto per il MapViewer.

![Livello interfaccia utente](/doc/images/livello_interfaccia_utente .png)

##Interazione tra le componenti
Per quanto riguarda la __parte grafica__: 

* Il __ServiceWidget__ contatta Orion per conoscere i servizi disponibili, effettua una sottoscrizione per essere aggiornato in modo asincrono sulla creazione di nuovi servizi o circa l’aggiornamento di servizi già esistenti 

* Il __ServiceWidget__ mostra all’utente i servizi appena scoperti, l’utente seleziona il servizio a cui è interessato cliccando con il mouse sul nome del servizio.

* Il __ServiceWidget__ invia al QueryWidget il servizio che l’utente ha selezionato 

* Il __QueryWidget__ contatta Orion per selezionare tutte le entità che appartengono al servizio richiesto, nel nostro caso le entità mostrate saranno i taxi e le misurazioni effettuate.

* Le entità trovate sono mostrate sulla mappa dal __MapViewer__.

Per la __parte di sensoristica__:

* Il tassista attiva la misurazione attraverso il tablet presente sulla propria autovettura. Per fare ciò contatta un server scritto in python (__server_rasp.py__) presente direttamente sulla scheda. Il server, ricevuto il comando, eseguirà gli script necessari per effettuare la misurazione.

* Ogni trenta secondi gli script __Obd.py, Shinyei.py, Send_measures.py, UpdateEntityAttribute.py__ si occupano di effettuare le misurazioni di temperatura pressione e PM10 e inviare i dati aggiornati al server Orion.

Per la __logica di comunicazione e memorizzazione__:

* Il __subscriptionServer__ resta in ascolto per aggiornamenti sui dati, quando riceva una notifica di update (nuove misurazioni) dal server Orion, invia il nuovo dato a Cosmos. Contemporaneamente il subscriptionServer si occuperà di salvare i dati su CKAN usando le api apposite.

* __Cosmos__, ottenuti i dati inviatigli dal subscriptionServer, li memorizza su un filesystem distribuito.

* Abbiamo detto che attraverso il __LinearGraph__ è possibile visualizzare in un grafico i dati relativi ad una misurazione, il LinearGraph per fare questo contatta il __RestServerHive__. Il compito del RestServerHive è quello di fare da proxy tra il LinearGraph e Cosmos: il LinearGraph richiede i dati al server, quest'ultimo effettua una query Hive su Cosmos e restituisce i dati al widget in un formato opportuno. I passaggi appena descritti risultano necessari in quanto le api NGSI di Wirecloud non mettono a disposizione delle procedure per contattare direttamente Cosmos. 

* Abbiamo dunque due modalità di accesso ai dati; la prima, descritta sopra, attraverso i widget di wirecloud, la seconda tramite i dataset pubblicati su CKAN.

##How to start

###__Livello sensoristica__ 
Utilizza il codice nella cartella [raspberry](https://github.com/arkimede/smart-health/tree/master/livello_sensoristica/raspberry) o [linino](https://github.com/arkimede/smart-health/tree/master/livello_sensoristica/linino) a seconda della tua piattorma. Nel caso di linino one, ricorda che come prima cosa dovrai caricare lo sketch __Shinyei.ino__ sul microcontrollore. 

* lanciare il __server_rasp__ per ricevere la richiesta di misurazione

```javascript
#nohup sudo python ./server_rasp.py >> server_rasp.out
```

* lanciare __l'emulatore__ che simulata i diversi taxi che effettuano le misurazioni. E' impostante lanciare l'emulatore solo dopo aver lanciato il server che gestisce le richieste dei tassisti.
```javascript
#nohup sudo python ./taxi_emulator.py >> taxi_emulator.out
```

###__Livello backend__
Hai bisogno di aver precedentemente installato questi componenti:
* [redis](http://redis.io/download)
* [rush](https://github.com/telefonicaid/Rush/wiki)
* [orion](https://forge.fiware.org/plugins/mediawiki/wiki/fiware/index.php/Publish/Subscribe_Broker_-_Orion_Context_Broker_-_Installation_and_Administration_Guide)

I link contengono le informazioni utili per eseguire con successo l'installazione dei software, puoi trovare delle info aggiuntive nei pdf presenti nella cartella doc di questo repository.

* lancia il __redis-server__
```javascript
#nohup ./redis-server >> redis-server.out
```

* lancia __rush__ (listener e consumer)
```javascript
#nohup ./consumer >> consumer.out
```

```javascript
#nohup ./listener >> listener.out
```

* lancia il __contextBroker__ (Orion). Fai attenzione all'opzione -rush. E' importante che rush sia in esecuzione prima di lanciare Orion.
```javascript
#/usr/bin/contextBroker -port 1026 -logDir /var/log/contextBroker -pidpath /var/run/contextBroker/contextBroker.pid -dbhost localhost -db orion -rush localhost:5001
```
* lancia il __subscriptionServer__
```javascript
#nohup subscriptionServer.py 7777 /accumulate on >> subscriptionServer.out
```

* lancia il __restServerHive__
```javascript
#nohup  python restServerHive.py 1027 >> restServerHive.out
```

###__Livello interfaccia utente__
Hai bisogno di un account su [fi-lab](https://account.lab.fiware.org/) e dei seguenti widget/operatori installati:
* serviceWidget
* queryWidget
* NGSI Entity2Poi
* MapViewer
* historyHiveToLinearGraph
* LienarGraph

E' richiesta una minima conoscenza dei concetti e dell'interfaccia di Wireclod, a questo scopo puoi leggere questa [guida](https://forge.fiware.org/plugins/mediawiki/wiki/fiware/index.php/Application_Mashup_-_Wirecloud_-_User_and_Programmer_Guide#Sharing_your_mashups)

Puoi trovare i .wgt che ti servono in questa [cartella](https://github.com/arkimede/smart-health/tree/master/livello_interfaccia_utente/wgt).
La procedura per caricare i .wgt su fi-lab è spiegata in questo [video](https://www.youtube.com/watch?v=DSon3TSO9T8&feature=youtu.be)

Crea il workspace che ospiterà il tuo mashup, usa l'immagine di sotto per collegare nel modo corretto i componenti del tuo mashup
![Wiring](/doc/images/mashup_wiring.png)

Al termine di queste operazioni dovresti avere l'interfaccia installata come nella foto di sotto.

![Interface](/doc/images/mashup_vista_utente.png)

