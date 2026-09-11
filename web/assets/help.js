/* 실습실·문제·주제 옆 도움 요청. 큐에 올린 뒤에도 학습은 그대로 이어집니다. */
import {ready} from './firebase-config.js';
import {load} from './auth.js';
import {classId} from './class-picker.js';
import {NOT_GRADED_NOTE, isTopicId} from './understanding-model.js';
import {
 HELP_LABEL, HELP_CANCEL_LABEL, HELP_SENT, HELP_KEEP_WORKING, helpRequestFields, canCreateHelp,
 openHelpForTopic
} from './help-model.js';

const node = (tag, cls, text) => {
 const el = document.createElement(tag);
 if (cls) el.className = cls;
 if (text !== undefined) el.textContent = text;
 return el;
};

let user = null;
let profile = null;
let classroom = '';
let mine = [];
let lastCreateAt = 0;
let unsub = null;

function toast(text) {
 const box = document.getElementById('toast');
 if (box) box.textContent = text || '';
}

function currentExample() {
 if (window.aipyLearning && typeof window.aipyLearning.currentExample === 'function') {
  return window.aipyLearning.currentExample();
 }
 return null;
}

function lastError() {
 if (window.aipyLearning && typeof window.aipyLearning.lastError === 'function') {
  return window.aipyLearning.lastError();
 }
 return '';
}

function currentTopic(fallback) {
 if (isTopicId(fallback)) return fallback;
 const unit = Number(document.body.dataset.unit || 0);
 const lab = document.getElementById('lab');
 const workspace = lab && lab.closest('[data-workspace]');
 if (unit && workspace && workspace.dataset.workspace) return `u${unit}-${workspace.dataset.workspace}`;
 const hash = location.hash.replace(/^#/, '');
 if (unit && hash && document.getElementById(hash)?.classList.contains('lesson')) return `u${unit}-${hash}`;
 return fallback || null;
}

function paintButtons() {
 document.querySelectorAll('[data-help-topic], [data-help-slot]').forEach((button) => {
  const topic = currentTopic(button.dataset.helpTopic || '');
  const open = openHelpForTopic(mine, topic);
  const active = Boolean(open);
  button.dataset.helpId = open ? open.id : '';
  button.setAttribute('aria-pressed', String(active));
  button.textContent = active ? HELP_CANCEL_LABEL : HELP_LABEL;
  button.disabled = !user || !classroom;
  button.title = classroom ? HELP_KEEP_WORKING : '명단에 있는 학교 계정으로 로그인하면 요청할 수 있어요.';
 });
}

function helpButton(topic, slot) {
 const button = node('button', 'help-request', HELP_LABEL);
 button.type = 'button';
 if (topic) button.dataset.helpTopic = topic;
 if (slot) button.dataset.helpSlot = slot;
 button.setAttribute('aria-pressed', 'false');
 button.addEventListener('click', () => onHelpClick(button));
 return button;
}

function mountTopicHelp() {
 document.querySelectorAll('.topic-signals[data-topic]').forEach((root) => {
  if (root.querySelector('[data-help-topic]')) return;
  root.append(helpButton(root.dataset.topic));
 });
}

function mountAreaHelp(selector, slot) {
 const host = document.querySelector(selector);
 if (!host || host.querySelector(`[data-help-slot="${slot}"]`)) return;
 let actions = host.querySelector('.actions');
 if (!actions) {
  actions = node('div', 'actions help-actions');
  host.append(actions);
 }
 const wrap = node('div', 'help-slot');
 wrap.append(helpButton('', slot), node('span', 'small understanding-note', NOT_GRADED_NOTE));
 actions.append(wrap);
}

async function createHelp(topic) {
 const check = canCreateHelp({openRequests: mine, topic, now: Date.now(), lastCreateAt});
 if (!check.ok && check.reason === 'cooldown') {
  toast('조금 뒤에 다시 요청할 수 있어요. 그동안 계속 시도해도 됩니다.');
  return;
 }
 if (!check.ok && check.reason === 'duplicate') return;
 if (!user || !profile || !classroom || !ready) {
  toast('학교 계정으로 로그인하고 명단에 있어야 요청할 수 있어요.');
  return;
 }
 try {
  const {db, store} = await load();
  const payload = helpRequestFields({
   profile,
   classId: classroom,
   topic,
   example: currentExample(),
   lastError: lastError()
  });
  payload.createdAt = store.serverTimestamp();
  payload.updatedAt = store.serverTimestamp();
  const ref = await store.addDoc(store.collection(db, 'helpRequests'), payload);
  lastCreateAt = Date.now();
  mine = [...mine, {id: ref.id, ...payload, status: 'open'}];
  paintButtons();
  toast(HELP_SENT);
 } catch (error) {
  console.warn('[help]', error);
  toast('요청을 보내지 못했습니다. 학습은 이어서 하면 됩니다.');
 }
}

async function cancelHelp(id) {
 if (!id || !ready) return;
 try {
  const {db, store} = await load();
  await store.updateDoc(store.doc(db, 'helpRequests', id), {
   status: 'cancelled',
   updatedAt: store.serverTimestamp()
  });
  mine = mine.map((row) => row.id === id ? {...row, status: 'cancelled'} : row);
  paintButtons();
  toast('도움 요청을 취소했습니다.');
 } catch (error) {
  console.warn('[help]', error);
  toast('취소를 저장하지 못했습니다.');
 }
}

function onHelpClick(button) {
 const topic = currentTopic(button.dataset.helpTopic || '');
 const open = openHelpForTopic(mine, topic) || (button.dataset.helpId ? mine.find((row) => row.id === button.dataset.helpId) : null);
 if (open) cancelHelp(open.id);
 else createHelp(topic);
}

function listenMine() {
 if (unsub) {
  unsub();
  unsub = null;
 }
 mine = [];
 paintButtons();
 if (!user || !ready) return;
 load().then(({db, store}) => {
  unsub = store.onSnapshot(
   store.query(store.collection(db, 'helpRequests'), store.where('uid', '==', user.uid)),
   (snap) => {
    mine = [];
    snap.forEach((doc) => mine.push({id: doc.id, ...doc.data()}));
    paintButtons();
   },
   (error) => { console.warn('[help] listen', error); }
  );
 }).catch((error) => console.warn('[help]', error));
}

function onAccount(detail) {
 user = detail && detail.user;
 profile = detail && detail.profile;
 classroom = classId(profile);
 if (!user || !classroom) {
  if (unsub) {
   unsub();
   unsub = null;
  }
  mine = [];
  paintButtons();
  return;
 }
 listenMine();
}

function start() {
 if (document.getElementById('teacher-shell')) return;
 if (!document.getElementById('account')) return;
 mountTopicHelp();
 mountAreaHelp('#lab', 'lab');
 mountAreaHelp('#practice', 'practice');
 paintButtons();
 document.addEventListener('aipy:account', (event) => onAccount(event.detail));
 document.addEventListener('aipy:learning-ready', () => {
  mountTopicHelp();
  mountAreaHelp('#lab', 'lab');
  mountAreaHelp('#practice', 'practice');
  paintButtons();
 });
 if (window.aipyAccount) onAccount(window.aipyAccount);
 window.aipyHelp = {mine: () => mine};
}

start();
