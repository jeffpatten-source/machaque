
// ---------- course data ----------
const items = DATA.items;
const byId = Object.fromEntries(items.map(i=>[i.id,i]));
const unitsMeta = DATA.meta;                    // {u:{title,struct,count,course:bool}}
const COURSE = DATA.course;                     // unit numbers in order, contiguous from 1
const EXTRA = Object.keys(unitsMeta).map(Number).filter(u=>!COURSE.includes(u)).sort((a,b)=>a-b);
const unitItems = {}; for(const it of items) (unitItems[it.u] ||= []).push(it.id);
const NEW_PER_DAY = 15, MAX_REVIEWS = 20;
const LADDER = [1,3,7,14,30,60,120,240];       // days until a unit's next review, by level

function today(){ const d=new Date(); return Math.floor((d.getTime() - d.getTimezoneOffset()*60000)/86400000) }
function pruneStore(){ for(const id of Object.keys(store.items)) if(!byId[id]) delete store.items[id] }

// ---------- scheduling ----------
// Each unit is a structure. After all its items have been seen once, the unit is reviewed on a
// widening ladder; each review pulls the items of that unit seen least recently, so the same
// structure comes back in different sentences. Items missed get their own review the next day.
function seen(id){ return !!store.items[id] }
function newCandidates(){
  const out=[];
  for(const u of COURSE) for(const id of unitItems[u]) if(!seen(id)) out.push(id);
  return out;
}
function newLeftToday(){ const t=today(); return store.newDay===t ? Math.max(0, NEW_PER_DAY-store.newCount) : NEW_PER_DAY }
function dueUnits(){ const t=today(); return Object.entries(store.units).filter(([u,s])=>s.due<=t && unitsMeta[u]).sort((a,b)=>a[1].due-b[1].due).map(([u])=>+u) }
function dueItems(){ const t=today(); return Object.entries(store.items).filter(([id,s])=>s.due!=null && s.due<=t && byId[id]).sort((a,b)=>a[1].due-b[1].due).map(([id])=>id) }
function reviewSize(lvl){ return lvl<=1 ? 5 : lvl<=3 ? 4 : 3 }
function freshest(u, k, skip){
  // least recently seen items of a unit that have already been introduced
  const ids = unitItems[u].filter(id=>seen(id) && !skip.has(id));
  shuffle(ids);
  ids.sort((a,b)=>(store.items[a].last||0)-(store.items[b].last||0));
  return ids.slice(0,k);
}
function planToday(){
  const rev=[], unitRev={}, taken=new Set();
  for(const id of dueItems().slice(0,8)){ rev.push(id); taken.add(id) }
  for(const u of dueUnits()){
    if(rev.length>=MAX_REVIEWS) break;
    const ids = freshest(u, Math.min(reviewSize(store.units[u].lvl), MAX_REVIEWS-rev.length), taken);
    if(!ids.length) continue;
    unitRev[u] = {ids:new Set(ids), miss:0, left:new Set(ids)};
    for(const id of ids){ rev.push(id); taken.add(id) }
  }
  const fresh = newCandidates().slice(0, newLeftToday());
  return {rev, unitRev, fresh};
}

// ---------- sessions ----------
let S = null;
function shuffle(a){ for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]} return a }
function startToday(extraNew){
  const p = planToday();
  let fresh = p.fresh;
  if(extraNew) fresh = newCandidates().slice(0, extraNew);
  const queue = extraNew ? fresh : shuffle(p.rev).concat(fresh);
  if(!queue.length) return renderHome();
  S = {mode:'today', title:'Hoy', queue, total:queue.length, unitRev: extraNew?{}:p.unitRev, isNew:new Set(fresh), done:new Set(), firstTry:0, missed:new Set(), attempts:{}, redo:{}};
  next();
}
function startPractice(u){
  // free practice on one unit: everything already introduced (or every item for pilot units)
  let ids = unitItems[u].filter(id=> COURSE.includes(+u) ? seen(id) : true);
  shuffle(ids); ids = ids.filter(id=>!byId[id].w).concat(ids.filter(id=>byId[id].w));
  if(COURSE.includes(+u)) ids = ids.slice(0, 30);
  S = {mode:'practice', title:'Unidad '+u, queue:ids, total:ids.length, unitRev:{}, isNew:new Set(), done:new Set(), firstTry:0, missed:new Set(), attempts:{}, redo:{}};
  next();
}
function next(){
  if(!S.queue.length) return finish();
  S.cur = byId[S.queue.shift()]; S.curRedo = S.redo[S.cur.id]||null; S.res=null; S.input=''; S.picked=null; S.blanks=null;
  renderDrill();
}
function grade(input, picked){
  const it=S.cur; S.input=input; S.picked=picked;
  const rd=S.curRedo;
  if(it.t==='mc') S.res={ok: picked===it.acc[0], kind:'exact', match:it.acc[0], best:it.acc[0]};
  else if(rd) S.res=gradeRedo(rd);
  else S.res=check(it, input);
  record(S.res.ok);
  renderDrill();
}
function gradeRedo(rd){
  const vals=S.blanks; let kind='exact', typos=[];
  const per = rd.segs.filter(s=>'blank' in s).map((s,i)=>{ const r=vals[i].trim() ? matchOne(s.blank, vals[i]) : null; if(r){ if(r.kind==='typo'){kind='typo'; typos=typos.concat(r.typos)} else if(r.kind==='se'&&kind!=='typo') kind='se'; else if(r.kind==='accent'&&kind==='exact') kind='accent' } return !!r });
  const ok=per.every(Boolean);
  return ok ? {ok, kind, typos, match:rd.best, per} : {ok, best:rd.best, per};
}
function record(ok){
  const it=S.cur, id=it.id, t=today(), n=(S.attempts[id]||0)+1; S.attempts[id]=n;
  const st = store.items[id] || {n:0, ok:0};
  const firstEver = !store.items[id];
  if(n===1){
    st.n++; if(ok) st.ok++; st.last=t;
    if(ok) delete st.due; else st.due = t+1;
    if(firstEver && S.mode==='today' && S.isNew.has(id)){
      if(store.newDay!==t){ store.newDay=t; store.newCount=0 }
      store.newCount++;
    }
    store.items[id]=st;
    // unit review bookkeeping
    const ur = S.unitRev[it.u];
    if(ur && ur.left.has(id)){
      ur.left.delete(id); if(!ok) ur.miss++;
      if(!ur.left.size){
        // up a level with at most one miss; two misses repeat the level; more drop back
        const us=store.units[it.u];
        if(ur.miss<=1){ us.lvl=Math.min(us.lvl+1, LADDER.length-1); us.due=t+LADDER[us.lvl] }
        else if(ur.miss===2){ us.due=t+LADDER[us.lvl] }
        else { us.lvl=Math.max(us.lvl-1, 0); us.due=t+1 }
        delete S.unitRev[it.u];
      }
    }
    // a unit enters the review ladder once every item has been seen
    if(COURSE.includes(it.u) && !store.units[it.u] && unitItems[it.u].every(seen)) store.units[it.u]={lvl:0, due:t+1, intro:t};
    store.answered=(store.answered||0)+1;
  }
  if(ok){ S.done.add(id); if(n===1) S.firstTry++; delete S.redo[id] }
  else {
    S.missed.add(id);
    if(it.t==='tr' && !S.redo[id]){ const rd=makeRedo(it, S.res.best, S.input); if(rd) S.redo[id]=rd }
    S.queue.splice(Math.min(4,S.queue.length),0,id);
  }
  save();
}
function override(){
  const it=S.cur, rd=S.curRedo, t=today();
  store.notes.push({id:it.id, u:it.u, tipo:'Tenía razón', prompt:it.p||it.s, suya: rd ? S.blanks.join(' / ') : S.input, esperada: rd ? rd.segs.filter(s=>'blank' in s).map(s=>s.blank).join(' / ') : full(it,S.res.best)});
  const i=S.queue.lastIndexOf(it.id); if(i>-1) S.queue.splice(i,1);
  if(S.attempts[it.id]===1){
    S.firstTry++; S.missed.delete(it.id);
    const st=store.items[it.id]; if(st){ st.ok++; delete st.due }
  }
  S.done.add(it.id); delete S.redo[it.id]; S.res={ok:true, kind:'override', match:S.input}; save(); renderDrill();
}
function finish(){ renderEnd() }

// ---------- backup ----------
function backupText(){ return JSON.stringify({app:'machaque', saved:new Date().toISOString(), store}) }
function downloadBackup(){
  const blob=new Blob([backupText()],{type:'application/json'}), a=document.createElement('a');
  const d=new Date(), stamp=d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');
  a.href=URL.createObjectURL(blob); a.download='machaque-'+stamp+'.json'; document.body.appendChild(a); a.click();
  setTimeout(()=>{URL.revokeObjectURL(a.href); a.remove()}, 1000);
  store.backup=Date.now(); save(); renderHome();
}
function restoreBackup(file){
  const r=new FileReader();
  r.onload=()=>{ try{ const j=JSON.parse(r.result); if(j.app!=='machaque'||!j.store) throw 0;
      Object.keys(store).forEach(k=>delete store[k]); Object.assign(store, defaults(), j.store); pruneStore(); save(); renderHome('Progreso restaurado.') }
    catch(e){ renderHome('Ese archivo no es una copia de Machaque.') } };
  r.readAsText(file);
}

// ---------- rendering ----------
const app = document.getElementById('app');
function header(right){ return `<header><span class="brand">Machaque</span><span class="meta">${right||''}</span></header>` }
function plural(n, one, many){ return n+' '+(n===1?one:many) }
function unitStatus(u){
  const ids=unitItems[u], s=ids.filter(seen).length, us=store.units[u], t=today();
  if(us){ const d=us.due-t; return d<=0 ? `Nivel ${us.lvl} · repaso hoy` : `Nivel ${us.lvl} · repaso en ${plural(d,'día','días')}` }
  if(s) return `En curso · ${s} de ${ids.length} vistos`;
  return 'Sin empezar';
}
function renderHome(msg){
  S=null;
  const p=planToday(), nr=p.rev.length, nn=p.fresh.length, more=newCandidates().length;
  const standalone = window.navigator.standalone || matchMedia('(display-mode: standalone)').matches;
  let todayBox;
  if(nr||nn){
    todayBox = `<div class="unit"><span class="label">Hoy</span><h2>${[nr?plural(nr,'repaso','repasos'):'', nn?plural(nn,'nuevo','nuevos'):''].filter(Boolean).join(' · ')}</h2>
      <p>Puedes parar cuando quieras: cada respuesta se guarda al momento.</p>
      <div class="row"><button class="primary" id="go">Empezar</button></div></div>`;
  } else {
    todayBox = `<div class="unit"><span class="label">Hoy</span><h2>Todo hecho por hoy.</h2>
      <p>${more?'Puedes adelantar más material nuevo o practicar una unidad.':'No quedan unidades nuevas: pídele a Claude las siguientes. Mientras tanto, repasa.'}</p>
      <div class="row">${more?`<button class="primary" id="more">${Math.min(NEW_PER_DAY,more)} nuevos más</button>`:''}</div></div>`;
  }
  const row = u => `<li><button class="ulist" data-u="${u}" ${(!COURSE.includes(u) || unitItems[u].some(seen))?'':'disabled'}>
      <span class="un">${u}</span><span class="ut"><b>${esc(unitsMeta[u].title)}</b><small>${esc(unitsMeta[u].struct)}</small><small>${COURSE.includes(u)?unitStatus(u):'Práctica libre'}</small></span></button></li>`;
  const course = `<section><h3>Curso</h3><ul class="units">${COURSE.map(row).join('')}</ul>
      ${EXTRA.length?`<h3 style="margin-top:18px">Unidades piloto</h3><ul class="units">${EXTRA.map(row).join('')}</ul>`:''}</section>`;
  const notes = store.notes.length ? `<section class="notes"><h3>Notas para Claude (${store.notes.length})</h3>
      <pre id="notesText">${esc(notesText())}</pre>
      <div class="row" style="margin-top:10px"><button id="copy">Copiar notas</button><button class="quiet" id="clear">Borrar notas</button></div>
      <p class="small" id="copyMsg"></p></section>` : '';
  const days = store.backup ? Math.floor((Date.now()-store.backup)/86400000) : null;
  const backup = `<section><h3>Copia de seguridad</h3>
      <p class="small">El progreso se guarda solo en este teléfono, al instante. Haz una copia de vez en cuando por si el teléfono se borra. ${days==null?'Aún no has hecho ninguna.':days===0?'Última copia: hoy.':`Última copia: hace ${plural(days,'día','días')}.`}</p>
      <div class="row" style="margin-top:10px"><button id="dl">Guardar copia</button><label class="filebtn">Restaurar copia<input type="file" id="rs" accept="application/json,.json" hidden></label></div></section>`;
  const tip = standalone ? '' : `<p class="tip">Para usarla sin conexión: en Safari, pulsa Compartir → «Añadir a pantalla de inicio» y ábrela siempre desde ese icono.</p>`;
  app.innerHTML = header(`${store.answered||0} respuestas`) + (msg?`<p class="tip">${esc(msg)}</p>`:'') + tip + todayBox + course + notes + backup +
    `<p class="small">Contenido: ${items.length} ítems · versión ${DATA.build}</p>`;
  const go=document.getElementById('go'); if(go) go.onclick=()=>startToday();
  const mo=document.getElementById('more'); if(mo) mo.onclick=()=>startToday(NEW_PER_DAY);
  app.querySelectorAll('[data-u]').forEach(b=>b.onclick=()=>startPractice(+b.dataset.u));
  const c=document.getElementById('copy'); if(c) c.onclick=copyNotes;
  const cl=document.getElementById('clear'); if(cl) cl.onclick=()=>{ if(cl.dataset.armed){ store.notes=[]; save(); renderHome() } else { cl.dataset.armed=1; cl.textContent='Pulsa otra vez para borrar' } };
  document.getElementById('dl').onclick=downloadBackup;
  document.getElementById('rs').onchange=e=>{ if(e.target.files[0]) restoreBackup(e.target.files[0]) };
}
function notesText(){
  return store.notes.map(n=>`[${n.id}] ${n.tipo}\n  Enunciado: ${n.prompt}\n  Mi respuesta: ${n.suya||'—'}\n  Esperada: ${n.esperada}${n.comentario?'\n  Comentario: '+n.comentario:''}`).join('\n\n');
}
function copyNotes(){
  const msg=document.getElementById('copyMsg'), txt=notesText();
  try{ navigator.clipboard.writeText(txt).then(()=>msg.textContent='Copiado.').catch(sel) }catch(e){ sel() }
  function sel(){ const r=document.createRange(); r.selectNodeContents(document.getElementById('notesText')); const s=getSelection(); s.removeAllRanges(); s.addRange(r); msg.textContent='Seleccionado: cópialo tú.' }
}
function promptHTML(it){
  const cue = it.cue ? `<div class="cue">(${esc(it.cue)})</div>` : '';
  if(it.t==='tr') return `<div class="prompt">${esc(it.p)}</div>${cue}`;
  const s = esc(it.s).replace(/___ \(([^)]*)\)/,'<span class="blank"></span> <span class="hint">($1)</span>').replace('___','<span class="blank"></span>');
  return `<div class="prompt">${s}</div>${cue}`;
}
const INPUT_ATTRS = 'lang="es" autocomplete="off" autocorrect="off" autocapitalize="none" spellcheck="false"';
function redoHTML(rd, r){
  let b=0, out='';
  rd.segs.forEach((s,i)=>{
    if('blank' in s){
      const k=b++, cls = r ? (r.per[k]?'ok':'bad') : '', w=Math.max(4, s.blank.length+2);
      out += (i&&!s.glue?' ':'') + `<input type="text" class="bl ${cls}" data-b="${k}" ${INPUT_ATTRS} enterkeyhint="${r?'next':'done'}" ${r?'readonly':''} style="width:calc(${w}ch + 18px);max-width:100%" value="${esc((S.blanks&&S.blanks[k])||'')}">`;
    } else out += (i&&!s.glue?' ':'') + esc(s.text);
  });
  return `<div class="redo">${out}</div>`;
}
function renderDrill(){
  const it=S.cur, r=S.res, pos=S.done.size, pct=100*pos/S.total, rd=S.curRedo;
  const kind = rd ? 'Repite · solo lo que fallaste' : {tr:'Traduce', gap:'Completa', mc:'Elige'}[it.t];
  const where = S.mode==='today' ? (S.isNew.has(it.id) ? `Nuevo · unidad ${it.u}` : `Repaso · unidad ${it.u}`) : (it.w?'repaso':'');
  let body = `${header(`${esc(S.title)} · ${pos}/${S.total}`)}<div class="bar"><i style="width:${pct}%"></i></div>
    <div class="toprow"><span class="label">${kind}${where?' · '+where:''}</span><button class="quiet" id="stop">Parar</button></div>${promptHTML(it)}`;
  if(it.t==='mc'){
    if(!S.opts || S.optsFor!==it.id){ S.opts=shuffle(it.o.slice()); S.optsFor=it.id }
    body += `<div class="opts">${S.opts.map((o,i)=>{
      let cls=''; if(r){ if(o===it.acc[0]) cls='right'; else if(o===S.picked) cls='wrong' }
      return `<button data-opt="${i}" class="${cls}" ${r?'disabled':''}>${esc(o)}</button>` }).join('')}</div>`;
  } else if(rd){
    if(!S.blanks) S.blanks = rd.segs.filter(s=>'blank' in s).map(()=> '');
    body += redoHTML(rd, r);
  } else {
    const inp = `<input type="text" id="ans" ${INPUT_ATTRS} enterkeyhint="${r?'next':'done'}" ${r?'readonly':''} value="${esc(S.input)}" placeholder="${it.t==='gap'?'Solo lo que falta':'Escribe en español'}">`;
    body += (it.fs||it.fe) ? `<div class="frame">${it.fs?`<span class="given">${esc(it.fs)} …</span>`:''}${inp}${it.fe?`<span class="given">… ${esc(it.fe)}</span>`:''}</div>` : inp;
  }
  if(!r){
    if(it.t!=='mc') body += `<div class="row"><button class="primary" id="go">Comprobar</button></div>`;
  } else {
    body += verdictHTML(it, r, rd);
    body += `<div class="row"><button class="primary" id="nx">Siguiente</button>${(!r.ok && it.t!=='mc')?'<button id="ovr">Tenía razón</button>':''}<button class="quiet" id="flag">Señalar</button></div><div id="flagBox"></div>`;
  }
  app.innerHTML = body;
  window.scrollTo(0,0);
  const ans=document.getElementById('ans');
  if(ans){ ans.focus(); ans.setSelectionRange(ans.value.length, ans.value.length);
    ans.onkeydown=e=>{ if(e.key==='Enter'){ e.preventDefault(); r ? next() : grade(ans.value) } } }
  const bls=[...app.querySelectorAll('input.bl')];
  bls.forEach((el,k)=>{
    el.oninput=()=>{ S.blanks[k]=el.value };
    el.onkeydown=e=>{ if(e.key!=='Enter') return; e.preventDefault();
      if(r) return next();
      if(k<bls.length-1) bls[k+1].focus(); else grade('') };
  });
  if(bls.length){ const first = r ? bls[0] : (bls.find(b=>!b.value)||bls[0]); first.focus() }
  app.querySelectorAll('[data-opt]').forEach(b=>b.onclick=()=>grade('', S.opts[+b.dataset.opt]));
  const go=document.getElementById('go'); if(go) go.onclick=()=>grade(ans?ans.value:'');
  const nx=document.getElementById('nx'); if(nx){ nx.onclick=next; if(!ans && !bls.length) nx.focus() }
  const ov=document.getElementById('ovr'); if(ov) ov.onclick=override;
  const fl=document.getElementById('flag'); if(fl) fl.onclick=openFlag;
  document.getElementById('stop').onclick=finish;
}
function markTypos(text, typos){
  if(!typos || !typos.length) return esc(text);
  const set=new Set(typos);
  return text.split(' ').map(w=>{ const p=parts(w); return set.has(loose(p.core)) ? esc(p.lead)+'<ins>'+esc(p.core)+'</ins>'+esc(p.trail) : esc(w) }).join(' ');
}
function verdictHTML(it, r, rd){
  let h='';
  if(r.ok){
    const head = {exact:'Correcto.', accent:'Correcto. Ojo a las tildes:', se:'Correcto. Aquí usamos la forma en -ra:', typo:'Correcto, con una errata:', override:'Anotado como correcto.'}[r.kind];
    let shownAns;
    if(it.t==='gap') shownAns = esc(fillGap(it, r.match));
    else if(it.t==='mc') shownAns = esc(it.show);
    else shownAns = markTypos(full(it, r.match), r.typos);
    h = `<div class="verdict ok"><div class="v-head">${head}</div>${r.kind!=='override'?`<div class="answer">${shownAns}</div>`:''}`;
  } else if(it.t==='mc'){
    h = `<div class="verdict bad"><div class="v-head">No.</div><div class="answer">${esc(it.show)}</div>`;
  } else if(it.t==='gap'){
    h = `<div class="verdict bad"><div class="v-head">No.</div><div class="answer">${esc(fillGap(it,r.best)).replace(esc(r.best),'<mark>'+esc(r.best)+'</mark>')}</div>${S.input.trim()?`<div class="yours">Tu respuesta: ${esc(S.input)}</div>`:''}`;
  } else if(rd){
    let k=0; const txt = rd.segs.map((s,i)=>{ const sp=(i&&!s.glue)?' ':''; if('blank' in s){ const ok=r.per[k++]; return sp+(ok?esc(s.blank):'<mark>'+esc(s.blank)+'</mark>') } return sp+esc(s.text) }).join('');
    h = `<div class="verdict bad"><div class="v-head">Todavía no.</div><div class="answer">${txt}</div>`;
  } else {
    const d = diffHTML(r.best, S.input);
    h = `<div class="verdict bad"><div class="v-head">No.</div><div class="answer">${[it.fs?esc(it.fs):'', d.exp, it.fe?esc(it.fe):''].filter(Boolean).join(' ')}</div>
      ${S.input.trim()?`<div class="yours">Tu respuesta: ${d.you}</div>`:''}`;
  }
  h += `<div class="note">${esc(it.note)}</div>`;
  if(it.alts && it.alts.length){
    const used = r.match ? loose(full(it, r.match)) : '';
    const others = it.alts.filter(a=>loose(a)!==used && loose(a)!==loose(it.show)).slice(0,3);
    if(r.ok && loose(it.show)!==used) others.unshift(it.show);
    if(others.length) h += `<div class="alts">También vale: ${others.map(esc).join(' · ')}</div>`;
  }
  return h + '</div>';
}
function fillGap(it, a){ return capS(it.s.replace(/___ \([^)]*\)/, a).replace('___', a)) }
const capS = s => s.replace(/^([¡¿]?)(\p{L})/u,(m,a,b)=>a+b.toUpperCase());
function openFlag(){
  const box=document.getElementById('flagBox');
  box.innerHTML=`<div style="display:flex;flex-direction:column;gap:8px"><textarea id="fc" rows="3" lang="es" placeholder="¿Qué falla? (opcional)"></textarea><div class="row"><button id="fs">Guardar nota</button></div></div>`;
  document.getElementById('fc').focus();
  document.getElementById('fs').onclick=()=>{
    const it=S.cur;
    store.notes.push({id:it.id, u:it.u, tipo:'Señalado', prompt:it.p||it.s, suya:(S.blanks?S.blanks.join(' / '):'')||S.input||S.picked||'', esperada:it.show, comentario:document.getElementById('fc').value.trim()});
    save(); box.innerHTML='<p class="small">Nota guardada.</p>';
  };
}
function renderEnd(){
  const answered = Object.keys(S.attempts).length;
  const miss=[...S.missed].map(id=>byId[id]);
  const list = miss.length ? `<section><h3>Fallos (${miss.length})</h3><ul class="misses">${miss.map(it=>`<li><div class="en">${esc(it.p||it.s)}</div><div class="answer">${esc(it.show)}</div></li>`).join('')}</ul></section>` : '';
  const left = S.queue.filter(id=>!S.done.has(id)).length;
  app.innerHTML = `${header(esc(S.title))}<div class="prompt">${left?'Sesión en pausa.':'Sesión terminada.'}</div>
    <p>${plural(answered,'ítem','ítems')} · ${S.firstTry} a la primera${answered?` (${Math.round(100*S.firstTry/answered)}%)`:''}. Todo guardado.</p>
    ${left?`<p class="small">Lo que quedaba volverá a salir la próxima vez.</p>`:''}
    <div class="row"><button class="primary" id="home">Inicio</button></div>${list}`;
  document.getElementById('home').onclick=()=>renderHome();
}
document.addEventListener('keydown',e=>{
  if(!S||!S.res||e.key!=='Enter') return;
  const a=document.activeElement;
  if(a && (a.tagName==='INPUT'||a.tagName==='TEXTAREA'||a.tagName==='BUTTON')) return;
  e.preventDefault(); next();
});
// a new calendar day while the app sits open: refresh the home screen
document.addEventListener('visibilitychange',()=>{ if(!document.hidden && !S) renderHome() });
if('serviceWorker' in navigator) navigator.serviceWorker.register('sw.js').catch(()=>{});
if(navigator.storage && navigator.storage.persist) navigator.storage.persist().catch(()=>{});
pruneStore();
renderHome();
