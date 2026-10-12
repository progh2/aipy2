/* (#144) 학교망(디벗망) 일부에서 Firebase 기본 인증 주소(*.firebaseapp.com)가 막혀 로그인 창이
   ERR_CONNECTION_REFUSED로 끝난다. 같은 프로젝트가 제공하는 다른 인증 주소(*.web.app)를 순서대로
   시도하기 위한 순수 로직. 실제 네트워크 확인(probe)은 auth.js가 하고, 여기서는 후보 목록·저장값
   검증·다음 후보 선택만 한다. */

export const AUTH_DOMAIN_STORAGE_KEY = 'aipy-auth-domain-v1';

// 기본 주소를 맨 앞에 두고, 같은 프로젝트의 대체 주소를 뒤에 둔다. 다른 프로젝트·임의 도메인은 허용하지 않는다.
export function authDomainCandidates(defaultDomain) {
 const d = String(defaultDomain || '');
 const m = d.match(/^([a-z0-9-]+)\.(firebaseapp\.com|web\.app)$/);
 if (!m) return d ? [d] : [];
 const project = m[1];
 const list = [d, `${project}.firebaseapp.com`, `${project}.web.app`];
 return [...new Set(list)];
}

// 저장된 값이 후보 목록 안에 있을 때만 쓴다(조작·오타 방지). 없으면 기본 주소.
export function pickAuthDomain(defaultDomain, stored) {
 const candidates = authDomainCandidates(defaultDomain);
 return candidates.includes(stored) ? stored : (candidates[0] || defaultDomain);
}

// 현재 주소가 막혔을 때 시도할 나머지 후보(현재 제외, 원래 순서 유지).
export function fallbackOrder(defaultDomain, current) {
 return authDomainCandidates(defaultDomain).filter((d) => d !== current);
}

// probe 결과 {도메인: true|false}로 다음 행동을 정한다.
// - 현재 주소가 열리면 'keep'
// - 막혔고 열리는 대체 주소가 있으면 {action:'switch', domain}
// - 모두 막히면 'blocked'
export function decideAuthDomain(defaultDomain, current, reachable) {
 if (reachable[current]) return {action: 'keep', domain: current};
 const next = fallbackOrder(defaultDomain, current).find((d) => reachable[d]);
 if (next) return {action: 'switch', domain: next};
 return {action: 'blocked', domain: current};
}
