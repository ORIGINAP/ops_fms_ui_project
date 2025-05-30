<template>
  <div class="alert-container" v-if="isAlertActive">
    <div class="alert-box">
      <div class="alert-icon">⚠️</div>
      <div class="alert-message">{{ alertMessage }}</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AlertComponent',
  data() {
    return {
      isAlertActive: false,
      alertMessage: ''
    }
  },
  methods: {
    activateAlert(message) {
      this.isAlertActive = true
      this.alertMessage = message
    }
  }
}
</script>

<style scoped>
.alert-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.alert-box {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

.alert-icon {
  font-size: 48px;
}

.alert-message {
  font-size: 18px;
  color: #333;
  text-align: center;
}

</style> 