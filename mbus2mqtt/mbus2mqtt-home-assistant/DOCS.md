# M-Bus to MQTT - Documentazione Completa

## Indice

1. [Introduzione](#introduzione)
2. [Cos'è M-Bus](#cosè-m-bus)
3. [Requisiti Hardware](#requisiti-hardware)
4. [Installazione](#installazione)
5. [Configurazione Dettagliata](#configurazione-dettagliata)
6. [Trovare Indirizzi M-Bus](#trovare-indirizzi-m-bus)
7. [Esempi Configurazione](#esempi-configurazione)
8. [Come Funziona](#come-funziona)
9. [MQTT Topics](#mqtt-topics)
10. [Troubleshooting](#troubleshooting)
11. [Advanced](#advanced)
12. [FAQ](#faq)

---

## Introduzione

Questo add-on Home Assistant permette di integrare dispositivi M-Bus (Meter-Bus) tramite MQTT con auto-discovery. Supporta dispositivi multipli sullo stesso bus seriale e crea automaticamente sensori in Home Assistant.

**Use Case Tipici:**
- Lettura contabilizzatori di calore
- Monitoraggio contatori acqua
- Tracking consumo energia
- Gestione impianti di riscaldamento centralizzati

---

## Cos'è M-Bus

**M-Bus (Meter-Bus)** è uno standard europeo (EN 13757) per la lettura remota di contatori e sensori.

### Caratteristiche
- Bus seriale a 2 fili
- Alimentazione e dati sullo stesso cavo
- Distanza fino a 350m (senza ripetitori)
- Fino a 250 dispositivi per bus
- Ampiamente usato in contabilizzazione calore/acqua

### ⚠️ Non è Modbus!
M-Bus ≠ Modbus. Sono protocolli completamente diversi.

---

## Requisiti Hardware

### 1. Convertitore USB M-Bus

Serve un convertitore per collegare il bus M-Bus al Raspberry Pi/NUC.

**Modelli Compatibili:**
- M-Bus Master USB
- Zenner USB dongles
- Qualsiasi convertitore basato su chip FTDI/CH340

**Verifica Compatibilità:**
Il dongle deve apparire come `/dev/ttyUSB0` o `/dev/ttyACM0` quando collegato.

### 2. Dispositivi M-Bus

**Compatibili:**
- Contabilizzatori di calore (Kamstrup, Zenner, Itron, Siemens, etc.)
- Contatori acqua M-Bus
- Contatori energia elettrica M-Bus
- Sensori temperatura M-Bus
- Qualsiasi dispositivo M-Bus standard

**Verifica Device:**
Cerca "M-Bus" nelle specifiche tecniche del tuo contatore.

### 3. Home Assistant

- **Richiesto:** Home Assistant OS o Supervised
- **Non funziona:** Home Assistant Container, Core
- **Architetture:** Raspberry Pi 3/4/5, Intel NUC, x86-64

---

## Installazione

### 1. Aggiungi Repository

[![Add Repository](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2FTUO_USERNAME%2Fhassio-addons-mbus2mqtt)

Oppure manualmente:
1. **Settings** → **Add-ons** → **Add-on Store**
2. Menu (3 puntini) → **Repositories**
3. Aggiungi: `https://github.com/TUO_USERNAME/hassio-addons-mbus2mqtt`

### 2. Installa Add-on

1. Aggiorna la pagina Add-on Store
2. Trova **M-Bus to MQTT**
3. Clicca **Install**
4. Attendi il completamento (può richiedere 5-10 minuti per il build)

### 3. Installa Mosquitto Broker

Se non lo hai già:
1. Add-on Store → **Mosquitto Broker**
2. Install → Start → Enable "Start on boot"

### 4. Configura MQTT Integration

1. **Settings** → **Devices & Services**
2. **Add Integration** → cerca **MQTT**
3. Inserisci: `core-mosquitto` / `1883`
4. Username/password (se configurato)

---

## Configurazione Dettagliata

### Parametri MQTT

#### mqtt_host
Indirizzo del broker MQTT con porta.

**Broker locale (consigliato):**
mqtt_host: "core-mosquitto:1883"

**Broker esterno:**
mqtt_host: "192.168.1.100:1883"

#### mqtt_user / mqtt_password

**Accesso anonimo:**
mqtt_user: ""
mqtt_password: ""

**Con autenticazione:**
mqtt_user: "homeassistant"
mqtt_password: "password_sicura"

### Parametri M-Bus

#### poll_interval

Intervallo tra letture in secondi (30-3600).

**Consigliato per tipo dispositivo:**
- **Contabilizzatori calore:** 1800 (30 min) - valori cambiano lentamente
- **Contatori acqua:** 3600 (1 ora) - uso sporadico
- **Contatori energia:** 300 (5 min) - monitoraggio real-time

poll_interval: 1800 # 30 minuti

**Non usare valori troppo bassi:** I contabilizzatori non aggiornano i valori ogni secondo!

#### serial_device

Percorso del dispositivo USB.

**Trovare il dispositivo:**

ls -la /dev/tty*

**Comuni:**

serial_device: "/dev/ttyUSB0" # FTDI, CH340
serial_device: "/dev/ttyACM0" # Alcuni convertitori

#### baudrate

Velocità comunicazione M-Bus.

**Valori disponibili:**
- 300 (alcuni dispositivi vecchi)
- 600
- 1200
- **2400** ← Default standard
- 4800
- 9600
- 19200
- 38400

baudrate: 2400


**Come scegliere:**
1. Prova 2400 (standard)
2. Se non funziona, prova 9600
3. Consulta manuale del dispositivo

### Dispositivi M-Bus

#### Struttura

mbus_devices:

device_name: "nome_univoco"
address: 0


#### device_name

Nome univoco del dispositivo.

**Regole:**
- Usa solo lettere, numeri, underscore
- Evita spazi (usa `_`)
- Deve essere univoco
- Diventerà parte del nome entity in HA

**Esempi:**

device_name: "contabilizzatore_soggiorno"
device_name: "contatore_acqua_principale"
device_name: "meter_apartment_2A"


#### address

Indirizzo M-Bus del dispositivo (0-250).

Ogni dispositivo sul bus ha un indirizzo univoco configurato in fabbrica o tramite programmazione.

**Come trovarlo:** Vedi sezione [Trovare Indirizzi M-Bus](#trovare-indirizzi-m-bus)

---

## Trovare Indirizzi M-Bus

### Metodo 1: Scan Bus

1. Installa add-on "Terminal & SSH" o "SSH & Web Terminal"
2. Avvia M-Bus to MQTT add-on
3. Accedi al container:

docker exec -it addon_local_mbus2mqtt sh


4. Esegui scan:

/libmbus/bin/mbus-serial-scan -b 2400 /dev/ttyUSB0

**Output esempio:**

Found a M-Bus device at address 0
Found a M-Bus device at address 1
Found a M-Bus device at address 5

### Metodo 2: Scan con Baudrate Diversi

Se non trova nulla con 2400:

/libmbus/bin/mbus-serial-scan -b 9600 /dev/ttyUSB0
/libmbus/bin/mbus-serial-scan -b 300 /dev/ttyUSB0

### Testare Lettura

Dopo aver trovato un indirizzo, testa la lettura:

/libmbus/bin/mbus-serial-request-data -b 2400 /dev/ttyUSB0 0

**Output:** XML con tutti i dati del dispositivo (energia, volume, potenza, etc.)

---

## Esempi Configurazione

### Esempio 1: Casa Singola (2 contabilizzatori)

mqtt_host: "core-mosquitto:1883"
mqtt_user: ""
mqtt_password: ""
poll_interval: 1800
serial_device: "/dev/ttyUSB0"
baudrate: 2400
mbus_devices:

device_name: "contabilizzatore_genitori"
address: 0

device_name: "contabilizzatore_andrea"
address: 1

### Esempio 2: Condominio (4 appartamenti)

mqtt_host: "192.168.1.100:1883"
mqtt_user: "mqtt_admin"
mqtt_password: "secure_password_123"
poll_interval: 3600
serial_device: "/dev/ttyUSB0"
baudrate: 2400
mbus_devices:

device_name: "apt_1A"
address: 0

device_name: "apt_1B"
address: 1

device_name: "apt_2A"
address: 2

device_name: "apt_2B"
address: 3


### Esempio 3: Monitoraggio Multiplo

mqtt_host: "core-mosquitto:1883"
mqtt_user: ""
mqtt_password: ""
poll_interval: 300
serial_device: "/dev/ttyUSB0"
baudrate: 2400
mbus_devices:

device_name: "contabilizzatore_riscaldamento"
address: 0

device_name: "contatore_acqua_fredda"
address: 1

device_name: "contatore_acqua_calda"
address: 2

device_name: "contatore_energia_elettrica"
address: 5


---

## Come Funziona

### 1. Avvio Add-on

Quando avvii l'add-on:

1. Script `run.sh` legge la configurazione da `/data/options.json`
2. Per ogni dispositivo in `mbus_devices`, avvia un processo Python separato
3. Delay di 2 secondi tra ogni avvio per evitare conflitti sul bus

### 2. Processo per Dispositivo

Ogni processo Python:

1. Si connette al broker MQTT
2. Esegue il comando libmbus per leggere il dispositivo
3. Parsa l'output XML
4. Pubblica discovery messages (una volta all'avvio)
5. Entra in loop: ogni `poll_interval` secondi legge e pubblica dati

### 3. Auto-Discovery

Al primo avvio, vengono pubblicate discovery messages MQTT:

homeassistant/sensor/contabilizzatore_genitori/energy_0/config
homeassistant/sensor/contabilizzatore_genitori/volume_1/config

Home Assistant le riceve e crea automaticamente le entità sensor.

### 4. Pubblicazione Dati

Ogni `poll_interval`, i valori vengono pubblicati:

mbus/contabilizzatore_genitori/Energy_0 {"value": 1234.5}
mbus/contabilizzatore_genitori/Volume_1 {"value": 5.2}

---

## MQTT Topics

### Discovery Topics

homeassistant/sensor/{device_name}/{unique_id}/config

**Payload esempio:**

{
"name": "Energy_0",
"uniq_id": "contabilizzatore_genitori_abc123",
"state_topic": "mbus/contabilizzatore_genitori/Energy_0",
"value_template": "{{ value_json.value }}",
"device_class": "energy",
"unit_of_measurement": "kWh",
"device": {
"identifiers": ["12345678"],
"name": "contabilizzatore_genitori",
"manufacturer": "Kamstrup"
}
}


### State Topics

mbus/{device_name}/{sensor_name}


**Payload esempio:**
{"value": 1234.5}


### Monitorare con MQTT Explorer

Installa [MQTT Explorer](http://mqtt-explorer.com/) per vedere tutti i topic.

Topics da monitorare:
- `homeassistant/sensor/#`
- `mbus/#`

---

## Troubleshooting

### Add-on non si avvia

**Sintomo:** Add-on esce subito dopo l'avvio

**Causa possibile:** Errore configurazione

**Soluzione:**
1. Vai al tab **Log** dell'add-on
2. Cerca messaggi di errore
3. Verifica configurazione (YAML syntax)

### Dongle USB non rilevato

**Sintomo:** Log mostra "No such file or directory: /dev/ttyUSB0"

**Verifica dispositivo:**
ha hardware info

oppure
ls -la /dev/tty*


**Soluzioni:**
- Scollega e ricollega il dongle
- Prova `/dev/ttyACM0` se presente
- Verifica con `dmesg` che il kernel lo rilevi

### Nessun dispositivo trovato con scan

**Sintomo:** `mbus-serial-scan` non trova dispositivi

**Verifica:**
1. **Cablaggio:** M-Bus+ e M-Bus- collegati correttamente
2. **Alimentazione:** Misura ~36V tra M-Bus+ e M-Bus- con multimetro
3. **Baudrate:** Prova 2400, 9600, 300
4. **Polarità:** Inverti M-Bus+ con M-Bus- se ancora non funziona

### Timeout durante lettura

**Sintomo:** "Error executing command" o timeout

**Causa:** Dispositivo non risponde o troppo lento

**Soluzioni:**
- Aumenta `poll_interval` a 3600 (1 ora)
- Verifica cablaggio
- Prova baudrate diverso
- Controlla distanza (<350m senza ripetitori)

### Sensori non compaiono in HA

**Verifica checklist:**
- [ ] Mosquitto Broker installato e avviato
- [ ] MQTT integration configurata
- [ ] Credenziali MQTT corrette
- [ ] Log add-on mostra "Published discovery"
- [ ] MQTT Explorer vede i topic `homeassistant/sensor/#`

### Letture inconsistenti

**Sintomo:** Valori cambiano drasticamente o errori casuali

**Causa:** Conflitti sul bus M-Bus

**Soluzione:**
- Aumenta `poll_interval`
- Non interrogare lo stesso dispositivo da più container/add-on
- Verifica cablaggio (interferenze, distanza)

---

## Advanced

### Cambiare Primary Address

Alcuni dispositivi permettono di cambiare indirizzo:

/libmbus/bin/mbus-serial-set-address -b 2400 /dev/ttyUSB0 OLD_ADDR NEW_ADDR

Usa con cautela! Puoi perdere il contatto con il dispositivo.

### Secondary Addressing

Per dispositivi configurati con secondary address:

/libmbus/bin/mbus-serial-request-data-multi-reply -b 2400 /dev/ttyUSB0


### Log Levels

Modifica `/mbus2mqtt/mbus2mqtt-home-assistant/mbus2mqtt-home-assistant.py`:

logging.basicConfig(level=logging.DEBUG) # Dettagli massimi
logging.basicConfig(level=logging.INFO) # Default
logging.basicConfig(level=logging.ERROR) # Solo errori


### Custom Device Class

Se l'add-on non riconosce correttamente il tipo di sensore, puoi modificare il mapping in `mbus2mqtt-home-assistant.py`:

device_class_mapping = {
'kWh': ('energy', 'k', None),
'm^3': ('volume', None, 'm³'),
'W': ('power', None, None),
'deg C': ('temperature', None, '°C'),
# Aggiungi il tuo qui
}


---

## FAQ

### Quanti dispositivi posso collegare?

Teoricamente fino a 250 dispositivi per bus M-Bus. In pratica:
- **1-10 dispositivi:** Nessun problema
- **10-50 dispositivi:** Aumenta `poll_interval`
- **50+ dispositivi:** Considera ripetitori M-Bus o bus multipli

### Posso usare TCP invece di seriale?

Sì! Se hai un gateway M-Bus-to-Ethernet, usa:

mbus_request_cmd: "/libmbus/bin/mbus-tcp-request-data 192.168.1.100 5000 0"


(Richiede modifica manuale dello script per ora)

### L'add-on funziona offline?

Sì, se usi broker MQTT locale (`core-mosquitto`). Non serve connessione internet.

### Posso leggere dispositivi con indirizzi > 250?

No, M-Bus standard supporta indirizzi 0-250 (primary addressing).

### Quanto è preciso il polling?

Il polling è best-effort. Ritardi di 1-2 secondi sono normali, soprattutto con dispositivi lenti.

### Posso usare LoRaWAN/WMBUS?

No, questo add-on supporta solo M-Bus cablato. LoRaWAN e Wireless M-Bus sono protocolli diversi.

---

## Supporto

- **Issues GitHub:** [Apri Issue](https://github.com/TUO_USERNAME/hassio-addons-mbus2mqtt/issues)
- **Home Assistant Community:** [Forum](https://community.home-assistant.io/)
- **Repository Originale:** [mbus2mqtt-home-assistant](https://gitlab.com/marcofl/mbus2mqtt-home-assistant)

---

## Credits

- Sviluppato basandosi su [mbus2mqtt-home-assistant](https://gitlab.com/marcofl/mbus2mqtt-home-assistant) di **Marco Fretz**
- Usa [libmbus](https://github.com/rscada/libmbus) per la comunicazione M-Bus
- Usa [paho-mqtt](https://github.com/eclipse/paho.mqtt.python) per MQTT

---

## License

MIT License - vedi [LICENSE](../LICENSE)





