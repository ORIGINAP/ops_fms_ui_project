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
        <h2 class="settings-title">{{ $t('system.title') }}</h2>
      </div>

      <!-- 탭 메뉴 -->
      <div class="tabs">
        <button class="tab" :class="{ active: activeTab === 'Profile' }" @click="activeTab = 'Profile'">{{ $t('system.profile.edit') }}</button>
        <button class="tab" :class="{ active: activeTab === 'Account' }" @click="activeTab = 'Account'">{{ $t('system.account.title') }}</button>
        <button class="tab" :class="{ active: activeTab === 'Sound' }" @click="activeTab = 'Sound'">{{ $t('system.sound.title') }}</button>
        <button class="tab" :class="{ active: activeTab === 'Notification' }" @click="activeTab = 'Notification'">{{ $t('system.notification.title') }}</button>
      </div>

      <!-- 탭 콘텐츠 -->
      <div class="form-section">
        <div v-if="activeTab === 'Profile'" class="profile-view">
          <div class="form-group">
            <label>{{ $t('system.profile.name') }}</label>
            <p class="profile-text">{{ profileData.name }}</p>
          </div>
          <div class="form-group">
            <label>{{ $t('system.profile.email') }}</label>
            <p class="profile-text">{{ profileData.email }}</p>
          </div>
          <div class="form-group">
            <label>{{ $t('system.profile.phone') }}</label>
            <p class="profile-text">{{ profileData.phone }}</p>
          </div>

          <!-- Edit 버튼 -->
          <div class="edit-footer">
            <button class="edit-button" @click="activeTab = 'EditProfile'">{{ $t('system.profile.edit') }}</button>
          </div>
        </div>

        <div v-if="activeTab === 'Account'" class="language-settings">
          <h2>{{ $t('system.language.title') }}</h2>
          <select v-model="selectedLanguage" @change="changeLanguage">
            <option value="ko">{{ $t('system.language.ko') }}</option>
            <option value="en">{{ $t('system.language.en') }}</option>
          </select>
        </div>

        <div v-if="activeTab === 'Sound'">
          <div class="form-group">
            <label>{{ $t('system.sound.title') }}</label>
            <div class="toggle-group">
              <label><input type="checkbox" /> {{ $t('system.sound.enable') }}</label>
            </div>
          </div>
        </div>

        <div v-if="activeTab === 'Notification'">
          <div class="form-group">
            <label>{{ $t('system.notification.theme') }}</label>
            <div class="toggle-group">
              <label class="switch">
                <input type="checkbox" v-model="isDarkTheme">
                <span class="slider round"></span>
              </label>
              <span>{{ isDarkTheme ? $t('system.notification.dark') : $t('system.notification.light') }}</span>
            </div>
          </div>
        </div>

        <div v-if="activeTab === 'EditProfile'" class="profile-settings">
          <h2>{{ $t('system.profile.edit') }}</h2>
          <div class="profile-field">
            <label>{{ $t('system.profile.name') }}</label>
            <input type="text" v-model="profileData.name" />
          </div>
          <div class="profile-field">
            <label>{{ $t('system.profile.email') }}</label>
            <input type="email" v-model="profileData.email" />
          </div>
          <div class="profile-field">
            <label>{{ $t('system.profile.role') }}</label>
            <input type="text" v-model="profileData.role" />
          </div>
          <div class="profile-field">
            <label>{{ $t('system.profile.department') }}</label>
            <input type="text" v-model="profileData.department" />
          </div>
          <div class="profile-field">
            <label>{{ $t('system.profile.phone') }}</label>
            <input type="text" v-model="profileData.phone" />
          </div>
          <button class="save-button" @click="saveProfile">{{ $t('system.profile.save') }}</button>
          <button class="cancel-button" @click="activeTab = 'Profile'">{{ $t('system.profile.cancel') }}</button>
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
      profileData: {
        name: '',
        email: '',
        phone: '',
        role: '',
        department: ''
      },
      selectedLanguage: localStorage.getItem('language') || 'ko',
      isDarkTheme: false
    }
  },
  methods: {
    changeLanguage() {
      this.$i18n.locale = this.selectedLanguage;
      localStorage.setItem('language', this.selectedLanguage);
    },
    saveProfile() {
      axios.post('http://localhost:5000/update-profile', {
        username: this.profileData.name,
        email: this.profileData.email,
        phone: this.profileData.phone,
        role: this.profileData.role,
        department: this.profileData.department
      }, { withCredentials: true })
        .then(res => {
          this.activeTab = 'Profile';
          alert(this.$t('system.profile.saveSuccess'));
        })
        .catch(err => {
          console.error(err);
          alert(this.$t('system.profile.saveError'));
        });
    }
  },
  created() {
    axios.get('http://localhost:5000/me', { withCredentials: true })
      .then(res => {
        this.profileData.name = res.data.username;
        this.profileData.email = res.data.email;
        this.profileData.phone = res.data.phone;
        this.profileData.role = res.data.role;
        this.profileData.department = res.data.department;
      })
      .catch(err => {
        console.error(err);
      });
  }
}
</script>

<style scoped>
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
  background-color: white;
  box-shadow: 2px 0 5px rgba(8,120,255,0.2);
  border-radius: 16px;
  padding: 30px 20px;
  display: flex;
  align-items: center;
  position: relative;
  margin-bottom: 20px;
}

.user-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  margin-right: 20px;
}

.settings-title {
  font-size: 24px;
  color: #333;
  margin: 0;
}

.tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.tab {
  padding: 10px 20px;
  border: none;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  color: #666;
  transition: all 0.3s ease;
}

.tab.active {
  background: #0878ff;
  color: white;
}

.form-section {
  background: white;
  border-radius: 16px;
  padding: 30px;
  box-shadow: 2px 0 5px rgba(8,120,255,0.2);
}

.profile-view {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 14px;
  color: #666;
  font-weight: 500;
}

.profile-text {
  font-size: 16px;
  color: #333;
  margin: 0;
  padding: 8px 0;
}

.edit-footer {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.edit-button {
  padding: 8px 20px;
  background-color: #0878ff;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s ease;
}

.edit-button:hover {
  background-color: #005ecb;
}

.profile-settings {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.profile-field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.profile-field input {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  transition: border-color 0.3s ease;
}

.profile-field input:focus {
  border-color: #0878ff;
  outline: none;
}

.save-button, .cancel-button {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s ease;
}

.save-button {
  background-color: #0878ff;
  color: white;
}

.save-button:hover {
  background-color: #005ecb;
}

.cancel-button {
  background-color: #f5f5f5;
  color: #666;
  margin-left: 10px;
}

.cancel-button:hover {
  background-color: #e0e0e0;
}
</style>
