<template>
  <div class="side-menu">
    <!-- 메뉴 내용 -->
    <div class="menu-body">
      <!-- 첫 번째 줄: 네트워크 -->
      <div class="menu-row">
        <div class="menu-network">
          <p>{{ $t('status.network') }}</p>
        </div>
      </div>

      <div class="menu-row">
        <div class="menu-temperature" :class="{ 'night-block': isNight, 'day-block': !isNight }">
          <div class="temp-header">실외온도</div>  <!-- 추가 -->
          <div>
            <img
                v-if="weatherIconUrl"
                class="weather-svg-icon"
                :src="weatherIconUrl"
                alt="weather icon"
            />
            <p v-if="temperature !== null">{{ temperature }}℃</p>
            <p v-else>{{ $t('status.loading') }}</p>
          </div>
        </div>

        <div class="menu-temperature">
          <div class="temp-header">실내온도</div>  <!-- 추가 -->
          <div class="internal-block" v-if="internalTemperature !== null">
            <img
                class="thermometer-icon"
                :src="thermometerIconUrl"
                alt="thermometer icon"
            />
            <p>{{ internalTemperature }}℃</p>
          </div>
          <div v-else>
            <p>{{ $t('status.loading') }}</p>
          </div>
        </div>
      </div>

      <!-- 원형차트 + 레이블 행 (추가) -->
      <div class="menu-chart-row">
        <div class="chart-labels">
          <div v-for="(label, index) in labels" :key="index" class="chart-label">
    <span
        class="color-box"
        :style="{ backgroundColor: colors[index % colors.length] }"
    ></span>
            <span class="label-key">{{ label }}</span>
            <span class="label-value">{{ chartData[index] }}</span>
          </div>
        </div>
        <svg
            class="pie-chart"
            viewBox="0 0 200 200"
            width="200"
            height="200"
            aria-label="원형 차트"
            role="img"
        >
          <circle
              v-for="(slice, index) in pieSlices"
              :key="index"
              :r="radius"
              :cx="center"
              :cy="center"
              :stroke="slice.color"
              :stroke-dasharray="slice.dashArray"
              :stroke-dashoffset="slice.dashOffset"
              fill="transparent"
              stroke-width="40"
          />
        </svg>
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
      labels: [
        this.$t('status.areas.a'),
        this.$t('status.areas.b'),
        this.$t('status.areas.c'),
        this.$t('status.areas.d')
      ],
      chartData: [25, 25, 25, 25],
      colors: ['rgba(0,62,136,1)', 'rgba(8,120,255,1)', 'rgba(110,180,255,1)', 'rgba(180,222,245,1)'],
      center: 100,
      radius: 60,
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
    },
    totalValue() {
      return this.chartData.reduce((a, b) => a + b, 0);
    },
    pieSlices() {
      const circumference = 2 * Math.PI * this.radius;
      let offset = 0;

      return this.chartData.map((value, i) => {
        const sliceLength = (value / this.totalValue) * circumference;
        const dashArray = `${sliceLength} ${circumference - sliceLength}`;
        const dashOffset = circumference - offset;
        offset += sliceLength;
        return {
          color: this.colors[i % this.colors.length],
          dashArray,
          dashOffset,
        };
      });
    }
  },
  mounted() {
    this.init();
    this.updateInterval = setInterval(this.init, 3600000); // 1시간마다 날씨 갱신

    this.updateIsNight(); // 초기 판단
    setInterval(this.updateIsNight, 60000); // 매 1분마다 갱신

    this.generateRandomChartData(); // 랜덤 차트 데이터 생성
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
    generateRandomChartData() {
      this.chartData = this.chartData.map(() => Math.floor(Math.random() * 101));

      if (this.totalValue === 0) {
        this.chartData = [25, 25, 25, 25];
      }
    },
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
        const response = await axios.get(url, { params, withCredentials: false });
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
  top: 15px;
  right: 130px;
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
  height: 330px;
  border-radius: 10px;
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 16px;
  font-weight: bold;
  color: darkgray;
}

.temp-header {
  font-size: 15px !important;
  font-weight: 600;
  color: gray;
  margin: 0;             /* 기본 margin 제거 */
  position: absolute;    /* 절대 위치로 고정 */
  top: -32px !important;             /* 위쪽 여백 조정 */
  left: 30px;            /* 왼쪽 여백 조정 */
  z-index: 10;
}
.menu-temperature {
  position: relative; /* 텍스트 위치 기준 */
  box-shadow: 2px 0 5px rgba(178,214,255,0.5);
  background-color: white;
  height: 200px;
  border-radius: 10px;
  flex-grow: 1;
  color: darkgray;
  transition: box-shadow 0.3s ease;
}

.menu-temperature > div {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  font-size: 30px;
  gap: 10px;
  line-height: 1;
  margin-top: 60px;
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


.menu-chart-row {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  background: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 2px 0 5px rgba(178,214,255,0.5);
  height: 280px;
  color: darkgray;
}

.chart-labels {
  display: flex;
  flex-direction: column;
  gap: 15px;
  font-size: 18px;
  font-weight: 600;
  min-width: 60px;
  text-align: left;
  user-select: none;
}

.chart-label {
  display: flex;
  justify-content: flex-start;
  gap: 10px;
}

.label-key {
  min-width: 20px;
}

.label-value {
  min-width: 30px;
}


.pie-chart {
  transform: rotate(-90deg); /* 시작점을 12시 방향으로 조정 */
}

.weather-svg-icon {
  width: 60px;
  height: 60px;
}
.thermometer-icon {
  width: 30px;
  height: 60px;
}
.color-box {
  margin-top: 7px;
  display: inline-block;
  width: 14px;
  height: 14px;
  border-radius: 3px;
  margin-right: 8px;
  vertical-align: middle;
}
</style>
