# Datafordeler

# Vigtig info - pluginet nedlægges pr. 15. december 2023
Datafordeler-pluginet blev lavet tilbage i 2016 for, at data fra Datafordeleren kunne ses i QGIS. Dengang var det ikke muligt at tilgå Datafordelerens data i QGIS. Datafordeler-pluginet - og Septimas tilhørende proxy - gjorde det således muligt at få vist data fra Datafordeleren. Siden da har Styrelsen for Dataforsyning og Infrastruktur (SDFI) også lavet en proxy til Datafordeleren, og SDFI udstiller nu en række datasæt fra Datafordeleren via pluginet 'Dataforsyningen'. 

Vi har i Septima således besluttet at ændre Datafordeler-pluginets status til 'forældet'/'deprecated', og den proxy som pluginet bruger vil blive nedlagt d. 15. december 2023.

# Om pluginet

Plugin til QGIS som gør det nemmere at tilføje services fra Datafordeleren. Koden til dette plugin er baseret på koden fra Kortforsyningspluginet.

![Skærmdump](docs/images/screendump.png)

Bemærk, at Septima stiller pluginet frit og gratis til rådighed i det håb, at det kan være til nytte. Vi kan desværre ikke tilbyde gratis support.

## Installation
Pluginet installeres gennem QGIS´ plugin manager ved at søge på `Datafordeler`.
  
## Første gang du bruger pluginet
Pluginet kræver en tjenestebruger til Datafordeleren. For at kunne oprette en tjenestebruger skal du først oprette en webbruger, derefter kan der oprettes en tjenestebruger under denne webbruger. Læs mere på [Datafordelerens dokumentation](https://datafordeler.dk/vejledning/brugeradgang/brugeroprettelse/).

I QGIS konfigurerer du pluginet med brugernavn og password således:
- Søg efter 'Datafordeler' i Locator-feltet (dvs. søgefelter i nederste venstre hjørne af QGIS), og klik på 'Datafordeler (Muligheder)'/'Datafordeler (Settings)', herved åbnes en dialog
- I denne dialog indtastes **tjenestebrugernavn** og adgangskode til tjenestebrugeren
- Klik 'OK'
