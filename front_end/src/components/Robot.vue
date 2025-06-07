<template>
  <canvas ref="canvas"
          @click="handleCanvasClick"
          style="position: fixed; top: 0; left: 0; z-index: 10; width: 100vw; height: 100vh; border: 2px solid black;" />
  <div v-if="selectedRobot" :style="popupStyle" class="robot-popup">
    <strong>{{ selectedRobot.name }}</strong><br />
    Battery: {{ selectedRobot.battery }}%<br />
    Speed: {{ (selectedRobot.velocity / SCALE).toFixed(2) }}<br />
    Route: {{ selectedRobot.route }}
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { io } from 'socket.io-client'

const canvas = ref(null)
let ctx = null

const SCALE = 1.6
const EXTRA_SCALE = 1.2 // 추가 스케일링
const PADDING = 6 * SCALE
const selectedRobot = ref(null)
const popupStyle = ref({ top: '0px', left: '0px', position: 'fixed', background: 'white', border: '1px solid gray', padding: '8px', zIndex: 20 })

const zones = reactive({
  A: { x: 150 * SCALE, y: 100 * SCALE, width: 120 * SCALE *EXTRA_SCALE , height: 100 * SCALE *EXTRA_SCALE },
  B: { x: 500 * SCALE, y: 120 * SCALE, width: 130 * SCALE *EXTRA_SCALE, height: 110 * SCALE *EXTRA_SCALE },
  C: { x: 550 * SCALE, y: 300 * SCALE, width: 150 * SCALE *EXTRA_SCALE, height: 90 * SCALE *EXTRA_SCALE },
  D: { x: 200 * SCALE, y: 300 * SCALE, width: 110 * SCALE *EXTRA_SCALE, height: 120 * SCALE *EXTRA_SCALE }
})

function getRectOutline(x, y, width, height) {
  return [
    { x: x, y: y },
    { x: x + width, y: y },
    { x: x + width, y: y + height },
    { x: x, y: y + height }
  ]
}

function getCombinedRectanglePath(zoneIds) {
  let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity
  for (const id of zoneIds) {
    const z = zones[id]
    minX = Math.min(minX, z.x)
    minY = Math.min(minY, z.y)
    maxX = Math.max(maxX, z.x + z.width)
    maxY = Math.max(maxY, z.y + z.height)
  }
  return getRectOutline(minX, minY, maxX - minX, maxY - minY)
}

const robots = ref({})
const DEFAULT_SPEED = 2 * SCALE

const socket = io('http://localhost:5002')

socket.on('robot_status_update', (data) => {
  for (const key in data) {
    const incoming = data[key]
    let robot = robots.value[key]

    if (!robot) {
      robot = {
        name: incoming.name,
        x: 0, y: 0,
        path: [],
        index: 0,
        progress: 0,
        battery: incoming.battery,
        route: incoming.route,
        velocity: (parseFloat(incoming.velocity) || DEFAULT_SPEED) * SCALE
      }
      updateRobotRoute(robot, incoming.route)
      const start = robot.path[0]
      if (start) {
        robot.x = start.x
        robot.y = start.y
      }
      robots.value[key] = robot
    } else {
      robot.battery = incoming.battery
      robot.velocity = (parseFloat(incoming.velocity) || DEFAULT_SPEED) * SCALE
      if (robot.route !== incoming.route) {
        robot.route = incoming.route
        updateRobotRoute(robot, incoming.route)
        const start = robot.path[0]
        if (start) {
          robot.x = start.x
          robot.y = start.y
        }
      }
    }
  }
})

function updateRobotRoute(robot, routeString) {
  const zoneIds = routeString.split('#')
  robot.path = getCombinedRectanglePath(zoneIds)
  robot.index = 0
  robot.progress = 0
}

function getDistance(a, b) {
  return Math.hypot(b.x - a.x, b.y - a.y)
}

function updateRobots() {
  for (const key in robots.value) {
    const robot = robots.value[key]
    if (robot.battery <= 0 || !robot.path || robot.path.length < 2) continue

    const current = robot.path[robot.index]
    const next = robot.path[(robot.index + 1) % robot.path.length]
    const dist = getDistance(current, next)

    robot.progress = Math.min(robot.progress + robot.velocity, dist)
    const ratio = robot.progress / dist
    robot.x = current.x + (next.x - current.x) * ratio
    robot.y = current.y + (next.y - current.y) * ratio

    if (robot.progress >= dist) {
      robot.index = (robot.index + 1) % robot.path.length
      robot.progress = 0
    }
  }
}

function drawZones() {
  ctx.lineWidth = 1
  ctx.font = `${14 * SCALE}px Arial`

  for (const key in zones) {
    const z = zones[key]
    const radius = 10 * SCALE

    const x = z.x + PADDING
    const y = z.y + PADDING
    const w = z.width - 2 * PADDING
    const h = z.height - 2 * PADDING

    ctx.fillStyle = '#007bff'
    ctx.beginPath()
    ctx.moveTo(x + radius, y)
    ctx.lineTo(x + w - radius, y)
    ctx.quadraticCurveTo(x + w, y, x + w, y + radius)
    ctx.lineTo(x + w, y + h - radius)
    ctx.quadraticCurveTo(x + w, y + h, x + w - radius, y + h)
    ctx.lineTo(x + radius, y + h)
    ctx.quadraticCurveTo(x, y + h, x, y + h - radius)
    ctx.lineTo(x, y + radius)
    ctx.quadraticCurveTo(x, y, x + radius, y)
    ctx.closePath()
    ctx.fill()

    ctx.strokeStyle = 'gray'
    ctx.strokeRect(z.x, z.y, z.width, z.height)

    // ✅ 중앙 흰색 텍스트
    ctx.fillStyle = 'white'
    ctx.textAlign = 'center'
    ctx.textBaseline = 'middle'
    ctx.fillText(key, z.x + z.width / 2, z.y + z.height / 2)
  }
}



function drawZoneLinks() {
  const path = getCombinedRectanglePath(Object.keys(zones))
  ctx.strokeStyle = 'lightgray' // 변경됨
  ctx.lineWidth = 2
  ctx.beginPath()
  path.forEach((pt, idx) => {
    if (idx === 0) ctx.moveTo(pt.x, pt.y)
    else ctx.lineTo(pt.x, pt.y)
  })
  ctx.closePath()
  ctx.stroke()

  ctx.strokeStyle = 'lightgray' // 변경됨
  ctx.lineWidth = 1
  for (const key in zones) {
    const z = zones[key]
    ctx.strokeRect(z.x, z.y, z.width, z.height)
  }
}

function drawRobotPaths() {
  ctx.lineWidth = 1
  ctx.setLineDash([4, 2])
  for (const key in robots.value) {
    const robot = robots.value[key]
    if (!robot.path || robot.path.length < 2) continue
    ctx.beginPath()
    ctx.strokeStyle = 'lightgray' // 변경됨
    robot.path.forEach((pt, idx) => {
      if (idx === 0) ctx.moveTo(pt.x, pt.y)
      else ctx.lineTo(pt.x, pt.y)
    })
    ctx.closePath()
    ctx.stroke()
  }
  ctx.setLineDash([])
}

function getBatteryColor(battery) {
  return battery < 50 ? 'red' : '#39FF14'
}

function handleCanvasClick(e) {
  const rect = canvas.value.getBoundingClientRect()
  const mouseX = e.clientX - rect.left
  const mouseY = e.clientY - rect.top
  for (const key in robots.value) {
    const r = robots.value[key]
    const size = 20 * SCALE
    if (mouseX >= r.x - size / 2 && mouseX <= r.x + size / 2 && mouseY >= r.y - size / 2 && mouseY <= r.y + size / 2) {
      selectedRobot.value = r
      popupStyle.value = {
        top: `${e.clientY + 10}px`,
        left: `${e.clientX + 10}px`,
        position: 'fixed',
        background: 'white',
        border: '1px solid gray',
        padding: '8px',
        zIndex: 20
      }
      return
    }
  }
  selectedRobot.value = null
}

function draw() {
  ctx.clearRect(0, 0, canvas.value.width, canvas.value.height)
  drawZones()
  drawZoneLinks()
  drawRobotPaths()
  for (const key in robots.value) {
    const robot = robots.value[key]
    if (isNaN(robot.x) || isNaN(robot.y)) continue
    const size = 20 * SCALE
    const batteryHeight = size * (robot.battery / 100)
    const batteryColor = getBatteryColor(robot.battery)
    ctx.strokeStyle = 'black'
    ctx.strokeRect(robot.x - size / 2, robot.y - size / 2, size, size)
    ctx.fillStyle = batteryColor
    ctx.fillRect(robot.x - size / 2, robot.y + size / 2 - batteryHeight, size, batteryHeight)
    ctx.fillStyle = 'black'
    ctx.font = `${12 * SCALE}px Arial`
    ctx.fillText(robot.name, robot.x - 15, robot.y - size / 2 - 5)
  }
}

function animate(timestamp) {
  requestAnimationFrame(animate)
  updateRobots()
  draw()
}

onMounted(() => {
  const el = canvas.value
  el.width = window.innerWidth
  el.height = window.innerHeight
  ctx = el.getContext('2d')
  animate()
})
</script>

<style scoped>
.robot-popup {
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  min-width: 150px;
}
</style>
