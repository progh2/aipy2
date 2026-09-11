/* 도움 요청(M3/F6) 순수 헬퍼. 큐 정렬·중복 방지·쓰기 억제를 Firebase 없이 검사합니다. */
import {isTopicId, studentLabel, clipComment} from './understanding-model.js';
import {classId as rosterClassId} from './class-picker.js';
import {timestampMillis} from './follow-model.js';

export const HELP_COOLDOWN_MS = 5000;
export const HELP_ERROR_MAX = 300;
export const HELP_STATUSES = ['open', 'cancelled', 'resolved'];
export const HELP_LABEL = '도움 요청';
export const HELP_CANCEL_LABEL = '요청 취소';
export const HELP_SENT = '선생님께 보냈어요.';
export const HELP_KEEP_WORKING = '요청한 뒤에도 계속 시도할 수 있어요.';

export function clipLastError(text) {
 if (text == null) return '';
 return String(text).replace(/\s+/g, ' ').trim().slice(0, HELP_ERROR_MAX);
}

export function optionalShort(value, max) {
 if (value == null) return null;
 const text = String(value).trim();
 if (!text) return null;
 return text.slice(0, max);
}

export function helpRequestFields({profile, classId, topic, example, lastError} = {}) {
 const person = profile && typeof profile === 'object' ? profile : {};
 const classroomId = classId || rosterClassId(person);
 return {
  uid: person.uid || '',
  email: person.email || '',
  studentId: person.studentId ?? null,
  admissionYear: person.admissionYear ?? null,
  name: typeof person.name === 'string' ? person.name : '',
  grade: person.grade ?? null,
  classroom: person.classroom ?? null,
  number: person.number ?? null,
  classId: classroomId || '',
  topic: isTopicId(topic) ? topic : optionalShort(topic, 80),
  example: optionalShort(example, 80),
  lastError: clipLastError(lastError) || null,
  status: 'open'
 };
}

export function canCreateHelp({openRequests, topic, now, lastCreateAt} = {}) {
 if (lastCreateAt && Number(now) - Number(lastCreateAt) < HELP_COOLDOWN_MS) {
  return {ok: false, reason: 'cooldown'};
 }
 const topicId = isTopicId(topic) ? topic : (topic || null);
 if ((openRequests || []).some((row) => row && row.status === 'open' && (row.topic || null) === topicId)) {
  return {ok: false, reason: 'duplicate'};
 }
 return {ok: true, reason: ''};
}

export function openHelpForTopic(rows, topic) {
 const topicId = topic || null;
 return (rows || []).find((row) => row && row.status === 'open' && (row.topic || null) === topicId) || null;
}

export function sortOpenHelp(rows) {
 return (rows || [])
  .filter((row) => row && row.status === 'open')
  .slice()
  .sort((a, b) => {
   const ta = timestampMillis(a.createdAt);
   const tb = timestampMillis(b.createdAt);
   if (ta !== tb) return ta - tb;
   return studentLabel(a).localeCompare(studentLabel(b), 'ko');
  });
}

export function helpStatusLabel(status) {
 if (status === 'cancelled') return '취소됨';
 if (status === 'resolved') return '해결';
 return '대기';
}

export {studentLabel, clipComment, timestampMillis};
