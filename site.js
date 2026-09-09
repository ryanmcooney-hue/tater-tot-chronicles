
const progress=document.getElementById('progress');
if(progress){const update=()=>{const d=document.documentElement,m=d.scrollHeight-d.clientHeight;progress.style.width=(m?d.scrollTop/m*100:0)+'%'};addEventListener('scroll',update,{passive:true});update();}
