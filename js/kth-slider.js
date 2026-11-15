/* Shared Key To Home slider: swipe, arrows, dots, gentle autoplay (pauses on hover/touch/focus, off for reduced motion). */
(()=>{
const RM=matchMedia('(prefers-reduced-motion: reduce)');
function KS(track){
 if(track._ks){track._ks.refresh();return track._ks}
 const wrap=document.createElement('div');wrap.className='ks';track.parentNode.insertBefore(wrap,track);wrap.appendChild(track);
 const prev=Object.assign(document.createElement('button'),{className:'ks-nav ks-prev',innerHTML:'&#8249;',type:'button'});prev.setAttribute('aria-label','Previous');
 const next=Object.assign(document.createElement('button'),{className:'ks-nav ks-next',innerHTML:'&#8250;',type:'button'});next.setAttribute('aria-label','Next');
 const dots=document.createElement('div');dots.className='ks-dots';wrap.append(prev,next,dots);
 const slides=()=>[...track.children].filter(c=>c.offsetParent!==null||c.getClientRects().length);
 const idx=()=>{const s=slides(),x=track.scrollLeft;let b=0,d=1e9;s.forEach((c,i)=>{const v=Math.abs(c.offsetLeft-track.offsetLeft-x);if(v<d){d=v;b=i}});return b};
 const atEnd=()=>track.scrollLeft+track.clientWidth>=track.scrollWidth-4;
 const to=i=>{const s=slides();if(!s.length)return;i=Math.max(0,Math.min(i,s.length-1));track.scrollTo({left:s[i].offsetLeft-track.offsetLeft,behavior:RM.matches?'auto':'smooth'})};
 const upd=()=>{const i=idx(),s=slides();[...dots.children].forEach((d,j)=>d.setAttribute('aria-current',j===i));prev.disabled=track.scrollLeft<4;next.disabled=atEnd();const fit=track.scrollWidth<=track.clientWidth+4;prev.hidden=next.hidden=dots.hidden=fit};
 const refresh=()=>{const s=slides();dots.innerHTML=s.map((_,i)=>`<button type="button" aria-label="Go to slide ${i+1}"></button>`).join('');[...dots.children].forEach((d,i)=>d.onclick=()=>{pause(6000);to(i)});requestAnimationFrame(upd)};
 prev.onclick=()=>{pause(6000);atEndOr(-1)};next.onclick=()=>{pause(6000);atEndOr(1)};
 function atEndOr(d){to(idx()+d)}
 let t=null,hold=false,vis=true,until=0;
 const pause=ms=>{until=Date.now()+ms};
 const tick=()=>{if(RM.matches||hold||!vis||Date.now()<until||document.hidden)return;if(atEnd())to(0);else to(idx()+1)};
 wrap.addEventListener('mouseenter',()=>hold=true);wrap.addEventListener('mouseleave',()=>hold=false);
 wrap.addEventListener('focusin',()=>hold=true);wrap.addEventListener('focusout',()=>hold=false);
 track.addEventListener('touchstart',()=>{hold=true},{passive:true});track.addEventListener('touchend',()=>{hold=false;pause(8000)},{passive:true});
 track.addEventListener('scroll',()=>{clearTimeout(track._st);track._st=setTimeout(upd,60)},{passive:true});
 addEventListener('resize',()=>upd());
 if('IntersectionObserver'in window)new IntersectionObserver(e=>{vis=e[0].isIntersecting}).observe(wrap);
 t=setInterval(tick,5000);
 track._ks={refresh,to};refresh();return track._ks}
window.KS=KS;
const auto=()=>document.querySelectorAll('[data-ks]').forEach(KS);
document.readyState==='loading'?document.addEventListener('DOMContentLoaded',auto):auto();
})();