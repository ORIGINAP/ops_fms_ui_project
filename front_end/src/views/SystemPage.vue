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
        <button class="tab" :class="{ active: activeTab === 'Alert' }" @click="activeTab = 'Alert'">{{ $t('system.alert.title') }}</button>
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

        <div v-if="activeTab === 'Sound'" class="sound-settings">
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

        <div v-if="activeTab === 'Alert'" class="alert-tab">
          <div class="form-group">
            <label>{{ $t('system.alert.title') }}</label>
            <p class="description">{{ $t('system.alert.description') }}</p>
            <div class="toggle-group">
              <label class="switch">
                <input type="checkbox" v-model="isAlertSimulationEnabled" @change="toggleAlertSimulation" />
                <span class="slider round"></span>
              </label>
              <span class="alert-label">{{ isAlertSimulationEnabled ? $t('system.alert.enable') : $t('system.alert.enable') }}</span>
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
          <div class="profile-buttons">
            <button class="save-button" @click="saveProfile">{{ $t('system.profile.save') }}</button>
            <button class="cancel-button" @click="activeTab = 'Profile'">{{ $t('system.profile.cancel') }}</button>
          </div>
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
      isDarkTheme: false,
      isAlertSimulationEnabled: localStorage.getItem('alertSimulation') === 'true'
    }
  },
  methods: {
    changeLanguage() {
      this.$i18n.locale = this.selectedLanguage;
      localStorage.setItem('language', this.selectedLanguage);
    },
    toggleAlertSimulation() {
      localStorage.setItem('alertSimulation', this.isAlertSimulationEnabled);
      // 이벤트를 발생시켜 Map 컴포넌트에 알림
      window.dispatchEvent(new CustomEvent('alertSimulationChanged', {
        detail: { enabled: this.isAlertSimulationEnabled }
      }));
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
  width: 94.2%;
  min-height: 100vh;
  background-color: #f5f7fa;
}

.settings-container {
  flex: 1;
  padding: 40px 38px;
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
  margin-right: 30px;
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
  margin-left: 10px;
}

.tab {
  padding: 15px 20px;
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
  height: 580px; /*비율 맞추려고 늘렸는데 가변길이로 하고싶다면 없애요..*/
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
  max-width: 500px;
}

.form-group label {
  font-size: 20px;
  color: #666;
  font-weight: 500;
  margin-top: 20px;
  margin-left: 20px;
}

.form-group select {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  background-color: white;
  cursor: pointer;
  transition: border-color 0.3s ease;
  width: 200px;
}

.form-group select:focus {
  border-color: #0878ff;
  outline: none;
}

.form-group select option {
  padding: 10px;
}

.profile-text {
  font-size: 16px;
  color: #333;
  padding: 8px 0;
  margin-left: 20px;
}

.edit-footer {
  margin-top: 20px;
  display: flex;
  justify-content: flex-start;
}

.edit-button {
  padding: 8px 16px;
  background-color: #0878ff;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s ease;
  min-width: 80px;
}

.edit-button:hover {
  background-color: #005ecb;
}

.profile-settings {
  display: flex;
  flex-direction: column;
  gap: 10px;
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
  min-width: 100px;
  width: 100px;
}

.save-button {
  background-color: #0878ff;
  color: white;
  margin-left: 10px;
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

.language-settings {
  width: 500px;
  font-size: 16px;
  padding: 8px 12px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.alert-label {
  font-size: 15px;
  color: #333;
}
.language-field label {
  font-size: 14px;
  color: #666;
  font-weight: 500;
}

.language-field select {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  background-color: white;
  cursor: pointer;
  transition: border-color 0.3s ease;
  width: 200px;
}

.language-field select:focus {
  border-color: #0878ff;
  outline: none;
}

.language-field select option {
  padding: 10px;
}

.profile-buttons {
  display: flex;
  gap: 10px;
  margin-top: 20px;
  justify-content: flex-start;
}

.sound-settings label {
  margin-left: 20px;
  margin-top: 20px;
  letter-spacing: 0.08em;
  font-size: 20px;
  font-weight: 600;
  color: #333;
  gap : 50px;
}

.description {
  font-size: 14px;
  color: #666;
  margin-left: 20px;
}
.sound-field label {

  font-size: 14px;
  color: #666;
  font-weight: 500;

}
.profile-field label {
  font-size: 14px!important;
  color: #666;
  font-weight: 500;
}

.alert-tab label {
  line-height: 1.8;
  font-size: 20px;
}

.toggle-group {
  display: flex;
  align-items: center;
  gap: 12px;
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
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
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

.toggle-label {
  font-size: 14px;
  color: #333;
}
</style>