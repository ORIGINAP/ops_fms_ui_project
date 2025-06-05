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
        <button class="edit-button" @click="activeTab = 'EditProfile'">Edit</button>
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
        <div v-if="activeTab === 'Profile'">
          <div class="form-group">
            <label>Full Name</label>
            <input type="text" placeholder="Enter your full name" />
          </div>
          <div class="form-group">
            <label>Email Address</label>
            <input type="email" placeholder="example@robotfms.com" />
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
            <select>
              <option>Light</option>
              <option>Dark</option>
            </select>
          </div>
        </div>
        <!-- edit function -->
        <div v-if="activeTab === 'EditProfile'">
          <h1>Edit Profile</h1>
          <div class="form-group">
            <label>New Name</label>
            <input type="text" placeholder="Enter new name" v-model="newUsername" />
          </div>
          <div class="form-group">
            <label>New Email</label>
            <input type="email" placeholder="Enter new email" v-model="newEmail" />
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
      newEmail: ''
    }
  },
  methods: {
    saveProfile() {
      axios.post('http://localhost:5000/update-profile', {
        username: this.newUsername,
        email: this.newEmail
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
  padding: 40px 20px; /* 좌우 padding 줄이기 */
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

.edit-button {
  margin-right: 40px;
  padding: 6px 18px;
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

.form-group {
  display: flex;
  flex-direction: column;
  max-width: 500px;
  width: 100%;
}

.form-group label {
  font-size: 14px;
  color: #333;
  margin-bottom: 6px;
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
  align-items: center;
  gap: 10px;
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
</style>
