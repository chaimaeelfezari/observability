#!/bin/bash
# ============================================
# CHAOS DEMO - Observability Stack
# Scénario : panne → alerte → trace → log
# ============================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔══════════════════════════════════════╗${NC}"
echo -e "${BLUE}║        CHAOS DEMO - LIVE             ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════╝${NC}"
echo ""

# ─── SCÉNARIO 1 : KILL CONTAINER ───────────────────────────────
scenario_kill() {
  echo -e "${RED}[CHAOS 1] Kill python-app container...${NC}"
  docker stop python-app
  echo -e "${YELLOW}⏳ Attendre l'alerte InstanceDown dans Prometheus (1 min)...${NC}"
  echo -e "${YELLOW}👉 Ouvrir : http://localhost:9090/alerts${NC}"
  sleep 10
  echo -e "${GREEN}[RECOVERY] Restart python-app...${NC}"
  docker start python-app
  echo -e "${GREEN}✅ Container redémarré — vérifier Grafana http://localhost:3000${NC}"
  echo ""
}

# ─── SCÉNARIO 2 : STRESS CPU ───────────────────────────────────
scenario_cpu() {
  echo -e "${RED}[CHAOS 2] Stress CPU pendant 2 minutes...${NC}"
  echo -e "${YELLOW}👉 Surveiller : http://localhost:3000 → CPU Usage %${NC}"
  
  # stress-ng si dispo, sinon yes
  if command -v stress-ng &> /dev/null; then
    stress-ng --cpu 4 --timeout 120s &
    STRESS_PID=$!
  else
    # fallback : boucles infinies
    for i in 1 2 3 4; do
      yes > /dev/null &
      PIDS+=($!)
    done
    sleep 120
    kill "${PIDS[@]}" 2>/dev/null
    echo -e "${GREEN}✅ CPU stress stoppé${NC}"
    return
  fi

  sleep 120
  kill $STRESS_PID 2>/dev/null
  echo -e "${GREEN}✅ CPU stress stoppé — alerte HighCPU devrait avoir fired${NC}"
  echo ""
}

# ─── SCÉNARIO 3 : KILL + CPU (FULL DEMO) ──────────────────────
scenario_full() {
  echo -e "${RED}╔══════════════════════════════════════╗${NC}"
  echo -e "${RED}║     FULL CHAOS - TOUT EN MÊME TEMPS  ║${NC}"
  echo -e "${RED}╚══════════════════════════════════════╝${NC}"
  
  echo -e "${YELLOW}[STEP 1] Stress CPU...${NC}"
  yes > /dev/null & YES_PID=$!
  yes > /dev/null & YES_PID2=$!

  echo -e "${YELLOW}[STEP 2] Kill python-app...${NC}"
  docker stop python-app

  echo ""
  echo -e "${BLUE}═══ WHAT TO SHOW NOW ════════════════════${NC}"
  echo -e "  📊 Prometheus alerts : http://localhost:9090/alerts"
  echo -e "  📈 Grafana CPU spike : http://localhost:3000"
  echo -e "  🔍 Loki logs erreurs : http://localhost:3000 → Explore → Loki"
  echo -e "  🔗 Tempo traces      : http://localhost:3000 → Explore → Tempo"
  echo -e "${BLUE}═════════════════════════════════════════${NC}"
  echo ""

  echo -e "${YELLOW}⏳ 60 secondes de chaos...${NC}"
  sleep 60

  echo -e "${GREEN}[RECOVERY] Tout remet en ordre...${NC}"
  kill $YES_PID $YES_PID2 2>/dev/null
  docker start python-app
  echo -e "${GREEN}✅ Stack recovered !${NC}"
}

# ─── MENU ──────────────────────────────────────────────────────
echo "Choisir un scénario :"
echo "  1) Kill container    → alerte InstanceDown"
echo "  2) Stress CPU        → alerte HighCPU"
echo "  3) Full chaos demo   → tout en même temps (recommandé pour soutenance)"
echo ""
read -p "Choix [1/2/3] : " CHOICE

case $CHOICE in
  1) scenario_kill ;;
  2) scenario_cpu ;;
  3) scenario_full ;;
  *) echo "Choix invalide"; exit 1 ;;
esac