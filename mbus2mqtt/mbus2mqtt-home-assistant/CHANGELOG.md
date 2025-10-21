# Changelog

Tutte le modifiche importanti a questo add-on saranno documentate in questo file.

Il formato è basato su [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.1.0] - 2025-10-21

### Added
- Supporto per dispositivi M-Bus multipli sullo stesso bus
- Configurazione baudrate tramite interfaccia UI con dropdown
- Device seriale configurabile via UI
- Logging migliorato con identificazione dispositivo `[nome_dispositivo]`
- Gestione errori robusta con try/except
- Device class automatico per sensori (energy, volume, power, temperature)
- Unit of measurement corrette (kWh, m³, W, °C)
- Delay di 2 secondi tra l'avvio dei processi per evitare conflitti bus

### Changed
- Refactored script `run.sh` per supportare array di dispositivi
- Script Python usa variabile d'ambiente `POLL_INTERVAL` invece di valore hardcoded
- Migliorato parsing XML M-Bus con gestione errori
- Aggiornate immagini base Alpine a 3.19

### Fixed
- Gestione corretta di device_class e unit_of_measurement nella MQTT discovery
- Gestione errori XML parsing con try/except
- Logging errori MQTT connection

## [1.0.0] - 2025-10-21

### Added
- Release iniziale dell'add-on
- Integrazione M-Bus to MQTT base
- MQTT auto-discovery per Home Assistant
- Supporto libmbus per comunicazione M-Bus
- Supporto architetture: aarch64, amd64, armv7, armhf
- Polling configurabile (30-3600 secondi)
- Supporto autenticazione MQTT (user/password)
- Documentazione completa

### Notes
- Basato su [mbus2mqtt-home-assistant](https://gitlab.com/marcofl/mbus2mqtt-home-assistant) di Marco Fretz
- Proof-of-concept quality - libmbus non è più mantenuto attivamente
