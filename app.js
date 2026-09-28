const escapeHtml = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const renderNotes = value => `<ul class="speaker-outline">${value.split('\n').filter(Boolean).map(point => `<li>${escapeHtml(point.replace(/^•\s*/,''))}</li>`).join('')}</ul>`;
const optionalSlides = {autumn:"autumn",cloud:"cloud"};
const slideOptions = new URLSearchParams(location.search);
const slides = window.PITCH_SLIDES.filter(slide => !optionalSlides[slide.id] || slideOptions.has(optionalSlides[slide.id]) || location.hash === `#/${slide.id}`);
if(new URLSearchParams(location.search).has('capture'))document.body.classList.add('capture');
document.getElementById('slides').innerHTML = slides.map(slide => `<section id="${slide.id}" class="${slide.theme}" data-background-color="#111111"><div class="slide-content">${slide.html}</div><aside class="notes">${renderNotes(slide.notes)}</aside></section>`).join('');

const deck = new Reveal({width:1440,height:810,margin:0.06,center:false,view:'slide',scrollActivationWidth:0,hash:true,controls:false,progress:true,transition:'none',backgroundTransition:'none',slideNumber:false,help:false,plugins:[RevealNotes],pdfSeparateFragments:false,pdfMaxPagesPerSlide:1,keyboard:{79:()=>deck.toggleOverview()},disableLayout:false});
deck.initialize().then(()=>{updatePosition();updateNexusState();});
function updatePosition(){const i=deck.getIndices().h;document.getElementById('position').textContent=`${String(i+1).padStart(2,'0')} / ${slides.length}`;document.getElementById('previous').disabled=i===0;document.getElementById('next').disabled=i===slides.length-1;}
deck.on('slidechanged',updatePosition);
function updateNexusState(){const section=document.getElementById('nexus');if(!section)return;const revealed=section.querySelector('.nexus-problems').classList.contains('visible');section.classList.toggle('nexus-scaled',section.querySelector('.nexus-scale').classList.contains('visible'));section.classList.toggle('nexus-revealed',revealed);section.querySelector('.nexus-meta-title').setAttribute('aria-hidden',String(revealed));section.querySelector('.nexus-challenge-title').setAttribute('aria-hidden',String(!revealed));}
deck.on('fragmentshown',updateNexusState);
deck.on('fragmenthidden',updateNexusState);
deck.on('slidechanged',updateNexusState);
document.getElementById('previous').onclick=()=>deck.prev();
document.getElementById('next').onclick=()=>deck.next();
document.getElementById('overview').onclick=()=>deck.toggleOverview();
const notesDialog=document.getElementById('notes-dialog');
document.getElementById('notes').onclick=()=>{const i=deck.getIndices().h;document.getElementById('notes-title').textContent=`Slide ${i+1} · ${slides[i].label}`;document.getElementById('notes-content').innerHTML=renderNotes(slides[i].notes);deck.configure({keyboard:false});notesDialog.showModal();};
document.getElementById('close-notes').onclick=()=>notesDialog.close();
notesDialog.addEventListener('close',()=>deck.configure({keyboard:{79:()=>deck.toggleOverview()}}));
document.getElementById('fullscreen').onclick=()=>{if(!document.fullscreenElement)document.documentElement.requestFullscreen?.();else document.exitFullscreen?.();};
const help=document.getElementById('help-dialog');
document.getElementById('help').onclick=()=>{deck.configure({keyboard:false});help.showModal();};
document.getElementById('close-help').onclick=()=>help.close();
help.addEventListener('close',()=>deck.configure({keyboard:{79:()=>deck.toggleOverview()}}));
