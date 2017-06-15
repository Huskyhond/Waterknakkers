Documentatie

###API

De API is de tussenlaag van de eindgebruiker en de boten. De boten kunnen worden bestuurd met API calls via WebSockets. Een gebruiker kan vanuit zijn WebBrowser commando’s sturen naar de API, de API stuurt de data dan door naar de gegeven boot.

**Database**  
De API gebruikt MongoDB als database, hiervoor is gekozen omdat de NOSQL-structuur makkelijk werkt met objecten in javascript. Performance is niet echt van belang aangezien we weinig gebruik maken van de database buiten authenticatie en sensor data om.
De sensor data kan verschillen per boot, sommige boten hebben meer sensoren dan andere boten, dit werkt dan ook makkelijk in de NOSQL-structuur.

**Waarom WebSockets?**   
Voor de API gebruiken wij NodeJS omdat deze met Socket.IO werkt. Wij hebben gekozen voor een open WebSocket connectie om polling te voorkomen, hierdoor wordt er minder data onnodig verstuurd naar de boot die op een 3G module werkt.

**API requirements**

*	Node.JS (>= v6.10.3)
*	MongoDB (>= v3.0.4)

De Applicatie heeft nog wat library requirements deze kan je installeren door npm install te doen in de map api.

Om de API-server te starten moet er in een terminal sessie het volgende worden getypt
``` 
node app.js 
```

**Met de API communiceren**

Als client dien je een wrapper te hebben voor Socket.IO veel programmeertalen hebben een wrapper hiervoor. 

Connect eerst met de server we gebruiken in het voorbeeld NodeJs:

```JS
var socket = io();
```

Je kan in de io als eerste parameter ook een ip en poort opgeven als de client niet dezelfde host heeft. Nadat je geauthentiseerd bent met de server kan je aan de slag.

**Emit**
*   ```authentication``` - Geef een valide authenticatie token als payload van de functie.
*	```getBoats``` – Vraag een boot emit aan de server, ontvang deze met on(‘getBoats’)

**On**
*   ```authenticated``` - Response op emit 'authentication' als deze geslaagt is.
*   ```unautherized``` - Reponse op emit 'authentication als deze mislukt is, hierna word de socket meteen gesloten. Dit gaat gepaart met een reason, dit kan een ```error``` zijn of een ```Authentication failure```
*	```boatConnected``` – Als er een nieuwe boot is geconnect tijdens je sessie.
*	```boatDisconnected``` – Als er een boot geen internet meer heeft.
*	```getBoats``` – Ontvang alle verbonden boten van de server. (eerst emitten)
*	```controller``` – Ontvang de motor en rudder informatie (Je kan deze alleen ontvangen als je je als boot geauthentiseerd hebt.

**Authenticatie**

De authenticatie procedure een WebSocket connectie bestaat uit een aantal stappen die onderverdeeld zijn in functies. Hier volgt per functie een uitleg wat hij doet.

*   ```api.login``` - Deze functie neemt ```username``` en ```password``` als parameter. Deze parameters dienen aan de functie gegeven te worden door middel van een HTTP POST request naar ```<hostname / ip-address>/login```. De parameters kunnen in de body worden geplaats van de request als ```<key>: <value>``` paren. De request dient ```x-www-form-urlencoded``` te zijn.  
    ```
    <key> : <value>
    username : boot
    password : secret
    ```
    
    Als de opgegeven username en password correct is, krijgt de user een response met een ```token``` die gebruikt kan worden om zich te authoriseren met de WebSocket.

    login succesvol (HTTP reponse)
    ```JS
    {
        "error": 0,
        "payload": {
            "token": "1a2b3c4d5f6g7h1a2b3c"
        }
    }
    ```
    login onsuccesvol (HTTP reponse)
    ```JS
    {
        "error": 'example error message',
        "payload": {
            "token": 0
        }
    }
    ```
*   ```authenticate``` - Deze functie neemt als parameter een token verkregen uit functie hierboven. Deze token moet meegestuurt worden zodra de gebruiker een connectie maakt met de WebSocket. Hieronder is een voorbeeld te zien in JavaScript.

    ```JS
    socket.on('connect', function(){
        socket.emit('authentication', authdata)
    })
    ```
    Als de token foutief of niet geldig blijkt te zijn zal de server een ```unautherized``` event sturen. Hierna zal de connectie direct worden verbroken.

    Als de token geldig is zal de server een ```autherized``` event sturen en word de verbinding toegestaan en kunnen de api functies worden aangeroepen.

*   ```postAuthenticate``` - Hierin staan de functies die aangeroepen kunnen worden nadat de client connected en authorized is.

*   ```disconnect``` - Deze functie neemt als parameter de huidige socket connectie. Als een boot de WebSocket connectie verbreekt zal zijn token in de database ongeldig worden door middel van de ```api.logout``` functie. 

