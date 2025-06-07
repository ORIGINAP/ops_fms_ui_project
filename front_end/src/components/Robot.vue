<template>
  <canvas ref="canvas"
          style="position: fixed; top: 0; left: 0; z-index: 10; width: 100vw; height: 100vh; pointer-events: none;" />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { io } from 'socket.io-client'

const canvas = ref(null)
let ctx = null

const zones = {
  A: { x: 100, y: 100, width: 100, height: 100 },
  B: { x: 300, y: 100, width: 100, height: 100 },
  C: { x: 300, y: 300, width: 100, height: 100 },
  D: { x: 100, y: 300, width: 100, height: 100 }
}

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
const DEFAULT_SPEED = 2

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
        velocity: parseFloat(incoming.velocity) || DEFAULT_SPEED
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
      robot.velocity = parseFloat(incoming.velocity) || DEFAULT_SPEED
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
  ctx.strokeStyle = 'gray'
  ctx.lineWidth = 1
  ctx.font = '14px Arial'
  ctx.fillStyle = 'black'

  for (const key in zones) {
    const z = zones[key]
    ctx.strokeRect(z.x, z.y, z.width, z.height)
    ctx.fillText(key, z.x + 5, z.y + 20)
  }
}

function drawZoneLinks() {
  const path = getCombinedRectanglePath(Object.keys(zones))
  ctx.strokeStyle = 'lightblue'
  ctx.lineWidth = 2
  ctx.beginPath()
  path.forEach((pt, idx) => {
    if (idx === 0) ctx.moveTo(pt.x, pt.y)
    else ctx.lineTo(pt.x, pt.y)
  })
  ctx.closePath()
  ctx.stroke()

  ctx.strokeStyle = 'lightblue'
  ctx.lineWidth = 1
  for (const key in zones) {
    const z = zones[key]
    ctx.strokeRect(z.x, z.y, z.width, z.height)
  }

  ctx.strokeStyle = 'lightblue'
  ctx.lineWidth = 2
  const midX = 200
  const midY = 200
  const midSize = 100
  ctx.strokeRect(midX, midY, midSize, midSize)
}

function getBatteryColor(battery) {
  return battery < 50 ? 'red' : '#39FF14'
}

function draw() {
  ctx.clearRect(0, 0, canvas.value.width, canvas.value.height)
  drawZones()
  drawZoneLinks()

  for (const key in robots.value) {
    const robot = robots.value[key]
    if (isNaN(robot.x) || isNaN(robot.y)) continue

    const size = 20
    const batteryHeight = size * (robot.battery / 100)
    const batteryColor = getBatteryColor(robot.battery)

    ctx.strokeStyle = 'black'
    ctx.strokeRect(robot.x - size / 2, robot.y - size / 2, size, size)

    ctx.fillStyle = batteryColor
    ctx.fillRect(robot.x - size / 2, robot.y + size / 2 - batteryHeight, size, batteryHeight)

    ctx.fillStyle = 'black'
    ctx.font = '12px Arial'
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