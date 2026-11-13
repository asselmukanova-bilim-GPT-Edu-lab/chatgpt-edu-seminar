(()=>{
if(!new URLSearchParams(location.search).has('presentation'))return;
const type=document.documentElement.dataset.presentation;
document.querySelectorAll('h1 br').forEach(br=>br.replaceWith(document.createTextNode(' ')));
if(type==='tomato'){
 const text=document.querySelector('#lab>.two');
 const details=document.createElement('details');details.className='lab-explanations';
 const summary=document.createElement('summary');summary.textContent='Уақытша солу мен циклдің аяқталуы';details.append(summary,text);
 document.querySelector('#lab>.grid>div').append(details);
}
if(type==='sugar'){
 const pages=[...document.querySelectorAll('main>.theater,main>.layout,main>.explore,main>.quiz,main>footer')];
 const names=['Молекулалар','Саяхат картасы','Жағдайларды салыстыру','Өзіңді тексер','Модель туралы'];
 const nav=document.createElement('nav');nav.className='presentation-tabs';nav.setAttribute('aria-label','Зерттеу бөлімдері');
 pages.forEach((page,i)=>{page.classList.add('presentation-page');page.id=page.id||'presentation-page-'+i;const b=document.createElement('button');b.textContent=names[i];b.setAttribute('aria-controls',page.id);b.onclick=()=>select(i);nav.append(b)});
 const stagesNav=document.createElement('nav');stagesNav.className='molecule-stage-tabs';stagesNav.setAttribute('aria-label','Қанттың өзгеру кезеңдері');
 const stageNames=['Ас қанты','Қорытылу және сіңу','Инсулин сигналы','Энергия · АТФ','Гликоген қоры','Май түзілуі','Майдан энергия'];
 stageNames.forEach((name,i)=>{const b=document.createElement('button');b.type='button';b.innerHTML='<span>'+(i+1)+'</span>'+name;b.setAttribute('aria-label',(i+1)+'. '+name);b.onclick=()=>{pause();show(i)};stagesNav.append(b)});
 function syncStages(){const i=Number(document.querySelector('#sceneBadge').textContent.match(/\d+/)?.[0]||1)-1;[...stagesNav.children].forEach((b,j)=>{b.setAttribute('aria-pressed',String(i===j));if(i===j)b.setAttribute('aria-current','step');else b.removeAttribute('aria-current')})}
 new MutationObserver(syncStages).observe(document.querySelector('#sceneBadge'),{childList:true,subtree:true});syncStages();
 function select(i){pages.forEach((p,j)=>{p.hidden=i!==j;nav.children[j].setAttribute('aria-selected',String(i===j))});stagesNav.hidden=i>1}
 document.querySelector('header').append(nav,stagesNav);select(0);
}
if(type==='car'){
 const side=document.createElement('aside');side.className='model-sidebar';side.setAttribute('aria-label','Управление моделью');
 document.querySelector('main').append(side);
 document.querySelectorAll('.assembly-control,.actions,.detail,main>footer').forEach(e=>side.append(e));
 window.dispatchEvent(new Event('resize'));
}
})();
