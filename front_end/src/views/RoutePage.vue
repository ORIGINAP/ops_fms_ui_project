<template>
  <div class="robot-control-container">
    <Menu />

    <div class="main-panel">
      <!-- 로봇 정보 카드 -->
      <div class="robot-info-card">
        <div class="form-group">
          <label>로봇 선택</label>
          <select v-model="selectedRobotId">
            <option disabled value="">로봇을 선택하세요</option>
            <option v-for="robot in robotList" :key="robot.id" :value="robot.id">
              {{ robot.name }}
            </option>
          </select>
        </div>

        <div v-if="selectedRobot" class="robot-info">
          <p><strong>배터리 상태 :</strong> {{ selectedRobot.battery }}%</p>
          <p><strong>이동 루트 :</strong> {{ selectedRobot.location.replaceAll('#', '→') }}</p>
          <p><strong>고장 상태 :</strong> {{ selectedRobot.fault ? '⚠️ 고장' : '정상' }}</p>
        </div>
      </div>

      <!-- 커맨드 입력 -->
      <div class="cmd-panel">
        <h2 class="cmd-header">
          명령어 입력 <span v-if="selectedRobot">({{ selectedRobot.name }})</span>
        </h2>
        <ul ref="logList">
          <li v-for="(log, idx) in (selectedRobot?.logs || [])" :key="idx">{{ log }}</li>
        </ul>

        <div class="command-box" v-if="selectedRobot">
          <input
            v-model="commandText"
            @keyup.enter="sendCommand"
            placeholder="예: 이동 A B / 충전완료"
          />
          <button @click="sendCommand">전송</button>
        </div>
        <p v-else class="cmd-hint">먼저 로봇을 선택하세요.</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { io } from "socket.io-client";
import Menu from "../components/Menu.vue";

const socket = io("http://localhost:5002");

export default {
  name: "RobotControlPage",
  components: { Menu },
  data() {
    return {
      selectedRobotId: "",
      commandText: "",
      robotList: [],
    };
  },
  computed: {
    selectedRobot() {
      return this.robotList.find(r => r.id === this.selectedRobotId);
    },
  },
  methods: {
    async fetchRobotsFromServer() {
      try {
        const res = await axios.get("http://127.0.0.1:5002/robots", {
          withCredentials: true,
        });

        this.robotList = res.data.map((rid, index) => ({
          id: index + 1,
          name: `로봇 ${index + 1}`,
          battery: 100,
          location: "A",
          fault: false,
          logs: [],
          backendId: rid
        }));

        if (!this.selectedRobotId && this.robotList.length > 0) {
          this.selectedRobotId = this.robotList[0].id;
        }
      } catch (err) {
        console.error("❌ 로봇 목록 불러오기 실패:", err);
      }
    },

    async sendCommand() {
      if (!this.selectedRobot || !this.commandText.trim()) return;

      const cmd = this.commandText.trim();
      this.appendLog(`📤 명령 전송: ${cmd}`);

      if (cmd.startsWith("이동 ")) {
        const parts = cmd.split(" ").slice(1); // ["A", "B"]
        if (parts.every(loc => ["A", "B", "C", "D"].includes(loc))) {
          const route = parts.join("#");
          try {
            await axios.post("http://127.0.0.1:5002/update_robot", {
              robot_id: this.selectedRobot.backendId,
              route
            }, { withCredentials: true });

            this.appendLog(`🚗 이동 경로 설정: ${parts.join("→")}`);
          } catch (err) {
            this.appendLog("❗ 이동 명령 실패");
          }
        } else {
          this.appendLog("❗ 위치는 A~D만 허용됩니다.");
        }
      } else if (cmd === "충전완료") {
        try {
          await axios.post("http://127.0.0.1:5002/update_robot", {
            robot_id: this.selectedRobot.backendId,
            battery: 100
          }, { withCredentials: true });

          this.appendLog("🔋 배터리 100%로 충전 완료!");
        } catch (err) {
          this.appendLog("❗ 충전 실패");
        }
      } else {
        this.appendLog("❗ 알 수 없는 명령입니다");
      }

      this.commandText = "";
    },

    appendLog(msg) {
      this.selectedRobot.logs.push(`[${new Date().toLocaleTimeString()}] ${msg}`);
      this.$nextTick(() => {
        const list = this.$refs.logList;
        if (list) list.scrollTop = list.scrollHeight;
      });
    },

    handleSocketUpdate(data) {
      for (const backendId in data) {
        const incoming = data[backendId];
        const robot = this.robotList.find(r => r.backendId === backendId);
        if (robot) {
          robot.battery = incoming.battery;
          robot.location = incoming.route;
        }
      }
    },
  },
  mounted() {
    this.fetchRobotsFromServer();
    socket.on("robot_status_update", this.handleSocketUpdate);
  },
  unmounted() {
    socket.off("robot_status_update", this.handleSocketUpdate);
  }
};
</script>

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
  margin-bottom: 20px;
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
