const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for (const [n,w,h] of [['desk',1360,900],['mob',390,844]]){
 const p=await b.newPage({viewport:{width:w,height:h}});
 await p.goto('file://'+process.argv[2]); await p.waitForLoadState('load'); for(let y=0;y<12000;y+=600){await p.evaluate(v=>scrollTo(0,v),y);await p.waitForTimeout(120);} await p.evaluate(()=>scrollTo(0,0)); await p.waitForTimeout(600);
 const sw=await p.evaluate(()=>document.documentElement.scrollWidth); console.log(n,'scrollWidth',sw);
 await p.screenshot({path:`shot-${n}.png`,fullPage:true});}
await b.close();})();
