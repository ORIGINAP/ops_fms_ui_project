<template>
  <div class="robot-control-container">
    <!-- 좌측 메뉴 -->
    <Menu />

    <!-- 우측 메인 패널 -->
    <div class="main-panel">
      <!-- 로봇 상태 카드 -->
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
          <p><strong>배터리 상태 : </strong> {{ selectedRobot.battery }}%</p>
          <p><strong>현재 위치 : </strong> {{ selectedRobot.location }}</p>
          <p><strong>결함 여부 : </strong> {{ selectedRobot.fault ? "결함 있음" : "정상" }}</p>
        </div>
      </div>

      <!-- 로그 및 커맨드 패널 -->
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
              placeholder="ex: 이동 A"
          />
          <button @click="sendCommand">전송</button>
        </div>
        <p v-else class="cmd-hint">왼쪽에서 로봇을 선택하면 명령어를 입력할 수 있습니다.</p>
      </div>
    </div>
  </div>
</template>

<script>import axios from "axios";
import Menu from "../components/Menu.vue";

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

        // 서버 응답: ["robotA", "robotB", ...]
        this.robotList = res.data.map((rid, index) => ({
          id: index + 1,
          name: `로봇 ${index + 1}`,
          battery: 100,
          location: "A",
          fault: false,
          logs: [],
          backendId: rid, // 예: "robotA"
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

      const raw = this.commandText.trim();
      this.appendLog(`명령 전송: ${raw}`);

      if (raw.startsWith("이동")) {
        const parts = raw.split(" ").slice(1); // ["A", "B"]
        const route = parts.join("#");

        const validZones = ["A", "B", "C", "D"];
        const allValid = parts.every(zone => validZones.includes(zone));
        if (!allValid) {
          this.appendLog("❗ 잘못된 영역이 포함되어 있습니다 (A~D만 가능)");
          return;
        }

        try {
          await axios.post(
            "http://127.0.0.1:5002/update_robot",
            {
              robot_id: this.selectedRobot.backendId,
              route,
            },
            { withCredentials: true }
          );
          this.appendLog(`✅ ${route} 경로로 이동 업데이트 완료`);
        } catch (err) {
          this.appendLog("❌ 서버 오류로 명령 전송 실패");
          console.error(err);
        }
      } else {
        this.appendLog("❗ 알 수 없는 명령어입니다. 예: 이동 A B");
      }

      this.commandText = "";
    },

    appendLog(msg) {
      this.selectedRobot.logs.push(
        `[${new Date().toLocaleTimeString()}] ${msg}`
      );
      this.$nextTick(() => {
        const list = this.$refs.logList;
        if (list) list.scrollTop = list.scrollHeight;
      });
    },
  },
  mounted() {
    this.fetchRobotsFromServer();
  },
};

</script>


<style scoped>
.robot-control-container {
  display: flex;
  height: 100vh;
  box-shadow: 2px 0 5px rgba(21,100,191,0.2);
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
  border-radius: 10px;
  box-shadow: 2px 0 5px rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.robot-info p {
  margin-bottom: 40px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

select {
  margin-top: 6px;
  padding: 10px;
  border-radius: 10px;
  border: 1px solid #ccc;
}

/* cmd 패널 */
.cmd-panel {
  flex: 0.941; /* 기존 1 → 더 좁게 조정 */
  background: #fff;
  padding: 20px;
  border-radius: 10px;
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
  color: rgba(0,0,0,0.6);
  margin-left: 20px;
  margin-bottom: 12px;
  font-weight: 600;
  font-size: 30px;
}

.command-box {
  display: flex;
  gap: 10px;
  margin-top: 16px;
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
  height: 80px;
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
