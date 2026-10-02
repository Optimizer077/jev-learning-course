"""Public course landing page and progressively enhanced notebook reading view."""
from html import escape
from bs4 import BeautifulSoup


def homepage(lessons):
    # Map labels by lesson ID so a new lesson cannot disappear through zip truncation.
    tracks = {'00': 'START HERE', '01': 'BEGINNER', '02': 'BUILD WITH PYTHON',
              '03': 'PROBABILITY', '04': 'BEGINNER', '05': 'OPTIONAL API',
              '06': 'ADVANCED', '07': 'PROJECT', '08': 'PRACTICE',
              '09': 'COMPARE', '10': 'OPTIONAL PYTORCH'}
    lesson_count = len(lessons)
    cards = ''.join(
        f'<article class="card"><div class="number">{name[:2]} / {tracks.get(name[:2], "LEARNING LAB")}</div>'
        f'<h3>{escape(title)}</h3><p>{escape(description)}</p><div class="actions">'
        f'<a href="lessons/{name}.html" aria-label="Read lesson {name[:2]}: {escape(title, quote=True)}">Read lesson →</a>'
        f'<a href="../notebooks/{name}.ipynb" download aria-label="Download notebook {name[:2]}: {escape(title, quote=True)}">Notebook ↓</a>'
        f'<a href="https://colab.research.google.com/github/Optimizer077/jev-learning-course/blob/main/notebooks/{name}.ipynb" '
        f'aria-label="Run lesson {name[:2]} in Colab: {escape(title, quote=True)}">Run in Colab ↗</a></div></article>'
        for name, title, description in lessons
    )
    return '''<style>
:root{--warm:#6245b7}
.skip-link{position:fixed;top:8px;left:8px;z-index:1000;background:#13243b;color:white;
padding:12px 18px;border-radius:6px;transform:translateY(-180%)}
.skip-link:focus{transform:translateY(0);outline:3px solid #70e0d1;outline-offset:3px}
.course-home .grid>*{min-width:0}.course-home .card .actions{flex-direction:column;gap:4px;
border-top:1px solid #d9e2f0;padding-top:10px}.course-home .card .actions a{display:flex;
align-items:center;min-height:44px}.course-home .button{min-height:44px}
.course-home .learning-loop{display:flex;flex-wrap:wrap;gap:8px;list-style:none;padding:0;
margin:22px 0 0}.course-home .learning-loop li{border:1px solid #425670;border-radius:8px;
padding:8px 12px;color:#e1e9f4;font-size:14px}.course-home .learning-loop strong{color:#70e0d1}
nav[aria-label="Course navigation"] a{display:inline-flex;align-items:center;min-height:44px}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{scroll-behavior:auto!important;
transition:none!important;animation:none!important}}
</style><a class="skip-link" href="#course-content">Skip to course content</a>
<nav aria-label="Course navigation"><strong>LEARN JEV</strong>
<a href="playground.html">Playground</a><a href="practice.html">Guided practice</a><a href="lessons/SETUP.html">Setup help</a>
<a href="lessons/VISUAL_GUIDE.html">Visual guide</a><a href="lessons/GLOSSARY.html">Glossary</a><a href="lessons/FAQ.html">FAQ</a></nav><main class="course-home" id="course-content" tabindex="-1"><section class="course-hero">
<div class="eyebrow">An independent, practical introduction</div>
<h1>Learn Jev,<br>one decision at a time.</h1>
<p class="lead">How does a model turn evidence into a decision your software can use?
Start with a support message. Follow the example. Try changing one thing.</p>
<div class="chips"><span class="chip">Beginner path: no coding needed</span>
<span class="chip">Saved results included</span><span class="chip">No account needed to start</span></div>
<div class="actions"><a class="button" href="lessons/00_start_here.html">Start here →</a>
<a class="button" style="background:white;color:var(--blue);border:1px solid var(--line)" href="playground.html">Try the playground</a></div>
<ol class="learning-loop" aria-label="A useful routine for every lesson">
<li><strong>1.</strong> Read one example</li><li><strong>2.</strong> Predict a change</li>
<li><strong>3.</strong> Run or inspect results</li><li><strong>4.</strong> Explain why</li></ol></section>
<section class="section panel"><div class="eyebrow">The idea in one minute</div>
<h2 style="margin-top:12px">The model estimates. Your program decides.</h2>
<p>A customer writes: <strong>“The export button crashes. I cannot finish my report.”</strong>
Which team should help: technical, billing, or another team?</p>
<div class="grid"><div><h3>1. Give the evidence</h3><p>Provide the message and a focused question.</p></div>
<div><h3>2. Estimate an answer</h3><p>The model returns a typed result, such as probabilities over allowed queues.</p></div>
<div><h3>3. Apply your rule</h3><p>Your code routes the message or asks for review. A valid answer can still be wrong.</p></div></div>
<p class="small">Jev is TypeSafe AI's model for bounded judgments. The local examples in this course are teaching models;
they do not reproduce Jev. <a href="lessons/SOURCES.html">Read the evidence and limits</a>.</p></section>
<section class="section"><h2>Choose the path that fits you</h2>
<picture><source media="(max-width:650px)" srcset="../assets/learning-path-mobile.svg">
<img class="path-art" src="../assets/learning-path.svg" alt="Understand: 00, 01, 04. Experiment: 02, 03 after 01. Build: 07, 09 after 02 and 03; add optional 10 for PyTorch training."></picture><div class="grid">
<article class="card"><div class="number">FIRST / UNDERSTAND</div><h3>Just the main idea</h3>
<p>Read 00 → 01 → 04. Skip code and equations on your first pass. Explain the distinction between a prediction and an action.</p>
<a href="lessons/00_start_here.html">Begin without installation →</a><p class="small"><a href="lessons/LEARNING_GUIDE.html">Follow the short learning plan</a></p></article>
<article class="card"><div class="number">NEXT / EXPERIMENT</div><h3>Change the numbers</h3>
<p>Try the playground, then lesson 03. Watch probabilities and review decisions change as you move a slider.</p>
<a href="playground.html">Make a prediction, then try it →</a></article>
<article class="card"><div class="number">THEN / BUILD</div><h3>Run a small project</h3>
<p>Follow 02 → 03 → 07. Train a local text router, evaluate it, and inspect the mistakes. Basic Python helps.</p>
<a href="lessons/SETUP.html">Set up Python →</a></article></div></section>
<section class="section two"><div class="panel"><h2>Compare related approaches</h2>
<p>Try rules, weighted word matching, and a learned classifier on the same messages.
Then inspect a pair they cannot distinguish.</p><a href="lessons/09_related_models_lab.html">Open the optional comparison lab →</a>
<p class="small"><a href="lessons/MODEL_GUIDE.html">Read the model guide</a></p></div>
<div class="panel"><h2>A reference while you learn</h2><p>Keep question types, worked calculations,
decision costs, and common confusions on one page beside your notebook.</p>
<a href="lessons/QUICK_REFERENCE.html">Open the quick reference →</a></div></section>
<section class="section panel"><div class="eyebrow">Optional next step · after 07 and 09</div>
<h2>Train small models with PyTorch</h2><p>Compare six models on a fictional text task.
Follow the training curves, compare held-out mistakes, and test whether changing word order changes the prediction.
You can read the saved results first; a CPU is enough to run the experiment.</p>
<a href="lessons/10_pytorch_models_lab.html">Open the PyTorch training lab →</a>
<p class="small">This lab trains educational models. It does not train Jev or reveal its private architecture.</p></section>
<section class="section" id="lesson-catalogue"><h2>All '''+str(lesson_count)+''' lessons</h2><p>You do not need to finish them in order.
Each lesson tells you what to know first and includes a short self-check.
The API and PyTorch labs are optional.</p><div class="grid">'''+cards+'''</div></section>
<section class="section two"><div class="panel"><h2>Read first. Run later.</h2>
<p>The browser lessons show explanations and saved results. Select <strong>Show Python code</strong>
when you want to see the implementation. Download the whole folder to keep the notebooks and helpers together.</p>
<a href="lessons/SETUP.html">Windows, macOS, and Linux setup →</a></div>
<div class="panel"><h2>Pause and explain</h2><p>Predict a small change before you run it.
Use the self-check before opening its answer. Understanding means explaining why, not just rerunning code.</p>
<a href="practice.html">Try 12 guided questions →</a><p><a href="lessons/08_exercises_and_solutions.html">Continue with runnable exercises</a></p></div></section>
<div class="note">Independent educational resource; not an official TypeSafe course.
All local data and model results are teaching examples. The optional live API call is disabled by default.</div>
<p class="small">Documentation checked 2026-10-01 · <a href="lessons/SOURCES.html">Sources</a> ·
<a href="lessons/data_README.html">Data provenance</a> · <a href="lessons/SHARING.html">Maintainer guide</a></p></main>'''


def reader_view(html, is_lesson, image_descriptions=None):
    """Keep saved output visible; reveal code with a keyboard-accessible control."""
    soup = BeautifulSoup(html, 'html.parser')
    soup.html['lang'] = 'en'
    extra = soup.new_tag('style')
    extra.string = '''
.reader-tools{max-width:1120px;margin:0 auto;padding:16px 28px;background:#eaf0f7;
font:15px/1.55 system-ui,Segoe UI,sans-serif;color:#182b41}
.reader-tools p{margin:6px 0}.reader-tools label{font-weight:650;cursor:pointer;
display:inline-flex;align-items:center;min-height:44px}
.reader-tools input{accent-color:#0d766f;margin-right:8px}
.reader-tools details{margin-top:12px}.reader-tools summary{cursor:pointer;font-weight:650;
min-height:44px;padding:10px 0}
.reader-tools ul{padding-left:22px;columns:2;column-gap:30px}.reader-tools li{break-inside:avoid;margin:5px 0}
.reader-tools a{color:#0d766f}.reading-mode .jp-CodeCell .jp-InputArea,.reading-mode .jp-InputPrompt,
.reading-mode .jp-OutputPrompt,.reading-mode .jp-CodeCell.jp-mod-noOutputs{display:none!important}
.lesson-skip-link{position:fixed;top:8px;left:8px;z-index:1000;padding:12px 18px;
background:#13243b;color:white;border-radius:6px;transform:translateY(-180%)}
.lesson-skip-link:focus{transform:translateY(0);outline:3px solid #70e0d1;outline-offset:3px}
.jp-RenderedImage img,.jp-RenderedHTMLCommon img{max-width:100%;height:auto}
.jp-RenderedHTMLCommon details{background:#f0f5fb;border:1px solid #d9e2eb;border-radius:8px;padding:12px 16px;margin:16px 0}
.jp-RenderedHTMLCommon summary{cursor:pointer;font-weight:650;color:#0d766f}
.jp-RenderedHTMLCommon blockquote{border-left:3px solid #ad5b20!important;background:#fff8f1;padding:8px 18px!important}
.jp-RenderedHTMLCommon a:focus-visible,summary:focus-visible,input:focus-visible{outline:3px solid #ad5b20;outline-offset:3px}
.jp-RenderedHTMLCommon{overflow-wrap:anywhere}.jp-RenderedHTMLCommon pre{white-space:pre-wrap}
@media(max-width:650px){.reader-tools{padding:16px 20px}.reader-tools ul{columns:1}
.jp-InputPrompt,.jp-OutputPrompt{display:none!important}.jp-RenderedHTMLCommon table{display:block;overflow-x:auto}}
@media print{.course-nav,.reader-tools,.lesson-skip-link{display:none!important}.jp-Notebook{max-width:none}}
'''
    soup.head.append(extra)
    content = soup.select_one('.jp-Notebook') or soup.find('main')
    if content:
        content['id'] = 'lesson-content'
        content['tabindex'] = '-1'
        if content.name != 'main':
            content['role'] = 'main'
        skip = soup.new_tag('a', href='#lesson-content')
        skip['class'] = 'lesson-skip-link'
        skip.string = 'Skip to lesson content'
        soup.body.insert(0, skip)
    nav = soup.select_one('.course-nav')
    if nav:
        nav['aria-label'] = 'Course and lesson navigation'
    if not is_lesson:
        return str(soup)
    headings = soup.select('.jp-RenderedHTMLCommon h2[id]')
    outline = ''.join(f'<li><a href="#{escape(h["id"], quote=True)}">'
                      f'{escape(h.get_text().rstrip("¶"))}</a></li>' for h in headings)
    tools = BeautifulSoup('''<section class="reader-tools" aria-label="Reading controls">
<label><input type="checkbox" id="show-code" aria-controls="lesson-content" disabled>Show Python code</label>
<p>Reading mode keeps the saved results visible. Open the notebook in Jupyter to run or change code.</p>
<noscript><p>Python code stays visible when JavaScript is unavailable. You can still read all explanations and saved results.</p></noscript>
<details><summary>In this lesson</summary><ul>'''+outline+'</ul></details></section>', 'html.parser')
    if nav:
        nav.insert_after(tools)
    else:
        soup.body.insert(1 if content else 0, tools)
    script = soup.new_tag('script')
    script.string = '''const codeToggle=document.getElementById('show-code');
codeToggle.disabled=false;document.body.classList.add('reading-mode');
codeToggle.addEventListener('change',function(){
document.body.classList.toggle('reading-mode',!this.checked);});'''
    soup.body.append(script)
    # The preceding prose provides context for saved figures; expose that context to assistive readers.
    for img in soup.select('.jp-RenderedImage img'):
        encoded = img.get('src', '').removeprefix('data:image/png;base64,')
        if image_descriptions and encoded in image_descriptions:
            img['alt'] = image_descriptions[encoded]
        existing_alt = img.get('alt', '').strip()
        if existing_alt and 'no description' not in existing_alt.lower():
            continue
        cell = img.find_parent(class_='jp-Cell')
        heading = cell.find_previous(['h2', 'h3']) if cell else None
        if heading:
            img['alt'] = 'Figure for '+heading.get_text().rstrip('¶')+'. Interpretation follows in the lesson.'
    return str(soup)
