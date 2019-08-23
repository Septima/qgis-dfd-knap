# qgis-dfd-knap

Plugin til QGIS som gør det nemmere at tilføje services fra Datafordeleren. Koden til dette plugin er baseret på koden fra Kortforsyningspluginet.

## Installation
Indtil videre skal pluginet installeres manuelt. Dette gøres således:

- Download Datafordeler-pluginet. På sigt vil plugin'et blive tilgængeligt gennem QGIS' plugin repository, men indtil da downloades en zip-fil med pluginet fra [Septimas Github](https://github.com/Septima/qgis-dfd-knap/releases)
- Start QGIS 3.4 eller senere
- Installér pluginet
  - Klik på menuen 'Plugins' og derefter 'Administrér og Installér Plugins'
  - Udpeg zip-filen (`Datafordeler.zip`) med Datafordeler-pluginet som du hentede i trin 1
  - Klik 'Installér'

  
## Første gang du bruger pluginet
Pluginet kræver en tjenestebruger til Datafordeleren. For at kunne oprette en tjenestebruger skal du først oprette en webbruger, derefter kan der oprettes en tjenestebruger under denne webbruger. Læs mere på [Datafordelerens dokumentation](https://datafordeler.dk/vejledning/brugeradgang/brugeroprettelse/).

I QGIS konfigurerer du pluginet med brugernavn og password således:
- Søg efter 'Datafordeler' i Locator-feltet (dvs. søgefelter i nederste venstre hjørne af QGIS), og klik på 'Datafordeler (Muligheder)'/'Datafordeler (Settings)', herved åbnes en dialog
- I denne dialog indtastes **tjenestebrugernavn** og adgangskode til tjenestebrugeren
- Klik 'OK'
