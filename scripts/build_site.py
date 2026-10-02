"""Build a local course index, interactive teaching page, and lesson navigation."""
from pathlib import Path
import os
from html import escape
import re
import nbformat
from urllib.parse import unquote, urlsplit, urlunsplit
from bs4 import BeautifulSoup
from public_site import homepage, reader_view
from build_practice import build_practice

from course_paths import ROOT, NOTEBOOKS, DOCS, SITE, EXPORTS, legacy_location
STYLE = '''
:root{--ink:#13243b;--muted:#405671;--blue:#0d766f;--warm:#7356cf;--line:#d9e2f0;--paper:#f5f7fc}
*{box-sizing:border-box}[hidden]{display:none!important}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.65 system-ui,-apple-system,Segoe UI,sans-serif}
a{color:var(--blue);text-underline-offset:3px}main{max-width:1100px;margin:auto;padding:46px 30px 70px}
nav{border-bottom:1px solid var(--line);background:white;padding:15px max(24px,calc((100vw - 1040px)/2));display:flex;gap:22px;flex-wrap:wrap;font-size:14px}
nav a{text-decoration:none;font-weight:650}h1{font-size:clamp(34px,5vw,58px);line-height:1.08;letter-spacing:-1.8px;margin:20px 0}h2{font-size:25px;line-height:1.25;margin:0 0 14px}h3{font-size:19px;margin:0 0 8px}
p{max-width:800px}.eyebrow{font-size:12px;text-transform:uppercase;letter-spacing:2px;font-weight:750;color:var(--warm)}.lead{font-size:20px;color:var(--muted);max-width:780px}
.chips{display:flex;flex-wrap:wrap;gap:10px;margin:22px 0 32px}.chip{background:#e6eef8;padding:5px 12px;border-radius:30px;font-size:13px}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.card,.panel{background:white;border:1px solid var(--line);border-radius:12px;padding:24px}.card{display:flex;flex-direction:column}.card p{font-size:14px;color:var(--muted);flex:1;margin:6px 0 20px}.card .number{font-size:12px;letter-spacing:1px;color:var(--warm);font-weight:700;margin-bottom:10px}
.actions{display:flex;gap:15px;font-size:14px}.button{display:inline-block;background:var(--ink);color:white;text-decoration:none;border-radius:6px;padding:10px 18px}.section{margin-top:40px}.note{border-left:3px solid var(--warm);padding:10px 18px;background:#fff8f1;margin:24px 0;font-size:14px}.small{font-size:13px;color:var(--muted)}
.two{display:grid;grid-template-columns:1fr 1fr;gap:24px}.control{margin:15px 0}.control label{display:flex;justify-content:space-between;gap:15px;font-size:14px;font-weight:650}.control input{width:100%;accent-color:var(--blue);cursor:pointer}.barrow{display:grid;grid-template-columns:30px 1fr 60px;gap:12px;align-items:center;margin:18px 0}.track{height:28px;background:#edf2f8}.bar{height:100%;background:var(--blue);transition:width .12s}.metric{font-size:30px;font-weight:750;color:var(--blue)}button{font:inherit;cursor:pointer;padding:7px 14px;border:1px solid var(--line);border-radius:5px;background:white;color:var(--ink)}button:hover{background:#e6eef8}button:focus-visible,a:focus-visible,input:focus-visible{outline:3px solid #c46b20;outline-offset:3px}
table{border-collapse:collapse;width:100%;font-size:14px}th,td{text-align:left;border-bottom:1px solid var(--line);padding:10px}summary{cursor:pointer;font-weight:650}svg{max-width:100%;height:auto}code{background:#edf2f8;padding:2px 5px;border-radius:3px}
@media(max-width:780px){.grid{grid-template-columns:1fr 1fr}.two{grid-template-columns:1fr}main{padding:28px 18px}h1{letter-spacing:-1px}}
@media(max-width:500px){.grid{grid-template-columns:1fr}.card,.panel{padding:20px}}
.course-hero{background:#13243b;color:white;padding:38px;border-radius:22px;box-shadow:0 14px 35px #13243b12;border-top:6px solid #3dd8c6}.course-hero .lead{color:#afc4df}.course-hero .eyebrow{color:#70e0d1}.course-hero .chip{background:#235557;color:white}.course-hero .button{background:#70e0d1;color:#13243b}.course-hero .chips{margin-bottom:22px}.card{border-top:4px solid #c2afff}.card:hover{box-shadow:0 8px 24px #13243b0c}.note{background:#f1edfb}.button{background:#0d766f}.path-art{display:block;width:100%;height:auto;margin:18px 0 24px}nav strong{color:#0d766f}@media(max-width:500px){.course-hero{padding:24px}}
.actions{flex-wrap:wrap}
'''

SUPPORT_PAGES = [
    ('README.md','README'), ('COURSE.md','COURSE'), ('CONTRIBUTING.md','CONTRIBUTING'),
    ('REPOSITORY.md','REPOSITORY'), ('GITHUB_PUBLISHING.md','GITHUB_PUBLISHING'),
    ('SETUP.md','SETUP'), ('FAQ.md','FAQ'), ('SHARING.md','SHARING'),
    ('GLOSSARY.md','GLOSSARY'), ('SOURCES.md','SOURCES'), ('PAPER_GUIDE.md','PAPER_GUIDE'),
    ('LEARNING_GUIDE.md','LEARNING_GUIDE'), ('PRACTICE.md','PRACTICE'),
    ('MODEL_GUIDE.md','MODEL_GUIDE'), ('QUICK_REFERENCE.md','QUICK_REFERENCE'),
    ('data/README.md','data_README'), ('assignments/README.md','assignments_README'),
    ('assignments/01_design_a_decision.md','assignments_01_design_a_decision'),
    ('assignments/02_probabilities_and_actions.md','assignments_02_probabilities_and_actions'),
    ('assignments/03_evaluate_a_router.md','assignments_03_evaluate_a_router'),
    ('assignments/04_compare_torch_models.md','assignments_04_compare_torch_models'),
]

SUPPORT_PAGES = [(legacy_location(source), target) for source, target in SUPPORT_PAGES]
SUPPORT_PAGES += [('docs/README.md', 'guides'), ('notebooks/README.md', 'notebooks')]
SUPPORT_PAGES += [('docs/VISUAL_GUIDE.md', 'VISUAL_GUIDE'), ('docs/SELF_REVIEW.md', 'SELF_REVIEW')]

LESSONS = [
('00_start_here','Start here','Choose a path, understand the evidence labels, and check your setup.'),
('01_jev_basics','The decision interface','State, Choice, Score, and Noul. Valid output can still be wrong.'),
('02_decision_model_from_scratch','Build a decision model','Train with NumPy, inspect tensor shapes, and see the decision boundaries.'),
('03_calibration_and_decisions','Trust the probability?','Fit temperature on separate data and explore the costs of acting or reviewing.'),
('04_workflows_and_related_models','Compose the workflow','Separate judgment, evidence retrieval, permissions, and deterministic rules.'),
('05_optional_real_jev_api','Call real Jev, optionally','Inspect the official request, validate answers, and enable a live call yourself.'),
('06_architecture_and_training_lab','Inside the mechanisms','Candidate scoring, isolated attention, shared work, and learning objectives.'),
('07_text_routing_capstone','Build the complete system','Train a local text router on fictional tickets, then inspect held-out results and failures.'),
('08_exercises_and_solutions','Check your understanding','Worked answers with runnable checks, from softmax to label leakage.'),
('09_related_models_lab','Compare related approaches','Try rules, lexical prototypes, and a learned classifier on the same fictional messages.'),
('10_pytorch_models_lab','Train six PyTorch models','Trace updates, compare word-order representations, and evaluate three seeds on a paired toy task.'),
]

def document(title, body, script=''):
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)}</title><style>{STYLE}</style></head><body>{body}<script>{script}</script></body></html>'

def build_site():
    EXPORTS.mkdir(parents=True, exist_ok=True)
    (SITE/'index.html').write_text(document('Learn Jev, one decision at a time',homepage(LESSONS)),encoding='utf-8')
    build_practice(ROOT, document)

    playground = '''<nav><a href="index.html">← Course home</a><a href="lessons/02_decision_model_from_scratch.html">Softmax lesson</a><a href="lessons/03_calibration_and_decisions.html">Calibration lesson</a></nav><main>
    <div class="eyebrow">Interactive teaching experiments · no model calls</div><h1>Change the numbers.<br>Watch the decision move.</h1><p class="lead">These controls illustrate mathematical rules. They are not Jev settings or measurements.</p>
    <section class="section panel"><h2>1. Logits become probabilities</h2><p>Adjust three scores and a positive temperature. Softmax normalizes the scores into one distribution. Higher temperature spreads probability more evenly.</p><div class="two"><div>
    <div class="control"><label for="z0">Logit A <output id="z0out"></output></label><input id="z0" type="range" min="-4" max="4" step=".1" value=".2"></div>
    <div class="control"><label for="z1">Logit B <output id="z1out"></output></label><input id="z1" type="range" min="-4" max="4" step=".1" value="1.4"></div>
    <div class="control"><label for="z2">Logit C <output id="z2out"></output></label><input id="z2" type="range" min="-4" max="4" step=".1" value="-.3"></div>
    <div class="control"><label for="temp">Temperature <output id="tempout"></output></label><input id="temp" type="range" min=".1" max="4" step=".1" value="1"></div><button id="resetsoft">Reset softmax</button></div>
    <div><div class="barrow"><span>A</span><div class="track"><div class="bar" id="bar0"></div></div><output id="p0"></output></div><div class="barrow"><span>B</span><div class="track"><div class="bar" id="bar1"></div></div><output id="p1"></output></div><div class="barrow"><span>C</span><div class="track"><div class="bar" id="bar2"></div></div><output id="p2"></output></div><p>Most likely: <strong id="winner"></strong></p><p>Entropy: <strong id="entropy"></strong> nats</p><p class="small">Entropy measures distribution spread. It is not the Jev confidence field. A normalized probability can still be miscalibrated.</p></div></div>
    <details><summary>Try this</summary><p>Set all logits equal. Change temperature: the probabilities remain one-third each. Now make B largest and lower temperature: the winner stays B while the distribution sharpens.</p></details></section>
    <section class="section panel"><h2>2. Choose between acting and reviewing</h2><p>Assume correct automatic actions cost zero and review is perfectly accurate. Choose the action with the lowest expected cost; the probability alone does not determine the best action.</p><div class="two"><div>
    <div class="control"><label for="prob">Probability of yes <output id="probout"></output></label><input id="prob" type="range" min="0" max="1" step=".01" value=".5"></div>
    <div class="control"><label for="fp">False-positive cost <output id="fpout"></output></label><input id="fp" type="range" min=".1" max="10" step=".1" value="4"></div>
    <div class="control"><label for="fn">False-negative cost <output id="fnout"></output></label><input id="fn" type="range" min=".1" max="10" step=".1" value="1"></div>
    <div class="control"><label for="review">Review cost <output id="reviewout"></output></label><input id="review" type="range" min="0" max="2" step=".01" value=".2"></div><button id="resetcost">Reset costs</button></div>
    <div><div class="small">LOWEST EXPECTED COST</div><div class="metric" id="action" aria-live="polite"></div><table><thead><tr><th>Action</th><th>Expected cost</th></tr></thead><tbody><tr><td>Yes: (1 − p) × FP</td><td id="yescost"></td></tr><tr><td>No: p × FN</td><td id="nocost"></td></tr><tr><td>Perfect review</td><td id="reviewcost"></td></tr></tbody></table><p id="threshold" class="small"></p></div></div>
    <svg id="costplot" viewBox="0 0 780 260" role="img" aria-label="Expected action costs across probabilities"><g id="plotcontents"></g></svg>
    <details><summary>Try this</summary><p>At p = 0.5 and the default costs, review is cheapest. Raise review cost to 0.8: review has no strict advantage at any probability. Raise p to 0.99 with the default costs: acting yes is cheaper than review.</p></details></section>
    <div class="note">These policies depend on calibrated probabilities, correct costs, and the stated review assumption. Real reviewers make mistakes. Permissions remain separate deterministic checks.</div></main>'''
    script = r'''
const $=id=>document.getElementById(id), val=id=>Number($(id).value);
function soft(){const z=['z0','z1','z2'].map(val),t=val('temp'),mx=Math.max(...z);const e=z.map(x=>Math.exp((x-mx)/t)),s=e.reduce((a,b)=>a+b,0),p=e.map(x=>x/s);['z0','z1','z2','temp'].forEach(id=>$(id+'out').textContent=val(id).toFixed(1));p.forEach((x,i)=>{$('bar'+i).style.width=(100*x)+'%';$('p'+i).textContent=(100*x).toFixed(1)+'%'});const max=Math.max(...p),w=p.map((x,i)=>Math.abs(x-max)<1e-10?'ABC'[i]:null).filter(Boolean);$('winner').textContent=w.join(' / ')+(w.length>1?' (tie)':'');$('entropy').textContent=(-p.reduce((a,x)=>a+x*Math.log(Math.max(x,1e-300)),0)).toFixed(3);}
function costs(){const p=val('prob'),fp=val('fp'),fn=val('fn'),r=val('review');['prob','fp','fn','review'].forEach(id=>$(id+'out').textContent=val(id).toFixed(2));const c=[(1-p)*fp,p*fn,r],m=Math.min(...c),names=['Act yes','Act no','Review'];$('action').textContent=names.filter((_,i)=>Math.abs(c[i]-m)<1e-10).join(' / ');['yescost','nocost','reviewcost'].forEach((id,i)=>$(id).textContent=c[i].toFixed(3));$('threshold').textContent='Without review, the yes/no boundary is p = '+(fp/(fp+fn)).toFixed(3)+'.';const yMax=Math.max(fp,fn,r,1),X=x=>55+690*x,Y=y=>215-175*y/yMax;let out='<line x1="55" y1="215" x2="745" y2="215" stroke="#526375"/><line x1="55" y1="40" x2="55" y2="215" stroke="#526375"/>';out+='<line x1="55" y1="'+Y(fp)+'" x2="745" y2="215" stroke="#ad5b20" stroke-width="3"/><line x1="55" y1="215" x2="745" y2="'+Y(fn)+'" stroke="#245ea0" stroke-width="3"/><line x1="55" y1="'+Y(r)+'" x2="745" y2="'+Y(r)+'" stroke="#444" stroke-width="2" stroke-dasharray="7 4"/>';out+='<line x1="'+X(p)+'" y1="40" x2="'+X(p)+'" y2="215" stroke="#777" stroke-dasharray="2 4"/>';for(let i=0;i<=4;i++){let x=i/4;out+='<text x="'+X(x)+'" y="237" text-anchor="middle" font-size="12">'+x.toFixed(2)+'</text>';let yy=yMax*i/4;out+='<text x="45" y="'+(Y(yy)+4)+'" text-anchor="end" font-size="12">'+yy.toFixed(1)+'</text>';}out+='<text x="400" y="257" text-anchor="middle" font-size="13">Probability of yes</text><text x="55" y="20" font-size="13">Expected cost (units)</text><text x="360" y="20" fill="#ad5b20" font-size="13">Yes</text><text x="435" y="20" fill="#245ea0" font-size="13">No</text><text x="500" y="20" fill="#444" font-size="13">Review (dashed)</text>';$('plotcontents').innerHTML=out;}
['z0','z1','z2','temp'].forEach(id=>$(id).addEventListener('input',soft));['prob','fp','fn','review'].forEach(id=>$(id).addEventListener('input',costs));$('resetsoft').addEventListener('click',()=>{['.2','1.4','-.3','1'].forEach((v,i)=>$( ['z0','z1','z2','temp'][i]).value=v);soft()});$('resetcost').addEventListener('click',()=>{['.5','4','1','.2'].forEach((v,i)=>$( ['prob','fp','fn','review'][i]).value=v);costs()});soft();costs();
'''
    (SITE/'playground.html').write_text(document('Interactive decision playground',playground,script),encoding='utf-8')
    # Render supporting Markdown with the same notebook exporter, keeping one publication path.
    from nbconvert import HTMLExporter
    for source, target in SUPPORT_PAGES:
        notebook=nbformat.v4.new_notebook(cells=[nbformat.v4.new_markdown_cell((ROOT/source).read_text(encoding='utf-8'))])
        html,_=HTMLExporter().from_notebook_node(notebook)
        html=style_lesson(html,target,[],source_path=source) # Supporting pages have no previous/next lesson.
        (EXPORTS/f'{target}.html').write_text(html,encoding='utf-8')

def rewrite_local_references(html, source_path):
    """Resolve Markdown-relative links before placing the optional export in lessons/."""
    soup = BeautifulSoup(html, 'html.parser')
    # Match GitHub section links and avoid percent-encoded characters in HTML IDs.
    old_ids, seen = {}, {}
    for heading in soup.select('h1[id], h2[id], h3[id], h4[id], h5[id], h6[id]'):
        text = heading.get_text().rstrip('¶').strip().lower()
        base = re.sub(r'[^\w -]', '', text).replace(' ', '-')
        occurrence = seen.get(base, 0)
        seen[base] = occurrence+1
        new_id = base if occurrence == 0 else f'{base}-{occurrence}'
        old_ids[heading['id']] = new_id
        old_ids[unquote(heading['id'])] = new_id
        heading['id'] = new_id
    for anchor in soup.select('a[href^="#"]'):
        fragment = unquote(anchor['href'][1:])
        if fragment in old_ids:
            anchor['href'] = '#'+old_ids[fragment]
    source_dir = (ROOT/source_path).parent
    pages = dict(SUPPORT_PAGES)
    def rewrite_url(value):
        link = urlsplit(value)
        if link.scheme or link.netloc or not link.path:
            return value
        target = (source_dir/unquote(link.path)).resolve()
        if not target.is_relative_to(ROOT):
            return value
        relative = target.relative_to(ROOT).as_posix()
        if target.suffix == '.ipynb' and target.parent == NOTEBOOKS:
            destination = target.stem+'.html'
        elif relative in pages:
            destination = pages[relative]+'.html'
        else:
            destination = Path(os.path.relpath(target, EXPORTS)).as_posix()
        return urlunsplit(('', '', destination, link.query, link.fragment))

    for tag in soup.select('[href], [src], [srcset]'):
        for attribute in ('href', 'src'):
            if tag.has_attr(attribute):
                tag[attribute] = rewrite_url(tag[attribute])
        if tag.has_attr('srcset') and not tag['srcset'].startswith('data:'):
            candidates = []
            for candidate in tag['srcset'].split(','):
                fields = candidate.strip().split()
                if fields:
                    fields[0] = rewrite_url(fields[0])
                    candidates.append(' '.join(fields))
            tag['srcset'] = ', '.join(candidates)
    return str(soup)


def style_lesson(html, stem, names, source_path=None, notebook=None):
    html = rewrite_local_references(html, source_path or 'notebooks/'+stem+'.ipynb')
    html=html.replace('<title>Notebook</title>',f'<title>{escape(stem.replace("_"," "))} · Jev learning lab</title>')
    links='<a href="../index.html">← Course home</a><a href="../playground.html">Playground</a><a href="../practice.html">Practice</a><a href="GLOSSARY.html">Glossary</a>'
    if stem in names:
        index=names.index(stem)
        if index: links+=f'<a href="{names[index-1]}.html">Previous lesson</a>'
        if index<len(names)-1: links+=f'<a href="{names[index+1]}.html">Next lesson →</a>'
        links+=f'<a href="../../notebooks/{stem}.ipynb" download>Notebook ↓</a>'
    css='''<style>
body{background:#f6f8fb!important;color:#182b41!important}.jp-Notebook{max-width:1120px;margin:0 auto;background:white;padding:30px 25px!important}.jp-RenderedHTMLCommon{font-family:system-ui,Segoe UI,sans-serif;font-size:16px!important;line-height:1.75!important}.jp-RenderedHTMLCommon h1{font-size:34px!important;line-height:1.2!important;color:#182b41}.jp-RenderedHTMLCommon h2{color:#0d766f;border-top:1px solid #dde5ee;padding-top:22px}.jp-RenderedHTMLCommon h3{font-size:20px!important}.jp-RenderedHTMLCommon table{font-size:14px!important;line-height:1.5!important}.jp-InputArea-editor{border-radius:7px;background:#f4f6f9!important}.jp-InputArea pre{font-size:13px!important;white-space:pre-wrap!important;overflow-wrap:anywhere}.jp-RenderedImage img{max-width:100%;height:auto}.course-nav{max-width:1120px;margin:auto;display:flex;flex-wrap:wrap;gap:20px;padding:20px 28px;font:14px system-ui}.course-nav a{color:#0d766f;text-decoration:none;font-weight:650}.jp-OutputArea-output{overflow-x:auto}.jp-Cell{margin-bottom:15px!important}@media(max-width:650px){.jp-Notebook{padding:20px 8px!important}.jp-RenderedHTMLCommon{font-size:15px!important}.jp-RenderedHTMLCommon h1{font-size:27px!important}.jp-InputPrompt,.jp-OutputPrompt{min-width:34px!important;width:34px!important}}
</style>'''
    html=html.replace('</head>',css+'</head>')
    html=re.sub(r'(<body[^>]*>)',r'\1<nav class="course-nav">'+links+'</nav>',html,count=1)
    descriptions = {}
    if notebook is not None:
        for cell in notebook.cells:
            for output in cell.get('outputs', []):
                if 'image/png' in output.get('data', {}):
                    alt = output.get('metadata', {}).get('alt') or output.metadata.get('image/png', {}).get('alt')
                    if alt:
                        descriptions[output.data['image/png']] = alt
    return reader_view(html, stem in names, descriptions)

if __name__=='__main__':
    build_site()
