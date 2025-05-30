<template>
  <div id="container" @mousemove="onMouseMove">
    <div
      class="circle"
      :style="{
        transform: `translate(${position.x}px, ${position.y}px)`
      }"
    />
  </div>
</template>

<script>
export default {
  data() {
    return {
      target: { x: 0, y: 0 },  // 목표 위치
      position: { x: 0, y: 0 }, // 실제 위치
    };
  },
  watch: {
    target: {
      deep: true,
      handler() {
        this.animateToTarget();
      }
    }
  },
  methods: {
    onMouseMove(e) {
      this.target.x = e.clientX;
      this.target.y = e.clientY;
    },
    animateToTarget() {
      cancelAnimationFrame(this.frame); // 중복 방지
      const animate = () => {
        const dx = this.target.x - this.position.x;
        const dy = this.target.y - this.position.y;
        this.position.x += dx * 0.1; // 보간 (lerp)
        this.position.y += dy * 0.1;
        if (Math.abs(dx) > 0.5 || Math.abs(dy) > 0.5) {
          this.frame = requestAnimationFrame(animate);
        }
      };
      this.frame = requestAnimationFrame(animate);
    }
  },
  beforeDestroy() {
    cancelAnimationFrame(this.frame);
  }
};
</script>

<style>
#container {
  width: 100vw;
  height: 100vh;
  background: #f0f0f0;
  position: relative;
  overflow: hidden;
}
.circle {
  width: 40px;
  height: 40px;
  background: tomato;
  border-radius: 50%;
  position: absolute;
  transition: transform 0.05s linear;
}
</style>
