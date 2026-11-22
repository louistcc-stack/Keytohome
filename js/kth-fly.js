// Scroll-driven hero. Scroll progress p (0..1) through the tall .fly section drives:
//   0.00-0.62  scrub the drone video (skyline -> tower -> window)
//   0.58-0.70  warm light blooms (the window "opens")
//   0.68-0.93  scrub a walk-through of one real home Louis sold
//   0.92-1.00  "Could your home be next?" call to action
// The home shown is set in the .fly-cap data-title / data-area attributes in index.html.
(function(){
  const S=document.querySelector('.fly');if(!S)return;
  const RM=matchMedia('(prefers-reduced-motion: reduce)').matches;
  const v=S.querySelector('.fly-v'),h=S.querySelector('.fly-house'),copy=S.querySelector('.fly-copy'),hint=S.querySelector('.fly-hint'),
        bloom=S.querySelector('.fly-bloom'),reel=S.querySelector('.fly-reel'),cap=S.querySelector('.fly-cap'),end=S.querySelector('.fly-end');
  const clamp=(x,a,b)=>Math.max(a,Math.min(b,x)),seg=(p,a,b)=>clamp((p-a)/(b-a),0,1);
  let dv=0,dh=0;
  if(cap.dataset.title)cap.innerHTML=`<span class="tag">SOLD</span><b>${cap.dataset.title}</b><span>${cap.dataset.area}</span>`;
  if(!RM){
    v.addEventListener('loadedmetadata',()=>{dv=v.duration;S.classList.add('has-video');tick()});v.load();
    h.addEventListener('loadedmetadata',()=>{dh=h.duration;tick()});h.load();
  }
  function tick(){
    if(RM)return;
    const r=S.getBoundingClientRect(),p=clamp(-r.top/(r.height-innerHeight),0,1);
    if(dv)v.currentTime=Math.min(dv-0.05,seg(p,0,.62)*dv);
    if(dh)h.currentTime=Math.min(dh-0.05,seg(p,.70,.93)*dh);
    const c=seg(p,0,.08);copy.style.opacity=1-c;copy.style.transform=`translateY(${-30*c}px)`;hint.style.opacity=1-seg(p,0,.03);
    bloom.style.opacity=clamp(seg(p,.56,.66)-seg(p,.70,.76),0,1);
    reel.style.opacity=seg(p,.68,.71);
    const e=seg(p,.92,.97);end.style.opacity=e;end.classList.toggle('on',e>.5);cap.style.opacity=seg(p,.72,.76)*(1-e);
  }
  let raf=0;addEventListener('scroll',()=>{if(!raf)raf=requestAnimationFrame(()=>{raf=0;tick()})},{passive:true});
  addEventListener('resize',tick);
})();
