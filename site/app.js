(function(){
'use strict';
var D=window.SVOK, app=document.getElementById('app'), L='ABCDEFGH';
if(!D){app.innerHTML='<p>Nepavyko įkelti duomenų. Perkrauk puslapį.</p>';return}

/* ---------- helpers ---------- */
function store(k,v){try{if(v===undefined)return JSON.parse(localStorage.getItem('svok_'+k)||'null');if(v===null)localStorage.removeItem('svok_'+k);else localStorage.setItem('svok_'+k,JSON.stringify(v))}catch(e){return null}}
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function shuffle(a){a=a.slice();for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=a[i];a[i]=a[j];a[j]=t}return a}
function plain(h){var d=document.createElement('div');d.innerHTML=h;return (d.textContent||'').replace(/\s+/g,' ').trim()}
function wrapTables(el){el.querySelectorAll('.content table').forEach(function(t){if(t.parentNode.classList.contains('tablewrap'))return;var w=document.createElement('div');w.className='tablewrap';t.parentNode.insertBefore(w,t);w.appendChild(t)})}
function fmtTime(s){var m=Math.floor(s/60),x=s%60;return m+':'+(x<10?'0':'')+x}
function letters(a){return a.map(function(j){return L[j]}).join(', ')}

/* ---------- question bank ---------- */
function mk(id,n,r,src){return{id:id,n:n,q:/^</.test(r.q)?r.q:'<p>'+esc(r.q)+'</p>',o:r.o.map(function(x){return r.html?x:esc(x)}),a:r.a,conflict:r.conflict,why:r.why,refs:r.refs||[],src:src}}
function extras(q,open){return (q.conflict?'<div class="conflict"><b>⚠ Sąsiuvinio atsakymas patikslintas.</b> '+esc(q.conflict)+'</div>':'')+(q.why?'<div class="why"><b>💡 Kodėl?</b> '+esc(q.why)+'</div>':'')+(q.refs&&q.refs.length?'<details class="refs"'+(open?' open':'')+'><summary>📚 Šaltiniai ('+q.refs.length+')</summary><ul>'+q.refs.map(function(r){return '<li>'+esc(r)+'</li>'}).join('')+'</ul></details>':'')}
var PRE=D.pre.map(function(q,i){return mk('p:'+i,i+1,q,'Pradinis testas, '+(i+1)+' kl.')});
var FIN=D.fin.map(function(q){return mk('f:'+q.n,q.n,q,'Baigiamasis testas, '+q.n+' kl.')});
var MT=(D.mtests||[]).map(function(t,ti){return{name:t.name,qs:t.qs.map(function(q){return mk('m'+ti+':'+q.n,q.n,q,'Modulio testas „'+t.name+'“, '+q.n+' kl.')})}});
var ALL=PRE.concat(FIN);MT.forEach(function(t){ALL=ALL.concat(t.qs)});
var BYID={};ALL.forEach(function(q){BYID[q.id]=q});
function range(a,b){return FIN.filter(function(q){return q.n>=a&&q.n<=b})}
var TOPICS=[
 {k:'t-vanduo',name:'Vandentiekis ir nuotekos',qs:range(1,17)},
 {k:'t-sildymas',name:'Šildymas',qs:range(18,39).concat(range(102,102))},
 {k:'t-sauga',name:'Darbų sauga ir brėžiniai',qs:range(40,47).concat(range(99,101))},
 {k:'t-vedinimas',name:'Vėdinimas',qs:range(49,98)},
 {k:'t-siurbliai',name:'Šilumos siurbliai',qs:range(103,111)}
];
function quizDef(kind){
  var m;
  if(kind==='pradinis')return{title:'Pradinis testas',qs:PRE};
  if(kind==='baigiamasis')return{title:'Baigiamasis testas',qs:FIN};
  if(kind==='baigiamasis-mix')return{title:'Baigiamasis testas (sumaišytas)',qs:FIN,mix:true};
  if((m=/^egzaminas(\d*)$/.exec(kind))){var n=+m[1]||30;return{title:'Egzamino simuliacija ('+n+')',qs:FIN,mix:true,limit:n,timer:true}}
  if(kind==='klaidos')return{title:'Mano klaidos',qs:Object.keys(wrong()).map(function(k){return BYID[k]}).filter(Boolean),mix:true};
  if(kind==='pazymeti')return{title:'Pažymėti klausimai',qs:Object.keys(flags()).map(function(k){return BYID[k]}).filter(Boolean)};
  if((m=/^modulis(\d+)$/.exec(kind))&&MT[+m[1]])return{title:'Modulio testas: '+MT[+m[1]].name,qs:MT[+m[1]].qs};
  for(var i=0;i<TOPICS.length;i++)if(TOPICS[i].k===kind)return{title:'Tema: '+TOPICS[i].name,qs:TOPICS[i].qs,mix:true};
  return null;
}
function wrong(){return store('wrong')||{}}
function flags(){return store('flags')||{}}
function best(k){var b=store('best')||{};return b[k]}
function setNav(k){document.querySelectorAll('nav a').forEach(function(a){a.classList.toggle('on',a.dataset.nav===k)})}

/* ---------- theme ---------- */
var themeBtn=document.getElementById('theme');
function applyTheme(){var t=store('theme');if(t)document.documentElement.setAttribute('data-theme',t);else document.documentElement.removeAttribute('data-theme');
  if(themeBtn){var dark=t?t==='dark':matchMedia('(prefers-color-scheme: dark)').matches;themeBtn.textContent=dark?'☀':'☾';themeBtn.title=dark?'Šviesi tema':'Tamsi tema'}}
if(themeBtn)themeBtn.onclick=function(){var t=store('theme'),dark=t?t==='dark':matchMedia('(prefers-color-scheme: dark)').matches;store('theme',dark?'light':'dark');applyTheme()};
applyTheme();

/* ---------- lightbox ---------- */
var lb=document.createElement('div');lb.className='lightbox';lb.hidden=true;lb.innerHTML='<img alt="Padidintas paveikslėlis"><button aria-label="Uždaryti">✕</button>';document.body.appendChild(lb);
lb.onclick=function(){lb.hidden=true};
document.addEventListener('click',function(e){var im=e.target.closest&&e.target.closest('.content img');if(!im)return;if(im.closest('.opt'))return;e.preventDefault();lb.querySelector('img').src=im.src;lb.hidden=false});
document.addEventListener('keydown',function(e){if(e.key==='Escape')lb.hidden=true});

/* ---------- back to top ---------- */
var topBtn=document.createElement('button');topBtn.className='totop';topBtn.textContent='↑';topBtn.title='Į viršų';topBtn.hidden=true;document.body.appendChild(topBtn);
topBtn.onclick=function(){window.scrollTo({top:0,behavior:'smooth'})};
window.addEventListener('scroll',function(){topBtn.hidden=window.scrollY<600},{passive:true});

/* ---------- pages ---------- */
function card(h,t,s,b,extra){return '<a class="card'+(extra||'')+'" href="'+h+'"><h3>'+esc(t)+'</h3><div class="stat">'+esc(s)+(b!=null?' · geriausias: <b>'+b+'%</b>':'')+'</div></a>'}
function resumeCard(){var r=store('run');if(!r||!quizDef(r.kind))return '';return '<a class="card accent" href="#/testas/'+r.kind+'?resume"><h3>Tęsti nebaigtą testą</h3><div class="stat">'+esc(r.title)+' · '+r.i+' / '+r.ids.length+' atsakyta</div></a>'}
function home(){
  setNav('home');
  var done=store('done')||{}, dn=Object.keys(done).length, tn=D.modules.reduce(function(s,m){return s+m.tasks.length},0);
  var w=Object.keys(wrong()).length, st=store('stats')||{runs:0,answered:0,correct:0};
  app.innerHTML='<h1>Pasiruošk ŠVOK montuotojo egzaminui</h1>'+
  '<p class="muted">Šildymo, vėdinimo, oro kondicionavimo sistemų montuotojo (III lygis) sąsiuvinio medžiaga: '+ALL.length+' testo klausimų ir '+tn+' praktinės užduotys su atsakymais.</p>'+
  (st.answered?'<div class="stats"><div><b>'+st.runs+'</b><span>baigti testai</span></div><div><b>'+st.answered+'</b><span>atsakyta klausimų</span></div><div><b>'+Math.round(st.correct/st.answered*100)+'%</b><span>teisingų</span></div><div><b>'+dn+'/'+tn+'</b><span>užduočių atlikta</span></div></div>':'')+
  '<div class="grid">'+resumeCard()+
  card('#/testas/egzaminas30','Egzamino simuliacija','30 atsitiktinių klausimų su laikmačiu',best('egzaminas30'),' accent')+
  (w?card('#/testas/klaidos','Mano klaidos','Kartok '+w+' klausimus, kuriuose suklydai'):'')+
  card('#/testai','Visi testai','Pagal temas, modulius ir visas testas')+
  card('#/mokytis','Mokytis','Visi klausimai su teisingais atsakymais ir paieška')+
  card('#/uzduotys','Praktinės užduotys','Atlikta '+dn+' iš '+tn)+
  '</div>';
}
function testsPage(){
  setNav('testai');
  var w=Object.keys(wrong()).length,f=Object.keys(flags()).length;
  app.innerHTML='<h1>Testai</h1><p class="muted">Atsakymas tikrinamas iš karto. Klaviatūra: A–F arba 1–6 pasirenka atsakymą, Enter tikrina ir pereina toliau.</p>'+
  '<div class="grid">'+resumeCard()+'</div>'+
  '<h2>Egzamino simuliacija</h2><p class="muted">Atsitiktiniai baigiamojo testo klausimai su laikmačiu.</p><div class="grid">'+
  [10,20,30,50].map(function(n){return card('#/testas/egzaminas'+n,n+' klausimų','~'+Math.round(n*0.75)+' min.',best('egzaminas'+n))}).join('')+'</div>'+
  '<h2>Pagal temas</h2><div class="grid">'+TOPICS.map(function(t){return card('#/testas/'+t.k,t.name,t.qs.length+' klausimai',best(t.k))}).join('')+'</div>'+
  (MT.length?'<h2>Modulių testai</h2><div class="grid">'+MT.map(function(t,i){return card('#/testas/modulis'+i,t.name,t.qs.length+' klausimai',best('modulis'+i))}).join('')+'</div>':'')+
  '<h2>Visi testai</h2><div class="grid">'+
  card('#/testas/baigiamasis','Baigiamasis testas','Visi '+FIN.length+' klausimai iš eilės',best('baigiamasis'))+
  card('#/testas/baigiamasis-mix','Baigiamasis (sumaišytas)','Visi '+FIN.length+' klausimai atsitiktine tvarka',best('baigiamasis-mix'))+
  card('#/testas/pradinis','Pradinis testas','Įvadas į profesiją, '+PRE.length+' klausimų',best('pradinis'))+
  '</div><h2>Kartojimas</h2><div class="grid">'+
  card('#/testas/klaidos','Mano klaidos',w?w+' klausimai kartojimui':'Kol kas klaidų nėra')+
  card('#/testas/pazymeti','Pažymėti klausimai',f?f+' pažymėti ☆':'Pažymėk klausimus žvaigždute teste')+
  '</div>';
}

function startQuiz(kind,resume){
  setNav('testai');
  var def=quizDef(kind); if(!def)return notFound();
  var st, saved=store('run');
  if(resume&&saved&&saved.kind===kind){st=saved}
  else{
    var qs=def.mix?shuffle(def.qs):def.qs.slice(); if(def.limit)qs=qs.slice(0,def.limit);
    st={kind:kind,title:def.title,ids:qs.map(function(q){return q.id}),i:0,score:0,log:[],t0:Date.now(),el:0};
  }
  if(!st.ids.length){app.innerHTML='<h1>'+esc(def.title)+'</h1><p>Sąrašas tuščias. '+(kind==='klaidos'?'Išspręsk testą ir čia atsiras klausimai, kuriuose suklydai.':'Teste pažymėk klausimus žvaigždute ☆, ir jie atsiras čia.')+'</p><a class="btn" href="#/testai">Į testus</a>';return}
  var sel=[],checked=false,timerId=null,started=Date.now();
  function elapsed(){return st.el+Math.floor((Date.now()-started)/1000)}
  function save(){st.el=elapsed();started=Date.now();store('run',st)}
  function render(){
    var q=BYID[st.ids[st.i]], multi=q.a.length>1, fl=flags()[q.id];
    sel=[];checked=false;
    app.innerHTML='<div class="row" style="justify-content:space-between"><span class="chip">'+esc(st.title)+'</span><span class="stat">'+(st.i+1)+' / '+st.ids.length+' · teisingai '+st.score+(def.timer?' · <span id="tm">'+fmtTime(elapsed())+'</span>':'')+'</span></div>'+
    '<div class="bar"><i style="width:'+(st.i/st.ids.length*100)+'%"></i></div>'+
    '<div class="qhead"><div class="q content">'+q.q+'</div><button class="flag'+(fl?' on':'')+'" id="flag" title="Pažymėti kartojimui" aria-label="Pažymėti kartojimui">'+(fl?'★':'☆')+'</button></div>'+
    (multi?'<div class="hint">Keli teisingi atsakymai, pažymėk visus ir spausk „Tikrinti“.</div>':'')+
    '<div class="opts">'+q.o.map(function(o,j){return '<button class="opt'+(multi?' multi':'')+'" data-j="'+j+'"><span class="k">'+L[j]+'</span><span class="content">'+o+'</span></button>'}).join('')+'</div>'+
    '<div id="fb"></div><div class="row"><button class="btn" id="go" disabled>Tikrinti</button><button class="btn ghost" id="quit">Baigti ir žiūrėti rezultatą</button></div>'+
    '<p class="stat src">'+esc(q.src)+'</p>';
    wrapTables(app);
    var go=document.getElementById('go');
    function pick(j){
      if(checked||j>=q.o.length)return;
      if(multi){var k=sel.indexOf(j);k<0?sel.push(j):sel.splice(k,1)}else sel=[j];
      app.querySelectorAll('.opt').forEach(function(x){x.classList.toggle('sel',sel.indexOf(+x.dataset.j)>=0)});
      go.disabled=!sel.length;
      if(!multi)check();
    }
    app.querySelectorAll('.opt').forEach(function(b){b.onclick=function(){pick(+b.dataset.j)}});
    go.onclick=function(){checked?next():check()};
    document.getElementById('quit').onclick=function(){result()};
    document.getElementById('flag').onclick=function(){var f=flags();if(f[q.id])delete f[q.id];else f[q.id]=1;store('flags',f);this.classList.toggle('on',!!f[q.id]);this.textContent=f[q.id]?'★':'☆'};
    keyHandler=function(e){
      if(e.ctrlKey||e.metaKey||e.altKey||!lb.hidden)return;
      var k=e.key.toUpperCase(), j=L.indexOf(k); if(j<0&&/^[1-6]$/.test(k))j=+k-1;
      if(j>=0&&k.length===1){pick(j);e.preventDefault()}
      else if(e.key==='Enter'&&!go.disabled&&document.activeElement!==go){go.click();e.preventDefault()}
    };
    function check(){
      checked=true;
      var ok=sel.length===q.a.length&&sel.every(function(j){return q.a.indexOf(j)>=0});
      app.querySelectorAll('.opt').forEach(function(x){var j=+x.dataset.j;x.classList.remove('sel');x.disabled=true;if(q.a.indexOf(j)>=0)x.classList.add('ok');else if(sel.indexOf(j)>=0)x.classList.add('bad')});
      var w=wrong(); if(ok){st.score++; if(kind==='klaidos')delete w[q.id]} else w[q.id]=1; store('wrong',w);
      var s=store('stats')||{runs:0,answered:0,correct:0};s.answered++;if(ok)s.correct++;store('stats',s);
      st.log.push({id:q.id,sel:sel.slice(),ok:ok}); st.i++; save();
      document.getElementById('fb').innerHTML='<div class="fb '+(ok?'ok':'bad')+'">'+(ok?'Teisingai!':'Neteisingai. Teisingas atsakymas: '+letters(q.a))+'</div>'+extras(q);
      go.disabled=false; go.textContent=st.i<st.ids.length?'Kitas klausimas →':'Rezultatai'; go.focus({preventScroll:true});
    }
  }
  function next(){if(st.i<st.ids.length){render();window.scrollTo(0,0)}else result()}
  function result(){
    keyHandler=null; clearInterval(timerId); st.el=elapsed(); started=Date.now(); store('run',null);
    var n=st.log.length;
    if(!n){location.hash='#/testai';return}
    var pct=Math.round(st.score/n*100), b=store('best')||{};
    var full=n===st.ids.length;
    if(full&&kind!=='klaidos'&&kind!=='pazymeti'&&(b[kind]==null||pct>b[kind])){b[kind]=pct;store('best',b)}
    var s=store('stats')||{runs:0,answered:0,correct:0};s.runs++;store('stats',s);
    var bad=st.log.filter(function(x){return!x.ok});
    app.innerHTML='<span class="chip">'+esc(st.title)+'</span><div class="card result" style="margin-top:12px"><div class="stat">Rezultatas'+(full?'':' (atsakyta '+n+' iš '+st.ids.length+')')+'</div><div class="big '+(pct>=80?'good':pct>=60?'mid':'low')+'">'+pct+'%</div><div>'+st.score+' iš '+n+' teisingai'+(def.timer?' per '+fmtTime(st.el):'')+'. '+(pct>=80?'Puikiai pasiruošęs!':pct>=60?'Neblogai, pakartok klaidas.':'Dar reikia pasimokyti.')+'</div>'+
    '<div class="row" style="margin-top:14px"><a class="btn" href="#/testas/'+kind+'?'+Date.now()+'">Kartoti</a>'+(bad.length?'<a class="btn ghost" href="#/testas/klaidos?'+Date.now()+'">Kartoti klaidas</a>':'')+'<a class="btn ghost" href="#/testai">Kiti testai</a></div></div>'+
    (bad.length?'<h2>Klaidų peržiūra ('+bad.length+')</h2>'+bad.map(function(x){var q=BYID[x.id];return '<div class="review"><div class="content">'+q.q+'</div><ol class="ropts">'+q.o.map(function(o,j){var c=q.a.indexOf(j)>=0?'right':x.sel.indexOf(j)>=0?'your':'';return '<li class="'+c+'"><b>'+L[j]+'.</b> <span class="content">'+o+'</span>'+(c==='right'?' ✓':c==='your'?' ✗':'')+'</li>'}).join('')+'</ol>'+extras(q)+'</div>'}).join(''):'');
    wrapTables(app); window.scrollTo(0,0);
  }
  if(def.timer){timerId=setInterval(function(){var t=document.getElementById('tm');if(t)t.textContent=fmtTime(elapsed());else clearInterval(timerId)},1000)}
  if(st.i>=st.ids.length)result();else render();
}

function studyPage(){
  setNav('mokytis');
  var groups=[{name:'Pradinis testas',qs:PRE},{name:'Baigiamasis testas',qs:FIN}].concat(MT.map(function(t){return{name:'Modulio testas: '+t.name,qs:t.qs}}));
  app.innerHTML='<h1>Mokytis</h1><p class="muted">Visi klausimai su teisingais atsakymais, paaiškinimais 💡 ir šaltiniais 📚. Ženklu ⚠ pažymėti klausimai, kuriuose sąsiuvinio atsakymas prieštarauja realiems techniniams reikalavimams. Jie patikslinti.</p>'+
  '<div class="searchbar"><input type="search" id="q" placeholder="Ieškoti, pvz. radiatorius, ortakis, slėgis…" autocomplete="off"><label class="chk"><input type="checkbox" id="hide"> Slėpti atsakymus</label><label class="chk"><input type="checkbox" id="onlyc"> Tik patikslinti ⚠</label></div><p class="stat" id="cnt"></p><div id="list"></div>';
  var list=document.getElementById('list'), inp=document.getElementById('q'), hide=document.getElementById('hide');
  var html=groups.map(function(g,gi){return '<h2 class="grp" data-g="'+gi+'">'+esc(g.name)+'</h2>'+g.qs.map(function(q){
    return '<div class="sq'+(q.conflict?' hasc':'')+'" data-g="'+gi+'" data-t="'+esc((plain(q.q)+' '+q.o.map(plain).join(' ')).toLowerCase())+'"><div class="content q2"><span class="num">'+q.n+'.</span> '+q.q+'</div><ul class="sopts">'+q.o.map(function(o,j){return '<li class="'+(q.a.indexOf(j)>=0?'right':'')+'"><b>'+L[j]+'.</b> <span class="content">'+o+'</span></li>'}).join('')+'</ul><div class="sx">'+extras(q)+'</div></div>'}).join('')}).join('');
  list.innerHTML=html; wrapTables(list);
  var items=[].slice.call(list.querySelectorAll('.sq')), heads=[].slice.call(list.querySelectorAll('.grp'));
  var onlyc=document.getElementById('onlyc');onlyc.onchange=function(){filter()};
  function filter(){var v=inp.value.trim().toLowerCase(),n=0,seen={},oc=onlyc.checked;items.forEach(function(it){var s=(!v||it.dataset.t.indexOf(v)>=0)&&(!oc||it.classList.contains('hasc'));it.hidden=!s;if(s){n++;seen[it.dataset.g]=1}});heads.forEach(function(h){h.hidden=!seen[h.dataset.g]});document.getElementById('cnt').textContent=(v||oc)?'Rasta: '+n:''}
  var tmo;inp.oninput=function(){clearTimeout(tmo);tmo=setTimeout(filter,120)};
  hide.onchange=function(){list.classList.toggle('hideans',hide.checked)};
  list.addEventListener('click',function(e){if(!list.classList.contains('hideans'))return;var sq=e.target.closest('.sq');if(sq)sq.classList.toggle('reveal')});
}

function tasksPage(){
  setNav('uzduotys'); var done=store('done')||{};
  app.innerHTML='<h1>Praktinės užduotys</h1><p class="muted">Pirmiausia pabandyk atsakyti pats, tada atsiversk atsakymą. Atliktas užduotis pasižymėk.</p><div class="grid">'+
  D.modules.map(function(m,i){var c=m.tasks.filter(function(t){return done[i+':'+t.n]}).length;return '<a class="card" href="#/uzduotys/'+i+'"><h3>'+esc(m.name)+'</h3><div class="stat">'+m.tasks.length+' užduotys · atlikta '+c+'</div><div class="bar sm"><i style="width:'+(c/m.tasks.length*100)+'%"></i></div></a>'}).join('')+'</div>';
}
function modulePage(i){
  setNav('uzduotys'); var m=D.modules[i]; if(!m)return notFound(); var done=store('done')||{};
  var c=m.tasks.filter(function(t){return done[i+':'+t.n]}).length;
  app.innerHTML='<a href="#/uzduotys">← Visi moduliai</a><h1 style="margin-top:10px">'+esc(m.name)+'</h1><p class="muted" id="prog">Atlikta '+c+' iš '+m.tasks.length+'</p>'+
  '<div class="row" style="margin-bottom:12px"><button class="btn ghost sm" id="openall">Išskleisti visas</button><button class="btn ghost sm" id="ansall">Rodyti visus atsakymus</button>'+(D.modules[i+1]?'<a class="btn ghost sm" href="#/uzduotys/'+(i+1)+'">Kitas modulis →</a>':'')+'</div>'+
  m.tasks.map(function(t){var k=i+':'+t.n;return '<details class="task'+(done[k]?' done':'')+'" data-k="'+k+'" id="u'+t.n+'"><summary><span class="n">'+(done[k]?'✓':t.n)+'</span><span>'+esc(t.title)+'</span></summary><div class="body"><div class="content">'+t.q+'</div>'+
  '<div class="row" style="margin-top:14px">'+(t.a?'<button class="btn ghost showans">Rodyti atsakymą</button>':'<span class="stat">Šios užduoties atsakymo sąsiuvinyje nėra, pasitikrink su mokytoju.</span>')+'<label class="chk"><input type="checkbox" class="dn"'+(done[k]?' checked':'')+'> Atlikta</label></div>'+
  (t.a?'<div class="ans" hidden><h4>Atsakymas'+(t.extra?' <span class="chip">parengta papildomai, sąsiuvinyje atsakymo nėra</span>':'')+'</h4><div class="content">'+t.a+'</div></div>':'')+'</div></details>'}).join('');
  wrapTables(app);
  function toggleAns(b,show){var a=b.closest('.body').querySelector('.ans');a.hidden=show===undefined?!a.hidden:!show;b.textContent=a.hidden?'Rodyti atsakymą':'Slėpti atsakymą'}
  app.querySelectorAll('.showans').forEach(function(b){b.onclick=function(){toggleAns(b)}});
  var open=false,ans=false;
  document.getElementById('openall').onclick=function(){open=!open;app.querySelectorAll('details.task').forEach(function(d){d.open=open});this.textContent=open?'Suskleisti visas':'Išskleisti visas'};
  document.getElementById('ansall').onclick=function(){ans=!ans;app.querySelectorAll('details.task').forEach(function(d){if(ans)d.open=true});app.querySelectorAll('.showans').forEach(function(b){toggleAns(b,ans)});this.textContent=ans?'Slėpti visus atsakymus':'Rodyti visus atsakymus'};
  app.querySelectorAll('.dn').forEach(function(cb){cb.onchange=function(){var d=cb.closest('details'),k=d.dataset.k,s=store('done')||{};if(cb.checked)s[k]=1;else delete s[k];store('done',s);d.classList.toggle('done',cb.checked);d.querySelector('summary .n').textContent=cb.checked?'✓':k.split(':')[1];
    var c=m.tasks.filter(function(t){return s[i+':'+t.n]}).length;document.getElementById('prog').textContent='Atlikta '+c+' iš '+m.tasks.length}});
}
function notFound(){app.innerHTML='<h1>Puslapis nerastas</h1><a href="#/">Į pradžią</a>'}

var reset=document.getElementById('reset');
if(reset)reset.onclick=function(e){e.preventDefault();if(confirm('Ištrinti visą progresą (rezultatus, klaidas, pažymėjimus)?')){['wrong','flags','best','done','stats','run'].forEach(function(k){store(k,null)});route()}};

var keyHandler=null;
document.addEventListener('keydown',function(e){if(keyHandler&&!/INPUT|TEXTAREA/.test((e.target.tagName||'')))keyHandler(e)});
function route(){
  keyHandler=null;
  var full=(location.hash||'#/').slice(1), parts=full.split('?'), h=parts[0], qs=parts[1]||'', p=h.split('/').filter(Boolean);
  if(!p.length)home(); else if(p[0]==='testai')testsPage(); else if(p[0]==='testas')startQuiz(p[1],qs==='resume');
  else if(p[0]==='mokytis')studyPage();
  else if(p[0]==='uzduotys')p[1]!=null?modulePage(+p[1]):tasksPage(); else notFound();
  window.scrollTo(0,0);
}
window.addEventListener('hashchange',route); route();
})();
