<template>
  <div class="container">
    <div ref="areaA" class="area">A</div>
    <div ref="areaB" class="area">B</div>
    <div ref="areaC" class="area">C</div>
    <div ref="areaD" class="big-area">D</div>
    <div class="safety-facility safety-facility-left">소방시설</div>
    <div class="safety-facility safety-facility-right">소방시설</div>
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

const areaA = ref(null)
const areaB = ref(null)
const areaC = ref(null)
const areaD = ref(null)
const canvas = ref(null)

let ctx = null 

const NUM_ROBOTS = 5
const robots = []
const api_robot = ref({"name": "", "version": "","description":""})

const alertCount = ref(0)
const alertComponent = ref(null)

// 시설 상태 관리를 위한 ref
const facilityStatus = ref({
  A: { isOnFire: false, lastCheck: Date.now() },
  B: { isOnFire: false, lastCheck: Date.now() },
  C: { isOnFire: false, lastCheck: Date.now() },
  D: { isOnFire: false, lastCheck: Date.now() }
})

// 화재 발생 확률 (1%)
const FIRE_PROBABILITY = 0.0000000000000005

// 화재 로그를 저장할 배열
const fireLogs = ref([])

// 경보 활성화 함수 주입
const activateAlert = inject('activateAlert')

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

// 영역 중심 좌표 구하기 함수
// 각 영역의 출구 방향을 기준으로 경계 근처 좌표 반환
function getEdgePoint(el) {
  const rect = el.getBoundingClientRect()
  return {
    x: rect.left + rect.width / 2,
    y: rect.top + rect.height / 2
  }
}


// 두 지점 사이 90도 꺾인 경로 만들기 (ㄱ자 형태)
function makeRightAnglePath(points) {
  const result = []
  for (let i = 0; i < points.length - 1; i++) {
    const from = points[i]
    const to = points[i + 1]

    const mid = {
      x: (from.x + to.x) / 2,
      y: (from.y + to.y) / 2
    }

    result.push(from)
    result.push({ x: mid.x, y: from.y }) // 수평
    result.push({ x: mid.x, y: to.y })   // 수직
    result.push(to)
  }
  return result
}


function drawArea(areaEl, label) {
  const rect = areaEl.getBoundingClientRect()
  ctx.fillStyle = '#444' // 어두운 회색
  ctx.fillRect(rect.left, rect.top, rect.width, rect.height)

  ctx.fillStyle = '#fff' // 흰색 글씨
  ctx.font = 'bold 18px Arial'
  ctx.textAlign = 'center'
  ctx.textBaseline = 'middle'
  ctx.fillText(label, rect.left + rect.width / 2, rect.top + rect.height / 2)
}

function drawRobot(robot) {
  ctx.fillStyle = 'limegreen'
  ctx.fillRect(robot.x - robot.size / 2, robot.y - robot.size / 2, robot.size, robot.size)
}

function drawPath(path) {
  ctx.strokeStyle = '#0f0' // 초록색 선
  ctx.lineWidth = 2
  ctx.beginPath()
  for (let i = 0; i < path.length; i++) {
    const p = path[i]
    if (i === 0) ctx.moveTo(p.x, p.y)
    else ctx.lineTo(p.x, p.y)
  }
  ctx.stroke()
}

// 로봇 이동 함수 (독립 동작)
function moveRobot(robot) {
  const target = robot.path[robot.targetIndex]
  const dx = target.x - robot.x
  const dy = target.y - robot.y
  const dist = Math.hypot(dx, dy)

  if (dist < robot.speed) {
    robot.x = target.x
    robot.y = target.y
    robot.logs.push({ reached: { ...target }, time: Date.now() }) // 위치 도착 로그
    robot.targetIndex = (robot.targetIndex + 1) % robot.path.length
  } else {
    robot.x += (dx / dist) * robot.speed
    robot.y += (dy / dist) * robot.speed
  }
}

// 시설 상태 업데이트 함수
function updateFacilityStatus() {
  Object.keys(facilityStatus.value).forEach(area => {
    if (Math.random() < FIRE_PROBABILITY) {
      facilityStatus.value[area].isOnFire = true
      // 화재 발생 시 로그 추가
      const log = {
        id: Date.now(),
        area,
        timestamp: new Date().toLocaleTimeString(),
        message: `${area} 영역에서 화재가 발생했습니다!`
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
    alertComponent.value.activateAlert('현재 감지된 위험 없음')
  }
}

// 애니메이션 함수 수정
function animate() {
  ctx.clearRect(0, 0, canvas.value.width, canvas.value.height)

  // 영역 그리기
  drawArea(areaA.value, 'A')
  drawArea(areaB.value, 'B')
  drawArea(areaC.value, 'C')
  drawArea(areaD.value, 'D')

  // 모든 로봇 그리기 및 이동
  for (const robot of robots) {
    moveRobot(robot)
    drawPath(robot.path) // 각 로봇 경로 시각화(원한다면 제거 가능)
    drawRobot(robot)
  }

  // 시설 상태 업데이트
  updateFacilityStatus()

  requestAnimationFrame(animate)
}

onMounted(() => {
  const canvasEl = canvas.value
  canvasEl.width  = window.innerWidth
  canvasEl.height = window.innerHeight
  ctx = canvasEl.getContext('2d')

  // 각 영역을 한 바퀴 도는 루프들을 순서대로 연결
  const loops = [
    makePerimeterLoop(areaA.value),
    makePerimeterLoop(areaB.value),
    makePerimeterLoop(areaC.value),
    makePerimeterLoop(areaD.value)
  ]
  // A → B → C → D → A 로 이어 붙이기
  let basePath = []
  loops.forEach(loop => { basePath = basePath.concat(loop) })
  // 마지막에 A의 시작점을 한 번 더 추가해 순환 고리 완성
  basePath.push(loops[0][0])

  // 여러 로봇 독립적으로 생성
  for (let i = 0; i < NUM_ROBOTS; i++) {
    robots.push({
      id: i,
      x: basePath[0].x + 5 * i, // 시작점에 약간씩 오프셋
      y: basePath[0].y + 3 * i,
      size: 16,
      speed: 0.7 + Math.random() * 0.3,
      path: basePath.map(p => ({ ...p })),
      targetIndex: 1,
      logs: []
    })
  }

  animate()
})
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