### GPS Module
#### Tinkerforge Setup
Voor de Tinkerforge setup dien je eerst de Daemon en Viewer te installeren:
https://www.tinkerforge.com/en/doc/Downloads.html#downloads-tools

Na de installatie open je de Brick Viewer en bekijk je de UID, deze pas je aaan in het python script van de Tinkerforge module.

#### Pip requirements
tinkerforge

#### Wat doet Tinkerforge?
Tinkerforge is de library die alle bricks laat communiceren met elkaar in Python.

### API Connectie
Dit is de verbinding tussen een boot en de server.
Dit doen we met ```client.js``` die uitgevoerd kan worden met NodeJS.

#### Setup
In de ```config.js``` dien je eerst de url op te geven van je server. De id is een random string aan waardes. Hiermee wordt er onderscheid gemaakt op de server.
```js
module.exports = {
    host: 'http://127.0.0.1',
    id: "8ads8dsaudsua898sad",
    name: 'NIEK_PC',
    username: '', // De gebruikersnaam en wachtwoord wordt vergeleken
    password: ''  // met de server. (Zie API authentication)
}
```

Daarna voer je het volgende uit in de console:
```bash
node client.js
```
