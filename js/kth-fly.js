// Scroll-driven hero. Scroll progress p (0..1) through the tall .fly section drives:
//   0.00-0.62  scrub the drone video (skyline -> tower -> window)
//   0.58-0.70  warm light blooms (the window "opens")
//   0.68-0.94  reel of real sold homes, one per step
//   0.92-1.00  "Could your home be next?" call to action
(function(){
  const S=document.querySelector('.fly');if(!S)return;
  const RM=matchMedia('(prefers-reduced-motion: reduce)').matches;
  const v=S.querySelector('.fly-v'),copy=S.querySelector('.fly-copy'),hint=S.querySelector('.fly-hint'),
        bloom=S.querySelector('.fly-bloom'),reel=S.querySelector('.fly-reel'),cap=S.querySelector('.fly-cap'),
        cnt=S.querySelector('.fly-count'),end=S.querySelector('.fly-end');
  const clamp=(x,a,b)=>Math.max(a,Math.min(b,x)),seg=(p,a,b)=>clamp((p-a)/(b-a),0,1);
  let deals=[],imgs=[],shown=-1,dur=0;
  if(v&&!RM){v.addEventListener('loadedmetadata',()=>{dur=v.duration;S.classList.add('has-video');tick()});v.load()}
  fetch('data/kth/transactions.json').then(r=>r.json()).then(j=>{
    // One photo per deal (its first, a living room), interleaved by town so the reel feels varied.
    const by={};j.transactions.filter(t=>t.photos&&t.photos.length&&t.side!=='buyer').forEach(t=>(by[t.area]=by[t.area]||[]).push(t));
    const towns=Object.values(by).sort((a,b)=>b.length-a.length);
    for(let i=0;deals.length<24&&towns.some(t=>t[i]);i++)towns.forEach(t=>{if(t[i]&&deals.length<24)deals.push(t[i])});
    deals.forEach((d,i)=>{const im=new Image();im.alt='';im.decoding='async';im.dataset.src=d.photos[0];reel.appendChild(im);imgs.push(im)});
    tick();
  });
  function load(i){const im=imgs[i];if(im&&!im.src)im.src=im.dataset.src}
  function tick(){
    if(RM)return;
    const r=S.getBoundingClientRect(),p=clamp(-r.top/(r.height-innerHeight),0,1);
    if(dur)v.currentTime=Math.min(dur-0.05,seg(p,0,.62)*dur);
    const c=seg(p,0,.08);copy.style.opacity=1-c;copy.style.transform=`translateY(${-30*c}px)`;hint.style.opacity=1-seg(p,0,.03);
    const b=seg(p,.56,.66)-seg(p,.70,.76);bloom.style.opacity=clamp(b,0,1);
    reel.style.opacity=seg(p,.68,.71);
    if(deals.length){
      const q=seg(p,.70,.93),i=Math.min(deals.length-1,Math.floor(q*deals.length));
      if(p>.5)for(let k=0;k<4;k++)load(Math.min(deals.length-1,i+k));
      if(i!==shown){imgs.forEach((im,k)=>im.classList.toggle('on',k===i));shown=i;const d=deals[i];
        cap.innerHTML=`<span class="tag">SOLD</span><b>${d.title}</b><span>${d.area} · ${d.type==='HDB'?'HDB resale':'Private home'}</span>`;cnt.textContent=`${i+1} / ${deals.length}`}
      const z=(q*deals.length)%1;imgs[i].style.transform=`scale(${1.08-.06*z})`;
    }
    const e=seg(p,.92,.97);end.style.opacity=e;cap.style.opacity=cnt.style.opacity=1-e;end.classList.toggle('on',e>.5);
  }
  let raf=0;addEventListener('scroll',()=>{if(!raf)raf=requestAnimationFrame(()=>{raf=0;tick()})},{passive:true});
  addEventListener('resize',tick);
})();
