<template>
  <div class="body">
    <div class="table-wrapper">
      <p class="title">LogPage</p>
      <table>
        <thead>
          <tr>
            <th>로봇명</th>
            <th>시간</th>
            <th>현재 위치</th>
            <th>배터리 잔량</th>
            <th>관리자</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(log, index) in logs" :key="index">
            <td>{{ log.name }}</td>
            <td>{{ log.time }}</td>
            <td>{{ log.location }}</td>
            <td>{{ log.battery }}%</td>
            <td>{{ log.admin }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <Menu />
  </div>



<div class="pagination">
  <button
    v-for="page in totalPages"
    :key="page"
    @click="changePage(page)"
    :class="{ active: currentPage === page }"
  >
    {{ page }}
  </button>
</div>




</template>

<script>
import axios from 'axios';
import Menu from "../components/Menu.vue";

export default {
  name: 'LogPage',
  components: { Menu },
  data() {
    return {
      logs: [],
      currentPage: 1,
      pageSize: 15,
      totalLogs: 0
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.totalLogs / this.pageSize);
    }
  },
  methods: {
    async fetchLogs(page = 1) {
      try {
        const response = await axios.get(`http://localhost:5000/api/logs?page=${page}&limit=${this.pageSize}`);
        this.logs = response.data.logs;
        this.totalLogs = response.data.total;
        this.currentPage = page;
      } catch (error) {
        console.error("로그 불러오기 실패", error);
      }
    },
    changePage(page) {
      this.fetchLogs(page);
    },
    showDetail(log) {
      alert('임시 작업');
    }
  },
  mounted() {
    this.fetchLogs();
  }
};
</script>


<style scoped>

.body {
  position: fixed;
  top: 40px;
  left: 40px;

  width: 89%;
  height: 92%;
  box-shadow: 3px 3px 7px rgba(21,100,191, 0.13);
  background-color: white;
  display: flex;
  justify-content: flex-start;
  flex-direction: column;
  align-items: center;
  border-radius: 30px;
}

.table-wrapper {
  width: 100%;
  overflow-x: auto;
}

.title {
  font-size: 24px;
  margin-bottom: 10px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 10px;
  text-align: center;
  border-bottom: 1px solid #ccc;
}

button {
  padding: 5px 10px;
  border: none;
  background-color: #1564bf;
  color: white;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #0f4ea0;
}

.pagination {
  margin-top: 20px;
}
.pagination button {
  margin: 0 5px;
  padding: 6px 10px;
  background-color: #f2f2f2;
  border: none;
  cursor: pointer;
}
.pagination button.active {
  background-color: #1564bf;
  color: white;
  font-weight: bold;
}

</style>