<template>
  <div class="network-graph-container">
    <canvas ref="canvas" class="network-graph-canvas"></canvas>
    <div class="robot-values">
      <p v-for="(val, robot) in networkValues" :key="robot">
        {{ robot }}: {{ val }}%
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { io } from 'socket.io-client'

const canvas = ref(null)
const maxHistory = 50
const robotColors = {
  robotA: '#0A74FF',
  robotB: '#FF4D4D',
  robotC: '#00C49F',
  robotD: '#FFBB28',
}

const networkData = ref({
  robotA: [],
  robotB: [],
  robotC: [],
  robotD: []
})

const networkValues = ref({
  robotA: 0,
  robotB: 0,
  robotC: 0,
  robotD: 0,
})

function pushValue(robot, val) {
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

function drawGraph() {
  const c = canvas.value
  if (!c) return
  const ctx = c.getContext('2d')
  ctx.clearRect(0, 0, c.width, c.height)

  const stepX = c.width / (maxHistory - 1)

  Object.keys(networkData.value).forEach((robot) => {
    const history = networkData.value[robot]
    if (history.length < 2) return
    ctx.beginPath()
    history.forEach((v, i) => {
      const x = i * stepX
      const y = c.height - (v / 100) * c.height * 1.2 // 세로 확대
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
    // payload 예시: { robotA: 85, robotB: 70, robotC: 50 }
    for (const [robot, val] of Object.entries(payload)) {
      if (networkData.value[robot]) {
        networkValues.value[robot] = val
        pushValue(robot, val)
      }
    }
    drawGraph()
  })

  nextTick(resizeCanvas)
  window.addEventListener('resize', resizeCanvas)
})

onBeforeUnmount(() => {
  if (socket) socket.disconnect()
  window.removeEventListener('resize', resizeCanvas)
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
