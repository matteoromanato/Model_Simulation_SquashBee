# Model_Simulation_SquashBee
 This is a model simulation of a squash bee's ecosystem

# DESCRIZIONE
L'ape di zucca ( Peponapis pruinosa ) è un'ape selvaggia e nativa che impollina Cucurbitacolture (ad esempio zucca, zucca e zucca). Queste colture dipendono dall'impollinazione delle api per produrre frutta. Molti contadini di zucca e zucca affittano le api da miele. Tuttavia, gli agricoltori potrebbero essere in grado di ridurre i costi associati alle api da miele in affitto se gestiscono la loro fattoria per sostenere le api da squash.
 Le api da squash hanno una generazione all'anno. In estate gli adulti voleranno in giro raccogliendo polline e costruendo nidi. I loro discendenti trascorreranno la maggior parte della loro vita sottoterra, in attesa del raccolto della prossima stagione. Come la maggior parte delle api autoctone, le api da squash sono api solitarie che nidificano nel terreno. I loro nidi sono una serie di tunnel, alla fine dei quali sono celle piene di polline e uova di api

# AGENTI 
#### APE
L' ape è definita ( posizione, tipo di agente, tempo di vita, quantità di polline che trasporta, miglioramento da to dal polline, energia, sesso, nel caso sia femmina c'è un parametro che dice se è incinta o no).

Ad ogni step l'ape deve : 
                          - spostarsi alla ricerca di un fiore
                          - se è femmina e incinta deposita la larva vicino ad una zucca
                          - quanto finisce l'energia o il tempo di vita muore

#### LARVA
La larva viene creata dall'ape vicino ad un agente zucca.
La larva è definita in particolare da un tempo di incubazione che va da 170 a 210 step
Ad ogni step questo tempo verrà decrementato e quando finito la larva diventerà un' ape

#### ZUCCA
La zucca è l'agente vicino al quale l'ape deposita i figli.
La zucca è definita da un tempo di vita che verrà decrementato ad ogni step.
Finito il tempo di vita la zucca "deposita i semi" ipotiziamo questa fase come la fase di seminatura fatta dal fattore nel suo campo in base al raccolto che ha avuto.

#### FIORE DI ZUCCA
Il fiore di zucca è un agente molto importante perchè oltre a diventare la zucca se impollinato gestisce l'accoppiamento delle api.
Le api infatti si accoppiano sul fiore.
Il fiore è quindi definito in particolare da una variabile impollinato (boolean) e una variabile pro_accoppiamento che deciderà la probabilità con cui due api si accoppiano.
Ad ogni step il fiore controlla i suoi vicini e se ha almeno una femmina e un maschio in base alla probabilità di accoppiamento la femmina rimarrà incinta o no.
Successivamente il polline dovrà controllare se è stato impollinato o no, questo lo capisce in base al parametro che descrive la quantità di polline che porta un'ape. Se l'ape porta tanto polline ci sarà una più alta probabilità che il fiore rimanga impollinato.
Quando il fiore finisce il suo tempo di vita muore e se è stato fecondato si trasformerà in una zucca.


#### SEME DI ZUCCA
Il seme di zucca è caratterizzato da un tempo di vita che sta a significare la crescita del seme in una pianta fino alla fioritura a quel punto il seme diventerà un fiore di zucca.

# COSA MOSTRA QUESTO MODELLO?
Il modello simula l'ecosistema composto da api e zucche. Si può studiare come la produzione di zucca migliori o peggiori nel tempo e come varia in presenza delle api.
