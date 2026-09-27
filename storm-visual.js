/* Questly v0.5 — presentation for the versioned 18-mission collection.
   Original vector UI artwork, local synthesized cues. No external requests. */
(function(){
'use strict';
const NS='http://www.w3.org/2000/svg',ROOT=document.getElementById('app');
if(!ROOT || !window.QuestGame)return;
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>Array.from(r.querySelectorAll(s));
const mq=window.matchMedia('(prefers-reduced-motion: reduce)');
let pref={sound:false,motion:true},audio=null,unlocked=false,last=null,lastScreen='',lastRover=null,lastFeedback='',pending=null,observer;
try{const p=JSON.parse(localStorage.getItem('questly-visual-v4'));if(p&&typeof p.sound==='boolean'&&typeof p.motion==='boolean')pref=p;}catch(_){}
const moving=()=>pref.motion&&!mq.matches;
const zh=()=>window.QuestGame.getState().lang==='zh';
const text=(en,cn)=>zh()?cn:en;
const savePref=()=>{try{localStorage.setItem('questly-visual-v4',JSON.stringify(pref));}catch(_){};};
function svg(body,box='0 0 100 100',cls=''){return `<svg viewBox="${box}" class="${cls}" aria-hidden="true" focusable="false">${body}</svg>`;}
const use=(name,cls='q-art',box='0 0 100 100')=>svg(`<use href="#q-${name}"/>`,box,cls);
const defs=`<defs>
 <linearGradient id="q-white" x2=".8" y2="1"><stop stop-color="#fffef2"/><stop offset="1" stop-color="#99cddd"/></linearGradient>
 <linearGradient id="q-metal" x2=".6" y2="1"><stop stop-color="#87fff0"/><stop offset=".5" stop-color="#34cfcc"/><stop offset="1" stop-color="#218eae"/></linearGradient>
 <linearGradient id="q-glass" x2=".6" y2="1"><stop stop-color="#163956"/><stop offset="1" stop-color="#06162c"/></linearGradient>
 <linearGradient id="q-gold" x2=".5" y2="1"><stop stop-color="#ffdd86"/><stop offset="1" stop-color="#ee944c"/></linearGradient>
 <linearGradient id="q-sea" x1="0" y1="0" x2=".6" y2="1"><stop stop-color="#224975"/><stop offset=".5" stop-color="#237e97"/><stop offset="1" stop-color="#0c4864"/></linearGradient>
 <linearGradient id="q-turf" x2=".4" y2="1"><stop stop-color="#89d4af"/><stop offset="1" stop-color="#399a8f"/></linearGradient>
 <linearGradient id="q-rock" x2="0" y2="1"><stop stop-color="#415c82"/><stop offset="1" stop-color="#162f57"/></linearGradient>
 <linearGradient id="q-roof" x2=".5" y2="1"><stop stop-color="#879ce9"/><stop offset="1" stop-color="#5265af"/></linearGradient>
 <linearGradient id="q-crate-top" x2="1" y2="1"><stop stop-color="currentColor"/><stop offset="1" stop-color="#eafbe7"/></linearGradient>
</defs>
<symbol id="q-nova" viewBox="0 0 100 120">
 <ellipse cx="50" cy="111" rx="32" ry="6" fill="#04182e" opacity=".24"/>
 <rect x="22" y="92" width="17" height="17" rx="6" fill="#102c4a"/><rect x="62" y="92" width="17" height="17" rx="6" fill="#102c4a"/>
 <path d="M26 96v8m6-8v8m36-8v8m6-8v8" stroke="#6589a3" stroke-width="2"/>
 <g class="q-nova-body">
 <path d="M20 67L12 80l5 5 12-13m51-6 8 16-6 4-13-13" fill="none" stroke="url(#q-white)" stroke-width="8" stroke-linecap="round"/>
 <rect x="24" y="62" width="53" height="37" rx="15" fill="url(#q-metal)" stroke="#83f7e5" stroke-width="1.5"/>
 <path d="M37 69h28v18H37z" fill="#166685"/><path d="M54 71l-10 9h7l-3 7 11-10h-7z" fill="#ffda78"/>
 <circle cx="31" cy="83" r="2" fill="#fff2c1"/><circle cx="70" cy="83" r="2" fill="#fff2c1"/>
 <path d="M52 20V10" stroke="#bedbeb" stroke-width="3"/><circle class="q-antenna" cx="52" cy="8" r="5" fill="#ffe4a1"/>
 <rect x="9" y="37" width="12" height="23" rx="5" fill="#63b8c9"/><rect x="80" y="37" width="12" height="23" rx="5" fill="#328aa7"/>
 <rect x="16" y="21" width="69" height="49" rx="19" fill="url(#q-white)" stroke="#edfefa" stroke-width="1.5"/>
 <path d="M25 28q25-7 51 0" fill="none" stroke="#fff" stroke-opacity=".8" stroke-width="3" stroke-linecap="round"/>
 <rect x="23" y="32" width="55" height="27" rx="11" fill="url(#q-glass)"/>
 <g class="q-eyes"><rect x="34" y="40" width="7" height="9" rx="3.5" fill="#83f9e4"/><rect x="61" y="40" width="7" height="9" rx="3.5" fill="#83f9e4"/></g>
 <path d="M46 51q5 4 10 0" stroke="#83f9e4" stroke-width="2" fill="none" stroke-linecap="round"/>
 <circle cx="23" cy="60" r="2" fill="#d79468"/><circle cx="77" cy="60" r="2" fill="#d79468"/>
 </g>
</symbol>
<symbol id="q-boat" viewBox="0 0 240 140">
 <ellipse cx="122" cy="119" rx="108" ry="12" fill="#6ef7e9" opacity=".16"/>
 <path d="M8 97l212-6-23 33H44z" fill="#174769"/><path d="M8 90l224-5-31 30H37z" fill="url(#q-white)"/>
 <path d="M15 102l208-5-8 10-188 6z" fill="#eeaa5e"/><path d="M25 88l176-3 19 10-185 6z" fill="#346e8a"/>
 <path d="M160 47l38-8 21 12v40l-59 4z" fill="url(#q-white)"/>
 <path d="M159 47l39-10 24 11-39 9z" fill="#57cdd2"/><path d="M166 56l18 1v20l-18 2zM190 56l19-5v24l-19 4z" fill="#133e61"/>
 <path d="M170 60l10 1m14 0 11-3" stroke="#89ddef" stroke-width="2"/>
 <path d="M187 39V22" stroke="#bccfcd" stroke-width="4"/><path d="M185 22h24l-7 7 7 4h-24" fill="#ffcd70"/>
 <circle cx="204" cy="93" r="6" fill="#173653" stroke="#e0eae2" stroke-width="3"/>
 <path d="M35 89V73m102 14V70M35 73h102" stroke="#cfebed" stroke-width="3"/>
 <circle cx="167" cy="107" r="3" fill="#e5ffff"/><circle cx="180" cy="107" r="3" fill="#e5ffff"/>
</symbol>
<symbol id="q-pine" viewBox="0 0 100 130"><ellipse cx="50" cy="117" rx="28" ry="9" fill="#174359" opacity=".24"/><path d="M46 77h9v41h-9z" fill="#927369"/><path d="M50 12L10 85h80z" fill="#247978"/><path d="M50 12v74H10z" fill="#66bea0"/><path d="M50 33L5 105h91z" fill="#236c70"/><path d="M50 33v72H5z" fill="#48a888"/></symbol>
<symbol id="q-house" viewBox="0 0 140 120"><ellipse cx="73" cy="105" rx="58" ry="11" fill="#0e2c4e" opacity=".2"/><path d="M25 54l56-19 36 25v37l-55 17-37-23z" fill="#abcbd6"/><path d="M62 70l55-18v45l-55 17z" fill="#4e82ab"/><path d="M11 53l50-41 64 29-56 40z" fill="url(#q-roof)"/><path d="M11 53l57 28 57-40-2 10-56 39L11 65z" fill="#344979"/><path d="M79 81l13-4v20l-13 4z" fill="#ffe59c"/><path d="M30 72l17 9v15l-17-8z" fill="#81f6de"/></symbol>
<symbol id="q-power" viewBox="0 0 170 170">
 <ellipse cx="85" cy="149" rx="67" ry="13" fill="#082d45" opacity=".3"/>
 <path d="M15 122l80-28 64 30-79 34z" fill="#c5dbce"/><path d="M15 122v10l65 36 79-34v-10l-79 34z" fill="#488a9a"/>
 <path d="M43 77l53-21 29 14v65l-54 22-28-15z" fill="url(#q-white)"/><path d="M71 93l54-23v65l-54 22z" fill="#4783af"/>
 <path d="M86 105l27-11v10l-27 11zm0 21 27-11v6l-27 11z" class="q-live" fill="#82f3ce"/>
 <path d="M95 76V27" stroke="#dfede4" stroke-width="8"/><circle cx="95" cy="25" r="7" fill="#80f2e0"/>
 <g class="q-turbine" style="transform-origin:95px 25px"><path d="M95 25l-8-3-19-42 8-4zM95 25l5-7 43 5v8zM95 25l3 9-29 36-7-6z" fill="#e4f2e6"/></g>
 <path d="M22 91l37-14 12 10-38 15z" fill="#7faae1"/><path d="M25 96l36-13m-18 3 10 10" stroke="#bdeaf1" stroke-width="1"/>
 <circle class="q-live" cx="135" cy="120" r="4" fill="#a4ffcc"/>
</symbol>
<symbol id="q-lab" viewBox="0 0 160 140">
 <ellipse cx="81" cy="124" rx="70" ry="10" fill="#103150" opacity=".3"/>
 <path d="M18 99l65-28 62 30-68 34z" fill="#6cafaa"/><path d="M18 99v9l59 34 68-30v-11l-68 34z" fill="#3a6685"/>
 <path d="M39 72l49-22 40 27v35l-48 20-41-22z" fill="url(#q-white)"/>
 <path d="M80 92l48-15v35l-48 20z" fill="#648bb2"/>
 <path d="M37 74c-3-51 80-72 94 1l-52 22z" fill="url(#q-metal)" stroke="#b4f9dd" stroke-width="2"/>
 <path d="M61 79c-11-35 18-64 18-40m0 0q27 16 22 48" fill="none" stroke="#baf4e5" stroke-width="3" opacity=".8"/>
 <path d="M37 64l45 20 43-16" fill="none" stroke="#baf4e5" stroke-width="3"/>
 <path d="M93 105l17-6v23l-17 7z" fill="#173c61"/><path class="q-live" d="M47 92l16 7v12l-16-7z" fill="#ffe4ab"/>
 <path d="M126 82V47m-11 1q10 12 20-1" fill="none" stroke="#d2e9ef" stroke-width="3"/>
</symbol>
<symbol id="q-port" viewBox="0 0 180 150">
 <path d="M10 113l81-35 78 30-86 39z" fill="#38577c"/><path d="M10 107l81-35 78 30-86 39z" fill="#b7a185"/>
 <path d="M29 105l75 28m-58-37 76 29m-58-38 76 31m-59-39 75 31" stroke="#d1b896" stroke-width="3"/>
 <path d="M51 100V15h76M51 15l40 38H51" fill="none" stroke="#fbc570" stroke-width="9" stroke-linejoin="round"/>
 <path d="M51 30l11 14m-11 17 11 14m-11 17 11 14" stroke="#8a754c" stroke-width="5"/>
 <path d="M127 16v43q12 8 0 17q-9 0-9-7" fill="none" stroke="#1b3650" stroke-width="4"/>
 <path d="M40 106l23-8 16 6-24 10z" fill="#244768"/>
 <path d="M109 105V83l20-8 17 8v23l-22 9z" fill="#6ea39e"/><path d="M109 83l20-8 17 8-23 8z" fill="#b9ded3"/><path d="M123 91v24l23-9V83" fill="#3b858c"/>
</symbol>`;
const sprite=document.createElementNS(NS,'svg');sprite.id='q-art-defs';sprite.setAttribute('aria-hidden','true');sprite.style.cssText='position:absolute;width:0;height:0;overflow:hidden;pointer-events:none';sprite.innerHTML=defs;document.body.appendChild(sprite);
function cargoArt(id){
 const colors=['#ffd177','#edb189','#7edecb','#81bfef','#b3d786','#f39b9e','#85d7ef','#d1b2ee','#efbe8b','#a7e5bb'];
 const glyph=[
 '<path d="M42 64V42h19M42 43l12 11H42M60 43v16l-3 3"/>',
 '<path d="M40 49l20-6 6 6-20 7zM40 57l6 8 20-8M46 56v9"/>',
 '<path d="M48 44v-4h9v4M43 45h18v25H43zM54 49l-7 10h7l-4 8"/>',
 '<path d="M53 43q-17 19-7 25q16 8 14-10z"/>',
 '<path d="M51 68V52M51 58q-15 0-13-14q13-1 13 14M52 63q17-3 15-16q-12-1-15 16"/>',
 '<path d="M52 44v24M41 56h22" stroke-width="6"/>',
 '<path d="M37 46h29v21H37zM47 46v21M57 46v21M37 56h29"/>',
 '<path d="M39 47h27v20H39zM45 47v-6h14v6M39 55h27M51 53v5"/>',
 '<path d="M39 62h27v7H39zM45 62V49h15v13M52 49V40h14M61 54h8v8"/>',
 '<path d="M39 49h27v20H39zM46 49V35M43 58h5m-5 6h5M58 56v8"/>'
 ][id];
 return svg(`<ellipse cx="50" cy="88" rx="33" ry="7" fill="#071d36" opacity=".25"/><path d="M16 34l34-16 34 16v42L50 93 16 76z" fill="${colors[id]}"/><path d="M50 51l34-17v42L50 93z" fill="#0c3554" opacity=".22"/><path d="M16 34l34-16 34 16-34 17z" fill="#fff" opacity=".32"/><path d="M19 39v35l26 13V53" fill="none" stroke="#fff" stroke-opacity=".26" stroke-width="2"/><path d="M35 25l34 18v11l-14 7V49L22 33" fill="#fff3cd" opacity=".45"/><g transform="translate(-4,1)" fill="none" stroke="#254969" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">${glyph}</g>`,'0 0 100 100','q-cargo-art');
}
function islandArt(c){
 const total=['cargo','power','robot'].filter(k=>c[k].done).length;
 const trees=[[205,279,.65],[254,275,.55],[316,373,.58],[367,402,.58],[684,308,.75],[715,358,.52],[556,143,.52],[603,184,.48],[427,282,.4],[602,421,.48]];
 return svg(`<rect width="900" height="620" fill="url(#q-sea)"/>
 <g opacity=".15" fill="#baf5ec"><circle cx="763" cy="60" r="81"/><circle cx="100" cy="97" r="2"/><circle cx="193" cy="38" r="2"/><circle cx="650" cy="32" r="2"/></g>
 <path d="M-30 76Q185 143 314 66T730 84T980 20" fill="none" stroke="#63d1d1" stroke-opacity=".1" stroke-width="42"/>
 <g class="q-water" fill="none" stroke="#a8fff0" stroke-width="2" opacity=".18"><path d="M32 339h35m-11 6h20M68 421h70m-20 7h40M727 466h74m-32 7h60M632 538h52M118 552h51M727 212h52m-24 7h47M76 229h61M361 79h57"/></g>
 <ellipse cx="456" cy="474" rx="325" ry="79" fill="#072742" opacity=".3"/>
 <ellipse class="q-island-ripple" cx="456" cy="404" rx="355" ry="156" fill="none" stroke="#56d6cb" stroke-width="20" stroke-opacity=".24"/>
 <path d="M152 332Q171 237 314 194L489 164Q637 160 732 280L762 348Q759 422 669 468L480 515Q268 514 175 439Z" fill="url(#q-rock)"/>
 <path d="M175 364l27 78 52 27-8-78M296 404l8 78 69 20-3-76M448 426l7 88 62-12 9-89M604 404l-13 81 73-21 22-88M709 347l-21 83 37-25 32-58" fill="#91b3ba" opacity=".18"/>
 <path d="M144 329Q161 232 317 182L489 155Q646 151 737 270L763 337Q757 402 666 442L480 483Q269 489 171 411Z" fill="#cbd3ab"/>
 <path d="M163 324Q180 240 321 198L492 171Q641 171 718 277L744 333Q735 386 655 425L480 465Q283 468 190 398Z" fill="url(#q-turf)"/>
 <path d="M212 327Q294 216 417 235T679 322Q665 415 549 432L410 430Q298 406 212 327" fill="#3a8987" opacity=".35"/>
 <path d="M251 371Q266 281 422 256L487 233Q558 248 588 327L633 367" fill="none" stroke="#b9d4b6" stroke-width="25" stroke-linecap="round"/>
 <path d="M251 371Q266 281 422 256L487 233Q558 248 588 327L633 367" fill="none" stroke="#f6e1a0" stroke-width="3" stroke-dasharray="4 14" opacity=".6"/>
 <g><path d="M255 219l69-151 73 143z" fill="#386881"/><path d="M324 68l73 143-91-2z" fill="#264964"/><path d="M303 114l21-46 25 49-19-8-13 13z" fill="#b5dbd1"/><path d="M331 215l74-131 90 131z" fill="#437e89"/><path d="M405 84l90 131-84-20z" fill="#2c5d78"/><path d="M382 124l23-40 31 45-24-12-15 15z" fill="#c0e3d7"/></g>
 <path d="M345 177Q376 242 395 326l50 139v44l22-3-5-56-45-135Q386 218 390 173" fill="#60dedd" opacity=".55"/>
 <path class="q-falls" d="M356 181Q379 249 407 326l43 136v46" fill="none" stroke="#bcfff1" stroke-width="5" stroke-dasharray="22 13" opacity=".6"/>
 <path d="M377 295l57-16 17 25-60 17z" fill="#637c90"/><path d="M379 290l56-17 17 24-60 18z" fill="#e2c18a"/><path d="M391 287l10 24m3-28 11 24m3-28 11 24" stroke="#ab966f" stroke-width="2"/>
 ${trees.map(([x,y,s])=>`<use href="#q-pine" x="${x}" y="${y-75*s}" width="${70*s}" height="${91*s}"/>`).join('')}
 <g class="q-port-building ${c.cargo.done?'restored':''}"><use href="#q-port" x="172" y="283" width="170" height="142"/></g>
 <g class="q-power-building ${c.power.done?'restored':''}"><use href="#q-power" x="444" y="118" width="152" height="170"/></g>
 <g class="q-lab-building ${c.robot.done?'restored':''}"><use href="#q-lab" x="587" y="274" width="154" height="148"/></g>
 <use href="#q-house" x="502" y="357" width="86" height="80"/><use href="#q-house" x="464" y="315" width="71" height="68"/>
 <g class="q-map-ferry"><use href="#q-boat" x="103" y="421" width="143" height="84"/></g>
 <g class="q-map-nova"><use href="#q-nova" x="347" y="342" width="82" height="100"/></g>
 ${[[342,268],[567,300],[578,404]].map(([x,y],i)=>`<g><path d="M${x} ${y}v-24" stroke="#233d61" stroke-width="3"/><circle cx="${x}" cy="${y-26}" r="${total>i?5:3}" fill="${total>i?'#ffde81':'#719aab'}"/>${total>i?`<circle class="q-lamp" cx="${x}" cy="${y-26}" r="13" fill="#ffd974" opacity=".14"/>`:''}</g>`).join('')}
 <g class="q-clouds" fill="#d6eef4" opacity=".24"><path d="M19 149q-5-20 16-21q6-31 42-12q22-8 27 21h30q15 19-8 21H27z"/><path d="M707 113q0-13 17-17q-4-33 32-30q25-15 40 20q25-4 28 20h31q13 17-7 20H723z"/></g>
 <g stroke="#c9ffec" fill="none" stroke-width="2" opacity=".8"><path d="M636 106q8-6 14 0q8-7 14 0M647 123q6-4 11 0q5-5 11 0"/></g>`,'0 0 900 620','q-island-art');
}
function harborArt(){return svg(`<rect width="700" height="240" fill="url(#q-sea)"/>
 <path d="M0 68Q163-3 334 44T700 23V0H0" fill="#385e86"/><path d="M436 35l91-32 126 26 58 29-1 38-136-5-96-19z" fill="#306979"/>
 <g opacity=".75"><use href="#q-pine" x="582" y="-9" width="51" height="79"/><use href="#q-pine" x="616" y="2" width="39" height="62"/></g>
 <path d="M-5 145l134-44 51 23-128 51z" fill="#d0b18e"/><path d="M-5 153l134-43 44 20-125 51z" fill="#715b63"/><path d="M11 151l123-42M40 164l120-41" stroke="#e6d0ab" stroke-width="4"/>
 <path d="M526 108l126-37 63 15-122 51z" fill="#d0b18e"/><path d="M527 113l125-35 63 15-120 51z" fill="#715b63"/>
 <path d="M631 79V19h-68m68 0-33 36h33" stroke="#ffd084" fill="none" stroke-width="6"/><path d="M563 19v43l-8 5" stroke="#123652" fill="none" stroke-width="3"/>
 <g class="q-water" stroke="#a8fff0" opacity=".2" stroke-width="2"><path d="M171 86h43m-10 8h19M341 177h53m-25 9h30M51 215h79m-22 9h46M499 199h42M346 64h53M587 167h63"/></g>
 <circle cx="443" cy="80" r="4" fill="#fdd586"/><path d="M443 84v16" stroke="#224d70" stroke-width="2"/>`,'0 0 700 240','q-harbor-art');}
function robotArt(){return use('nova','q-mini','0 0 100 120');}
function soundIcon(){return svg(`<path d="M3 9h4l5-5v16l-5-5H3z" fill="none" stroke="currentColor" stroke-width="1.8"/>${pref.sound?'<path d="M16 7q5 5 0 10m3-13q8 8 0 16" fill="none" stroke="currentColor" stroke-width="1.8"/>':'<path d="M16 9l6 6m0-6-6 6" stroke="currentColor" stroke-width="1.8"/>'}`,'0 0 24 24','icon');}
function controls(){return `<div class="q-toolbar"><span class="q-edition"><i></i>${text('STORM ISLAND · 18 MISSIONS','风暴岛 · 18 关挑战')}</span><div class="q-options"><button type="button" class="q-setting" data-visual="sound" aria-pressed="${pref.sound}" aria-label="${text('Sound effects','操作音效')}" title="${text('Optional sound effects. No background music.','可选操作音效，无背景音乐。')}">${soundIcon()}<span>${pref.sound?text('Sound on','音效开'):text('Sound off','音效关')}</span></button><button type="button" class="q-setting" data-visual="motion" aria-pressed="${moving()}" ${mq.matches?'disabled':''} aria-label="${text('Animations','动画')}" title="${text('Respects the device’s reduced-motion setting.','遵循设备的减弱动态效果设置。')}">${svg('<path d="M3 8h13m-8 8h13M13 4l4 4-4 4M8 12l-4 4 4 4" fill="none" stroke="currentColor" stroke-width="1.8"/>','0 0 24 24','icon')}<span>${moving()?text('Motion on','动画开'):text('Motion off','动画关')}</span></button></div></div>`;}
function cue(kind){
 if(!pref.sound||!unlocked||!audio||audio.state!=='running'||document.hidden)return;
 const notes=kind==='win'?[523.25,659.25,783.99]:kind==='error'?[220,196]:kind==='power'?[392,523.25]:kind==='pickup'?[660,880]:[480];
 notes.forEach((hz,i)=>{const o=audio.createOscillator(),g=audio.createGain(),at=audio.currentTime+i*.10;o.type='sine';o.frequency.value=hz;g.gain.setValueAtTime(0,at);g.gain.linearRampToValueAtTime(.032,at+.01);g.gain.exponentialRampToValueAtTime(.001,at+.12);o.connect(g);g.connect(audio.destination);o.start(at);o.stop(at+.13);o.onended=()=>{o.disconnect();g.disconnect();};});
}
function unlock(){if(!pref.sound)return;try{const AC=window.AudioContext||window.webkitAudioContext;if(!AC)return;if(!audio)audio=new AC();audio.resume().then(()=>{unlocked=audio.state==='running';}).catch(()=>{});}catch(_){unlocked=false;}}
function animate(node,frames,opts){if(!node||!moving()||typeof node.animate!=='function')return;node.animate(frames,opts);}
function burst(node){
 if(!moving()||!node)return;const rect=node.getBoundingClientRect();
 if(rect.bottom<0||rect.top>innerHeight)return;
 const host=document.createElement('div');host.className='q-burst';host.setAttribute('aria-hidden','true');host.style.left=(rect.left+rect.width/2)+'px';host.style.top=(rect.top+28)+'px';
 for(let i=0;i<12;i++){const p=document.createElement('i');p.style.setProperty('--x',(Math.cos(i*Math.PI/6)*94)+'px');p.style.setProperty('--y',(Math.sin(i*Math.PI/6)*64-16)+'px');p.style.setProperty('--r',(i*43)+'deg');host.appendChild(p);}document.body.appendChild(host);setTimeout(()=>host.remove(),850);
}
function enhance(){
 observer?.disconnect();
 $$('.q-island-art,.q-buddy,.q-harbor-art,.q-boat-art,.q-mini,.q-power-units,.q-current',ROOT).forEach(n=>n.remove());
 const state=window.QuestGame.getState(),screen=window.QuestGame.getScreen(),c=state.campaigns[state.mode],fresh=lastScreen!==screen;
 document.body.classList.add('q-premium');document.body.classList.toggle('q-reduce',!moving());document.body.dataset.scene=screen;
 const nav=$('.nav');if(nav&&!$('.q-toolbar'))nav.insertAdjacentHTML('afterend',controls());
 const footer=$('.footer>span');if(footer)footer.textContent='QUESTLY · STORM ISLAND · v0.5.0';
 const map=$('.world-map');
 if(map){
  map.classList.add('q-diorama');map.insertAdjacentHTML('afterbegin',islandArt(c));
  const h=$('h1');if(h)h.innerHTML=text('An island. <br>A robot. <br><em>Your big ideas.</em>','一座小岛。<br>一个伙伴。<br><em>你的大大想法。</em>');
  $$('.map-station').forEach((b,i)=>{const building=$('.building',b);if(building)building.innerHTML=`<span class="q-pin">${c[['cargo','power','robot'][i]].done?'✓':String(i+1).padStart(2,'0')}</span>`;});
  const lead=$('.home-copy .lead');if(lead)lead.textContent=text('The storm is over. Adventure starts here. Help Nova bring the island back to life — one clever idea at a time.','暴风雨过去了，冒险才刚开始。和 Nova 一起，用你的奇思妙想让小岛重新亮起来。');
  const mode=$('.mode-box');if(mode)mode.insertAdjacentHTML('beforebegin',`<div class="q-buddy">${use('nova','q-buddy-art','0 0 100 120')}<div><b>${text('Hey, I’m Nova.','嗨，我是 Nova。')}</b><span>${text('What should we build first?','我们先修好哪里？')}</span></div></div>`);
  $$('.chapter-card .badge').forEach((el,i)=>el.innerHTML=use(['port','power','lab'][i],'q-card-art',['0 0 180 150','0 0 170 170','0 0 160 140'][i]));
 }
 const harbor=$('.harbor');
 if(harbor){
  harbor.insertAdjacentHTML('afterbegin',harborArt());const boat=$('.boat',harbor);if(boat){boat.insertAdjacentHTML('afterbegin',use('boat','q-boat-art','0 0 240 140'));boat.style.setProperty('--draft',Math.min(12,c.cargo.load.reduce((a,i)=>a+QuestGame.getCargoConfig().items[i].weight,0))+'px');}
  $$('.cargo-item').forEach(el=>{const old=$(':scope>.icon',el);if(old)old.outerHTML=cargoArt(Number(el.dataset.value));});
  const cfg=QuestGame.getCargoConfig(),cap=cfg.capacity,w=c.cargo.load.reduce((a,i)=>a+cfg.items[i].weight,0);harbor.classList.toggle('q-overload',w>cap);
  if(pending?.action==='cargo'){animate($(`.cargo-item[data-value="${pending.value}"]`),[{transform:'translateY(-5px) scale(.97)'},{transform:'translateY(0) scale(1)'}],{duration:230,easing:'ease-out'});cue('tick');}
 }
 const pg=$('.power-grid');
 if(pg){
  $$('.wire.lit svg',pg).forEach(s=>{Array.from(s.children).filter(p=>p.tagName.toLowerCase()==='path'&&p.getAttribute('stroke')==='currentColor').forEach(path=>{const clone=path.cloneNode();clone.setAttribute('class','q-current');clone.setAttribute('stroke-width','3');s.appendChild(clone);});});
  if(pending?.action==='wire'){animate($(`.wire[data-value="${pending.value}"] svg`),[{transform:'rotate(-90deg)'},{transform:'rotate(0deg)'}],{duration:180,easing:'ease-out'});cue('tick');}
  if(pending?.action==='testPower'){pg.classList.add('q-scan');cue('power');}
  const side=$('.workspace>.panel:nth-child(2)'),targets=$$('.wire.target',pg);
  if(side){const units=`<div class="q-power-units">${targets.map((tile,i)=>`<div class="q-power-unit ${tile.classList.contains('lit')?'online':''}">${use(i?'lab':'house','q-station-art',i?'0 0 160 140':'0 0 140 120')}<span><i></i>${text('Station','站点')} ${i+1} · ${tile.classList.contains('lit')?text('ONLINE','已通电'):text('OFFLINE','未通电')}</span></div>`).join('')}</div>`;$('.power-score',side)?.insertAdjacentHTML('afterend',units);}
 }
 const rover=$('.rover');
 if(rover){
  rover.insertAdjacentHTML('afterbegin',robotArt());const pos=rover.dataset.rover.split(',').map(Number),grid=$('.robot-grid'),n=Math.round(Math.sqrt($$('.cell',grid).length));
  const arrow=$('svg.icon',rover);let dir=Number((arrow?.style.transform.match(/rotate\((\d+)deg\)/)||[])[1]||0);
  if(lastRover&&!fresh&&lastRover.mode===state.mode){const dx=(lastRover.c-pos[1])*(grid.clientWidth-14)/n,dy=(lastRover.r-pos[0])*(grid.clientHeight-14)/n;if(dx||dy)animate(rover,[{transform:`translate(${dx}px,${dy}px)`},{transform:'translate(0,0)'}],{duration:255,easing:'cubic-bezier(.2,.7,.2,1)'});if(dir!==lastRover.dir&&arrow){let from=lastRover.dir;while(from-dir>180)from-=360;while(dir-from>180)from+=360;animate(arrow,[{transform:`rotate(${from}deg)`},{transform:`rotate(${dir}deg)`}],{duration:200,easing:'ease-out'});}}
  lastRover={r:pos[0],c:pos[1],dir,mode:state.mode};
  const samples=$$('.sample',grid);samples.forEach(s=>s.parentElement.classList.add('q-has-sample'));
 }
 if(screen!=='robot')lastRover=null;
 const feedback=$('#feedback');
 if(feedback&&feedback.textContent!==lastFeedback){if(feedback.classList.contains('error')){cue('error');animate(rover||$('.boat'),[{transform:'translateX(0)'},{transform:'translateX(-4px)'},{transform:'translateX(4px)'},{transform:'translateX(0)'}],{duration:220});}else if(feedback.classList.contains('good'))cue('pickup');}
 lastFeedback=feedback?.textContent||'';
 if(last&&last.mode===state.mode){for(const stage of ['cargo','power','robot'])if(!last.campaigns[state.mode][stage].done&&c[stage].done){cue('win');burst($('.success'));}}
 if(fresh){animate($('#view'),[{opacity:.6,transform:'translateY(8px)'},{opacity:1,transform:'translateY(0)'}],{duration:240,easing:'ease-out'});}
 last=state;lastScreen=screen;pending=null;
 observer.observe(ROOT,{childList:true});
}
document.addEventListener('click',e=>{
 const setting=e.target.closest('[data-visual]');
 if(setting){if(setting.disabled)return;const which=setting.dataset.visual;pref[which]=!pref[which];savePref();if(which==='sound'){if(pref.sound){unlock();setTimeout(()=>cue('tick'),80);}else if(audio)audio.suspend().catch(()=>{});}$('.q-toolbar')?.remove();enhance();return;}
 const b=e.target.closest('button[data-action]');if(!b||b.disabled)return;pending={...b.dataset};unlock();
},true);
function systemMotion(){document.body.classList.toggle('q-reduce',!moving());$('.q-toolbar')?.remove();enhance();}
if(mq.addEventListener)mq.addEventListener('change',systemMotion);else if(mq.addListener)mq.addListener(systemMotion);
document.addEventListener('visibilitychange',()=>{if(document.hidden&&audio)audio.suspend().catch(()=>{});});
observer=new MutationObserver(enhance);enhance();
window.QuestVisual={version:'0.5.0',getPreferences:()=>({...pref,reducedBySystem:mq.matches}),hasAudioContext:()=>!!audio};
})();
