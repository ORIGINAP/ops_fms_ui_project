<template>
  <div class="body">
    <Menu />
  </div>

  <div class="system-page">
    <Menu class="menu" />

    <div class="settings-container">
      <!-- 상단 배너 -->
      <div class="header-banner">
        <img class="user-avatar" src="../assets/icon/avatar.svg" alt="User" />
        <h2 class="settings-title">{{ username }}</h2>
      </div>

      <!-- 탭 메뉴 -->
      <div class="tabs">
        <button class="tab" :class="{ active: activeTab === 'Profile' }" @click="activeTab = 'Profile'">Profile</button>
        <button class="tab" :class="{ active: activeTab === 'Account' }" @click="activeTab = 'Account'">Account</button>
        <button class="tab" :class="{ active: activeTab === 'Sound' }" @click="activeTab = 'Sound'">Sound</button>
        <button class="tab" :class="{ active: activeTab === 'Notification' }" @click="activeTab = 'Notification'">Notification</button>
      </div>

      <!-- 탭 콘텐츠 -->
      <div class="form-section">
        <div v-if="activeTab === 'Profile'" class="profile-view">
          <div class="form-group">
            <label>Full Name</label>
            <p class="profile-text">{{ profileData.name }}</p>
          </div>
          <div class="form-group">
            <label>Email Address</label>
            <p class="profile-text">{{ profileData.email }}</p>
          </div>
          <div class="form-group">
            <label>Phone Number</label>
            <p class="profile-text">{{ profileData.phone }}</p>
          </div>

          <!-- Edit 버튼 -->
          <div class="edit-footer">
            <button class="edit-button" @click="activeTab = 'EditProfile'">Edit</button>
          </div>
        </div>

        <div v-if="activeTab === 'Account'">
          <div class="form-group">
            <label>Language</label>
            <select>
              <option>Korean</option>
              <option>English</option>
            </select>
          </div>
        </div>

        <div v-if="activeTab === 'Sound'">
          <div class="form-group">
            <label>Sound Notification</label>
            <div class="toggle-group">
              <label><input type="checkbox" /> Enable Sounds</label>
            </div>
          </div>
        </div>

        <div v-if="activeTab === 'Notification'">
          <div class="form-group">
            <label>System Theme</label>
            <div class="toggle-group">
              <label class="switch">
                <input type="checkbox" v-model="isDarkTheme">
                <span class="slider round"></span>
              </label>
              <span>{{ isDarkTheme ? 'Dark Mode' : 'Light Mode' }}</span>
            </div>
          </div>
        </div>
        <!-- edit function -->
        <div v-if="activeTab === 'EditProfile'">
          <h1>Edit Profile</h1>
          <div class="form-group">
            <label>New Name</label>
            <input type="text" v-model="newUsername" placeholder="Enter new name" />
          </div>
          <div class="form-group">
            <label>New Email</label>
            <input type="email" v-model="newEmail" placeholder="Enter new email" />
          </div>
          <div class="form-group">
            <label>Phone Number</label>
            <input type="tel" v-model="newNumber" placeholder="Enter phone number" />
          </div>
          <button class="save-button" @click="saveProfile">Save</button>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import Menu from '../components/Menu.vue'
import axios from 'axios'
export default {
  name: 'SystemSettings',
  components: { Menu },
  data() {
    return {
      activeTab: 'Profile',
      username: '',
      newUsername: '',
      newEmail: '',
      newNumver:'',
      profileData: {
        name:'',
        email:'',
        phone:''
      }
    }
  },
  methods: {
    saveProfile() {
      axios.post('http://localhost:5000/update-profile', {
        username: this.newUsername,
        email: this.newEmail,
        phone: this.newNumber
      }, { withCredentials: true })
        .then(res => {
          this.username = this.newUsername;
          this.activeTab = 'Profile';
          alert('프로파일 수정 완료');
        })
        .catch(err => {
          console.error(err);
          alert('Something went wrong');
        });
    }
  },
  created() {
    axios.get('http://localhost:5000/me', { withCredentials: true })
      .then(res => {
        this.username = res.data.username;
      })
      .catch(err => {
        console.error(err);
      });
  }
}

</script>

<style scoped>
html, body {
  height: 100%;
  margin: 0;
  padding: 0;
}

.system-page {
  display: flex;
  width: 100%;
  min-height: 100vh;
  background-color: #f5f7fa;
}

.settings-container {
  flex: 1;
  padding: 40px 20px;
  display: flex;
  flex-direction: column;
}

.header-banner {
  left: 10px;
  width: 89.8%;
  background-color: white;
  box-shadow: 2px 0 5px rgba(8,120,255,0.2);
  border-radius: 16px;
  padding: 30px 20px;
  display: flex;
  align-items: center;
  position: relative;
}

.user-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  border: 4px solid #ffffff;
  object-fit: cover;
  background-color: #e0e0e0;
  margin-left: 20px;
}

.settings-title {
  font-size: 28px;
  color: rgba(0,63,136,100);
  flex-grow: 1;
  margin-left: 20px;
}

.profile-view {
  position: relative;
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 100%;
}

.profile-text {
  font-size: 20px;
  color: #333;
  margin: 6px 0 20px;
}

.edit-footer {
  position: absolute;
  top: 0px;
  right: 20px;
}

.edit-button {
  margin-right: 20px;
  padding: 11px 24px;
  font-size: 14px;
  border: 2px solid #0878ff;
  background-color: white;
  color: #0878ff;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.2s;
}

.edit-button:hover {
  background-color: #eaf3ff;
}

.tabs {
  display: flex;
  margin: 30px 0 -1px 0;
  position: relative;
  z-index: 2;
  padding-left: 10px;
}

.tab {
  height: 55px;
  padding: 10px 50px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  color: #666;
  background: transparent;
  border: none;
  transition: all 0.2s;
  position: relative;
  z-index: 2;
  letter-spacing: 1px;
}

.tab.active {
  background-color: white;
  color: #222;
  border-radius: 12px 12px 0 0;
  box-shadow: 0 -1px 0 white;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
  background-color: white;
  padding: 70px 30px 30px 70px;
  border-radius: 0 15px 15px 15px;
  box-shadow: 0 3px 8px rgba(0,0,0,0.2);
  flex-grow: 1;
  height: 545px;
  overflow-y: auto;
  margin-bottom: 100px;
  width: 86.5%;
  margin-left: 10px;
}

.form-section > div {
  display: flex;
  flex-direction: column;
  gap: 40px;
}
.form-section h1 {
  margin-top: 2px;
}

.form-group {
  display: flex;
  flex-direction: column;
  max-width: 500px;
  width: 100%;
}

.form-group label {
  font-weight: bold;
  font-size: 25px;
  color: #333;
  margin-bottom: 6px;
}

.form-section h1 {
  margin: 0 0 2px;
  font-size: 35px;
  line-height: 1.2;
}

.form-group input,
.form-group select {
  padding: 10px 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 14px;
}

.toggle-group {
  display: flex;
  align-items: center; /* ⬅️ 수직 가운데 정렬 */
  gap: 12px;            /* ⬅️ 토글과 글자 사이 간격 */
  padding-top: 6px;
}


.save-button {
  margin-top: 20px;
  margin-left: 24%;
  padding: 10px 20px;
  font-size: 14px;
  border: 2px solid #0878ff;
  background-color: #0878ff;
  color: white;
  border-radius: 8px;
  cursor: pointer;
  max-width: 100px;
  width: 100%;
  align-self: flex-start;
}

.save-button:hover {
  background-color: #005ecb;

}
/* 토글 스위치 스타일 */
.switch {
  position: relative;
  display: inline-block;
  width: 52px;
  height: 28px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

/* 슬라이더 바 */
.slider {
  position: absolute;
  cursor: pointer;
  top: 0; left: 0;
  right: 0; bottom: 0;
  background-color: #ccc;
  transition: 0.4s;
  border-radius: 34px;
}

/* 슬라이더 원 */
.slider::before {
  position: absolute;
  content: "";
  height: 22px;
  width: 22px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: 0.4s;
  border-radius: 50%;
}

/* 체크 시 배경색 */
input:checked + .slider {
  background-color: #0878ff;
}

/* 체크 시 원 위치 */
input:checked + .slider::before {
  transform: translateX(24px);
}

/* 둥근 스타일 클래스 */
.slider.round {
  border-radius: 34px;
}
.slider.round::before {
  border-radius: 50%;
}


</style>
