<template>
  <div class="network-graph-container">
    <canvas ref="canvas" class="network-graph-canvas"></canvas>
    <div class="robot-values">
      <p v-for="(val, robot) in networkValues" :key="robot">
        {{ robot }}: {{ Math.round(val) }}%
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { io } from 'socket.io-client'

const canvas = ref(null)
const maxHistory = 50
const zoomFactor = 0.6
const maxDelta = 1.5 // ✅ 프레임당 최대 이동 폭 제한

const robotColors = {
  robotA: '#0A74FF',
  robotB: '#FF4D4D',
  robotC: '#00C49F',
  robotD: '#FFBB28',
}

const robotList = Object.keys(robotColors)

const networkData = ref({})
const networkValues = ref({})
const animatedValue = ref({})
const animationFrame = ref(null)

// ✅ 초기화
robotList.forEach((robot) => {
  networkData.value[robot] = []
  networkValues.value[robot] = 0
  animatedValue.value[robot] = 0
})

function pushValue(robot, val) {
  if (isNaN(val)) return
  const data = networkData.value[robot]
  data.push(val)
  if (data.length > maxHistory) {
    data.shift()
  }
}

function resizeCanvas() {
  const c = canvas.value
  const rect = c.getBoundingClientRect()
  c.width = rect.width
  c.height = rect.height
  drawGraph()
}

function approach(current, target, maxDelta) {
  const diff = target - current
  if (Math.abs(diff) <= maxDelta) return target
  return current + Math.sign(diff) * maxDelta
}

function animate() {
  let changed = false

  for (const robot of robotList) {
    const current = animatedValue.value[robot]
    const target = networkValues.value[robot]

    const next = approach(current, target, maxDelta)

    if (Math.abs(next - current) > 0.01) {
      animatedValue.value[robot] = next
      pushValue(robot, next)
      changed = true
    } else {
      animatedValue.value[robot] = target
    }
  }

  if (changed) drawGraph()
  animationFrame.value = requestAnimationFrame(animate)
}

function drawGraph() {
  const c = canvas.value
  if (!c) return
  const ctx = c.getContext('2d')
  ctx.clearRect(0, 0, c.width, c.height)

  const visibleCount = Math.floor(maxHistory * zoomFactor)
  const stepX = c.width / (visibleCount - 1)
  const totalWidth = stepX * (visibleCount - 1)
  const offsetX = c.width - totalWidth

  robotList.forEach((robot) => {
    const history = networkData.value[robot]
    if (!history || history.length < 2) return

    const startIndex = Math.max(0, history.length - visibleCount)

    ctx.beginPath()
    history.slice(startIndex).forEach((v, i) => {
      const x = offsetX + i * stepX
      const y = c.height - (v / 100) * c.height * 1.2
      i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y)
    })
    ctx.strokeStyle = robotColors[robot] || 'gray'
    ctx.lineWidth = 2
    ctx.stroke()
  })
}

let socket = null

onMounted(() => {
  socket = io('http://localhost:5002')

  socket.on('network', (payload) => {
    for (const [robot, val] of Object.entries(payload)) {
      if (robotList.includes(robot)) {
        networkValues.value[robot] = val
      }
    }
  })

  nextTick(() => {
    resizeCanvas()
    animate()
  })

  window.addEventListener('resize', resizeCanvas)
})

onBeforeUnmount(() => {
  if (socket) socket.disconnect()
  window.removeEventListener('resize', resizeCanvas)
  cancelAnimationFrame(animationFrame.value)
})
</script>

<style scoped>
.network-graph-container {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.network-graph-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.robot-values {
  position: absolute;
  bottom: 10px;
  right: 10px;
  font-weight: bold;
  color: #333;
  background: rgba(255, 255, 255, 0.85);
  padding: 6px 8px;
  border-radius: 6px;
  font-size: 0.85rem;
}
</style>
