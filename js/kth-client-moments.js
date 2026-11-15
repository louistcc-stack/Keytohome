(()=>{
document.querySelectorAll('[data-cm]').forEach(root=>{
 const lim=+root.dataset.cm||12,strip=root.classList.contains('cm-strip'),more=root.parentElement.querySelector('.cm-more');let P=[],N=lim,cur=0;
 const lb=document.getElementById('cm-lb')||document.body.appendChild(Object.assign(document.createElement('div'),{id:'cm-lb',className:'cm-lb',hidden:true,innerHTML:'<button class="cm-x" aria-label="Close">×</button><button class="cm-p" aria-label="Previous">‹</button><img alt=""><button class="cm-n" aria-label="Next">›</button>'}));
 const show=i=>{cur=(i+P.length)%P.length;const im=lb.querySelector('img');im.src=P[cur].src;im.alt=P[cur].alt||'Louis with happy clients';lb.hidden=false;lb._p=show;lb._c=()=>cur};
 if(!lb._init){lb._init=1;lb.onclick=e=>{if(e.target===lb||e.target.classList.contains('cm-x'))lb.hidden=true;else if(e.target.classList.contains('cm-p'))lb._p(lb._c()-1);else if(e.target.classList.contains('cm-n'))lb._p(lb._c()+1)};
  document.addEventListener('keydown',e=>{if(lb.hidden)return;if(e.key==='Escape')lb.hidden=true;if(e.key==='ArrowLeft')lb._p(lb._c()-1);if(e.key==='ArrowRight')lb._p(lb._c()+1)})}
 const render=()=>{root.innerHTML=P.slice(0,N).map((p,i)=>`<button class="cm-item" data-i="${i}"><img src="${p.src}" width="${p.w}" height="${p.h}" alt="${p.alt||'Louis with happy clients'}" loading="lazy"></button>`).join('');if(more)more.hidden=strip||P.length<=N;window.KS&&KS(root)};
 root.onclick=e=>{const b=e.target.closest('.cm-item');if(b)show(+b.dataset.i)};
 if(more)more.onclick=()=>{N+=12;render()};
 fetch(root.dataset.src||'data/kth/client-photos.json').then(r=>r.json()).then(j=>{P=(j.photos||[]).slice();for(let i=P.length-1;i>0;i--){const k=Math.floor(Math.random()*(i+1));[P[i],P[k]]=[P[k],P[i]]}
  if(!P.length){root.closest('section').hidden=true;return}render()});
});})();