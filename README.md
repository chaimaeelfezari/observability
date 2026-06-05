# Observability Stack

Infrastructure complète de centralisation des logs, métriques et traces.

## Architecture
app / node-exporter → OTel Collector → Tempo (traces)
app / node-exporter → Prometheus (métriques)
app containers → Promtail → Loki (logs)
Prometheus + Loki + Tempo → Grafana (visualisation)

## Services

| Service | Port | Rôle |
|---------|------|------|
| Prometheus | 9090 | Collecte métriques |
| Grafana | 3000 | Visualisation |
| Loki | 3100 | Agrégation logs |
| Promtail | 9080 | Agent logs |
| Tempo | 3200 | Traces distribuées |
| OTel Collector | 4317/4318 | Réception traces |
| Node Exporter | 9100 | Métriques système |
| Python App | 8000 | App demo |

## Démarrage rapide

```bash
git clone https://github.com/chaimaeelfezari/observability
cd observability
docker compose up -d
```

## Runbooks

### Alerte InstanceDown
- **Cause** : container arrêté
- **Action** : `docker compose ps` → `docker compose restart <service>`

### Alerte HighCPU
- **Cause** : CPU > 80% depuis 2 min
- **Action** : vérifier les process dans `docker stats`

## Accès

- Grafana : http://localhost:3000 (admin/admin)
- Prometheus : http://localhost:9090