<template>
  <div v-if="isActive" class="alert-overlay" :class="{ 'blinking': isBlinking }">
    <div class="alert-content">
      <div class="alert-icon">⚠️</div>
      <div class="alert-message">{{ message }}</div>
      <button class="alert-close" @click="deactivateAlert">경보 해제</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AlertOverlay',
  data() {
    return {
      isActive: false,
      isBlinking: false,
      message: '',
      blinkInterval: null
    }
  },
  methods: {
    activateAlert(message) {
      this.message = message
      this.isActive = true
      this.isBlinking = true
      
      // 3초 후에 점멸 중지
      setTimeout(() => {
        this.isBlinking = false
      }, 3000)
    },
    deactivateAlert() {
      this.isActive = false
      this.isBlinking = false
      this.message = ''
    }
  }
}
</script>

<style scoped>
.alert-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(255, 0, 0, 0.3);
  z-index: 9999;
  display: flex;
  justify-content: center;
  align-items: center;
}

.alert-overlay.blinking {
  animation: blink 1s infinite;
}

.alert-content {
  background-color: rgba(255, 255, 255, 0.9);
  padding: 2rem;
  border-radius: 1rem;
  text-align: center;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
}

.alert-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.alert-message {
  font-size: 1.5rem;
  color: #d32f2f;
  font-weight: bold;
  margin-bottom: 1rem;
}

.alert-close {
  padding: 0.5rem 1rem;
  background-color: #d32f2f;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.alert-close:hover {
  background-color: #b71c1c;
}

@keyframes blink {
  0% { opacity: 0.3; }
  50% { opacity: 0.7; }
  100% { opacity: 0.3; }
}
</style> 