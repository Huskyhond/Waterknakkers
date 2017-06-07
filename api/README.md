Documentatie

#API

De API is de tussenlaag van de eindgebruiker en de boten. De boten kunnen worden bestuurd met API calls via WebSockets. Een gebruiker kan vanuit zijn WebBrowser commando’s sturen naar de API, de API stuurt de data dan door naar de gegeven boot.

**Database**
De API gebruikt MongoDB als database, hiervoor is gekozen omdat de NOSQL-structuur makkelijk werkt met objecten in javascript. Performance is niet echt van belang aangezien we weinig gebruik maken van de database buiten authenticatie en sensor data om.
De sensor data kan verschillen per boot, sommige boten hebben meer sensoren dan andere boten, dit werkt dan ook makkelijk in de NOSQL-structuur.

**Waarom WebSockets ?**
Voor de API gebruiken wij NodeJS omdat deze met Socket.IO werkt. Wij hebben gekozen voor een open WebSocket connectie om polling te voorkomen, hierdoor wordt er minder data onnodig verstuurd naar de boot die op een 3G module werkt.

**API requirements**

*	Node.JS (>= v6.10.3)
*	MongoDB (>= v3.0.4)

De Applicatie heeft nog wat library requirements deze kan je installeren door npm install te doen in de map api.

Om de API-server aan te zetten typen we ‘node app.js’

**Met de API communiceren**

Als client dien je een wrapper te hebben voor Socket.IO veel programmeertalen hebben een wrapper hiervoor. 

Connect eerst met de server we gebruiken in het voorbeeld NodeJs:

'''javascript
var socket = io();
'''

Je kan in de io als eerste parameter ook een ip en poort opgeven als de client niet dezelfde host heeft. Nadat je geauthentiseerd bent met de server kan je aan de slag.

**Emit**
*	getBoats – Vraag een boot emit aan de server, ontvang deze met on(‘getBoats’)

On
*	boatConnected – Als er een nieuwe boot is geconnect tijdens je sessie.
*	boatDisconnected – Als er een boot geen internet meer heeft.
*	getBoats – Ontvang alle verbonden boten van de server. (eerst emitten)
*	controller – Ontvang de motor en rudder informatie (Je kan deze alleen ontvangen als je je als boot geauthentiseerd hebt.
