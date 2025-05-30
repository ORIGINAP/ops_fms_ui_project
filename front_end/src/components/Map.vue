<template>
  <div class="container">
    <div ref="areaA" class="area">A</div>
    <div ref="areaB" class="area">B</div>
    <div ref="areaC" class="area">C</div>
    <div ref="areaC" class="big-area">D</div>
    <canvas ref="canvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const areaA = ref(null)
const areaB = ref(null)
const areaC = ref(null)
const areaD = ref(null)
const canvas = ref(null)

let ctx = null

const NUM_ROBOTS = 5
const robots = []

// 영역 중심 좌표 구하기 함수
function getCenter(el) {
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

    result.push(from)
    result.push({ x: from.x, y: to.y }) // 수직 → 수평 이동 (or 꺾임)
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

function animate() {
  ctx.clearRect(0, 0, canvas.value.width, canvas.value.height)

  // 영역 그리기
  drawArea(areaA.value, 'A')
  drawArea(areaB.value, 'B')
  drawArea(areaC.value, 'C')

  // 모든 로봇 그리기 및 이동
  for (const robot of robots) {
    moveRobot(robot)
    drawPath(robot.path) // 각 로봇 경로 시각화(원한다면 제거 가능)
    drawRobot(robot)
  }

  requestAnimationFrame(animate)
}

onMounted(() => {
  const canvasEl = canvas.value
  canvasEl.width = window.innerWidth
  canvasEl.height = window.innerHeight
  ctx = canvasEl.getContext('2d')

  // 영역 중심점들 가져오기
  const rawCenters = [
    getCenter(areaA.value),
    getCenter(areaB.value),
    getCenter(areaC.value),
    getCenter(areaA.value) // 순환 경로 만들기 위해 다시 A로
  ]

  // 90도 꺾이는 경로 생성
  const basePath = makeRightAnglePath(rawCenters)

  // 여러 로봇 독립적으로 생성
  for (let i = 0; i < NUM_ROBOTS; i++) {
    const offsetX = (i % 3) * 12
    const offsetY = (i % 3) * 8

    robots.push({
      id: i,
      x: basePath[0].x + offsetX,
      y: basePath[0].y + offsetY,
      size: 16,
      speed: 0.7 + Math.random() * 0.3, // 속도 약간씩 다르게
      path: basePath.map(p => ({ ...p })), // 완전 독립 복제
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
  width: 300px; /* 더 큰 가로로 영역 표시 */
  height: 180px; /* 세로로 더 길게 */
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
  width: 100px;
  height: 180px; /* 세로로 더 길게 */
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

/* 캔버스는 화면 전체 */
canvas {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 0;
}
</style>
