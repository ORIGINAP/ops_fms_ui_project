<template>
  <div>
    <canvas ref="canvas"
            width="800"
            height="500"
            style="border: 2px solid black;" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { io } from 'socket.io-client'

const canvas = ref(null)
let ctx = null

// A, B, C, D zone 정의
const zones = {
  A: { x: 100, y: 100, width: 100, height: 100 },
  B: { x: 300, y: 100, width: 100, height: 100 },
  C: { x: 100, y: 300, width: 100, height: 100 },
  D: { x: 300, y: 300, width: 100, height: 100 }
}

function getCenter(zone) {
  return {
    x: zone.x + zone.width / 2,
    y: zone.y + zone.height / 2
  }
}

const robots = ref({}) // 각 로봇의 상태 저장
const ROBOT_SPEED = 2

// 소켓 연결
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
        route: incoming.route
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
  robot.path = zoneIds.map(id => getCenter(zones[id]))
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

    robot.progress += ROBOT_SPEED
    if (robot.progress >= dist) {
      robot.index = (robot.index + 1) % robot.path.length
      robot.progress = 0
    }

    const ratio = robot.progress / dist
    robot.x = current.x + (next.x - current.x) * ratio
    robot.y = current.y + (next.y - current.y) * ratio
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

function draw() {
  ctx.clearRect(0, 0, canvas.value.width, canvas.value.height)
  drawZones()

  for (const key in robots.value) {
    const robot = robots.value[key]
    if (isNaN(robot.x) || isNaN(robot.y)) continue

    ctx.fillStyle = robot.battery > 0 ? 'blue' : 'gray'
    ctx.fillRect(robot.x - 10, robot.y - 10, 20, 20)

    ctx.fillStyle = 'black'
    ctx.font = '12px Arial'
    ctx.fillText(robot.name, robot.x - 15, robot.y - 15)
  }
}

function animate() {
  requestAnimationFrame(animate)
  updateRobots()
  draw()
}

onMounted(() => {
  ctx = canvas.value.getContext('2d')
  animate()
})
</script>