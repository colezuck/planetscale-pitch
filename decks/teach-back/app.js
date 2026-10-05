const escapeHtml = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const renderNotes = value => `<ul class="speaker-outline">${value.split('\n').filter(Boolean).map(point => `<li>${escapeHtml(point.replace(/^•\s*/,''))}</li>`).join('')}</ul>`;
const slideOptions = new URLSearchParams(location.search);
const slides = window.PITCH_SLIDES;
const hasNotes = slides.some(slide => Boolean(slide.notes));
if(!hasNotes){document.getElementById('notes')?.remove();document.getElementById('notes-dialog')?.remove();document.querySelector('#help-dialog').innerHTML = document.querySelector('#help-dialog').innerHTML.replace('S &nbsp; Speaker view with notes and timer','');}
if(slideOptions.has('present'))document.body.classList.add('presentation-mode');
if(new URLSearchParams(location.search).has('capture'))document.body.classList.add('capture');
document.getElementById('slides').innerHTML = slides.map(slide => `<section id="${slide.id}" class="${slide.theme}" data-background-color="#111111"><div class="slide-content">${slide.html}</div>${hasNotes ? `<aside class="notes">${renderNotes(slide.notes || '')}</aside>` : ''}</section>`).join('');

const deck = new Reveal({width:1440,height:810,margin:0.06,center:false,view:'slide',scrollActivationWidth:0,hash:true,controls:false,progress:true,transition:'none',backgroundTransition:'none',slideNumber:false,help:false,plugins:[PlanetScaleDiagrams.createPlugin(), ...(hasNotes ? [RevealNotes] : [])],pdfSeparateFragments:false,pdfMaxPagesPerSlide:1,keyboard:{79:()=>deck.toggleOverview()},disableLayout:false});
deck.initialize().then(updatePosition);
function updatePosition(){const i=deck.getIndices().h;document.getElementById('position').textContent=`${String(i+1).padStart(2,'0')} / ${slides.length}`;const f=deck.availableFragments();document.getElementById('previous').disabled=i===0&&!f.prev;document.getElementById('next').disabled=i===slides.length-1&&!f.next;}
deck.on('slidechanged',updatePosition);
document.getElementById('previous').onclick=()=>deck.prev();
document.getElementById('next').onclick=()=>deck.next();
document.getElementById('overview').onclick=()=>deck.toggleOverview();
const notesDialog=document.getElementById('notes-dialog');
if(hasNotes){
document.getElementById('notes').onclick=()=>{const i=deck.getIndices().h;document.getElementById('notes-title').textContent=`Slide ${i+1} · ${slides[i].label}`;document.getElementById('notes-content').innerHTML=renderNotes(slides[i].notes);deck.configure({keyboard:false});notesDialog.showModal();};
document.getElementById('close-notes').onclick=()=>notesDialog.close();
notesDialog.addEventListener('close',()=>deck.configure({keyboard:{79:()=>deck.toggleOverview()}}));
}
document.getElementById('fullscreen').onclick=()=>{if(!document.fullscreenElement)document.documentElement.requestFullscreen?.();else document.exitFullscreen?.();};
const help=document.getElementById('help-dialog');
document.getElementById('help').onclick=()=>{deck.configure({keyboard:false});help.showModal();};
document.getElementById('close-help').onclick=()=>help.close();
help.addEventListener('close',()=>deck.configure({keyboard:{79:()=>deck.toggleOverview()}}));
deck.on('fragmentshown',updatePosition);
deck.on('fragmenthidden',updatePosition);
