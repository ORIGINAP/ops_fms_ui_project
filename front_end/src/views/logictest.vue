<template>
  <div>
    <canvas ref="canvas"
            @click="addPoint"
            width="800"
            height="500"
            style="border: 2px solid black; display: block; margin: auto;" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const canvas = ref(null)
let ctx = null
let points = []
let robot = { x: 0, y: 0, index: 0, progress: 0 }
const ROBOT_SPEED = 2

onMounted(() => {
  ctx = canvas.value.getContext('2d')
  animate()
})

// 점 추가
function addPoint(event) {
  const rect = canvas.value.getBoundingClientRect()
  const x = event.clientX - rect.left
  const y = event.clientY - rect.top

  points.push({ x, y })

  // 첫 점이면 로봇 위치도 초기화
  if (points.length === 1) {
    robot.x = x
    robot.y = y
    robot.index = 0
    robot.progress = 0
  }
}

function getDistance(a, b) {
  return Math.hypot(b.x - a.x, b.y - a.y)
}

function updateRobot() {
  if (points.length < 2) return

  const current = points[robot.index]
  const next = points[robot.index + 1]
  const dist = getDistance(current, next)

  robot.progress += ROBOT_SPEED
  if (robot.progress >= dist) {
    robot.index++
    if (robot.index >= points.length - 1) {
      robot.index = 0
      robot.progress = 0
      return
    }
    robot.progress = 0
  }

  const ratio = robot.progress / dist
  robot.x = current.x + (next.x - current.x) * ratio
  robot.y = current.y + (next.y - current.y) * ratio
}

function draw() {
  ctx.clearRect(0, 0, canvas.value.width, canvas.value.height)

  // 점
  ctx.fillStyle = 'red'
  points.forEach(p => {
    ctx.beginPath()
    ctx.arc(p.x, p.y, 5, 0, Math.PI * 2)
    ctx.fill()
  })

  // 선
  if (points.length >= 2) {
    ctx.strokeStyle = 'black'
    ctx.lineWidth = 2
    ctx.beginPath()
    ctx.moveTo(points[0].x, points[0].y)
    for (let i = 1; i < points.length; i++) {
      ctx.lineTo(points[i].x, points[i].y)
    }
    ctx.stroke()
  }

  // 로봇
  ctx.fillStyle = 'blue'
  ctx.fillRect(robot.x - 10, robot.y - 10, 20, 20)
}

function animate() {
  requestAnimationFrame(animate)
  updateRobot()
  draw()
}
</script>
