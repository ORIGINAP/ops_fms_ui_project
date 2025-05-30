<template>
  <div class="container">
    <!-- 세로 긴 영역 3개 -->
    <div class="area" ref="areaA">A</div>
    <div class="area" ref="areaB">B</div>
    <div class="area" ref="areaC">C</div>

    <!-- 캔버스: 로봇 이동과 선 그리기 -->
    <canvas ref="canvas" class="canvas-layer"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const canvas = ref(null)
const areaA = ref(null)
const areaB = ref(null)
const areaC = ref(null)

const robot = {
  x: 0,
  y: 0,
  size: 16,
  speed: 1,
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
  ctx.strokeStyle = '#ccc'
  ctx.lineWidth = 2
  ctx.beginPath()
  ctx.moveTo(path[0].x, path[0].y)
  for (let i = 1; i < path.length; i++) {
    ctx.lineTo(path[i].x, path[i].y)
  }
  ctx.closePath()
  ctx.stroke()
}

function drawRobot() {
  ctx.fillStyle = 'green'
  ctx.fillRect(robot.x - robot.size / 2, robot.y - robot.size / 2, robot.size, robot.size)
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
    getCenter(areaA.value),
    getCenter(areaB.value),
    getCenter(areaC.value)
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
  background-color: #1a1a1a;
}

.area {
  width: 120px;
  height: 300px;
  background-color: #444;
  position: absolute;
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
  font-size: 32px;
  font-weight: bold;
  border-radius: 8px;
}

/* 세 영역 위치 고정 */
.area:nth-of-type(1) { top: 10%; left: 10%; }   /* A */
.area:nth-of-type(2) { top: 10%; left: 40%; }   /* B */
.area:nth-of-type(3) { top: 10%; left: 70%; }   /* C */

.canvas-layer {
  position: absolute;
  top: 0;
  left: 0;
  pointer-events: none;
  z-index: 0;
}
</style>
