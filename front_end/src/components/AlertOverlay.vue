<template>
  <div v-if="isActive" class="alert-overlay" :class="{ 'blinking': isBlinking }">
    <div class="alert-content">
      <div class="alert-icon">⚠️</div>
      <div class="alert-message">{{ message }}</div>
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
    },
    deactivateAlert() {
      this.isActive = false
      this.isBlinking = false
      this.message = ''
    }
  }
}
</script>