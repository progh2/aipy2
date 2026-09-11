/* 학생 화면 개인정보 안내. 수집 항목은 PRD F10 최소 목록과 같습니다.
   문구는 계정 패널·학습 기록 영역에 같이 씁니다. */
export const PRIVACY_TITLE = '무엇이 저장되나요?';
export const PRIVACY_LEAD = '수업 운영에 필요한 최소 항목만 저장해요.';
export const PRIVACY_STORED = [
 '학교 이메일',
 '이름',
 '학번과 입학년도',
 '학년·반·번호',
 '학습 기록(완료·답안·저널·코드)',
 '과제 제출물',
 '이해도 신호(이해했어요/어려워요, 도움 요청)'
];
export const PRIVACY_TEACHER_TITLE = '선생님이 보는 것';
export const PRIVACY_TEACHER = [
 '학번·이름·학년·반',
 '접속·완료·정답 요약',
 '이해도 신호와 도움 요청',
 '과제 제출 소스와 출력'
];
export const PRIVACY_GRADE_NOTE = '성적·출결에는 들어가지 않아요.';
export const PRIVACY_EXPORT_NOTE = '본인 학습 기록은 JSON으로 내보낼 수 있어요.';
export const PRIVACY_SCHOOL_NOTE = '실제 보관·동의는 학교 규정을 따릅니다.';
export const PRIVACY_BUTTON = '개인정보';
export const PRIVACY_DIALOG_TITLE = '개인정보 안내';
export const PRIVACY_CLOSE = '닫기';

function node(tag, cls, text) {
 const el = document.createElement(tag);
 if (cls) el.className = cls;
 if (text !== undefined) el.textContent = text;
 return el;
}

export function privacyBody() {
 const wrap = node('div', 'privacy-body');
 wrap.append(node('p', 'small', PRIVACY_LEAD));
 const stored = node('ul', 'privacy-list');
 for (const item of PRIVACY_STORED) stored.append(node('li', '', item));
 wrap.append(node('h3', '', PRIVACY_TITLE), stored);
 const seen = node('ul', 'privacy-list');
 for (const item of PRIVACY_TEACHER) seen.append(node('li', '', item));
 wrap.append(node('h3', '', PRIVACY_TEACHER_TITLE), seen);
 wrap.append(node('p', 'small', `${PRIVACY_GRADE_NOTE} ${PRIVACY_EXPORT_NOTE}`));
 wrap.append(node('p', 'small', PRIVACY_SCHOOL_NOTE));
 return wrap;
}

export function mountPrivacyNotice(host) {
 if (!host) return null;
 host.classList.add('privacy-notice');
 const details = node('details');
 const summary = node('summary', '', `${PRIVACY_TITLE} · ${PRIVACY_TEACHER_TITLE}`);
 details.append(summary, privacyBody());
 host.replaceChildren(details);
 return host;
}

export function openPrivacyDialog() {
 const existing = document.getElementById('privacy-overlay');
 if (existing) existing.remove();
 const overlay = node('div', 'sync-overlay');
 overlay.id = 'privacy-overlay';
 overlay.setAttribute('role', 'dialog');
 overlay.setAttribute('aria-modal', 'true');
 overlay.setAttribute('aria-labelledby', 'privacy-dialog-title');
 const box = node('div', 'sync-dialog privacy-dialog');
 const heading = node('h2', '', PRIVACY_DIALOG_TITLE);
 heading.id = 'privacy-dialog-title';
 box.append(heading);
 box.append(privacyBody());
 const actions = node('div', 'actions');
 const close = node('button', 'primary', PRIVACY_CLOSE);
 close.type = 'button';
 const finish = () => overlay.remove();
 close.onclick = finish;
 overlay.addEventListener('click', (event) => { if (event.target === overlay) finish(); });
 overlay.addEventListener('keydown', (event) => { if (event.key === 'Escape') finish(); });
 actions.append(close);
 box.append(actions);
 overlay.append(box);
 document.body.append(overlay);
 close.focus();
 return overlay;
}

export function privacyButton() {
 const button = node('button', 'account-privacy', PRIVACY_BUTTON);
 button.type = 'button';
 button.addEventListener('click', openPrivacyDialog);
 return button;
}
