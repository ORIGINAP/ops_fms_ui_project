<template>
  <div class="container">
    <!-- 영역 A, B, C -->
    <div class="area" ref="areaA">A</div>
    <div class="area" ref="areaB">B</div>
    <div class="area" ref="areaC">C</div>

    <!-- 캔버스 -->
    <canvas ref="canvas" class="canvas-layer"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const canvas = ref(null)
const areaA = ref(null)
const areaB = ref(null)
const areaC = ref(null)

let ctx, animationId

const NUM_ROBOTS = 5
const robots = []

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

function drawRobot(robot) {
  ctx.fillStyle = 'green'
  ctx.fillRect(robot.x - robot.size / 2, robot.y - robot.size / 2, robot.size, robot.size)
}

function moveRobot(robot) {
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
  if (robots[0]) drawPath(robots[0].path)

  for (const robot of robots) {
    moveRobot(robot)
    drawRobot(robot)
  }

  animationId = requestAnimationFrame(animate)
}

onMounted(() => {
  const canvasEl = canvas.value
  canvasEl.width = window.innerWidth
  canvasEl.height = window.innerHeight
  ctx = canvasEl.getContext('2d')

  const path = [
    getCenter(areaA.value),
    getCenter(areaB.value),
    getCenter(areaC.value)
  ]

  // 로봇 여러 개 초기화
  for (let i = 0; i < NUM_ROBOTS; i++) {
    const delay = i * 40 // 시간차로 시작 위치 다르게
    robots.push({
      x: path[0].x,
      y: path[0].y,
      size: 16,
      speed: 1,
      path,
      targetIndex: 1,
      delay
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
