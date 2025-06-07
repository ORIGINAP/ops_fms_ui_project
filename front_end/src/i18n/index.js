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
    },
    status: {
      network: '네트워크',
      loading: '로딩 중...',
      areas: {
        a: 'A구역',
        b: 'B구역',
        c: 'C구역',
        d: 'D구역'
      }
    },
    map: {
      safetyFacility: '소방시설',
      fireAlert: '{area} 영역에서 화재가 발생했습니다!',
      noDanger: '현재 감지된 위험 없음'
    },
    alert: {
      close: '닫기'
    },
    login: {
      title: '로그인',
      email: '이메일',
      password: '비밀번호',
      loginButton: '로그인',
      registerButton: '회원가입',
      emailRequired: '이메일을 입력하세요.',
      passwordRequired: '비밀번호를 입력하세요.',
      loginSuccess: '로그인 성공',
      loginFailed: '로그인 실패',
      error: '오류가 발생했습니다.'
    },
    register: {
      title: '회원가입 페이지',
      email: '이메일',
      password: '비밀번호',
      registerButton: '가입',
      allFieldsRequired: '모든 필드를 입력해주세요.',
      invalidEmail: '올바른 이메일 형식을 입력해주세요.'
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
    },
    status: {
      network: 'Network',
      loading: 'Loading...',
      areas: {
        a: 'Area A',
        b: 'Area B',
        c: 'Area C',
        d: 'Area D'
      }
    },
    map: {
      safetyFacility: 'Safety Facility',
      fireAlert: 'Fire detected in {area}!',
      noDanger: 'No danger detected'
    },
    alert: {
      close: 'Close'
    },
    login: {
      title: 'Login',
      email: 'Email',
      password: 'Password',
      loginButton: 'Login',
      registerButton: 'Register',
      emailRequired: 'Please enter your email.',
      passwordRequired: 'Please enter your password.',
      loginSuccess: 'Login successful',
      loginFailed: 'Login failed',
      error: 'An error occurred.'
    },
    register: {
      title: 'Register Page',
      email: 'Email',
      password: 'Password',
      registerButton: 'Register',
      allFieldsRequired: 'Please fill in all fields.',
      invalidEmail: 'Please enter a valid email format.'
    }
  }
}

const i18n = createI18n({
  legacy: false,
  locale: localStorage.getItem('language') || 'ko',
  fallbackLocale: 'en',
  messages
})

export default i18n 