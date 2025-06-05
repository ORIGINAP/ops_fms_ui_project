<template>
  <div class="side-menu">
    <div class="menu-body">
      <!-- 첫 번째 줄: 네트워크 -->
      <div class="menu-row">
        <div class="menu-network">
          <p>network</p>
        </div>
      </div>

      <!-- 두 번째 줄: 실외 / 실내 온도 -->
      <div class="menu-row">
        <!-- 실외 온도 -->
        <div class="menu-temperature" :class="{ 'night-block': isNight, 'day-block': !isNight }">
          <div>
            <p style="font-size: 30px; color: gray;">실외 온도</p>
            <p v-if="temperature !== null">{{ temperature }}℃</p>
            <p v-else>로딩 중...</p>
          </div>
        </div>

        <!-- 실내 온도 -->
        <div class="menu-temperature">
          <div>
            <p style="font-size: 30px; color: gray;">실내 온도</p>
            <p v-if="internalTemperature !== null">{{ internalTemperature }}℃</p>
            <p v-else>로딩 중...</p>
          </div>
        </div>
      </div>

      <!-- 세 번째 줄: 기타 -->
      <div class="menu-row">
        <div class="menu-other">
          <p>other</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Status',
  data() {
    return {
      temperature: null,
      weatherIcon: null,
      internalTemperature: null,
      updateInterval: null,
      isNight: false,
    };
  },
  computed: {
    weatherIconUrl() {
      if (!this.weatherIcon) return null;
      return new URL(`../assets/icon/${this.weatherIcon}.svg`, import.meta.url).href;
    },
    thermometerIconUrl() {
      const iconName = this.internalTemperature > this.temperature ? 'tp_up' : 'tp_down';
      return new URL(`../assets/icon/${iconName}.svg`, import.meta.url).href;
    }
  },
  mounted() {
    this.init();
    this.updateInterval = setInterval(this.init, 3600000); // 1시간마다 날씨 갱신

    this.updateIsNight(); // 초기 판단
    setInterval(this.updateIsNight, 60000); // 매 1분마다 갱신
  },
  beforeUnmount() {
    clearInterval(this.updateInterval);
  },
  watch: {
    temperature(newVal) {
      if (newVal !== null) {
        const randomOffset = Math.floor(Math.random() * 6) + 5; // 5~10
        this.internalTemperature = Number(newVal) + randomOffset;
      } else {
        this.internalTemperature = null;
      }
    }
  },
  methods: {
    updateIsNight() {
      const hour = new Date().getHours();
      this.isNight = hour < 6 || hour >= 18;
    },
    async init() {
      try {
        const position = await this.getCurrentLocation();
        const { x: nx, y: ny } = this.convertToGrid(position.latitude, position.longitude);
        await this.fetchWeatherData(nx, ny);
      } catch (error) {
        console.error('초기화 실패 (위치 정보 가져오기 실패):', error);
      }
    },

    async getCurrentLocation() {
      return new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(
            pos => {
              resolve({
                latitude: pos.coords.latitude,
                longitude: pos.coords.longitude,
              });
            },
            err => reject(err)
        );
      });
    },

    convertToGrid(lat, lon) {
      const RE = 6371.00877;
      const GRID = 5.0;
      const SLAT1 = 30.0;
      const SLAT2 = 60.0;
      const OLON = 126.0;
      const OLAT = 38.0;
      const XO = 43;
      const YO = 136;

      const DEGRAD = Math.PI / 180.0;
      const re = RE / GRID;
      const slat1 = SLAT1 * DEGRAD;
      const slat2 = SLAT2 * DEGRAD;
      const olon = OLON * DEGRAD;
      const olat = OLAT * DEGRAD;

      let sn = Math.tan(Math.PI * 0.25 + slat2 * 0.5) / Math.tan(Math.PI * 0.25 + slat1 * 0.5);
      sn = Math.log(Math.cos(slat1) / Math.cos(slat2)) / Math.log(sn);
      let sf = Math.tan(Math.PI * 0.25 + slat1 * 0.5);
      sf = Math.pow(sf, sn) * Math.cos(slat1) / sn;
      let ro = Math.tan(Math.PI * 0.25 + olat * 0.5);
      ro = re * sf / Math.pow(ro, sn);

      let ra = Math.tan(Math.PI * 0.25 + lat * DEGRAD * 0.5);
      ra = re * sf / Math.pow(ra, sn);
      let theta = lon * DEGRAD - olon;
      if (theta > Math.PI) theta -= 2.0 * Math.PI;
      if (theta < -Math.PI) theta += 2.0 * Math.PI;
      theta *= sn;

      const x = Math.floor(ra * Math.sin(theta) + XO + 0.5);
      const y = Math.floor(ro - ra * Math.cos(theta) + YO + 0.5);

      return { x, y };
    },

    async fetchWeatherData(nx, ny) {
      const serviceKey = 'QnGWF0isjBPG%2FEXxLVhwkts%2FGtuhtD3cAEf3bEzXPvt73kfBsPflla8lVoK8VtBQLaTw1rhvMpiMHjIFoX6Pew%3D%3D';
      const baseDate = this.getBaseDate();
      const baseTime = this.getBaseTime();

      const url = 'https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst';
      const params = {
        serviceKey: decodeURIComponent(serviceKey),
        numOfRows: 1000,
        pageNo: 1,
        dataType: 'JSON',
        base_date: baseDate,
        base_time: baseTime,
        nx,
        ny,
      };

      try {
        const response = await axios.get(url, { params });
        console.log("요청 시간:", baseDate, baseTime);

        const result = response.data.response;

        if (result?.header?.resultCode !== '00') {
          console.error('기상청 API 오류:', result?.header?.resultMsg || '알 수 없음');
          return;
        }

        const items = result?.body?.items?.item;
        if (!items || items.length === 0) {
          console.error('날씨 데이터가 없습니다.', result?.body);
          return;
        }

        const tempItem = items.find(item => item.category === 'T1H');
        const ptyItem = items.find(item => item.category === 'PTY');
        const skyItem = items.find(item => item.category === 'SKY');

        this.temperature = tempItem ? tempItem.fcstValue : null;

        const pty = ptyItem ? Number(ptyItem.fcstValue) : 0;
        const sky = skyItem ? Number(skyItem.fcstValue) : 1;

        this.weatherIcon = this.getWeatherIcon(pty, sky);
      } catch (error) {
        console.error('날씨 API 요청 실패:', error);
      }
    },

    getWeatherIcon(pty, sky) {
      const hour = new Date().getHours();
      const isNight = hour < 6 || hour >= 18;

      if (pty === 1) return 'rain';
      if (pty === 2 || pty === 6) return 'rain-snow';
      if (pty === 3 || pty === 7) return 'snow';
      if (pty === 5) return 'rain';

      if (pty === 0) {
        if (sky === 1) return isNight ? 'clear-n' : 'clear';
        if (sky === 3) return isNight ? 'clear-cloudy-n' : 'clear-cloudy';
        if (sky === 4) return 'cloudy';
      }

      return 'unknown';
    },

    getBaseDate() {
      const now = new Date();
      now.setMinutes(now.getMinutes() - 60); // 안정적으로 1시간 전
      const yyyy = now.getFullYear();
      const mm = String(now.getMonth() + 1).padStart(2, '0');
      const dd = String(now.getDate()).padStart(2, '0');
      return `${yyyy}${mm}${dd}`;
    },

    getBaseTime() {
      const now = new Date();
      now.setMinutes(now.getMinutes() - 60); // 안정적으로 1시간 전
      const hour = now.getHours();
      return `${String(hour).padStart(2, '0')}30`;
    }
  }
};
</script>

<style scoped>
.side-menu {
  position: fixed;
  top: 20px;
  right: 145px;
  width: 26%;
  height: 93%;
  margin: 0;
  z-index: 50;
  padding: 20px;
  display: flex;
  flex-direction: column;
  border-radius: 20px;
}

.menu-body {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.menu-row {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.menu-network {
  box-shadow: 2px 0 5px rgba(21,100,191,0.2);
  background-color: white;
  height: 350px;
  border-radius: 20px;
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 16px;
  font-weight: bold;
  color: darkgray;
}

.menu-temperature {
  box-shadow: 2px 0 5px rgba(178,214,255,0.5);
  background-color: white;
  height: 230px;
  border-radius: 20px;
  flex-grow: 1;
  color: rgba(73,135,207,0.5);
  transition: box-shadow 0.3s ease;
}

.menu-temperature > div {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  font-size: 30px;
  gap: 23px;
  line-height: 1;
  margin-top: 78px;
  padding: 0;
}

.menu-temperature > div img,
.menu-temperature > div p {
  margin: 0;
  padding: 0;
  line-height: 1;
}

.day-block {
  box-shadow: 2px 0 6px rgba(231,242,255,0.2);
}

.night-block {
  box-shadow: 2px 0 6px rgba(0,63,136,0.2);
}
.menu-other {
  box-shadow: 2px 0 5px rgba(21,100,191,0.2);
  background-color: white;
  height: 270px;
  border-radius: 20px;
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 16px;
  font-weight: bold;
  color: darkgray;
}

.weather-svg-icon {
  width: 80px;
  height: 80px;
}
.thermometer-icon {
  width: 45px;
  height: 80px;
}
</style>
