/* ops.js 부트·권한 게이트. HTML 기본 문구에 멈추지 않는지 검사합니다.
   node tools/web/test_ops_boot.mjs */
function el(tag, id, text) {
 const node = {
  tagName: String(tag).toUpperCase(),
  id: id || '',
  className: '',
  hidden: false,
  disabled: false,
  checked: false,
  value: '',
  textContent: text || '',
  children: [],
  dataset: {},
  style: {},
  onclick: null,
  onchange: null,
  oninput: null,
  type: '',
  append(...nodes) {
   this.children.push(...nodes);
   return this;
  },
  replaceChildren(...nodes) {
   this.children = nodes;
   this.textContent = nodes.map((child) => (child && child.textContent) || '').join('');
  },
  addEventListener() {},
  setAttribute() {},
  remove() {},
  click() { if (this.onclick) this.onclick(); },
  focus() {},
  querySelector() { return null; },
  querySelectorAll() { return []; }
 };
 return node;
}

const nodes = new Map();
function put(id, tag = 'div', text = '') {
 const node = el(tag, id, text);
 nodes.set(id, node);
 return node;
}

put('ops-gate', 'section', '권한을 확인합니다…');
put('ops-tools', 'div').hidden = true;
put('ops-year', 'select');
put('ops-include-archived', 'input');
put('ops-class-only', 'input');
put('ops-scope', 'p');
put('ops-count', 'span');
put('ops-list', 'div');
put('ops-promote', 'button');
put('ops-promote-preview', 'button');
put('ops-promote-preview-table', 'div');
put('ops-promote-note', 'p');
put('ops-next-grade', 'input');
put('ops-next-class', 'input');
put('ops-export', 'button');
put('ops-archive', 'button');
put('ops-remove', 'button');
put('ops-archive-note', 'p');
put('ops-load', 'button');

const listeners = new Map();
const document = new EventTarget();
document.body = el('body');
document.body.dataset = {};
document.body.append = () => {};
document.getElementById = (id) => nodes.get(id) || null;
document.createElement = (tag) => el(tag);
document.querySelectorAll = () => [];
document.querySelector = () => null;
const nativeAdd = document.addEventListener.bind(document);
document.addEventListener = (type, fn, opts) => {
 if (!listeners.has(type)) listeners.set(type, []);
 listeners.get(type).push(fn);
 nativeAdd(type, fn, opts);
};

globalThis.document = document;
globalThis.window = globalThis;
globalThis.HTMLElement = function HTMLElement() {};
globalThis.CustomEvent = CustomEvent;

const {renderFixture} = await import('../../web/assets/ops.js');

function gateText() {
 return nodes.get('ops-gate').textContent || '';
}

if (gateText() === '권한을 확인합니다…') {
 throw new Error(`gate stayed on HTML default: ${gateText()}`);
}
if (!gateText().includes('로그인과 권한을 확인합니다')) {
 throw new Error(`gate did not show checking status: ${gateText()}`);
}
if (!nodes.get('ops-tools').hidden) {
 throw new Error('tools should stay hidden until teacher review');
}

document.dispatchEvent(new CustomEvent('aipy:account', {detail: {user: null}}));
if (!gateText().includes('학교 계정으로 로그인')) {
 throw new Error(`signed-out gate: ${gateText()}`);
}
if (!nodes.get('ops-tools').hidden) {
 throw new Error('tools visible while signed out');
}

renderFixture({
 year: 2025,
 roster: [
  {email: 'a@e-mirim.hs.kr', studentId: '20314', admissionYear: 2025, name: '홍길동', grade: 2, classroom: 3}
 ]
});
if (nodes.get('ops-tools').hidden) {
 throw new Error('renderFixture should unhide tools');
}
if (!gateText().includes('미리보기')) {
 throw new Error(`fixture gate: ${gateText()}`);
}
if (!gateText() && !nodes.get('ops-list').children.length) {
 throw new Error('fixture list empty');
}

console.log('PASS: ops boot updates gate and opens tools in fixture');
