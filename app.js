const escapeHtml = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const slides = window.PITCH_SLIDES;
if(new URLSearchParams(location.search).has('capture'))document.body.classList.add('capture');
document.getElementById('slides').innerHTML = slides.map(slide => `<section id="${slide.id}" class="${slide.theme}" data-background-color="#111111">${slide.id === 'opening' ? '<div class="cover-brand"><img src="assets/planetscale-white.png" alt="PlanetScale"></div>' : ''}${slide.html}<aside class="notes">${escapeHtml(slide.notes)}</aside></section>`).join('');

const deck = new Reveal({width:1440,height:810,margin:0.06,center:false,hash:true,controls:false,progress:true,transition:'none',backgroundTransition:'none',slideNumber:false,help:false,plugins:[RevealNotes],pdfSeparateFragments:false,pdfMaxPagesPerSlide:1,keyboard:{79:()=>deck.toggleOverview()},disableLayout:false});
deck.initialize().then(updatePosition);
function updatePosition(){const i=deck.getIndices().h;document.getElementById('position').textContent=`${String(i+1).padStart(2,'0')} / ${slides.length}`;document.getElementById('previous').disabled=i===0;document.getElementById('next').disabled=i===slides.length-1;}
deck.on('slidechanged',updatePosition);
document.getElementById('previous').onclick=()=>deck.prev();
document.getElementById('next').onclick=()=>deck.next();
document.getElementById('overview').onclick=()=>deck.toggleOverview();
const notesDialog=document.getElementById('notes-dialog');
document.getElementById('notes').onclick=()=>{const i=deck.getIndices().h;document.getElementById('notes-title').textContent=`Slide ${i+1} · ${slides[i].label}`;document.getElementById('notes-content').textContent=slides[i].notes;deck.configure({keyboard:false});notesDialog.showModal();};
document.getElementById('close-notes').onclick=()=>notesDialog.close();
notesDialog.addEventListener('close',()=>deck.configure({keyboard:{79:()=>deck.toggleOverview()}}));
document.getElementById('fullscreen').onclick=()=>{if(!document.fullscreenElement)document.documentElement.requestFullscreen?.();else document.exitFullscreen?.();};
const help=document.getElementById('help-dialog');
document.getElementById('help').onclick=()=>{deck.configure({keyboard:false});help.showModal();};
document.getElementById('close-help').onclick=()=>help.close();
help.addEventListener('close',()=>deck.configure({keyboard:{79:()=>deck.toggleOverview()}}));
