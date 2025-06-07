<template>
  <div class="container">
    <div ref="areaA" class="area">A</div>
    <div ref="areaB" class="area">B</div>
    <div ref="areaC" class="area">C</div>
    <div ref="areaD" class="big-area">D</div>
    <div class="safety-facility safety-facility-left">{{ $t('map.safetyFacility') }}</div>
    <div class="safety-facility safety-facility-right">{{ $t('map.safetyFacility') }}</div>
    <canvas ref="canvas"></canvas>
    <div class="alert-icon-container" @click="showAlertLog">
      <div class="alert-icon">⚠️</div>
      <div class="alert-count" v-if="alertCount > 0">{{ alertCount }}</div>
    </div>
    <AlertComponent ref="alertComponent" />
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from 'vue'
import AlertComponent from './AlertComponent.vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const canvas = ref(null)

let ctx = null 

const alertCount = ref(0)
const alertComponent = ref(null)
const isAlertSimulationEnabled = ref(localStorage.getItem('alertSimulation') === 'true')

// 시설 상태 관리를 위한 ref
const facilityStatus = ref({
  A: { isOnFire: false, lastCheck: Date.now() },
  B: { isOnFire: false, lastCheck: Date.now() },
  C: { isOnFire: false, lastCheck: Date.now() },
  D: { isOnFire: false, lastCheck: Date.now() }
})

// 화재 발생 확률 (1%)
const FIRE_PROBABILITY = 0.0001

// 화재 로그를 저장할 배열
const fireLogs = ref([])

// 경보 활성화 함수 주입
const activateAlert = inject('activateAlert')

// 경보 시뮬레이션 설정 변경 이벤트 리스너
onMounted(() => {
  window.addEventListener('alertSimulationChanged', (event) => {
    isAlertSimulationEnabled.value = event.detail.enabled;
  });
});

function makePerimeterLoop(el) {
  const rect = el.getBoundingClientRect()
  const { left, top, width, height } = rect
  const right = left + width
  const bottom = top + height
  // 시계방향으로 네 모서리
  return [
    { x: left,  y: top    },
    { x: right, y: top    },
    { x: right, y: bottom },
    { x: left,  y: bottom },
    { x: left,  y: top    } // 루프를 닫기 위해 다시 시작점
  ]
}

// 시설 상태 업데이트 함수
function updateFacilityStatus() {
  if (!isAlertSimulationEnabled.value) return;
  
  Object.keys(facilityStatus.value).forEach(area => {
    if (Math.random() < FIRE_PROBABILITY) {
      facilityStatus.value[area].isOnFire = true
      // 화재 발생 시 로그 추가
      const log = {
        id: Date.now(),
        area,
        timestamp: new Date().toLocaleTimeString(),
        message: t('map.fireAlert', { area })
      }
      fireLogs.value.unshift(log)
      alertCount.value++
      // 전체화면 경보 활성화
      activateAlert(log.message)
    }
  })
}

// 경보 로그 표시 함수
function showAlertLog() {
  if (fireLogs.value.length > 0) {
    // 최근 5개의 로그만 표시
    const recentLogs = fireLogs.value.slice(0, 5)
    const logMessage = recentLogs
      .map(log => `[${log.timestamp}] ${log.message}`)
      .join('\n')
    alertComponent.value.activateAlert(logMessage)
  } else {
    alertComponent.value.activateAlert(t('map.noDanger'))
  }
}

// 애니메이션 함수 수정
function animate() {
  ctx.clearRect(0, 0, canvas.value.width, canvas.value.height)

  // 시설 상태 업데이트
  updateFacilityStatus()

  requestAnimationFrame(animate)
}

</script>

<style scoped>
.container {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

.big-area {
  position: absolute;
  width: 700px; /* 더 큰 가로로 영역 표시 */
  height: 300px; /* 세로로 더 길게 */
  background: #444;
  color: white;
  font-weight: bold;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 8px;
  user-select: none;
  pointer-events: none;
}

.area {
  position: absolute;
  width: 200px;
  height: 300px; /* 세로로 더 길게 */
  background: #445;
  color: white;
  font-weight: bold;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 8px;
  user-select: none;
  pointer-events: none;
}

/* 영역 위치 조정 */
.area:nth-of-type(1) {
  top: 15%;
  left: 15%;
}

.area:nth-of-type(2) {
  top: 15%;
  left: 30%;
}

.area:nth-of-type(3) {
  top: 15%;
  left: 45%;
}

.big-area:nth-of-type(4) {
  top: 50%;
  left: 15%;
}

/* 소방시설 스타일 수정 */
.safety-facility {
  position: absolute;
  width: 70px;
  height: 70px;
  background: #ff4444;
  color: white;
  font-weight: bold;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 8px;
  user-select: none;
  pointer-events: none;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  text-align: center;
  padding: 5px;
  font-size: 15px;
  line-height: 1.2;
  word-break: keep-all;
}

.safety-facility-left {
  bottom: 100px;
  left: 150px;
}

.safety-facility-right {
  top: 20px;
  right: 700px;
}

/* 캔버스는 화면 전체 */
canvas {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 0;
}

.area.on-fire, .big-area.on-fire {
  animation: fire-alert 1s infinite;
}

@keyframes fire-alert {
  0% { box-shadow: 0 0 10px #ff0000; }
  50% { box-shadow: 0 0 20px #ff0000; }
  100% { box-shadow: 0 0 10px #ff0000; }
}

.alert-icon-container {
  position: absolute;
  top: 20px;
  left: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  z-index: 1000;
}

.alert-icon {
  font-size: 32px;
}

.alert-count {
  background-color: #dc3545;
  color: white;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 14px;
  font-weight: bold;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}
</style>