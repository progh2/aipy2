/* Firebase 프로젝트 설정.
   apiKey는 비밀키가 아니라 프로젝트 식별자이므로 공개 저장소에 커밋해도 됩니다.
   실제 접근 권한은 firebase/firestore.rules가 판단합니다.
   값을 채우는 절차는 firebase/README.md를 보세요. 비어 있으면 로그인 UI가 나타나지 않습니다. */
export const firebaseConfig = {
  apiKey: "AIzaSyA95nzhwrP8LZTkG_qwQWnFI2sid2gD0cg",
  authDomain: "aipy2-9de30.firebaseapp.com",
  projectId: "aipy2-9de30",
  storageBucket: "aipy2-9de30.firebasestorage.app",
  messagingSenderId: "1053376050119",
  appId: "1:1053376050119:web:57f64c6eccc52e5605dfe2"
};
export const SCHOOL_DOMAIN = 'e-mirim.hs.kr';
export const SDK = 'https://www.gstatic.com/firebasejs/12.9.0';
export const ready = Boolean(firebaseConfig.apiKey && firebaseConfig.projectId && firebaseConfig.authDomain);
