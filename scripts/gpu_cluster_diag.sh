#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# gpu_cluster_diag.sh
#   3노드(master/n1/n3) 24-GPU 클러스터 진단 스크립트
#
#   회신 문서의 ○○ placeholder를 채우기 위한 실측값을 수집합니다.
#   읽기 전용 점검만 수행하며 시스템 설정을 변경하지 않습니다.
#
#   사용법:  ./gpu_cluster_diag.sh [노드1 노드2 ...]     (기본: master n1 n3)
#   결과:    ./gpu_diag_<타임스탬프>/ 디렉터리에 저장
# ---------------------------------------------------------------------------
set -uo pipefail

NODES=("${@:-}")
[[ -z "${NODES[0]:-}" ]] && NODES=(master n1 n3)

OUT="./gpu_diag_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUT"
REPORT="$OUT/report.txt"

log()  { echo -e "$*" | tee -a "$REPORT"; }
head1() { log "\n===============================================================";
          log "$*";
          log "==============================================================="; }

# 로컬/원격 공통 실행 래퍼
on() {
  local host="$1"; shift
  if [[ "$host" == "$(hostname)" || "$host" == "localhost" ]]; then
    bash -lc "$*" 2>&1
  else
    ssh -o BatchMode=yes -o ConnectTimeout=5 "$host" "$*" 2>&1
  fi
}

log "GPU 클러스터 진단 리포트"
log "수집 시각 : $(date -Is)"
log "대상 노드 : ${NODES[*]}"

# ---------------------------------------------------------------------------
head1 "[1] 노드 간 SSH 도달성"
# ---------------------------------------------------------------------------
for h in "${NODES[@]}"; do
  if on "$h" 'echo ok' | grep -q ok; then log "  $h : 접속 OK"; else log "  $h : ★접속 실패★"; fi
done

# ---------------------------------------------------------------------------
head1 "[2] GPU 인벤토리 (노드별 GPU 수 / 모델 / 드라이버)"
# ---------------------------------------------------------------------------
TOTAL=0
for h in "${NODES[@]}"; do
  log "\n--- $h ---"
  out=$(on "$h" 'nvidia-smi --query-gpu=index,name,memory.total,driver_version --format=csv,noheader')
  log "$out"
  n=$(echo "$out" | grep -c ',' )
  log "  → GPU 수: $n"
  TOTAL=$((TOTAL + n))
done
log "\n★ 전체 GPU 합계: $TOTAL 기  (기대값: 24)"

# ---------------------------------------------------------------------------
head1 "[3] 소프트웨어 버전 정합성 (3노드 완전 일치해야 정상)"
# ---------------------------------------------------------------------------
for h in "${NODES[@]}"; do
  log "\n--- $h ---"
  log "$(on "$h" 'nvidia-smi --query-gpu=driver_version --format=csv,noheader | head -1 | sed "s/^/  driver : /"')"
  log "$(on "$h" 'nvcc --version 2>/dev/null | grep -o "release.*" | sed "s/^/  cuda   : /" || echo "  cuda   : nvcc 없음"')"
  log "$(on "$h" 'python3 -c "import torch;print(\"  torch  :\",torch.__version__);print(\"  nccl   :\",torch.cuda.nccl.version())" 2>/dev/null || echo "  torch  : 미설치"')"
done
log "\n※ 위 4개 값이 노드마다 다르면 멀티노드 학습이 실패합니다."

# ---------------------------------------------------------------------------
head1 "[4] 네트워크 인터페이스 및 RDMA(InfiniBand/RoCE) 가용성  ★최우선 확인★"
# ---------------------------------------------------------------------------
for h in "${NODES[@]}"; do
  log "\n--- $h ---"
  log "[인터페이스]"; log "$(on "$h" 'ip -br addr | grep -v " lo "')"
  log "[IB 장치]";    log "$(on "$h" 'ibstat -l 2>/dev/null || echo "  IB 장치 없음 (RDMA 미가용 가능성)"')"
  log "[IB 링크]";    log "$(on "$h" 'ibstatus 2>/dev/null | grep -E "Infiniband|state|rate" || echo "  N/A"')"
  log "[IB↔NIC 매핑]"; log "$(on "$h" 'ibdev2netdev 2>/dev/null || echo "  N/A"')"
done
log "\n※ IB 장치가 없고 이더넷만 존재하면 NCCL이 TCP 소켓으로 폴백되어"
log "   멀티노드 학습 속도가 실용 수준에 미달합니다 (문서 §2-1 참조)."

# ---------------------------------------------------------------------------
head1 "[5] 노드 간 대역폭 실측 (iperf3, 8 스트림)"
# ---------------------------------------------------------------------------
if command -v iperf3 >/dev/null 2>&1; then
  SRC="${NODES[0]}"
  for h in "${NODES[@]:1}"; do
    log "\n--- $SRC → $h ---"
    on "$h" 'pkill -f "iperf3 -s" ; nohup iperf3 -s -D >/dev/null 2>&1; sleep 1'
    res=$(on "$SRC" "iperf3 -c $h -P 8 -t 10 2>&1 | tail -5")
    log "$res"
    on "$h" 'pkill -f "iperf3 -s"' >/dev/null
  done
  log "\n판정: 100Gbps↑ 정상 / 10~25Gbps 제한적 / 1Gbps↓ 멀티노드 학습 불가"
else
  log "  iperf3 미설치 → 설치 후 재실행 권장:  apt-get install -y iperf3"
fi

# ---------------------------------------------------------------------------
head1 "[6] 방화벽 / 호스트명 해석 / 랑데부 포트(29500)"
# ---------------------------------------------------------------------------
for h in "${NODES[@]}"; do
  log "\n--- $h ---"
  log "[방화벽] $(on "$h" 'systemctl is-active firewalld 2>/dev/null; systemctl is-active ufw 2>/dev/null' | tr '\n' ' ')"
  log "[호스트명 해석]"; log "$(on "$h" "getent hosts ${NODES[*]} || echo '  ★해석 실패 - /etc/hosts 확인 필요★'")"
done
log "\n[결번 노드(n2) 잔재 설정 점검]"
for h in "${NODES[@]}"; do
  log "  $h : $(on "$h" 'grep -l "n2" /etc/hosts /etc/slurm/slurm.conf ~/.ssh/config 2>/dev/null | tr "\n" " " || true')"
done
log "※ 위에 파일 경로가 출력되면 존재하지 않는 n2를 기다리다 타임아웃될 수 있습니다."

# ---------------------------------------------------------------------------
head1 "[7] 현재 GPU 사용 현황 스냅샷 (활용률 근거자료)"
# ---------------------------------------------------------------------------
for h in "${NODES[@]}"; do
  log "\n--- $h ---"
  log "$(on "$h" 'nvidia-smi --query-gpu=index,utilization.gpu,utilization.memory,memory.used,memory.total,power.draw,power.limit --format=csv')"
  log "[실행 중 프로세스]"
  log "$(on "$h" 'nvidia-smi --query-compute-apps=gpu_uuid,pid,used_memory --format=csv,noheader || echo "  없음(유휴)"')"
done

# ---------------------------------------------------------------------------
head1 "[8] 60초 평균 Utilization / 할당률 (회신 문서 §1-2 기재용)"
# ---------------------------------------------------------------------------
for h in "${NODES[@]}"; do
  log "\n--- $h (60초, 1초 간격 샘플링) ---"
  on "$h" 'nvidia-smi --query-gpu=index,utilization.gpu,memory.used --format=csv,noheader,nounits -l 1 -c 60' \
    > "$OUT/util_$h.csv" 2>&1
  awk -F', *' '
    $1 ~ /^[0-9]+$/ && $2 ~ /^[0-9]+$/ {u[$1]+=$2; m[$1]+=$3; c[$1]++}
    END{ tu=0; n=0;
         for(i in c){printf "  GPU %s : 평균 Util %.1f%% , 평균 MemUsed %.0f MiB\n", i, u[i]/c[i], m[i]/c[i];
                     tu+=u[i]/c[i]; n++}
         if(n>0) printf "  ▶ 노드 평균 Utilization : %.1f%%  (GPU %d기 기준)\n", tu/n, n;
         else    printf "  ※ 유효한 샘플 없음 (nvidia-smi 실행 불가)\n" }
  ' "$OUT/util_$h.csv" | tee -a "$REPORT"
done

# ---------------------------------------------------------------------------
head1 "[9] 스케줄러 구성 여부"
# ---------------------------------------------------------------------------
log "[Slurm]      $(command -v sinfo >/dev/null && sinfo -h 2>&1 | head -5 || echo '미설치')"
log "[Kubernetes] $(command -v kubectl >/dev/null && kubectl get nodes 2>&1 | head -5 || echo '미설치')"
log "※ 스케줄러가 없으면 유휴 시간에 대기 잡을 자동 투입할 수 없어 가동률이 낮아집니다."

# ---------------------------------------------------------------------------
head1 "[10] 공유 스토리지 여부"
# ---------------------------------------------------------------------------
for h in "${NODES[@]}"; do
  r=$(on "$h" 'mount | grep -E "nfs|lustre|gpfs|beegfs|ceph" | head -3')
  log "  $h : ${r:-공유 스토리지 미탑재}"
done

# ---------------------------------------------------------------------------
head1 "[요약] 회신 문서에 기재할 항목"
# ---------------------------------------------------------------------------
log "  1. 전체 GPU 수            : $TOTAL 기"
log "  2. RDMA(IB/RoCE) 가용     : [4] 섹션 확인"
log "  3. 노드 간 실측 대역폭    : [5] 섹션 확인"
log "  4. 버전 정합성            : [3] 섹션 확인"
log "  5. 평균 GPU Utilization   : [8] 섹션 확인"
log "  6. n2 결번 잔재 설정      : [6] 섹션 확인"
log "\n리포트 저장 위치: $REPORT"
log "\n[다음 단계] 위 항목이 모두 정상이면 nccl-tests로 24-GPU 집합통신을 검증하십시오:"
log "  mpirun -np 24 -H ${NODES[0]}:8,${NODES[1]:-n1}:8,${NODES[2]:-n3}:8 \\"
log "    -x NCCL_DEBUG=INFO -x NCCL_SOCKET_IFNAME=<데이터망 IF> \\"
log "    ./build/all_reduce_perf -b 8 -e 8G -f 2 -g 1"

echo
echo "완료. 결과: $REPORT"
