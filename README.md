# Projekat: Pametni senzori sa Apache Kafka

## Opis projekta
Ovaj projekat implementira sistem pametnih senzora koji šalju podatke u realnom vremenu koristeći **Apache Kafka**. Sistem se sastoji od:

- **Producer-a**: simulira pametne senzore i šalje podatke u Kafka topic.
- **Consumer-a**: prima podatke sa Kafka topica i obrađuje ih.
- **Kafka cluster**: koristi se za pouzdano slanje i distribuciju poruka.

Projekat omogućava skalabilnu obradu podataka sa više senzora i demonstrira osnovne principe **stream processing**.

---

## Tehnologije

- **Python 3** (za producer i consumer)
- **Docker** i **Docker Compose** (za Kafka i Zookeeper)
- **Apache Kafka** (za messaging)
- **Stream processing koncepti**: producer → Kafka topic → consumer

---

## Struktura projekta

kafka-project/
├─ docker-compose.yml
├─ producer.py
├─ consumer.py
├─ README.md
└─ requirements.txt

- `docker-compose.yml` – definiše Zookeeper i Kafka servise
- `producer.py` – Python skripta koja šalje simulirane podatke senzora
- `consumer.py` – Python skripta koja prima podatke iz Kafka topica
- `requirements.txt` – lista Python biblioteka (`kafka-python`)

---

## Pokretanje sistema
Preuzimanje zavisnosti:
```bash
pip install -r requirements.txt
```

Pokreni Docker servise:
```bash
docker compose up -d
```

Pokrenuti Producer:
```bash
python3 producer.py
```

Pokrenuti Consumer u drugom terminalu:
```bash
python3 consumer.py
```
