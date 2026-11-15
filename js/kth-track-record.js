(function(){
const grid=document.getElementById('tr-grid'),fa=document.getElementById('tr-fa');
let A='all',T='all',S='all',D=[];
function card(t){const n=t.photos.slice(0,5);return `<article class="tr-card" data-area="${t.area}" data-type="${t.type}"><div class="tr-car"><div class="tr-track">${n.map((p,i)=>`<img src="${p}" alt="${t.title} photo ${i+1}" width="1200" height="900" loading="lazy">`).join('')}</div>${n.length>1?'<button class="tr-nav tr-prev" aria-label="Previous photo">&#8249;</button><button class="tr-nav tr-next" aria-label="Next photo">&#8250;</button><div class="tr-dots">'+n.map((_,i)=>'<i class="'+(i?'':'on')+'"></i>').join('')+'</div>':''}<span class="tr-tag${t.side==='buyer'?' tr-tag-buy':''}">${t.status.toUpperCase()}</span>${t.note?`<span class="tr-note">${t.note}</span>`:''}</div><div class="tr-body"><h3>${t.title}</h3><p>${t.area} · ${t.type==='HDB'?'HDB resale':'Private condo'}</p>${t.dom?`<p class="tr-dom">${t.dom} days on market</p>`:''}</div></article>`}
let N=24;function render(){const F=D.filter(t=>(A==='all'||t.area===A)&&(T==='all'||t.type===T)&&(S==='all'||t.side===S));grid.innerHTML=F.slice(0,N).map(card).join('')||'<p>No homes match yet.</p>';const lm=document.getElementById('tr-more');lm.hidden=F.length<=N;lm.textContent='Load more ('+Math.min(N,F.length)+' of '+F.length+')';lm.onclick=()=>{N+=24;render()};
 grid.querySelectorAll('.tr-car').forEach(c=>{const tr=c.querySelector('.tr-track'),dots=[...c.querySelectorAll('.tr-dots i')];const go=d=>tr.scrollBy({left:d*tr.clientWidth,behavior:'smooth'});
  c.querySelector('.tr-prev')?.addEventListener('click',()=>go(-1));c.querySelector('.tr-next')?.addEventListener('click',()=>go(1));
  tr.addEventListener('scroll',()=>{const i=Math.round(tr.scrollLeft/tr.clientWidth);dots.forEach((d,j)=>d.classList.toggle('on',i===j))},{passive:true})})}
function chips(el,vals,cur,set){el.innerHTML=vals.map(([v,l])=>v===null?`<span class="tr-fgl">${l}</span>`:`<button class="tr-chip" data-v="${v}" aria-pressed="${v===cur}">${l}</button>`).join('');el.onclick=e=>{const b=e.target.closest('.tr-chip');if(!b)return;set(b.dataset.v);el.querySelectorAll('.tr-chip').forEach(x=>x.setAttribute('aria-pressed',x===b));render()}}
fetch('data/kth/transactions.json').then(r=>r.json()).then(j=>{D=j.transactions;
 const u=k=>[...new Set(D.filter(t=>t.type===k).map(t=>t.area))].sort();
 chips(fa,[['all','All areas'],[null,'HDB towns'],...u('HDB').map(a=>[a,a]),[null,'Private districts'],...u('Private').map(a=>[a,a])],'all',v=>A=v);
 chips(document.getElementById('tr-fs'),[['all','Sold & bought'],['seller','Sold'],['buyer','Bought']],'all',v=>S=v);
 chips(document.getElementById('tr-ft'),[['all','HDB & private'],['HDB','HDB'],['Private','Private']],'all',v=>T=v);
 
 render()});
})();
;(()=>{const el=document.getElementById('next-home');if(!el)return;const RM=matchMedia('(prefers-reduced-motion: reduce)');if(RM.matches){el.classList.add('in');return}
const io=new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting){el.classList.add('in');io.disconnect()}})},{threshold:.2});io.observe(el)})();
