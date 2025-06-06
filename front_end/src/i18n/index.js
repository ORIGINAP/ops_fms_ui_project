import { createI18n } from 'vue-i18n'

const messages = {
  ko: {
    system: {
      title: '시스템 설정',
      profile: {
        edit: '프로필 수정',
        name: '이름',
        email: '이메일',
        phone: '전화번호',
        role: '직책',
        department: '부서',
        save: '저장',
        cancel: '취소',
        saveSuccess: '프로필이 저장되었습니다',
        saveError: '프로필 저장 중 오류가 발생했습니다'
      },
      account: {
        title: '계정 설정'
      },
      language: {
        title: '언어 설정',
        ko: '한국어',
        en: '영어'
      },
      sound: {
        title: '소리 알림',
        enable: '소리 알림 사용'
      },
      notification: {
        title: '알림 설정',
        theme: '시스템 테마',
        dark: '다크 모드',
        light: '라이트 모드'
      }
    }
  },
  en: {
    system: {
      title: 'System Settings',
      profile: {
        edit: 'Edit Profile',
        name: 'Name',
        email: 'Email',
        phone: 'Phone',
        role: 'Role',
        department: 'Department',
        save: 'Save',
        cancel: 'Cancel',
        saveSuccess: 'Profile saved successfully',
        saveError: 'Error saving profile'
      },
      account: {
        title: 'Account Settings'
      },
      language: {
        title: 'Language Settings',
        ko: 'Korean',
        en: 'English'
      },
      sound: {
        title: 'Sound Notification',
        enable: 'Enable Sound'
      },
      notification: {
        title: 'Notification Settings',
        theme: 'System Theme',
        dark: 'Dark Mode',
        light: 'Light Mode'
      }
    }
  }
}

const i18n = createI18n({
  locale: localStorage.getItem('language') || 'ko',
  fallbackLocale: 'en',
  messages
})

export default i18n 