"""Build offline guided practice plus a printable Markdown companion."""
import json
from html import escape
from practice_questions import QUESTIONS


def build_practice(root, document):
    body = '''<nav aria-label="Practice navigation"><a href="index.html">← Course home</a>
<a href="html/00_start_here.html">Start here</a><a href="playground.html">Playground</a>
<a href="html/PRACTICE.html">Printable questions</a></nav><main style="max-width:920px">
<div class="eyebrow">Guided practice · 12 small decisions</div><h1>Predict.<br>Check. Explain.</h1>
<p class="lead">Choose an answer, read why, and connect it to a lesson. All messages and numbers are teaching examples.</p>
<p class="small">No installation or API calls. This page keeps answers only while it is open; refreshing starts over.</p>
<noscript><p>JavaScript is disabled. <a href="html/PRACTICE.html">Use the printable questions and explanations</a>.</p></noscript>
<section id="practice" class="panel section" hidden>
<p id="position" class="small"></p><progress id="progress" max="12" value="1" aria-label="Question position" style="width:100%;accent-color:var(--blue)"></progress>
<p id="stage" class="eyebrow" style="margin-top:24px"></p><h2 id="question" tabindex="-1"></h2>
<form id="answer-form"><fieldset style="border:0;margin:0;padding:0" aria-labelledby="question">
<legend style="font-weight:650;margin-bottom:10px">Choose one answer</legend><div id="options"></div></fieldset>
<button class="button" id="check" type="submit" style="margin-top:20px">Check my answer</button></form>
<details style="margin-top:22px"><summary>Need a hint?</summary><p id="hint"></p></details>
<section id="feedback" role="status" aria-live="polite" class="note" hidden></section>
<p><a id="review-link"></a></p>
<div class="actions" style="justify-content:space-between;margin-top:28px">
<button id="back" type="button">Previous</button><button id="next" type="button" disabled>Next question →</button></div></section>
<section id="finished" class="panel section" hidden><h2 tabindex="-1" id="finished-title">You have reviewed all 12 prompts.</h2>
<p>Now explain one answer without looking, then change a number in the playground and predict the result.
If an idea felt difficult, revisit its linked lesson before moving on.</p>
<div id="review-list"></div><div class="actions" style="margin-top:24px"><button id="restart" type="button">Practice again</button>
<a href="html/08_exercises_and_solutions.html">Continue with notebook exercises →</a></div></section></main>'''
    script = 'const questions = '+json.dumps(QUESTIONS, ensure_ascii=False).replace('</','<\\/')+';\n'+r'''
const $=id=>document.getElementById(id), answers=Array(questions.length).fill(null);
let current=0;
function render(){
 const q=questions[current],saved=answers[current];
 $('practice').hidden=false;$('finished').hidden=true;
 $('position').textContent='Question '+(current+1)+' of '+questions.length;
 $('progress').value=current+1;$('stage').textContent=q.stage;$('question').textContent=q.question;
 $('hint').textContent=q.hint;$('options').replaceChildren();
 q.options.forEach((text,i)=>{
  const label=document.createElement('label');
  label.style.cssText='display:flex;align-items:flex-start;gap:12px;padding:14px 16px;margin:10px 0;border:1px solid #d9e2eb;border-radius:8px;cursor:pointer';
  const input=document.createElement('input');input.type='radio';input.name='answer';input.value=i;input.required=true;
  input.style.cssText='margin-top:6px;accent-color:#245ea0';input.disabled=saved!==null;input.checked=saved===i;
  const span=document.createElement('span');span.textContent=text;label.append(input,span);$('options').append(label);
 });
 $('check').disabled=saved!==null;$('check').hidden=saved!==null;$('next').disabled=saved===null;
 $('next').textContent=current===questions.length-1?'Finish practice →':'Next question →';$('back').disabled=current===0;
 $('review-link').textContent='Read '+q.lesson_title+' →';$('review-link').href='html/'+q.lesson+'.html';
 $('feedback').hidden=saved===null;
 if(saved!==null){
  const title=document.createElement('strong');title.textContent=saved===q.correct?'That is right.':'Here is the distinction to notice.';
  const why=document.createElement('p');why.textContent=(q.feedback[saved]?q.feedback[saved]+' ':'')+q.explanation;
  const answer=document.createElement('p');answer.textContent='Answer: '+q.options[q.correct];
  $('feedback').replaceChildren(title,why,answer);
 }
}
$('answer-form').addEventListener('submit',event=>{
 event.preventDefault();const selected=document.querySelector('input[name="answer"]:checked');
 if(!selected)return;answers[current]=Number(selected.value);render();$('feedback').tabIndex=-1;$('feedback').focus();
});
$('back').addEventListener('click',()=>{if(current>0){current--;render();$('question').focus();}});
$('next').addEventListener('click',()=>{
 if(answers[current]===null)return;
 if(current<questions.length-1){current++;render();$('question').focus();return;}
 $('practice').hidden=true;$('finished').hidden=false;$('review-list').replaceChildren();
 const missed=questions.filter((q,i)=>answers[i]!==q.correct),unique=new Map(missed.map(q=>[q.lesson,q.lesson_title]));
 const p=document.createElement('p');p.textContent=missed.length?'Revisit the ideas that were tricky on your first attempt:':'For a next step, try the text-routing project and inspect its word-order failure.';$('review-list').append(p);
 const ul=document.createElement('ul');
 (unique.size?unique:new Map([['07_text_routing_capstone','07 · Text-routing project']])).forEach((title,lesson)=>{
  const li=document.createElement('li'),a=document.createElement('a');a.textContent=title;a.href='html/'+lesson+'.html';li.append(a);ul.append(li);
 });$('review-list').append(ul);$('finished-title').focus();
});
$('restart').addEventListener('click',()=>{answers.fill(null);current=0;render();$('question').focus();});
render();
'''
    (root/'practice.html').write_text(document('Guided practice · Learn Jev',body,script),encoding='utf-8')
    blocks = ['# Guided practice: predict, check, explain\n\n'
              'Try each question before opening the explanation. All numbers and messages are teaching examples.\n\n'
              '[Course home](README.md) · [Course outline](COURSE.md)\n\n'
              'For the optional interactive copy, download the course and open `practice.html` locally. '
              'The questions below work directly in GitHub’s Markdown viewer.\n\n'
              'The three sections move from the interface to probabilities and then to building a system. '
              'You can use this page for individual study or print it for a group.']
    for i,q in enumerate(QUESTIONS,1):
        blocks.append(f'## {i}. {q["stage"]}\n\n{q["question"]}\n\n'+
                      '\n'.join(f'- **{chr(65+j)}.** {text}' for j,text in enumerate(q['options']))+
                      f'\n\n<details><summary>Hint</summary><p>{escape(q["hint"])}</p></details>\n\n'
                      f'<details><summary>Answer and explanation</summary><p><strong>{chr(65+q["correct"])}.</strong> '
                      f'{escape(q["explanation"])}</p></details>\n\n'
                      f'[Review {q["lesson_title"]}]({q["lesson"]}.ipynb)')
    (root/'PRACTICE.md').write_text('\n\n'.join(blocks)+'\n',encoding='utf-8')
