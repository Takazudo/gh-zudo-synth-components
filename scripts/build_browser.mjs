#!/usr/bin/env node
/** Build the offline browser from project records and retained viewing assets. */
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),"..");
function installed(name){
 const direct=path.join(ROOT,"node_modules",name);
 if(fs.existsSync(direct))return direct;
 const store=path.join(ROOT,"node_modules/.pnpm");
 const prefix=name.replaceAll("/","+")+"@";
 const candidates=fs.readdirSync(store).filter(x=>x.startsWith(prefix)).sort();
 if(candidates.length!==1)throw new Error(`Expected one locked ${name} package; got ${candidates}`);
 return path.join(store,candidates[0],"node_modules",name);
}
const esbuild=await import(path.join(installed("esbuild"),"lib/main.js"));
const three=installed("three");
const build=await esbuild.build({
 entryPoints:[path.join(ROOT,"scripts/browser/browser.js")],bundle:true,write:false,
 format:"iife",minify:true,legalComments:"inline",platform:"browser",target:["es2020"],
 alias:{"three/addons":path.join(three,"examples/jsm"),"three":three}
});
const profiles=JSON.parse(fs.readFileSync(path.join(ROOT,"corpus/catalog.json"),"utf8"));
const data={profiles:profiles.map(({facts,sources,...p})=>({...p,sources:(sources||[]).map(s=>({
 source_id:s.source_id, document_title:s.document_title||s.title||s.label,
 authoritative_url:s.authoritative_url||s.url, authority_class:s.authority_class,
 byte_status:s.byte_status||(s.retained_path?"retained-hash-match":"link-only"),
 retained_path:s.retained_path, sha256:s.retained_path?s.sha256:undefined,
 locator:s.locator
}))})),wrl:{},mesh:{}};
for(const p of profiles){const m=p.model;if(!m)continue;
 if(m.kind==="wrl")data.wrl[m.id]=fs.readFileSync(path.join(ROOT,m.path),"utf8");
 else data.mesh[m.id]=JSON.parse(fs.readFileSync(path.join(ROOT,m.path),"utf8"));
}
const safe=JSON.stringify(data).replaceAll("<","\\u003c");
const template=fs.readFileSync(path.join(ROOT,"scripts/browser/browser.html"),"utf8");
const out=template.replace("__DATA__",()=>safe).replace("__SCRIPT__",()=>build.outputFiles[0].text.replaceAll("</script","<\\/script"));
const dest=path.join(ROOT,"doc/public/assets/corpus-browser.html");fs.mkdirSync(path.dirname(dest),{recursive:true});fs.writeFileSync(dest,out);
fs.mkdirSync(path.join(ROOT,"third-party-notices"),{recursive:true});
for(const name of ["three","esbuild"]){
 const dir=installed(name);for(const file of ["LICENSE","LICENSE.md"]){if(fs.existsSync(path.join(dir,file))){fs.copyFileSync(path.join(dir,file),path.join(ROOT,"third-party-notices",name+"-LICENSE.txt"));break;}}
}
console.log(JSON.stringify({profiles:profiles.length,wrl:Object.keys(data.wrl).length,step:Object.keys(data.mesh).length,bytes:Buffer.byteLength(out)}));
