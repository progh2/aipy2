import assert from 'node:assert/strict';
import {authDomainCandidates, pickAuthDomain, fallbackOrder, decideAuthDomain} from '../../web/assets/auth-domain-model.js';

const D = 'aipy2-9de30.firebaseapp.com', W = 'aipy2-9de30.web.app';
assert.deepEqual(authDomainCandidates(D), [D, W]);
assert.deepEqual(authDomainCandidates(W), [W, D]);
assert.deepEqual(authDomainCandidates('example.com'), ['example.com']);
assert.deepEqual(authDomainCandidates(''), []);

assert.equal(pickAuthDomain(D, null), D);
assert.equal(pickAuthDomain(D, W), W);
assert.equal(pickAuthDomain(D, 'evil.example.com'), D, '후보 밖 저장값은 무시');
assert.equal(pickAuthDomain(D, 'other-project.web.app'), D, '다른 프로젝트 주소는 무시');

assert.deepEqual(fallbackOrder(D, D), [W]);
assert.deepEqual(fallbackOrder(D, W), [D]);

assert.deepEqual(decideAuthDomain(D, D, {[D]: true}), {action: 'keep', domain: D});
assert.deepEqual(decideAuthDomain(D, D, {[D]: false, [W]: true}), {action: 'switch', domain: W});
assert.deepEqual(decideAuthDomain(D, W, {[W]: false, [D]: true}), {action: 'switch', domain: D}, '대체 주소가 막히면 기본으로 되돌림');
assert.deepEqual(decideAuthDomain(D, D, {[D]: false, [W]: false}), {action: 'blocked', domain: D});

console.log('PASS: auth-domain-model fallback rules');
