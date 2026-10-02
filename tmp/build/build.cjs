const fs=require('fs'),path=require('path'),qr=require('./qrcode.cjs');
const root=path.resolve(__dirname,'../..');
const asset=(p,mime='image/png')=>'data:'+mime+';base64,'+fs.readFileSync(p).toString('base64');
const qrcode=url=>{const q=qr(0,'M');q.addData(url);q.make();return q.createDataURL(5,20)};
let html=fs.readFileSync(path.join(__dirname,'deck.html'),'utf8');
html=html.replace('/*DATA*/',fs.readFileSync(path.join(__dirname,'data.js'),'utf8')).replace('/*APP*/',fs.readFileSync(path.join(__dirname,'privacy-cases.js'),'utf8')+'\n'+fs.readFileSync(path.join(__dirname,'ethics.js'),'utf8')+'\n'+fs.readFileSync(path.join(__dirname,'app.js'),'utf8'));
const vars={
 '/*AITEACHINGPARADIGMS*/':asset(path.join(root,'assets/ai-teaching-paradigms.png')),
 '/*TEACHERAIRESEARCH*/':asset(path.join(root,'assets/teacher-ai-research.png')),
 '/*SIMUSAGEBUTTON*/':asset(path.join(root,'assets/chat-simulation/usage-button.png')),
 '/*SIMUSAGELIMITS*/':asset(path.join(root,'assets/chat-simulation/usage-limits.png')),
 '/*SIMSETTINGSBUTTON*/':asset(path.join(root,'assets/chat-simulation/settings-button.png')),
 '/*SIMSETTINGSLIST*/':asset(path.join(root,'assets/chat-simulation/settings-list.png')),
 '/*SIMMODELMENU*/':asset(path.join(root,'assets/chat-simulation/models-menu.png')),
 '/*SIMMODELBUTTON*/':asset(path.join(root,'assets/chat-simulation/models-button.png')),
 '/*TEAMBG*/':asset(path.join(root,'assets/methodologists/background.png')),
 '/*NEWCOVER*/':asset(path.join(root,'assets/cover-national-project.png')),
 '/*SIMPERSONAL1*/':asset(path.join(root,'assets/chat-simulation/personalization-1.png')),
 '/*SIMPERSONAL2*/':asset(path.join(root,'assets/chat-simulation/personalization-2.png')),
 '/*SIMPERSONALBUTTON*/':asset(path.join(root,'assets/chat-simulation/personalization-button.png')),
 '/*SIMPLUGINS*/':asset(path.join(root,'assets/chat-simulation/plugins.png')),
 '/*SIMCHAT*/':asset(path.join(root,'assets/chat-simulation/chat.png')),
 '/*SIMPROFILE*/':asset(path.join(root,'assets/chat-simulation/profile-menu.png')),
 '/*SIMHOME*/':asset(path.join(root,'assets/chat-simulation/home.png')),
 '/*FONT*/':`@font-face{font-family:Inter;font-style:normal;font-weight:100 900;font-display:swap;src:url('${asset(path.join(__dirname,'Inter.ttf'),'font/ttf')}') format('truetype')}`,
 '/*BG*/':asset(path.join(root,'assets/backgrounds/ornament-light-wide.png')),
 '/*BLUE*/':asset(path.join(root,'assets/backgrounds/ornament-blue-portrait.png')),
 '/*LOGO*/':asset(path.join(root,'assets/bilim-ai-logo.png')),
 '/*FREEDOM*/':asset(path.join(__dirname,'image8.jpeg'),'image/jpeg'),
 '/*OPENAI*/':asset(path.join(__dirname,'image9.png')),
 '/*QRRES*/':qrcode('https://bilimai.kz/resources'),
 '/*QRCHAMP*/':qrcode('https://bilimai.kz/champions')
};
for(let i=1;i<=8;i++)vars['/*IMPORT'+i+'*/']=asset(path.join(root,'tmp/import-session/Слайд'+i+'.PNG'));
for(const name of ['assel','sabina','bukhar','diana','bakhytzhan'])vars['/*TEAM'+name.toUpperCase()+'*/']=asset(path.join(root,'assets/methodologists/'+name+'.png'));
for(const [k,v] of Object.entries(vars))html=html.split(k).join(v);
html=html.replace('</head>',`<!-- Inter font license\n${fs.readFileSync(path.join(__dirname,'Inter-OFL.txt'),'utf8').replace(/--/g,'—')}\n--></head>`);
fs.writeFileSync(path.join(root,'index.html'),html);
console.log('Written index.html',Buffer.byteLength(html),'bytes');
