
const A88_NAV=[
 {label:'Home',page:'index.html'},
 {label:'About',page:'about.html'},
 {label:'Track Record',page:'track-record.html'},
 {label:'Reviews',page:'reviews.html'},
 {label:'New Launches',page:'launches.html'},
 {label:'Valuation',page:'valuation.html'},
 {label:'OCTA Score',page:'octa-score.html'},
 {label:'Calculator',page:'hdb-upgrade-calculator.html'},
 {label:'Guides',page:'guides/'},
 {label:'Contact',page:'contact.html'}
];
const A88_BASE=document.documentElement.dataset.base||'';
function a88Page(){const parts=location.pathname.split('/');const file=parts.pop()||'index.html';const dir=parts.pop();if(dir==='guides')return 'guides/';return file}
function a88Href(item){return a88Page()==='index.html'&&item.hash?item.hash:A88_BASE+item.page+(item.hash||'')}
function a88Current(item){const here=a88Page();return item.hash?here==='index.html'&&location.hash===item.hash:here===item.page}
function a88Fill(root){
 root.replaceChildren();
 A88_NAV.forEach(item=>{
  const a=document.createElement('a');
  a.href=a88Href(item);
  a.textContent=item.label;
  if(a88Current(item))a.setAttribute('aria-current','page');
  root.append(a);
 });
}
const btn=document.querySelector('.menu-btn'),nav=document.getElementById('nav');
const bar=document.querySelector('header.nav');
if(nav)a88Fill(nav);
document.querySelectorAll('footer').forEach(footer=>{
 if(footer.querySelector('.foot-links'))return;
 const links=document.createElement('nav');
 links.className='foot-links';
 links.setAttribute('aria-label','Pages');
 a88Fill(links);
 const legal=footer.querySelector('.legal');
 footer.insertBefore(links,legal);
});
function paintNav(){if(bar)bar.classList.toggle('scrolled',window.scrollY>8)}
paintNav();
addEventListener('scroll',paintNav,{passive:true});
addEventListener('hashchange',()=>{if(nav)a88Fill(nav);document.querySelectorAll('.foot-links').forEach(a88Fill)});
btn&&btn.addEventListener('click',()=>{const o=nav.classList.toggle('open');btn.setAttribute('aria-expanded',o)});
nav&&nav.addEventListener('click',e=>{if(e.target.closest('a')){nav.classList.remove('open');btn&&btn.setAttribute('aria-expanded','false')}});
const A88_WA=KTH_WHATSAPP,A88_MAIL=KTH_EMAIL?'https://formsubmit.co/ajax/'+KTH_EMAIL:'';
if(!document.querySelector('.wa-float')){
 const wa=document.createElement('a');
 wa.className='wa-float';
 wa.href='https://wa.me/'+KTH_WHATSAPP+'?text='+encodeURIComponent('Hi Louis, I saw the Key To Home site and would like to chat.');
 wa.target='_blank';
 wa.rel='noopener';
 wa.setAttribute('aria-label','Chat with Louis on WhatsApp');
 wa.innerHTML='<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg><span>WhatsApp</span>';
 document.body.appendChild(wa);
}
document.querySelectorAll('a[href^="https://wa.me/"]').forEach(a=>{a.href=a.href.replace(/wa\.me\/\d+/,'wa.me/'+KTH_WHATSAPP)});
const A88_LABELS={goal:'Goal',name:'Name',phone:'Mobile',email:'Email',hdbType:'HDB type',town:'Town',timeline:'Timeline',address:'Property address',unit:'Unit no.',type:'Property type',topic:'Interested in',message:'Message',project:'Project / address',intent:'Buying, selling or upgrading',calc:'Calculator snapshot'};
document.querySelectorAll('form.a88-lead').forEach(f=>f.addEventListener('submit',e=>{e.preventDefault();
 const d=new FormData(f),note=f.querySelector('.form-note');const say=(t,c)=>{note.hidden=false;note.textContent=t;note.style.color=c};
 const name=(d.get('name')||'').trim(),phone=(d.get('phone')||'').trim();
 if(!name||!/^[+\d][\d\s-]{6,}$/.test(phone)){say('Please add your name and a valid mobile number.','#b42318');return}
 if(!d.get('consent')){say('Please tick the consent box so I can contact you.','#b42318');return}
 if(d.get('_honey'))return;
 const fields={};for(const k in A88_LABELS){const v=(d.get(k)||'').toString().trim();if(v)fields[A88_LABELS[k]]=k==='goal'?(v==='sell'?"What's my home worth?":'Planning an HDB upgrade'):v}
 fields['Form']=f.dataset.form||(f.id==='valuation'?'Hero lead form':'Enquiry form');fields['Page']=location.pathname;
 const msg='Hi Louis!\n'+Object.entries(fields).map(([k,v])=>k+': '+v).join('\n');
 window.open('https://wa.me/'+A88_WA+'?text='+encodeURIComponent(msg),'_blank');
 const body=Object.assign({_subject:f.dataset.subject||'New Key To Home website lead',_template:'table',_captcha:'false',_honey:''},fields);
 if(!A88_MAIL){say("Thanks, "+name+"! WhatsApp should have opened with your details. Just tap send.",'#3fae6a');f.reset();return}
 say('Sending...','#b8ab95');
 fetch(A88_MAIL,{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json'},body:JSON.stringify(body)})
  .then(r=>{if(!r.ok)throw 0;say("Thanks, "+name+"! I've got your details and will be in touch soon.",'#3fae6a');f.reset()})
  .catch(()=>say("Thanks, "+name+"! WhatsApp should have opened with your details.",'#3fae6a'));
}));
