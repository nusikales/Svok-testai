(function(){
'use strict';
var D=window.SVOK, app=document.getElementById('app'), L='ABCDEFGH';
function store(k,v){try{if(v===undefined){return JSON.parse(localStorage.getItem('svok_'+k)||'null')}localStorage.setItem('svok_'+k,JSON.stringify(v))}catch(e){return null}}
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function shuffle(a){a=a.slice();for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=a[i];a[i]=a[j];a[j]=t}return a}
function wrapTables(el){el.querySelectorAll('.content table').forEach(function(t){if(t.parentNode.classList.contains('tablewrap'))return;var w=document.createElement('div');w.className='tablewrap';t.parentNode.insertBefore(w,t);w.appendChild(t)})}
// Normalise questions into one bank
function qid(set,i){return set+':'+i}
var PRE=D.pre.map(function(q,i){return{id:qid('p',i),n:i+1,q:'<p>'+esc(q.q)+'</p>',o:q.o.map(esc),a:q.a}});
var FIN=D.fin.map(function(q){return{id:qid('f',q.n),n:q.n,q:/^</.test(q.q)?q.q:'<p>'+esc(q.q)+'</p>',o:q.o.map(function(x){return q.html?x:esc(x)}),a:q.a}});
var ALL=PRE.concat(FIN), BYID={};ALL.forEach(function(q){BYID[q.id]=q});
function wrong(){return store('wrong')||{}}
function setNav(k){document.querySelectorAll('nav a').forEach(function(a){a.classList.toggle('on',a.dataset.nav===k)})}
function best(k){var b=store('best')||{};return b[k]}

function home(){
  setNav('home');
  var done=store('done')||{}, dn=Object.keys(done).length, tn=D.modules.reduce(function(s,m){return s+m.tasks.length},0);
  var w=Object.keys(wrong()).length;
  app.innerHTML='<h1>Pasiruošk ŠVOK montuotojo egzaminui</h1>'+
  '<p class="muted">Šildymo, vėdinimo, oro kondicionavimo sistemų montuotojo (III lygis) teorinių ir praktinių užduočių sąsiuvinio medžiaga: '+ALL.length+' testo klausimai ir '+tn+' praktinės užduotys su atsakymais.</p>'+
  '<h2>Testai</h2><div class="grid">'+
  card('#/testas/egzaminas','Egzamino simuliacija','30 atsitiktinių klausimų iš baigiamojo testo',best('egzaminas'))+
  card('#/testas/baigiamasis','Baigiamasis testas','Visi '+FIN.length+' klausimai',best('baigiamasis'))+
  card('#/testas/pradinis','Pradinis testas','Įvadas į profesiją, '+PRE.length+' klausimų',best('pradinis'))+
  (w?card('#/testas/klaidos','Mano klaidos','Kartok klausimus, kuriuose suklydai ('+w+')'):'')+
  '</div><h2>Praktinės užduotys</h2><p class="muted">Atlikta '+dn+' iš '+tn+'.</p><div class="grid">'+
  D.modules.map(function(m,i){var c=m.tasks.filter(function(t){return done[i+':'+t.n]}).length;return card('#/uzduotys/'+i,m.name,c+' / '+m.tasks.length+' atlikta')}).join('')+'</div>';
}
function card(h,t,s,b){return '<a class="card" href="'+h+'"><h3>'+esc(t)+'</h3><div class="stat">'+esc(s)+(b!=null?' · geriausias: '+b+'%':'')+'</div></a>'}

function testsPage(){
  setNav('testai');
  var w=Object.keys(wrong()).length;
  app.innerHTML='<h1>Testai</h1><p class="muted">Pasirink testą. Atsakymą patikrinsi iš karto, o pabaigoje matysi rezultatą ir klaidų peržiūrą.</p><div class="grid">'+
  card('#/testas/egzaminas','Egzamino simuliacija','30 atsitiktinių klausimų, sumaišyta tvarka',best('egzaminas'))+
  card('#/testas/baigiamasis','Baigiamasis testas','Visi '+FIN.length+' klausimai iš eilės',best('baigiamasis'))+
  card('#/testas/baigiamasis-mix','Baigiamasis (sumaišytas)','Visi '+FIN.length+' klausimai atsitiktine tvarka',best('baigiamasis-mix'))+
  card('#/testas/pradinis','Pradinis testas','Įvadas į profesiją, '+PRE.length+' klausimų',best('pradinis'))+
  card('#/testas/klaidos','Mano klaidos',w?w+' klausimai kartojimui':'Kol kas klaidų nėra')+
  '</div>';
}

function startQuiz(kind){
  setNav('testai');
  var qs, title;
  if(kind==='pradinis'){qs=PRE;title='Pradinis testas'}
  else if(kind==='baigiamasis'){qs=FIN;title='Baigiamasis testas'}
  else if(kind==='baigiamasis-mix'){qs=shuffle(FIN);title='Baigiamasis testas (sumaišytas)'}
  else if(kind==='egzaminas'){qs=shuffle(FIN).slice(0,30);title='Egzamino simuliacija'}
  else if(kind==='klaidos'){qs=shuffle(Object.keys(wrong()).map(function(k){return BYID[k]}).filter(Boolean));title='Mano klaidos'}
  else return notFound();
  if(!qs.length){app.innerHTML='<h1>'+title+'</h1><p>Klaidų sąrašas tuščias. Puiku! Išspręsk testą ir čia atsiras klausimai, kuriuose suklydai.</p><a class="btn" href="#/testai">Į testus</a>';return}
  var st={i:0,sel:[],checked:false,score:0,log:[]};
  function render(){
    var q=qs[st.i], multi=q.a.length>1;
    app.innerHTML='<div class="row" style="justify-content:space-between"><span class="chip">'+esc(title)+'</span><span class="stat">Klausimas '+(st.i+1)+' / '+qs.length+' · teisingai '+st.score+'</span></div>'+
    '<div class="bar"><i style="width:'+(st.i/qs.length*100)+'%"></i></div>'+
    '<div class="q content">'+q.q+'</div>'+(multi?'<div class="hint">Šiame klausime yra keli teisingi atsakymai, pažymėk visus.</div>':'')+
    '<div class="opts">'+q.o.map(function(o,j){return '<button class="opt'+(multi?' multi':'')+'" data-j="'+j+'"><span class="k">'+L[j]+'</span><span class="content">'+o+'</span></button>'}).join('')+'</div>'+
    '<div id="fb"></div><div class="row"><button class="btn" id="go" disabled>Tikrinti</button><a class="btn ghost" href="#/testai">Baigti</a></div>';
    wrapTables(app);
    var go=document.getElementById('go');
    app.querySelectorAll('.opt').forEach(function(b){b.onclick=function(){
      if(st.checked)return; var j=+b.dataset.j;
      if(multi){var k=st.sel.indexOf(j);k<0?st.sel.push(j):st.sel.splice(k,1)}else st.sel=[j];
      app.querySelectorAll('.opt').forEach(function(x){x.classList.toggle('sel',st.sel.indexOf(+x.dataset.j)>=0)});
      go.disabled=!st.sel.length;
      if(!multi)check();
    }});
    go.onclick=function(){st.checked?next():check()};
    function check(){
      st.checked=true;
      var ok=st.sel.length===q.a.length&&st.sel.every(function(j){return q.a.indexOf(j)>=0});
      app.querySelectorAll('.opt').forEach(function(x){var j=+x.dataset.j;x.classList.remove('sel');if(q.a.indexOf(j)>=0)x.classList.add('ok');else if(st.sel.indexOf(j)>=0)x.classList.add('bad')});
      var w=wrong(); if(ok){st.score++; if(kind==='klaidos')delete w[q.id]} else w[q.id]=1; store('wrong',w);
      st.log.push({q:q,sel:st.sel.slice(),ok:ok});
      document.getElementById('fb').innerHTML='<div class="fb '+(ok?'ok':'bad')+'">'+(ok?'Teisingai!':'Neteisingai. Teisingas atsakymas: '+q.a.map(function(j){return L[j]}).join(', '))+'</div>';
      go.disabled=false; go.textContent=st.i+1<qs.length?'Kitas klausimas':'Rezultatai'; go.focus();
    }
  }
  function next(){st.i++;st.sel=[];st.checked=false;if(st.i<qs.length){render();window.scrollTo(0,0)}else result()}
  function result(){
    var pct=Math.round(st.score/qs.length*100), b=store('best')||{};
    if(kind!=='klaidos'&&(b[kind]==null||pct>b[kind])){b[kind]=pct;store('best',b)}
    var bad=st.log.filter(function(x){return!x.ok});
    app.innerHTML='<span class="chip">'+esc(title)+'</span><div class="card" style="margin-top:12px"><div class="stat">Rezultatas</div><div class="big">'+pct+'%</div><div>'+st.score+' iš '+qs.length+' teisingai. '+(pct>=80?'Puikiai pasiruošęs!':pct>=60?'Neblogai, pakartok klaidas.':'Dar reikia pasimokyti.')+'</div>'+
    '<div class="row" style="margin-top:14px"><a class="btn" href="#/testas/'+kind+'?'+Date.now()+'">Kartoti</a>'+(bad.length?'<a class="btn ghost" href="#/testas/klaidos?'+Date.now()+'">Kartoti klaidas</a>':'')+'<a class="btn ghost" href="#/testai">Kiti testai</a></div></div>'+
    (bad.length?'<h2>Klaidų peržiūra</h2>'+bad.map(function(x){return '<div class="review"><div class="content">'+x.q.q+'</div><div class="your">Tavo atsakymas: '+x.sel.map(function(j){return L[j]}).join(', ')+'</div><div class="right"><b>Teisingas: '+x.q.a.map(function(j){return L[j]+'. '+(/</.test(x.q.o[j])?'':x.q.o[j])}).join('; ')+'</b></div></div>'}).join(''):'');
    wrapTables(app); window.scrollTo(0,0);
  }
  render();
}

function tasksPage(){
  setNav('uzduotys'); var done=store('done')||{};
  app.innerHTML='<h1>Praktinės užduotys</h1><p class="muted">Pirmiausia pabandyk atsakyti pats, tada atsiversk atsakymą. Atliktas užduotis pasižymėk.</p><div class="grid">'+
  D.modules.map(function(m,i){var c=m.tasks.filter(function(t){return done[i+':'+t.n]}).length;return card('#/uzduotys/'+i,m.name,m.tasks.length+' užduotys · atlikta '+c)}).join('')+'</div>';
}
function modulePage(i){
  setNav('uzduotys'); var m=D.modules[i]; if(!m)return notFound(); var done=store('done')||{};
  app.innerHTML='<a href="#/uzduotys">← Visi moduliai</a><h1 style="margin-top:10px">'+esc(m.name)+'</h1><p class="muted">'+m.tasks.length+' užduotys</p>'+
  m.tasks.map(function(t){var k=i+':'+t.n;return '<details class="task'+(done[k]?' done':'')+'" data-k="'+k+'"><summary><span class="n">'+t.n+'</span><span>'+esc(t.title)+'</span></summary><div class="body"><div class="content">'+t.q+'</div>'+
  '<div class="row" style="margin-top:14px">'+(t.a?'<button class="btn ghost showans">Rodyti atsakymą</button>':'<span class="stat">Šios užduoties atsakymo sąsiuvinyje nėra, pasitikrink su mokytoju.</span>')+'<label class="chk"><input type="checkbox" class="dn"'+(done[k]?' checked':'')+'> Atlikta</label></div>'+
  (t.a?'<div class="ans" hidden><h4>Atsakymas</h4><div class="content">'+t.a+'</div></div>':'')+'</div></details>'}).join('');
  wrapTables(app);
  app.querySelectorAll('.showans').forEach(function(b){b.onclick=function(){var a=b.closest('.body').querySelector('.ans');a.hidden=!a.hidden;b.textContent=a.hidden?'Rodyti atsakymą':'Slėpti atsakymą'}});
  app.querySelectorAll('.dn').forEach(function(c){c.onchange=function(){var d=c.closest('details'),k=d.dataset.k,s=store('done')||{};if(c.checked)s[k]=1;else delete s[k];store('done',s);d.classList.toggle('done',c.checked)}});
}
function notFound(){app.innerHTML='<h1>Puslapis nerastas</h1><a href="#/">Į pradžią</a>'}
function route(){
  var h=(location.hash||'#/').slice(1).split('?')[0], p=h.split('/').filter(Boolean);
  if(!p.length)home(); else if(p[0]==='testai')testsPage(); else if(p[0]==='testas')startQuiz(p[1]);
  else if(p[0]==='uzduotys')p[1]!=null?modulePage(+p[1]):tasksPage(); else notFound();
  if(!/^testas/.test(p[0]||''))window.scrollTo(0,0);
}
window.addEventListener('hashchange',route); route();
})();
