# smart-health
This is the ropository for the Arkimede health monitor system. It uses a low cost sensor to detect temperature, pressure and PM10 in the air. It is economic, scalable, interoperable and open ;) . Try it!

#Il progetto
* Il sistema è __economico__: è stato infatti realizzato con hardware a basso
costo. Per effettuare le misurazioni sono stati scelti dei sistemi embedded
facilmente reperibili sul mercato, dai costi molto contenuti che allo stesso
tempo garantiscono buona capacità di elaborazione. Anche la scelta della
sensoristica è stata rivolta a mantenere bassi i costi, i sensori di particolato
sono purtroppo molto costosi. Il nostro approccio è stato quello di
risparmiare sulla qualità dei sensori, pensando di migliorare la precisione
della misurazione in un secondo momento attraverso una post elaborazione
dei dati. Studi in letteratura hanno dimostrato come un
elevato numero di sensori a basso costo, con opportune elaborazioni dei
dati, possono garantire delle misurazioni paragonabili a quelle di un
singolo sensore di alta qualità molto più costoso

* Il sistema è __scalabile__: la memorizzazione dei dati è distribuita attraverso
filesystem HDFS3 permettendo così lo storing di grosse moli di dati. Quando
i dati sono tanti, l’uso di un sistema di memorizzazione centralizzato
può rappresentare il collo di bottiglia dell’intera infrastruttura. Inoltre,
la distribuzione dei dati in un cluster di macchine, permette operazioni
di post elaborazione distribuite molto efficaci e ampiamente utilizzate in
ambito big data. Infine, i tempi di risposta del server di comunicazione
sono stati studiati sotto diverse condizioni di carico, ottenendo anche in
situazioni di stress buoni tempi di risposta.

* Il sistema sfrutta il paradigma RESTful, ciò garantisce un elevato livello
di __interoperabilità__ tra le varie parti. Il server che permette la comunicazione
e lo smistamento delle informazioni tra i livelli è di fatto un
web service che fornisce la proprie funzionalità attraverso chiamate rest
su protocollo http. Questa scelta lascia massima libertà sul linguaggio di
programmazione da utilizzare nell’implementazione di un’applicazione di
terze parti che volesse interagire con il sistema; non si è legati a nessuna
libreria di uno specifico linguaggio.

* Il sistema è in grado di pubblicare i dati raccolti in maniera automatica
in formato __open data__ sullo store del Fi-lab. Il nostro sistema doveva
infatti prevedere un metodo semplice per l’accesso ai dati da parte dei
programmatori che avessero intenzione di sviluppare applicazioni di tipo
ambientale. CKAN e il formato open data sono stati utilizzati proprio a
questo scopo. Il vantaggio nell’uso di CKAN è rappresentato dalla possibilità
di accedere ai dati delle misurazioni attraverso semplici api. Sviluppatori
di terze parti possono dunque utilizzare il sistema per le proprie
applicazioni come sorgente di dati ambientali.

* Il sistema fornisce un’ __interfaccia grafica__ per la consultazione delle misurazioni.
I dati non sono accessibili solamente in formato open data
per l’elaborazione automatica; attraverso un sistema innovativo di nome
Wirecloud i dati sono consultabili dagli utenti direttamente dal browser

##Architettura
Il sistema è diviso in tre livelli:

* Il livello di __sensoristica__: appartengono a questo livello i dispositivi embedded e i sensori utilizzati per la raccolta dei dati, le operazioni a questo livello consistono fondamentalmente nella raccolta e nell'inoltro delle informazioni al livello superiore che avrà il compito di elaborarle. 

* Il livello di __backend__: a questo livello troviamo la logica di funzionamento del sistema, il compito del backend è quello di ricevere i dati dal livello inferiore e inoltrarli al sistema di memorizzazione permanente, passarli al livello superiore per l'interrogazione da parte degli utenti finali. Svolge dunque sia una funzione di comunicazione tra il livello di sensoristica e di interfaccia utente, sia di elaborazione e memorizzazione permanente dei dati.

* Il livello di __interfaccia utente__: come si può intuire facilmente, questo è il livello al quale accedono gli utenti, attraverso di esso è possibile consultare i dati in modo intuitivo. Questo livello nasconde i livelli inferiori e rappresenta quindi l'interfaccia del sistema verso l'utente finale.
