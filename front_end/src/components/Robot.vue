<template>
  <canvas ref="canvas" @click="addPoint" width="800" height="500" style="border:1px solid black;"></canvas>
</template>

<script setup>
    import { ref, onMounted, onBeforeUnmount } from 'vue'
    import axios from 'axios'
    import { io } from 'socket.io-client'

    const socket = io('http://localhost:5002')
    const robots = ref({})


    onMounted(() => {
      // 소켓 연결
      socket.on('connect', () => {
        console.log('소켓 연결 성공:', socket.id)
      })

      // 서버로부터 'robot' 이벤트 수신
      socket.on('robot_status_update', (data) => {
        robots.value = data
        console.log('로봇 데이터 수신:', data)
      })

      // 에러 핸들링
      socket.on('error', (error) => {
        console.error('소켓 에러:', error)
      })
    })

    onBeforeUnmount(() => {
      // 컴포넌트 언마운트 시 소켓 연결 해제
      socket.disconnect()
      console.log('소켓 연결 해제')
    })


    // 캔버스에 로봇 위치 그리기
    const canvas = ref(null)
    let ctx = null
    let points = []
    let robot = { x: 0, y: 0, index: 0, progress: 0 }

    const ROBOT_SPEED = 2

    onMounted(() => {
      ctx = canvas.value.getContext('2d')
      animate()
    })

    // 클릭해서 점 추가
    function addPoint(event) {
      const rect = canvas.value.getBoundingClientRect()
      const x = event.clientX - rect.left
      const y = event.clientY - rect.top
      points.push({ x, y })

      // 처음 점 추가 시 로봇 위치 설정
      if (points.length === 1) {
        robot.x = x
        robot.y = y
        robot.index = 0
        robot.progress = 0
      }
    }
      // 거리 계산
    function getDistance(a, b) {
      return Math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)
    }

    // 선 따라 이동 로직
    function updateRobot() {
      if (points.length < 2) return

      const current = points[robot.index]
      const next = points[robot.index + 1]
      const totalDist = getDistance(current, next)

      robot.progress += ROBOT_SPEED
      if (robot.progress >= totalDist) {
        robot.index++
        if (robot.index >= points.length - 1) {
          robot.index = 0
          robot.progress = 0
          return
        }
        robot.progress = 0
      }

      const ratio = robot.progress / totalDist
      robot.x = current.x + (next.x - current.x) * ratio
      robot.y = current.y + (next.y - current.y) * ratio
    }
 
    function draw() {
    ctx.clearRect(0, 0, canvas.value.width, canvas.value.height)

    // 점 그리기
    ctx.fillStyle = 'red'
    for (const point of points) {
      ctx.beginPath()
      ctx.arc(point.x, point.y, 5, 0, Math.PI * 2)
      ctx.fill()
    }
    // 선 그리기
    ctx.strokeStyle = 'black'
    ctx.lineWidth = 2
    ctx.beginPath()
    for (let i = 0; i < points.length; i++) {
      const { x, y } = points[i]
      if (i === 0) ctx.moveTo(x, y)
      else ctx.lineTo(x, y)
    }
    ctx.stroke()

    // 로봇(네모) 그리기
    ctx.fillStyle = 'blue'
    ctx.fillRect(robot.x - 10, robot.y - 10, 20, 20)
  }

  function animate() {
  requestAnimationFrame(animate)
  updateRobot()
  draw()
  }
</script>

<style scoped>
.black-box {
    position: fixed;
    top: 30px;
  right: 40px;
    width: 1000px;
    height: 1000px;
  background-color: black;
}
</style>
