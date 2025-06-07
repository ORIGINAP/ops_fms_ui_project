<template>
  <div class="alert-container" v-if="isAlertActive">
    <div class="alert-box">
      <div class="alert-icon">⚠️</div>
      <div class="alert-message" v-html="alertMessage"></div>
      <button class="alert-close" @click="closeAlert">{{ $t('alert.close') }}</button>
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
    },
    closeAlert() {
      this.isAlertActive = false
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
  max-width: 80%;
  max-height: 80vh;
  overflow-y: auto;
}

.alert-icon {
  font-size: 48px;
}

.alert-message {
  font-size: 18px;
  color: #333;
  text-align: center;
  white-space: pre-line;
}

.alert-close {
  padding: 8px 16px;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.alert-close:hover {
  background-color: #c82333;
}
</style> 