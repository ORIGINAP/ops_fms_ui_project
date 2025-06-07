<template>
  <div class="robot-control-container">
    <!-- 좌측 메뉴 -->
    <Menu />

    <!-- 우측 메인 패널 -->
    <div class="main-panel">
      <!-- 로봇 상태 카드 -->
      <div class="robot-info-card">
        <div class="form-group">
          <label>{{ $t('route.robotSelect') }}</label>
          <select v-model="selectedRobotId">
            <option disabled value="">{{ $t('route.selectRobot') }}</option>
            <option v-for="robot in robotList" :key="robot.id" :value="robot.id">
              {{ robot.name }}
            </option>
          </select>
        </div>

        <div v-if="selectedRobot" class="robot-info">
          <p><strong>{{ $t('route.batteryStatus') }} : </strong> {{ selectedRobot.battery }}%</p>
          <p><strong>{{ $t('route.currentLocation') }} : </strong> {{ selectedRobot.location }}</p>
          <p><strong>{{ $t('route.faultStatus') }} : </strong> {{ selectedRobot.fault ? $t('route.hasFault') : $t('route.normal') }}</p>
        </div>
      </div>

      <!-- 로그 및 커맨드 패널 -->
      <div class="cmd-panel">
        <h2 class="cmd-header">
          {{ $t('route.commandInput') }} <span v-if="selectedRobot">({{ selectedRobot.name }})</span>
        </h2>
        <ul ref="logList">
          <li v-for="(log, idx) in (selectedRobot?.logs || [])" :key="idx">{{ log }}</li>
        </ul>

        <div class="command-box" v-if="selectedRobot">
          <input
            v-model="commandText"
            @keyup.enter="sendCommand"
            :placeholder="$t('route.moveCommand') + ' A'"
          />
          <button @click="sendCommand">{{ $t('route.send') }}</button>
        </div>
        <p v-else class="cmd-hint">{{ $t('route.commandHint') }}</p>
      </div>
    </div>
  </div>
</template>



<style scoped>
.robot-control-container {
  display: flex;
  height: 101vh;
  background: #f0f4f8;
}

.main-panel {
  flex: 1;
  display: flex;
  padding: 35px 58px 40px 36px;
  gap: 16px;
}

/* 상태 카드 */
.robot-info-card {
  width: 280px;
  background: #fff;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 2px 0 5px rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.robot-info p {
  margin-bottom: 30px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

select {
  margin-top: 6px;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #ccc;
}

/* cmd 패널 */
.cmd-panel {
  flex: 0.94;
  background: #fff;
  padding: 20px;
  border-radius: 13px;
  box-shadow: 2px 0 5px rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
  margin-right: 9px;
}

.cmd-panel ul {
  flex: 1;
  overflow-y: auto;
  margin: 16px 0;
  padding-left: 20px;
}

.cmd-header {
  color: rgba(0,0,0,0.5);
  margin-left: 20px;
  margin-bottom: 12px;
  font-weight: 600;
  font-size: 30px;
}

.command-box {
  display: flex;
  gap: 10px;
  margin-top: 15px;
  align-items: flex-start;
}

.command-box input {
  flex: 1;
  padding: 14px 16px;
  height: 48px;
  font-size: 16px;
  border-radius: 10px;
  border: 1px solid #ccc;
}

.command-box button {
  padding: 10px 20px;
  height: 81px;
  border: none;
  border-radius: 10px;
  background: #0878ff;
  color: #fff;
  font-weight: bold;
  cursor: pointer;
}

.command-box button:hover {
  background: #005ecb;
}

.cmd-hint {
  font-size: 14px;
  color: #889;
}
</style>
