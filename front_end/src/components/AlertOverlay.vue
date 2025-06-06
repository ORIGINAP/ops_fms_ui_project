<template>
    <div v-if="isActive" class="alert-overlay" :class="{ 'blinking': isBlinking }">
      <div class="alert-content">
        <div class="alert-icon">⚠️</div>
        <div class="alert-message">{{ message }}</div>
      </div>
    </div>
  </template>