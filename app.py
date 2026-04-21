import streamlit as st
import streamlit.components.v1 as components
import re, os, sys

sys.path.insert(0, os.path.dirname(__file__))

st.set_page_config(
    page_title="Research Analyst AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────────────────────────────────────
#  GLOBAL CSS — injected via st.markdown (CSS only, no scripts)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Outfit:wght@300;400;600;700;900&display=swap');

/* ── Make Streamlit surfaces transparent so Three.js canvas shows through ── */
html, body,
[data-testid="stApp"],
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main, .block-container,
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"] {
  background: transparent !important;
  background-color: transparent !important;
}

/* Force dark base so it doesn't flash white */
[data-testid="stApp"] {
  background: #00000a !important;
}

[data-testid="stHeader"]  { box-shadow: none !important; background: transparent !important; }
[data-testid="stSidebar"] { display: none !important; }

/* Lift all real content above the canvas iframe */
[data-testid="stMain"],
.block-container {
  position: relative;
  z-index: 10;
}
.block-container {
  padding: 0 2.5rem 5rem !important;
  max-width: 980px !important;
  margin: auto;
}

*, body { font-family: 'Outfit', sans-serif !important; color: #dde8f0; }

/* ── Hero ── */
.hero { text-align:center; padding:4rem 1rem 2.5rem; }
.hero-badge {
  font-family:'Space Mono',monospace !important; font-size:.63rem; letter-spacing:.22em;
  color:#00cfff; border:1px solid rgba(0,207,255,.35); border-radius:99px;
  padding:.28rem 1.1rem; display:inline-block; margin-bottom:1.4rem;
  background:rgba(0,207,255,.1);
}
.hero h1 {
  font-size:clamp(2.8rem,7vw,5rem); font-weight:900; line-height:1.05;
  background:linear-gradient(130deg,#ffffff 15%,#00cfff 52%,#8b5cf6 88%);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
  background-clip: text;
  margin-bottom:1rem;
}
.hero .sub {
  color:#8aaabb; font-size:1rem; max-width:480px; margin:0 auto 2.5rem;
  line-height:1.8; font-weight:300;
}

/* ── Input card ── */
.icard {
  background:linear-gradient(135deg,rgba(0,207,255,.08),rgba(139,92,246,.08));
  border:1px solid rgba(0,207,255,.28); border-radius:20px;
  padding:2rem 2rem 1.6rem; backdrop-filter:blur(24px);
  box-shadow:0 0 60px rgba(0,207,255,.08),inset 0 1px 0 rgba(255,255,255,.06);
}
.icard-lbl {
  font-family:'Space Mono',monospace !important; font-size:.62rem;
  letter-spacing:.18em; color:#00cfff; margin-bottom:.5rem; opacity:.7;
}

/* ── Step tracker ── */
.steps { display:grid; grid-template-columns:repeat(4,1fr); gap:.9rem; margin:1.8rem 0 .5rem; }
.step {
  border:1px solid rgba(255,255,255,.1); border-radius:14px; padding:1rem .8rem;
  text-align:center; background:rgba(0,0,0,.6); backdrop-filter:blur(14px); transition:all .4s;
}
.step.active {
  border-color:#00cfff; background:rgba(0,207,255,.12);
  box-shadow:0 0 28px rgba(0,207,255,.25); animation:pstep 1.6s ease-in-out infinite;
}
.step.done   { border-color:#10d4a0; background:rgba(16,212,160,.1); }
.step.wait   { opacity:.3; }
@keyframes pstep{0%,100%{box-shadow:0 0 28px rgba(0,207,255,.22)}50%{box-shadow:0 0 46px rgba(0,207,255,.45)}}
.step-ico  { font-size:1.5rem; margin-bottom:.35rem; }
.step-lbl  { font-family:'Space Mono',monospace !important; font-size:.56rem; color:#3a5060; letter-spacing:.12em; }
.step-name { font-size:.82rem; font-weight:600; margin-top:.15rem; color:#8aaabb; }
.step.active .step-name { color:#00cfff; }
.step.done   .step-name { color:#10d4a0; }

/* ── Status ── */
.status-line {
  font-family:'Space Mono',monospace !important; font-size:.72rem;
  letter-spacing:.08em; text-align:center; padding:.6rem; color:#00cfff; opacity:.9;
}

/* ── Section header ── */
.sec-hdr {
  display:flex; align-items:center; gap:.8rem; margin:2.5rem 0 .9rem;
  font-family:'Space Mono',monospace !important; font-size:.65rem;
  letter-spacing:.18em; color:#00cfff; text-transform:uppercase;
}
.sec-hdr::after { content:''; flex:1; height:1px; background:rgba(0,207,255,.2); }

/* ── Output boxes ── */
.outbox {
  background:rgba(0,0,0,.65); border:1px solid rgba(0,207,255,.2); border-radius:14px;
  padding:1.6rem; line-height:1.9; color:#a8c4d4; font-size:.91rem;
  white-space:pre-wrap; backdrop-filter:blur(14px);
}
.outbox.report { border-color:rgba(139,92,246,.4); }
.outbox.critic { border-color:rgba(16,212,160,.4); }

/* ── Score pill ── */
.score {
  display:inline-block;
  background:linear-gradient(120deg,#8b5cf6,#00cfff);
  border-radius:99px; padding:.3rem 1.4rem;
  font-family:'Space Mono',monospace !important;
  font-weight:700; font-size:1rem; color:#000; margin-bottom:1rem;
}

/* ── Streamlit widget overrides ── */
.stTextInput>div>div>input {
  background:rgba(0,207,255,.06) !important;
  border:1px solid rgba(0,207,255,.3) !important;
  border-radius:12px !important; color:#e2eaf0 !important;
  font-family:'Outfit',sans-serif !important; font-size:1.05rem !important;
  padding:.85rem 1.1rem !important; caret-color:#00cfff !important;
}
.stTextInput>div>div>input:focus {
  border-color:#00cfff !important;
  box-shadow:0 0 0 3px rgba(0,207,255,.18) !important; outline:none !important;
}
.stTextInput>div>div>input::placeholder { color:#2a4050 !important; }

.stButton>button {
  background:linear-gradient(120deg,#00cfff 0%,#8b5cf6 100%) !important;
  color:#000 !important; font-family:'Space Mono',monospace !important;
  font-weight:700 !important; font-size:.78rem !important; letter-spacing:.12em !important;
  border:none !important; border-radius:12px !important;
  padding:.85rem 2rem !important; width:100% !important;
  cursor:pointer !important; transition:opacity .2s,transform .1s !important;
}
.stButton>button:hover  { opacity:.82 !important; }
.stButton>button:active { transform:scale(.98) !important; }

div[data-testid="stDownloadButton"]>button {
  background:rgba(0,207,255,.08) !important; color:#00cfff !important;
  border:1px solid rgba(0,207,255,.25) !important;
  font-family:'Space Mono',monospace !important; font-weight:700 !important;
  font-size:.73rem !important; letter-spacing:.1em !important;
  border-radius:10px !important; width:100% !important;
}

.stProgress>div>div>div>div {
  background:linear-gradient(90deg,#00cfff,#8b5cf6) !important;
  border-radius:99px !important;
}

label[data-testid="stWidgetLabel"],
.stTextInput label { display:none !important; }

::-webkit-scrollbar { width:4px; }
::-webkit-scrollbar-thumb { background:rgba(0,207,255,.25); border-radius:4px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  THREE.JS BACKGROUND — rendered via components.html so scripts actually run
#  Height=0 + absolute positioning lets it cover the full viewport without
#  pushing Streamlit content down.
# ─────────────────────────────────────────────────────────────────────────────
components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
  * { margin:0; padding:0; overflow:hidden; }
  body { background: transparent; }
  canvas { display:block; }
</style>
</head>
<body>
<canvas id="c"></canvas>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
(function(){
  const canvas = document.getElementById('c');
  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setClearColor(0x00000a, 1);

  const W = () => window.parent.innerWidth;
  const H = () => window.parent.innerHeight;
  renderer.setSize(W(), H());

  const scene  = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(55, W()/H(), 0.1, 500);
  camera.position.set(0, 0, 55);

  /* 1. STAR FIELD */
  const sArr = new Float32Array(1400*3);
  for(let i=0;i<sArr.length;i++) sArr[i]=(Math.random()-0.5)*380;
  const sGeo = new THREE.BufferGeometry();
  sGeo.setAttribute('position', new THREE.BufferAttribute(sArr,3));
  scene.add(new THREE.Points(sGeo,
    new THREE.PointsMaterial({color:0xffffff,size:0.18,transparent:true,opacity:0.55})));

  /* 2. NEURAL PARTICLE CLOUD */
  const N=180;
  const nArr=new Float32Array(N*3), nVel=[];
  for(let i=0;i<N;i++){
    nArr[i*3]  =(Math.random()-0.5)*80;
    nArr[i*3+1]=(Math.random()-0.5)*50;
    nArr[i*3+2]=(Math.random()-0.5)*30;
    nVel.push({x:(Math.random()-0.5)*0.025,y:(Math.random()-0.5)*0.018,z:(Math.random()-0.5)*0.012});
  }
  const nGeo=new THREE.BufferGeometry();
  nGeo.setAttribute('position',new THREE.BufferAttribute(nArr,3));
  scene.add(new THREE.Points(nGeo,
    new THREE.PointsMaterial({color:0x00cfff,size:0.36,transparent:true,opacity:0.95})));

  /* 3. LIVE EDGES */
  const MAX_E=400, eBuf=new Float32Array(MAX_E*6);
  const eGeo=new THREE.BufferGeometry();
  eGeo.setAttribute('position',new THREE.BufferAttribute(eBuf,3));
  eGeo.setDrawRange(0,0);
  scene.add(new THREE.LineSegments(eGeo,
    new THREE.LineBasicMaterial({color:0x0099cc,transparent:true,opacity:0.25})));

  /* 4. TORUS RINGS */
  function mkRing(r,tube,col,rx,ry,rz){
    const m=new THREE.Mesh(
      new THREE.TorusGeometry(r,tube,6,120),
      new THREE.MeshBasicMaterial({color:col,wireframe:true,transparent:true,opacity:0.3}));
    m.rotation.set(rx,ry,rz); scene.add(m); return m;
  }
  const ring1=mkRing(18,0.055,0x00cfff,Math.PI/4, 0.3, 0);
  const ring2=mkRing(26,0.04, 0x8b5cf6,Math.PI/6,-0.5, 0.2);
  const ring3=mkRing(34,0.03, 0x10d4a0,Math.PI/8, 0.1,-0.3);

  /* 5. LEFT DNA HELIX */
  const hA=[],hB=[];
  for(let i=0;i<200;i++){
    const t=(i/200)*Math.PI*8-Math.PI*4, y=t*2.4;
    hA.push(new THREE.Vector3(-38+Math.cos(t)*4,      y,Math.sin(t)*2));
    hB.push(new THREE.Vector3(-38+Math.cos(t+Math.PI)*4,y,Math.sin(t+Math.PI)*2));
  }
  scene.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(hA),
    new THREE.LineBasicMaterial({color:0x00cfff,transparent:true,opacity:0.65})));
  scene.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(hB),
    new THREE.LineBasicMaterial({color:0x8b5cf6,transparent:true,opacity:0.65})));
  for(let i=0;i<200;i+=10)
    scene.add(new THREE.Line(
      new THREE.BufferGeometry().setFromPoints([hA[i],hB[i]]),
      new THREE.LineBasicMaterial({color:0x10d4a0,transparent:true,opacity:0.4})));

  /* 6. RIGHT DNA HELIX */
  const hC=[],hD=[];
  for(let i=0;i<200;i++){
    const t=(i/200)*Math.PI*6-Math.PI*3, y=t*2.8;
    hC.push(new THREE.Vector3(36+Math.cos(t+1)*3.5,      y,Math.sin(t+1)*1.5));
    hD.push(new THREE.Vector3(36+Math.cos(t+1+Math.PI)*3.5,y,Math.sin(t+1+Math.PI)*1.5));
  }
  scene.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(hC),
    new THREE.LineBasicMaterial({color:0x8b5cf6,transparent:true,opacity:0.55})));
  scene.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(hD),
    new THREE.LineBasicMaterial({color:0x10d4a0,transparent:true,opacity:0.55})));

  /* 7. ICOSAHEDRON CORE */
  const core=new THREE.Mesh(
    new THREE.IcosahedronGeometry(4,1),
    new THREE.MeshBasicMaterial({color:0x00cfff,wireframe:true,transparent:true,opacity:0.32}));
  scene.add(core);

  /* 8. ORBITING SATELLITES */
  const orbs=[];
  [0x00cfff,0x8b5cf6,0x10d4a0,0xf59e0b].forEach((col,i)=>{
    const m=new THREE.Mesh(
      new THREE.OctahedronGeometry(0.75,0),
      new THREE.MeshBasicMaterial({color:col,wireframe:true,transparent:true,opacity:0.9}));
    scene.add(m);
    orbs.push({mesh:m,radius:8+i*2.2,speed:0.38+i*0.14,phase:(Math.PI/2)*i});
  });

  /* 9. WIREFRAME DATA PLANES */
  function wPlane(x,y,z,ry){
    const m=new THREE.Mesh(
      new THREE.PlaneGeometry(14,8,9,5),
      new THREE.MeshBasicMaterial({color:0x00cfff,wireframe:true,transparent:true,opacity:0.07}));
    m.position.set(x,y,z); m.rotation.y=ry; scene.add(m); return m;
  }
  const pl1=wPlane(-20, 8,10, 0.6);
  const pl2=wPlane( 22,-6, 5,-0.5);
  const pl3=wPlane(  0,15,-15,0.1);

  /* ANIMATE */
  let f=0;
  (function loop(){
    requestAnimationFrame(loop); f++;
    const t=f*0.005;
    const p=nGeo.attributes.position.array;
    for(let i=0;i<N;i++){
      p[i*3]  +=nVel[i].x; p[i*3+1]+=nVel[i].y; p[i*3+2]+=nVel[i].z;
      if(Math.abs(p[i*3])  >40) nVel[i].x*=-1;
      if(Math.abs(p[i*3+1])>25) nVel[i].y*=-1;
      if(Math.abs(p[i*3+2])>15) nVel[i].z*=-1;
    }
    nGeo.attributes.position.needsUpdate=true;
    let ei=0;
    for(let i=0;i<N&&ei<MAX_E-1;i++)
      for(let j=i+1;j<N&&ei<MAX_E-1;j++){
        const dx=p[i*3]-p[j*3],dy=p[i*3+1]-p[j*3+1],dz=p[i*3+2]-p[j*3+2];
        if(dx*dx+dy*dy+dz*dz<110){
          eBuf[ei*6]=p[i*3]; eBuf[ei*6+1]=p[i*3+1]; eBuf[ei*6+2]=p[i*3+2];
          eBuf[ei*6+3]=p[j*3]; eBuf[ei*6+4]=p[j*3+1]; eBuf[ei*6+5]=p[j*3+2];
          ei++;
        }
      }
    eGeo.attributes.position.needsUpdate=true;
    eGeo.setDrawRange(0,ei*2);
    ring1.rotation.y=t*0.35; ring1.rotation.z=t*0.1;
    ring2.rotation.y=-t*0.26; ring2.rotation.x+=0.002;
    ring3.rotation.y=t*0.18;  ring3.rotation.z-=0.0015;
    core.rotation.y=t*0.6; core.rotation.x=t*0.4;
    const s=1+Math.sin(t*3)*0.08; core.scale.set(s,s,s);
    orbs.forEach(o=>{
      o.mesh.position.x=Math.cos(t*o.speed+o.phase)*o.radius;
      o.mesh.position.y=Math.sin(t*o.speed*0.7)*3;
      o.mesh.position.z=Math.sin(t*o.speed+o.phase)*o.radius*0.5;
      o.mesh.rotation.x=t*1.2; o.mesh.rotation.y=t*0.8;
    });
    pl1.rotation.y=Math.sin(t*0.3)*0.3+0.6;
    pl2.rotation.y=Math.cos(t*0.25)*0.3-0.5;
    pl3.position.y=15+Math.sin(t*0.4)*2;
    camera.position.x=Math.sin(t*0.08)*4;
    camera.position.y=Math.cos(t*0.06)*2;
    camera.lookAt(0,0,0);
    renderer.render(scene,camera);
  })();

  /* Resize to match parent window */
  function onResize(){
    const w=W(), h=H();
    camera.aspect=w/h;
    camera.updateProjectionMatrix();
    renderer.setSize(w,h);
  }
  window.addEventListener('resize', onResize);
  setInterval(onResize, 1000); /* poll in case resize event misses */
})();
</script>
</body>
</html>
""",
# Height 0 — the canvas is position:fixed in the parent doc via CSS below
height=0,
scrolling=False
)

# Inject CSS to pull the iframe behind everything and make it cover the screen
st.markdown("""
<style>
/* Target the components iframe and make it cover the full viewport */
iframe[title="st.iframe"] ,
iframe[title="streamlit_component.v1.iframe"],
div[data-testid="stIFrame"] > iframe {
  position: fixed !important;
  top: 0 !important; left: 0 !important;
  width: 100vw !important; height: 100vh !important;
  border: none !important;
  z-index: 0 !important;
  pointer-events: none !important;
}
/* Dark radial overlay for readability */
[data-testid="stApp"]::before {
  content: '';
  position: fixed;
  top: 0; left: 0;
  width: 100vw; height: 100vh;
  z-index: 1;
  pointer-events: none;
  background: radial-gradient(ellipse at 30% 40%,
    rgba(4,0,26,0.70) 0%,
    rgba(0,0,12,0.86) 60%,
    rgba(0,2,18,0.94) 100%);
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  HERO
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-badge">⬡ MULTI-AGENT RESEARCH SYSTEM</div>
  <h1>Research<br/>Analyst AI</h1>
  <p class="sub">Four specialized agents — Search · Read · Write · Critique —<br/>
  collaborate to produce publication-ready research reports.</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  INPUT CARD
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="icard">', unsafe_allow_html=True)
st.markdown('<div class="icard-lbl">RESEARCH TOPIC</div>', unsafe_allow_html=True)
topic = st.text_input("topic", placeholder="e.g.  Quantum computing breakthroughs in 2025 …", label_visibility="collapsed")
st.markdown('<div style="height:.8rem"></div>', unsafe_allow_html=True)
run = st.button("⚡  LAUNCH RESEARCH PIPELINE")
st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  STEP RENDERER
# ─────────────────────────────────────────────────────────────────────────────
STEPS = [
    ("🔍","STEP 01","Search Agent"),
    ("📖","STEP 02","Reader Agent"),
    ("✍️","STEP 03","Writer Chain"),
    ("🎯","STEP 04","Critic Chain"),
]

def render_steps(active: int):
    cards = ""
    for i,(ico,lbl,name) in enumerate(STEPS):
        cls = "active" if i==active else ("done" if i<active else "wait")
        cards += (f'<div class="step {cls}">'
                  f'<div class="step-ico">{ico}</div>'
                  f'<div class="step-lbl">{lbl}</div>'
                  f'<div class="step-name">{name}</div></div>')
    st.markdown(f'<div class="steps">{cards}</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  PIPELINE
# ─────────────────────────────────────────────────────────────────────────────
if run and topic.strip():
    try:
        from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain
    except ImportError as e:
        st.error(f"Import error: {e} — make sure agents.py is in the same folder."); st.stop()

    state  = {}
    prog   = st.progress(0)
    status = st.empty()

    # Step 1 — Search
    render_steps(0)
    status.markdown('<div class="status-line">🔍 Search agent scanning the web …</div>', unsafe_allow_html=True)
    prog.progress(8)
    try:
        r = build_search_agent().invoke({
            "messages":[("user", f"Find recent, reliable, detailed information about: {topic}")]})
        state["search"] = r["messages"][-1].content
        prog.progress(28)
    except Exception as e:
        st.error(f"Search agent failed: {e}"); st.stop()

    # Step 2 — Reader
    render_steps(1)
    status.markdown('<div class="status-line">📖 Reader agent scraping top sources …</div>', unsafe_allow_html=True)
    try:
        r2 = build_reader_agent().invoke({"messages":[("user",
            f"Based on these search results about '{topic}', pick the most relevant URL and scrape it.\n\n"
            f"{state['search'][:800]}")]})
        state["scraped"] = r2["messages"][-1].content
        prog.progress(54)
    except Exception as e:
        st.error(f"Reader agent failed: {e}"); st.stop()

    # Step 3 — Writer
    render_steps(2)
    status.markdown('<div class="status-line">✍️ Writer drafting your report …</div>', unsafe_allow_html=True)
    try:
        combined = f"SEARCH RESULTS:\n{state['search']}\n\nSCRAPED CONTENT:\n{state['scraped']}"
        state["report"] = writer_chain.invoke({"topic": topic, "research": combined})
        prog.progress(78)
    except Exception as e:
        st.error(f"Writer chain failed: {e}"); st.stop()

    # Step 4 — Critic
    render_steps(3)
    status.markdown('<div class="status-line">🎯 Critic reviewing the report …</div>', unsafe_allow_html=True)
    try:
        state["feedback"] = critic_chain.invoke({"report": state["report"]})
        prog.progress(100)
    except Exception as e:
        st.error(f"Critic chain failed: {e}"); st.stop()

    render_steps(5)
    status.markdown('<div class="status-line" style="color:#10d4a0">✅ Pipeline complete!</div>', unsafe_allow_html=True)

    # Report
    st.markdown('<div class="sec-hdr">📄 Research Report</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="outbox report">{state["report"]}</div>', unsafe_allow_html=True)

    # Feedback
    st.markdown('<div class="sec-hdr">🎯 Critic Evaluation</div>', unsafe_allow_html=True)
    m = re.search(r'Score:\s*(\d+(?:\.\d+)?)/10', state["feedback"])
    if m:
        st.markdown(f'<div class="score">Score: {m.group(1)} / 10</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="outbox critic">{state["feedback"]}</div>', unsafe_allow_html=True)

    # Download
    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    full = f"# {topic}\n\n{state['report']}\n\n---\n\n## Critic Evaluation\n\n{state['feedback']}"
    st.download_button("⬇  DOWNLOAD REPORT (.md)", full,
        file_name=f"research_{topic[:30].replace(' ','_')}.md",
        mime="text/markdown")

elif run:
    st.warning("Please enter a research topic first.")

# ─────────────────────────────────────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:5rem;
  border-top:1px solid rgba(0,207,255,.1);padding-top:1.5rem">
  <p style="font-family:'Space Mono',monospace;font-size:.6rem;
    color:#1a3a4a;letter-spacing:.18em">
    RESEARCH ANALYST AI · MULTI-AGENT PIPELINE
  </p>
</div>
""", unsafe_allow_html=True)