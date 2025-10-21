# M-Bus to MQTT Add-on

Integra dispositivi M-Bus (contabilizzatori di calore, contatori acqua/energia) in Home Assistant tramite MQTT auto-discovery.

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]
![Supports armv7 Architecture][armv7-shield]
![Supports armhf Architecture][armhf-shield]

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg
[armhf-shield]: https://img.shields.io/badge/armhf-yes-green.svg

## About

Questo add-on permette di leggere dispositivi M-Bus e pubblicare i dati su MQTT con auto-discovery per Home Assistant. Supporta dispositivi multipli sullo stesso bus seriale.

**Caratteristiche:**

- ✅ Supporto dispositivi M-Bus multipli
- ✅ Configurazione tramite interfaccia grafica
- ✅ MQTT auto-discovery (sensori automatici in HA)
- ✅ Baudrate configurabile
- ✅ Polling personalizzabile (30s - 1h)
- ✅ Logging dettagliato per dispositivo
- ✅ Gestione errori robusta

## Requisiti Hardware

- Convertitore USB M-Bus (es: M-Bus Master USB, Zenner dongles)
- Dispositivi M-Bus compatibili (contabilizzatori, meter)
- Home Assistant OS o Supervised

## Installation

1. Aggiungi questo repository agli add-on store di Home Assistant
2. Installa "M-Bus to MQTT"
3. Configura i parametri (vedi sotto)
4. Avvia l'add-on
5. I sensori appariranno automaticamente in Home Assistant

## Configuration

### Esempio Base (2 dispositivi)

mqtt_host: "core-mosquitto:1883"
mqtt_user: ""
mqtt_password: ""
poll_interval: 1800
serial_device: "/dev/ttyUSB0"
baudrate: 2400
device_name: "contabilizzatore_piano_terra"

device_name: "contabilizzatore_primo_piano"


### Parametri

**mqtt_host** (string, required)
- Indirizzo broker MQTT con porta
- Esempio: `core-mosquitto:1883` (broker locale)
- Esempio: `192.168.1.100:1883` (broker esterno)

**mqtt_user** (string, optional)
- Username MQTT (lascia vuoto per accesso anonimo)

**mqtt_password** (password, optional)
- Password MQTT

**poll_interval** (int, required, 30-3600)
- Intervallo polling in secondi
- Consigliato: `1800` (30 minuti) per contabilizzatori

**serial_device** (string, required)
- Dispositivo seriale del convertitore M-Bus
- Solitamente: `/dev/ttyUSB0` o `/dev/ttyACM0`

**baudrate** (list, required)
- Velocità comunicazione M-Bus
- Valori: 300, 600, 1200, 2400, 4800, 9600, 19200, 38400
- Default per la maggior parte dei dispositivi: `2400`

**mbus_devices** (list, required)
- Lista dei dispositivi M-Bus da interrogare
- Ogni dispositivo richiede:
  - **device_name** (string): Nome univoco
  - **address** (int, 0-250): Indirizzo M-Bus

## Trovare Indirizzi M-Bus

Per scoprire gli indirizzi dei tuoi dispositivi:

1. Installa e avvia l'add-on
2. Vai al tab **Log**
3. Esegui lo scan (via SSH o Terminal add-on):

docker exec -it addon_local_mbus2mqtt sh
/libmbus/

Output esempio:

Found a M-Bus device at address 0
Found a M-Bus device at address 1

### Testare Lettura Dispositivo

/libmbus/bin/mbus-serial-request-data -b 2400 /dev/ttyUSB0 0

Mostrerà l'output XML completo del dispositivo.

## Aggiungere/Rimuovere Dispositivi

### Aggiungere

1. Vai su **Configuration** dell'add-on
2. Nella sezione **M-Bus Devices**, clicca **"Add Item"**
3. Inserisci:
   - `device_name`: nome univoco (es: `contatore_garage`)
   - `address`: indirizzo M-Bus trovato con lo scan
4. **Save** e **Restart** l'add-on

### Rimuovere

1. Nella lista **M-Bus Devices**, clicca **"Remove"** sul dispositivo
2. **Save** e **Restart**

## Entità Home Assistant

Per ogni dispositivo M-Bus vengono create automaticamente entità come:

sensor.contabilizzatore_piano_terra_energy_0
sensor.contabilizzatore_piano_terra_volume_1
sensor.contabilizzatore_piano_terra_power_2
sensor.contabilizzatore_primo_piano_energy_0

Le entità includono:
- `device_class` automatico (energy, volume, power, temperature)
- `unit_of_measurement` corretta (kWh, m³, W, °C)
- Icone appropriate

## Troubleshooting

### Dongle USB non rilevato

Verifica dispositivi disponibili:

ls -la /dev/tty*


Se è `/dev/ttyACM0` invece di `ttyUSB0`, aggiorna `serial_device` nella configurazione.

### Nessun dato dai dispositivi

**Verifica:**
1. Cablaggio M-Bus corretto
2. Alimentazione M-Bus presente (~36V tra M-Bus+ e M-Bus-)
3. Baudrate corretto (prova 2400, poi 9600, 300)
4. Indirizzo corretto (esegui scan)

### Sensori non compaiono in HA

**Verifica:**
1. Broker MQTT attivo (`core-mosquitto` add-on installato e avviato)
2. MQTT integration configurata in Home Assistant
3. Credenziali MQTT corrette
4. Guarda i log dell'add-on per errori

### Conflitti sul bus M-Bus

Se hai errori di timeout:
- L'add-on introduce 2s di delay tra dispositivi
- Aumenta `poll_interval` a 3600 (1 ora) se persistono problemi
- Non interrogare lo stesso dispositivo da più add-on/container

## Support

- [📖 Documentazione Completa](DOCS.md)
- [📝 Changelog](CHANGELOG.md)
- [🐛 Report Issues](https://github.com/TUO_USERNAME/hassio-addons-mbus2mqtt/issues)
- [💬 Home Assistant Community](https://community.home-assistant.io/)

## Credits

Basato su [mbus2mqtt-home-assistant](https://gitlab.com/marcofl/mbus2mqtt-home-assistant) di Marco Fretz.

Usa [libmbus](https://github.com/rscada/libmbus) per comunicazione M-Bus.

## License

MIT License


