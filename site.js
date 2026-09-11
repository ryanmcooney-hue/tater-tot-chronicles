
const progress=document.getElementById('progress');
if(progress){const update=()=>{const d=document.documentElement,m=d.scrollHeight-d.clientHeight;progress.style.width=(m?d.scrollTop/m*100:0)+'%'};addEventListener('scroll',update,{passive:true});update();}
const cf=document.createElement('script');cf.type='module';cf.src='https://static.cloudflareinsights.com/beacon.min.js';cf.setAttribute('data-cf-beacon','{"token":"7579a5a0db2f44f4878a70243c6c2a17"}');document.body.appendChild(cf);
