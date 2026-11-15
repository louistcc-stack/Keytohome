(()=>{
const g=document.getElementById('rv-grid'),fs=document.getElementById('rv-fs');let S='all',D=[];
const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const fmt=d=>{if(!d||d.startsWith('YYYY'))return'';const x=new Date(d+'T00:00:00');return x.toLocaleDateString('en-SG',{day:'numeric',month:'short',year:'numeric'})};
function card(r){const st=r.rating?`<span class="rv-stars" aria-label="${r.rating} out of 5 stars">${'★'.repeat(r.rating)}${'☆'.repeat(5-r.rating)}</span>`:'<span class="rv-nostar">Star rating not shown at source</span>';
 return `<article class="rv-card"><div class="rv-top"><div><div class="rv-who">${esc(r.name)}</div><div class="rv-date">${fmt(r.date)}</div></div><span class="rv-badge s-${esc(r.source).replace(/\s/g,'')}">${esc(r.source)}</span></div>${st}${r.title?`<p class="rv-title">${esc(r.title)}</p>`:''}<p class="rv-text clamp">${esc(r.text)}</p><button class="rv-more" hidden>Read more</button></article>`}
function render(){const F=D.filter(r=>S==='all'||r.source===S);g.innerHTML=F.length?F.map(card).join(''):'<div class="rv-empty">No reviews here yet.</div>';g.scrollLeft=0;window.KS&&KS(g);
 g.querySelectorAll('.rv-card').forEach(c=>{const t=c.querySelector('.rv-text'),b=c.querySelector('.rv-more');if(t.scrollHeight>t.clientHeight+2){b.hidden=false;b.onclick=()=>{const o=t.classList.toggle('clamp');b.textContent=o?'Read more':'Show less'}}})}
fetch('data/kth/reviews.json').then(r=>r.json()).then(j=>{D=(j.reviews||[]).filter(r=>r.text&&r.name);
 const srcs=[...new Set(D.map(r=>r.source))];
 fs.innerHTML=[['all','All sources'],...srcs.map(s=>[s,s])].map(([v,l])=>`<button class="rv-chip" data-v="${esc(v)}" aria-pressed="${v==='all'}">${esc(l)}</button>`).join('');
 fs.hidden=srcs.length<2;fs.onclick=e=>{const b=e.target.closest('.rv-chip');if(!b)return;S=b.dataset.v;fs.querySelectorAll('.rv-chip').forEach(x=>x.setAttribute('aria-pressed',x===b));render()};
 const sm=document.getElementById('rv-sum');sm.innerHTML=(j.summary||[]).filter(s=>s.rating&&s.count).map(s=>`<p class="rv-sumc"><b>${s.rating}</b>★ on ${esc(s.source)}<small>${s.count} reviews on ${esc(s.source)}</small></p>`).join('');
 render()}).catch(()=>{g.innerHTML='<div class="rv-empty">Reviews could not load. Please refresh.</div>'});
})();