<template>
  <div class="container">
    <!-- 영역 컴포넌트들 (위치 고정) -->
    <div class="area" ref="area1">1</div>
    <div class="area" ref="area2">2</div>
    <div class="area" ref="area3">3</div>

    <!-- 캔버스 레이어 -->
    <canvas ref="canvas" class="canvas-layer"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const canvas = ref(null)
const area1 = ref(null)
const area2 = ref(null)
const area3 = ref(null)

const robot = {
  x: 0,
  y: 0,
  speed: 2, // 픽셀 단위 속도
  path: [],
  targetIndex: 1
}

let ctx, animationId

function getCenter(el) {
  const rect = el.getBoundingClientRect()
  return {
    x: rect.left + rect.width / 2,
    y: rect.top + rect.height / 2
  }
}

function drawPath(path) {
  ctx.strokeStyle = '#999'
  ctx.lineWidth = 2
  ctx.beginPath()
  ctx.moveTo(path[0].x, path[0].y)
  for (let i = 1; i < path.length; i++) {
    ctx.lineTo(path[i].x, path[i].y)
  }
  ctx.stroke()
}

function drawRobot() {
  ctx.beginPath()
  ctx.fillStyle = 'red'
  ctx.arc(robot.x, robot.y, 10, 0, Math.PI * 2)
  ctx.fill()
}

function moveRobot() {
  const target = robot.path[robot.targetIndex]
  const dx = target.x - robot.x
  const dy = target.y - robot.y
  const distance = Math.sqrt(dx * dx + dy * dy)

  if (distance < robot.speed) {
    robot.x = target.x
    robot.y = target.y
    robot.targetIndex = (robot.targetIndex + 1) % robot.path.length
  } else {
    robot.x += (dx / distance) * robot.speed
    robot.y += (dy / distance) * robot.speed
  }
}

function animate() {
  ctx.clearRect(0, 0, canvas.value.width, canvas.value.height)

  drawPath(robot.path)
  moveRobot()
  drawRobot()

  animationId = requestAnimationFrame(animate)
}

onMounted(() => {
  const canvasEl = canvas.value
  canvasEl.width = window.innerWidth
  canvasEl.height = window.innerHeight
  ctx = canvasEl.getContext('2d')

  robot.path = [
    getCenter(area1.value),
    getCenter(area2.value),
    getCenter(area3.value)
  ]
  robot.x = robot.path[0].x
  robot.y = robot.path[0].y

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
.area {
  width: 100px;
  height: 100px;
  background-color: lightblue;
  position: absolute;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: bold;
  font-size: 24px;
}
.area:nth-child(1) { top: 10%; left: 10%; }
.area:nth-child(2) { top: 40%; left: 60%; }
.area:nth-child(3) { top: 70%; left: 20%; }

.canvas-layer {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 0;
  pointer-events: none;
}
</style>
