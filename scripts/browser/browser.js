
import * as THREE from "three";
import {OrbitControls} from "three/addons/controls/OrbitControls.js";
import {SVGRenderer} from "three/addons/renderers/SVGRenderer.js";
import {VRMLLoader} from "three/addons/loaders/VRMLLoader.js";

const DATA=JSON.parse(document.getElementById("corpus-data").textContent);
const $=id=>document.getElementById(id);
const esc=v=>String(v??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const params=new URLSearchParams(location.search);
const state={part:params.get("part")||"alps-rk09l1140a5l",tab:params.get("tab")||"research",wire:false};
if(!DATA.profiles.some(p=>p.id===state.part))state.part=DATA.profiles[0].id;
if(!["research","model","sources"].includes(state.tab))state.tab="research";
let selected=null, renderer=null, scene=null, camera=null, controls=null, object=null, radius=10, loadedId=null, backend="WebGL";
const categories={controls:"Pots, faders, switches & buttons",patching:"Jacks, nuts & patch access",analog:"Analog ICs",logic:"Trigger & state logic",indicators:"LEDs & optics",interconnects:"Board & cable interconnects",power:"Power & rails",protection:"Fault protection",discretes:"Diodes & transistors",passives:"Resistors & capacitors"};
for(const [id,label] of Object.entries(categories)){
 const o=document.createElement("option");o.value=id;o.textContent=label;$("category").append(o);
}
$("models-only").checked=params.get("models")==="1";
function list(){
 const q=$("search").value.toLowerCase().trim(), category=$("category").value, only=$("models-only").checked;
 const rows=DATA.profiles.filter(p=>(!category||p.category===category)&&(!only||p.model)&&(!q||[p.mpn,p.manufacturer,p.role,p.why,p.cautions,p.lcsc].join(" ").toLowerCase().includes(q)));
 $("count").textContent=`${rows.length} of ${DATA.profiles.length} profiles · ${rows.filter(p=>p.model).length} with a preview`;
 $("list").innerHTML=rows.length?rows.map(p=>`<button class="item" data-part="${esc(p.id)}" aria-pressed="${p.id===state.part}"><b>${esc(p.mpn)}</b><span>${esc(p.manufacturer)} · ${esc(p.role)}</span>${p.model?'<em>3D</em>':""}</button>`).join(""):'<p class="empty">No matching profile. Clear the search or filter.</p>';
}
function setTab(tab){
 state.tab=tab;
 for(const b of document.querySelectorAll("[data-tab]"))b.setAttribute("aria-selected",String(b.dataset.tab===tab));
 for(const t of ["research","model","sources"])$(t+"-panel").hidden=t!==tab;
 if(tab==="model"){
  // A missing model must clear the previous preview before returning to the UI.
  if(!selected?.model)showModel(selected);
  else requestAnimationFrame(()=>{if(state.tab==="model")showModel(selected);});
 }
}
function select(id){
 selected=DATA.profiles.find(p=>p.id===id);if(!selected)return;state.part=id;
 $("manufacturer").textContent=selected.manufacturer+" / "+(categories[selected.category]||selected.category);
 $("title").textContent=selected.mpn;$("role").textContent=selected.role;
 $("badges").innerHTML=`<span class="badge important">${esc(selected.identity_scope)}</span><span class="badge">${esc(selected.origin==="instrument-snapshot"?"Pinned instrument evidence":"Historical / alternative research")}</span><span class="badge">${esc(selected.model?"Preview available — see fidelity":"3D not acquired")}</span>`;
 $("identity").innerHTML=[["Part / family",selected.mpn],["Identity state",selected.identity_state||"Research only"],["Supplier lead",selected.lcsc||"Exact code not established"],["Corpus use","Not fitted · no quantity or PCB placement"]].map(([k,v])=>`<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`).join("");
 $("why").textContent=selected.why;$("cautions").textContent=selected.cautions;$("history").textContent=selected.history;
 const doc=$("doc-link");
 if(location.protocol==="file:"){doc.textContent="Full docs: run the included local server";doc.removeAttribute("href");doc.style.color="var(--muted)";}
 else{doc.textContent="Full documentation ↗";doc.href=selected.doc_url;doc.style.color="";}
 const sources=selected.sources||[];
 $("sources").innerHTML=sources.length?sources.map(s=>{
   const url=s.authoritative_url||s.url||"";
   const allowed=/^https:\/\//.test(url);
   return `<article class="source"><h3>${esc(s.document_title||s.title||s.label||s.source_id||"Source lead")}</h3><p>${allowed?`<a data-source-url="${esc(url)}" target="_blank" rel="noreferrer">${esc(url)}</a>`:"Original URL not established."}</p><p>${esc(s.authority_class||s.status||"Research source")} · ${esc(s.byte_status||(s.retained_path?"retained-hash-match":"link-only"))}</p>${s.retained_path?`<p>Package: <code>${esc(s.retained_path)}</code></p>`:""}${s.sha256?`<p>SHA-256: <code>${esc(s.sha256)}</code></p>`:""}${s.locator?`<p>${esc(s.locator)}</p>`:""}</article>`;
 }).join(""):'<p>Exact datasheet and model acquisition are still open. See the acquisition queue in the project.</p>';
 document.querySelectorAll("#sources a[data-source-url]").forEach(a=>{a.href=a.dataset.sourceUrl;});
 list();setTab(state.tab);
 try{const u=new URL(location.href);u.searchParams.set("part",id);u.searchParams.set("tab",state.tab);history.replaceState(null,"",u);}catch{}
}
function init3D(){
 if(renderer)return;
 scene=new THREE.Scene();
 camera=new THREE.PerspectiveCamera(35,1,0.01,2000);
 try{
  renderer=new THREE.WebGLRenderer({antialias:true,alpha:true,preserveDrawingBuffer:true});
  renderer.setPixelRatio(Math.min(devicePixelRatio||1,2));renderer.outputColorSpace=THREE.SRGBColorSpace;
  renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.35;
 }catch(error){
  renderer=new SVGRenderer();renderer.setQuality("high");renderer.setClearColor(0x182028,1);backend="SVG fallback";
  $("viewer").dataset.fallbackReason="WebGL is unavailable; using geometric SVG projection.";
 }
 $("viewer").dataset.backend=backend;
 $("viewer").prepend(renderer.domElement);
 const h=new THREE.HemisphereLight(0xeaf3ff,0x69727c,2.3);scene.add(h);
 for(const [pos,intensity] of [[[1,2,3],3],[[-2,-1,1],1.8],[[0,1,-2],1]]){
  const l=new THREE.DirectionalLight(0xffffff,intensity);l.position.set(...pos);scene.add(l);
 }
 camera.up.set(0,0,1);controls=new OrbitControls(camera,renderer.domElement);
 controls.enableDamping=false;controls.addEventListener("change",render);
 new ResizeObserver(()=>resize()).observe($("viewer"));
}
function resize(){
 if(!renderer||$("model-panel").hidden)return;
 const w=$("viewer").clientWidth,h=$("viewer").clientHeight;
 if(!w||!h)return;renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix();render();
}
function render(){if(renderer&&camera)renderer.render(scene,camera);}
function cameraView(view){
 if(!camera)return;
 const d=radius*3.6;
 const dirs={iso:[1.4,-1.8,1.45],top:[0,0,2.5],front:[0,-2.5,.03],side:[2.5,0,.03]};
 const v=new THREE.Vector3(...(dirs[view]||dirs.iso)).normalize().multiplyScalar(d);
 camera.position.copy(v);camera.near=Math.max(radius/1000,.001);camera.far=radius*100;
 camera.updateProjectionMatrix();controls.target.set(0,0,0);controls.update();render();
}
function clearObject(){
 if(!object)return;scene.remove(object);
 object.traverse(n=>{if(n.geometry)n.geometry.dispose();if(n.material){for(const m of (Array.isArray(n.material)?n.material:[n.material]))m.dispose();}});
 object=null;
}
function showModel(p){
 if(!p)return;const m=p.model;
 $("viewer").hidden=!m;$("view-tools").hidden=!m;$("no-model").hidden=!!m;
 if(!m){
  clearObject();loadedId=null;
  delete $("viewer").dataset.ready;delete $("viewer").dataset.error;
  $("no-model").textContent="No qualified or explicitly scoped viewing model has been acquired for this profile. No substitute box has been invented.";
  $("model-notice").textContent="Model acquisition open. The research profile remains useful without a render.";
  $("model-metadata").textContent="The missing model is recorded separately from component identity and circuit suitability.";
  return;
 }
 if(loadedId===p.id){resize();return;}
 try{
 init3D();clearObject();
 if(m.kind==="wrl"){
   const raw=DATA.wrl[m.id];if(!raw)throw new Error("Retained WRL not embedded");
   object=new VRMLLoader().parse(raw,"");
   // KiCad VRML geometry is in tenths of an inch. Convert display units to mm.
   const tr=m.transform||{scale:[1,1,1],rotate:[0,0,0],offset:[0,0,0]};
   object.scale.set(...tr.scale.map(x=>x*2.54));
   object.rotation.set(...tr.rotate.map(x=>THREE.MathUtils.degToRad(x)));
   object.position.set(...tr.offset);
   object.updateMatrixWorld(true);
   $("model-notice").textContent="Inherited package preview. Many of these are drawing-derived body envelopes, not complete vendor CAD. They may omit shafts, pins, nuts, threads and tolerances; no installed-fit qualification.";
 }else{
   const mesh=DATA.mesh[m.id];if(!mesh)throw new Error("STEP-derived mesh not embedded");
   const geometry=new THREE.BufferGeometry();geometry.setAttribute("position",new THREE.Float32BufferAttribute(mesh.positions.flat(),3));
   geometry.setIndex(mesh.triangles.flat());geometry.computeVertexNormals();
   object=new THREE.Group();object.add(new THREE.Mesh(geometry,new THREE.MeshLambertMaterial({color:0xb8c5cd,side:THREE.DoubleSide})));
   $("model-notice").textContent=mesh.source_fidelity+" Viewing triangulation derived from retained STEP; no installed-fit approval. Model orientation is the source orientation, not a finished panel mounting plane.";
 }
 let bounds=new THREE.Box3().setFromObject(object), size=new THREE.Vector3(),centre=new THREE.Vector3();
 bounds.getSize(size);bounds.getCenter(centre);
 // Translate the complete imported object as a group without deforming geometry.
 const wrapper=new THREE.Group();wrapper.add(object);wrapper.position.copy(centre.negate());
 object=wrapper;scene.add(object);radius=Math.max(size.x,size.y,size.z)*.62||1;
 setWire(state.wire);loadedId=p.id;resize();cameraView("iso");
 $("model-status").textContent="Rendered via "+backend+" · "+(m.kind==="wrl"?"inherited WRL envelope":"retained STEP → browser mesh");
 $("model-metadata").textContent=`Displayed geometry bounds: ${size.x.toFixed(2)} × ${size.y.toFixed(2)} × ${size.z.toFixed(2)} mm. Bounds describe the imported mesh, not an independently verified component drawing.`;
 $("viewer").dataset.ready=p.id;
 }catch(e){$("model-status").textContent="Model rendering unavailable: "+e.message;$("viewer").dataset.error=e.message;console.error(e);}
}
function setWire(v){
 state.wire=v;$("wireframe").setAttribute("aria-pressed",String(v));
 object?.traverse(n=>{if(n.material)for(const m of (Array.isArray(n.material)?n.material:[n.material])){m.wireframe=v;m.needsUpdate=true;}});
 render();
}
$("list").addEventListener("click",e=>{const b=e.target.closest("[data-part]");if(b)select(b.dataset.part);});
for(const id of ["search","category","models-only"])$(id).addEventListener(id==="search"?"input":"change",list);
for(const b of document.querySelectorAll("[data-tab]"))b.addEventListener("click",()=>setTab(b.dataset.tab));
for(const b of document.querySelectorAll("[data-view]"))b.addEventListener("click",()=>cameraView(b.dataset.view));
$("wireframe").addEventListener("click",()=>setWire(!state.wire));
list();select(state.part);
window.__CORPUS_READY__={profiles:DATA.profiles.length,models:Object.keys(DATA.wrl).length+Object.keys(DATA.mesh).length};
