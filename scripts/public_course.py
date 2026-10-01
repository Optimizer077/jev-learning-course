"""Reader-facing teaching scaffolding, kept separate from computational examples."""
from textwrap import dedent
import hashlib

GUIDES = {
 '00': ('Start here', 'No Python or machine learning background needed',
        'You can learn the main idea by reading the saved examples. Running code comes later.',
        'Read the welcome and try the small example. Then open lesson 01.',
        'You know where to start and which lessons you can skip for now.',
        ('Do I need an API key to begin?', 'No. All reading, plots, and local experiments work without one. The optional live call is in lesson 05.')),
 '01': ('Beginner', 'No machine learning background; basic Python only if you run cells',
        'Imagine sorting support messages into queues. The model estimates which queue fits. Your program decides whether to use that estimate or ask for review.',
        'Read sections 1–5 first. The later sections add useful distinctions, but you can return to them.',
        'You can explain Choice, Score, and Noul in your own words, and why a valid answer can still be wrong.',
        ('A model returns billing, one of the allowed options. Does that prove the ticket is about billing?',
         'No. The value has the right shape, but the judgment can still be wrong. Output validity and accuracy answer different questions.')),
 '02': ('Optional math', 'Basic Python; lesson 01; matrix multiplication is explained here',
        'Training changes a table of numbers so examples receive better scores. We normalize those scores into probabilities, then choose the largest.',
        'Follow sections 1–4 for the main idea. Decision regions and the gradient check are optional deeper work.',
        'You can trace features → scores → probabilities → choice without claiming that this toy is Jev.',
        ('If I make probabilities more extreme, have I made the model more accurate?',
         'Not necessarily. Multiplying all logits by a positive constant keeps the winning class unchanged. It can change probability quality without changing classification accuracy.')),
 '03': ('Applied probability', 'Lesson 01; percentages; basic Python for the experiments',
        'When a model says 80%, compare many such predictions with what really happened. Then choose actions using the cost of mistakes, not certainty alone.',
        'Sections 1–4 are the core lesson. Temperature fitting, bootstrap intervals, and review costs are optional extensions.',
        'You can distinguish accuracy from calibration and explain why a threshold depends on the task.',
        ('A well-calibrated model predicts yes with probability 0.8. Must this case be yes?',
         'No. Calibration is a pattern across many predictions. Roughly one in five comparable 0.8 predictions should be negative.')),
 '04': ('Beginner → builder', 'Lesson 01; understand an if statement',
        'Let the model make a small judgment. Let ordinary code combine judgments, check permissions, and choose the next step.',
        'Work through the four fictional tickets. Then read the question rewrites and dependency example.',
        'You can decide which work belongs to the model and which rules belong in code.',
        ('Two questions run in parallel. Can I multiply their probabilities to get the probability that both are true?',
         'Only if statistical independence is justified. Running calculations together does not make the events independent.')),
 '05': ('Optional integration', 'Lesson 01; Python dictionaries; an API key only for the live call',
        'An API is a way for your program to ask another service for a result. First inspect the request and response locally; enable the real request only when you want it.',
        'Keep RUN_LIVE = False on your first pass. The long validator is reference code: understand its purpose before every line.',
        'You can identify exactly what gets sent and tell a handmade fixture from a real model result.',
        ('The local response validator passes. Did we establish that Jev answered correctly?',
         'No. In offline mode it checked a handmade fixture. Even a valid live response would establish structure, not semantic correctness.')),
 '06': ('Optional advanced lab', 'Lesson 02; matrix multiplication and softmax',
        'Several different mechanisms can produce bounded decisions. We experiment with generic candidate scoring and attention to understand the possibilities, not to reveal Jev’s unpublished design.',
        'Read each diagram and its explanation before the code. The loss derivation is optional.',
        'You can describe the attention-mask experiment and state what it does not tell us about Jev.',
        ('Our attention demo keeps questions separate. Does that prove Jev uses this mask?',
         'No. The experiment proves a property of our constructed example. A similar external behavior can be implemented in different ways.')),
 '07': ('Practical project', 'Lessons 02 and 03; lists, dictionaries, and arrays',
        'Build one small system from start to finish. Learn from labeled examples, choose a policy on separate examples, then inspect fresh cases and failure modes.',
        'Follow the fixed split. Read the failure pair even if you skip the implementation details.',
        'You can explain why a perfect score on twelve easy examples is not evidence of broad language understanding.',
        ('Why not adjust the threshold after looking at test mistakes?',
         'That would turn the test set into tuning data. Choose on validation data and reserve a fresh test set for judging the frozen system.')),
 '08': ('Practice and review', 'Attempt the matching exercise before opening its answer',
        'A useful explanation lets you predict what will happen when something changes. These worked answers check that skill.',
        'Read only the solution you need. Return to the originating lesson after checking it.',
        'You can justify an answer, not just reproduce a number.',
        ('I can rerun every cell. Does that mean I understand the course?',
         'A stronger check is to predict a small change, explain why it happens, and name one limitation of the experiment.')),
 '09': ('Optional comparison lab', 'Lesson 07; basic arrays; lexical matching is explained here',
        'Different mechanisms can return the same label while using different information. Compare their behavior on fixed examples, then inspect the cases where the representation fails.',
        'Read the mechanism table and the comparison counts first. Return to the implementation when ready.',
        'You can distinguish rules, similarities, and probabilities, and explain why the local comparison says little about a model family as a whole.',
        ('A cosine similarity is 0.80. Does that mean the selected queue has an 80% probability of being correct?',
         'No. Similarity measures how closely two vectors align. A probability interpretation requires a suitable probabilistic model and evaluation; the number alone does not provide it.')),
}

RECAPS = {
 '01': ['Choice compares named options; Score averages ordered levels; Noul answers a yes/no question with a probability.',
        'The application owns the threshold and the action.', 'Type safety prevents some format errors; it does not guarantee truth.'],
 '02': ['A matrix of weights maps features to scores. Softmax converts scores to a distribution.',
        'Learning changes the weights to reduce loss.', 'A confident prediction can still be wrong or outside the training distribution.'],
 '03': ['Accuracy measures correct labels; calibration compares probabilities with observed frequencies.',
        'Fit adjustments on separate data and check the result on held-out cases.', 'Review and mistake costs change which action is best.'],
 '04': ['Ask focused questions with clear criteria.', 'Use code for arithmetic, permissions, and combining results.',
        'Dependent stages need the right evidence before they can run.'],
 '05': ['A request contains the model ID, state, and typed questions.',
        'Local fixtures, valid responses, and correct judgments are three different things.', 'A successful request is the start of evaluation.'],
 '06': ['Candidate descriptions can be inputs to a scorer; a fixed classifier head works differently.',
        'Masks govern information flow; scheduling governs parallel execution.', 'The demonstrated mechanisms do not reproduce Jev or RLCD.'],
 '07': ['Fit on training, choose settings on validation, and assess the frozen system on test.',
        'Always report denominators and inspect individual failures.', 'A representation that drops word order cannot resolve every change in meaning.'],
 '08': ['Predict, run, explain, and state a limitation.', 'Keep output validity, accuracy, calibration, and authorization distinct.',
        'Use the smallest model and workflow that you can evaluate for your task.'],
 '09': ['Hold the task, examples, and label definitions fixed when comparing methods.',
        'A similarity score and a normalized probability have different meanings.',
        'If a representation drops the information needed to distinguish cases, a later decision rule cannot restore it.'],
}

WORDS = {
 '01': [('State', 'The evidence you give the model.'), ('Criteria', 'What each possible answer means.'),
        ('Distribution', 'The probability assigned to every option.'), ('Policy', 'Your program’s rule for choosing an action.')],
 '02': [('Feature', 'A number the model uses as an input.'), ('Weight', 'A learned number that changes an input’s contribution.'),
        ('Logit', 'A score before it becomes a probability.'), ('Loss', 'A penalty for a poor prediction.')],
 '03': [('Calibration', 'Whether stated probabilities match outcome frequencies across many cases.'),
        ('Coverage', 'The fraction of cases the policy handles automatically.'),
        ('Review', 'An alternative action for cases that should not be automated.')],
 '04': [('Workflow', 'The sequence of judgments and actions in a program.'),
        ('Permission', 'Whether the program is allowed to perform an action.'),
        ('Dependency', 'Information one step must receive from another step.')],
 '05': [('API', 'A way for programs to ask a service for a result.'), ('Request', 'The information sent to that service.'),
        ('Fixture', 'A handmade example used to check code locally.')],
 '06': [('Representation', 'The numbers used to describe an input.'), ('Attention', 'A calculation that combines information from positions in an input.'),
        ('Mask', 'A rule specifying which positions can read which others.')],
 '07': [('Training split', 'Examples used to learn weights.'), ('Validation split', 'Separate examples used to choose settings.'),
        ('Test split', 'Fresh examples used to assess the frozen system.')],
 '09': [('Prototype', 'A representative vector built from examples in a class.'),
        ('Cosine similarity', 'How closely the directions of two numerical vectors align.'),
        ('Abstention', 'Choosing review instead of an automatic answer.')],
}

def welcome(md, code):
    return [md(r'''
# Start here · Learn Jev one decision at a time

This is an **independent learning resource**, not official TypeSafe documentation.
You do not need to know machine learning to start. The first path uses ordinary language and small examples.

## The idea in one minute
Imagine this support message: **“The export button crashes. I cannot finish my report.”**
We want to decide which team should help. A decision model can estimate how well each allowed queue
fits the message. Our software then chooses a queue or asks someone to review the case.

Jev is TypeSafe AI's model for this kind of bounded judgment. It accepts state and typed questions.
Its output is designed for software to use. [Official introduction](https://docs.typesafe.ai/introduction).

## Try one decision — no model call
The probabilities below are invented for teaching. “0.90” means 90%. Our example rule uses a
threshold of 0.85. Before running, predict whether the message will be routed or reviewed.
'''), code('''
probabilities = {'technical': 0.90, 'billing': 0.06, 'other': 0.04}
best_queue = max(probabilities, key=probabilities.get)
threshold = 0.85  # Teaching choice, not a recommended production setting.
action = best_queue if probabilities[best_queue] >= threshold else 'review'
print('Most likely queue:', best_queue)
print('What our program does:', action)
'''), md(r'''
**What you should see:** `technical` for both lines. The model estimate and the software rule are
separate steps. Changing the threshold to 0.95 changes the action to `review`, while the most likely
queue stays `technical`. A real model's prediction can still be wrong.

## Choose your starting path

| You want to… | Start with… | What you can skip at first |
|---|---|---|
| Understand the idea without coding | [01 · Basics](01_jev_basics.ipynb) → [04 · Workflows](04_workflows_and_related_models.ipynb) | All code and equations |
| Try changing numbers | [Interactive playground](playground.html) → [03 · Calibration](03_calibration_and_decisions.ipynb) | The optional math extensions |
| Learn how a small model is trained | [02 · From scratch](02_decision_model_from_scratch.ipynb) | Lesson 06 until later |
| Build a complete local project | 02 → 03 → [07 · Text routing](07_text_routing_capstone.ipynb) | The live API lesson |
| Call real Jev | 01 → [05 · Optional API](05_optional_real_jev_api.ipynb) | The architecture lab |

The lesson numbers are reference labels, not a requirement to finish every lesson in sequence.
There are ten notebooks, including this welcome, the [worked solutions](08_exercises_and_solutions.ipynb),
and an optional [related-models lab](09_related_models_lab.ipynb).

## Read first; run when ready
You have four ways to use the course:

1. **Read on GitHub.** Start at [README.md](README.md), then follow the lesson links.
   The notebooks include saved explanations, charts, and results. Use [the course outline](COURSE.md) for checkpoints.
2. **Run in Colab.** Use the **Open in Colab** button above, then choose **Runtime → Run all**.
   The first cell fetches the included course helpers and fictional data. A CPU runtime is sufficient.
3. **Run locally.** Follow [SETUP.md](SETUP.md), open the whole extracted folder in JupyterLab,
   and choose **Restart Kernel and Run All**. No API key or GPU is needed for the local lessons.
4. **Use an optional browser copy.** After downloading the folder, open `site/index.html` locally.
   Its reading mode hides code while keeping saved results. GitHub itself displays HTML files as source.

### What is a notebook cell?
A notebook alternates between explanations and runnable pieces of Python called **cells**.
Select a code cell and press **Shift+Enter** to run it. Its result appears below.
Run from top to bottom because later cells may use names created earlier.
If a result looks stale after editing, restart the kernel (the Python session) and run all cells again.

## How to study a lesson
**Read → predict → run or inspect → explain.** Begin with the plain-language idea, predict one small
change, inspect the result, and explain what happened in one sentence. Use “Check your understanding”
before reading its answer. Optional deep dives can wait.

## Three labels that keep the course honest

| Label | Meaning |
|---|---|
| **Documented Jev behavior** | A statement linked to TypeSafe's public documentation |
| **General ML mechanism** | A small example of a method used in machine learning; not a Jev implementation |
| **Teaching data** | Invented examples, probabilities, or costs; not measured Jev results |

The detailed Jev architecture and RLCD training recipe are not supplied by the public pages reviewed.
We explain useful mechanisms without filling those gaps with guesses. The only real API call is
disabled by default in lesson 05. [Sources](SOURCES.md).

## A tiny Python reading guide

| You see… | Read it as… |
|---|---|
| `x = 0.8` | Store the value 0.8 under the name x |
| `{'yes': 0.8, 'no': 0.2}` | A dictionary: named values |
| `[0.8, 0.2]` | A list of values in order |
| `if p >= 0.8:` | Run the next indented lines when p is at least 0.8 |
| `assert condition` | Check that an expected property holds; stop if it does not |
| `np.array(...)` | A NumPy array for numerical calculations |

## Ready for lesson 01?
You are ready if you can say: **“The model estimates. The program chooses what to do.”**
You do not need to understand matrices, attention, or training yet.

[Open lesson 01 · The basics](01_jev_basics.ipynb).

Try the [practice questions](PRACTICE.md) after lesson 01, or use the
[learning plan](LEARNING_GUIDE.md) to organize several short sessions.
''')]

def prepare_public(name, cells, md, code):
    number = name[:2]
    if number == '00':
        cells = welcome(md, code)
    cells = [c for c in cells if not(c.cell_type == 'markdown' and c.source.startswith('**Study guide:**'))]
    track, prereq, intuition, route, done, (question, answer) = GUIDES[number]
    # Make the reader guide visible before the original introduction, not after Setup.
    first = cells[0].source
    title, remainder = first.split('\n', 1)
    header = md(f'{title}\n\n**Path:** {track}  \n**Before you start:** {prereq}\n\n'
                '[Course home](README.md) · [Course outline](COURSE.md) · [Setup help](SETUP.md) · [Glossary](GLOSSARY.md)')
    lead = md(f'## The idea before the code\n\n{intuition}\n\n**Your first pass:** {route}')
    cells = [header] + ([lead] if number != '00' else []) + [md(remainder)] + cells[1:]

    if number in WORDS:
        terms = '\n'.join(f'| **{term}** | {meaning} |' for term,meaning in WORDS[number])
        cells.insert(2,md('### Words you need for this lesson\n\n| Word | Everyday meaning |\n|---|---|\n'+terms))

    if number == '01':
        cells.insert(3,md('''### One message, three different questions

Our running message is **“The export button crashes. I cannot finish my report.”**
Changing the question changes what the answer should describe.

| What do you need to know? | Type | How to read the result |
|---|---|---|
| Which queue best fits: technical, billing, or other? | **Choice** | A selected queue and probabilities over the queues |
| How much is work disrupted on a 0–2 rubric? | **Score** | An expected level on an ordered scale |
| Is a refund explicitly requested? | **Noul** | A probability for yes |

The question types are documented in the official [Choice](https://docs.typesafe.ai/primitives/choice),
[Score](https://docs.typesafe.ai/primitives/score), and [Noul](https://docs.typesafe.ai/primitives/noul) pages.
The probabilities shown later in this notebook are invented examples.
'''))

    if number == '02':
        idx = next(i for i,c in enumerate(cells) if c.cell_type=='markdown' and '## Steps' in c.source)
        cells[idx:idx] = [md('''## Begin with numbers you can calculate by hand

Before the matrix notation, follow **one** example. We invent two input features: 2 and 1.
Each option has one weight for each feature and one extra number called a bias.

For the technical option: **2 × 0.8 + 1 × (−0.2) + 0.1 = 1.5**.
Repeat that multiplication-and-addition for the other options. The table below traces every term.
These fixed weights are handmade; the later training experiment learns its own weights.
'''),code('''
trace_inputs = np.array([2.0, 1.0])
trace_options = ['technical', 'billing', 'other']
trace_weights = np.array([[0.8, -0.3, 0.1], [-0.2, 0.6, 0.1]])
trace_bias = np.array([0.1, 0.0, -0.1])
trace_logits = trace_inputs @ trace_weights + trace_bias
trace_exp = np.exp(trace_logits - trace_logits.max())
trace_probabilities = trace_exp / trace_exp.sum()

table(['Option', 'Feature 1 contribution', 'Feature 2 contribution', 'Bias', 'Score (logit)', 'Probability'],
      [[name, f'{trace_inputs[0] * trace_weights[0,i]:.2f}',
        f'{trace_inputs[1] * trace_weights[1,i]:.2f}', f'{trace_bias[i]:.2f}',
        f'{trace_logits[i]:.2f}', f'{trace_probabilities[i]:.1%}']
       for i,name in enumerate(trace_options)])
print('Most likely option:', trace_options[trace_probabilities.argmax()])
'''),md('''**Read the result:** technical has the largest score and probability. The scores themselves
do not sum to 1; softmax converts them into probabilities that do. The `@` symbol performs the
same multiplication-and-addition for every option in one matrix operation.

**Predict a change:** change the technical bias from 0.1 to −2.0. Which option should win?
The technical score becomes −0.6; the other scores stay 0.0 and 0.2, so `other` wins.
Restart and Run All after trying it. This warm-up has its own variables and does not alter the later model.
''')]

    if number == '03':
        idx = next(i for i,c in enumerate(cells) if c.cell_type=='markdown' and '## Steps' in c.source)
        cells[idx:idx] = [md('''## Begin with ten outcomes

Imagine ten cases, each predicted to be yes with probability 0.80. We invent eight yes outcomes
and two no outcomes. The predicted frequency is 80%; the observed frequency is 8 ÷ 10 = 80%.

That is agreement **for this one constructed group**. It does not establish calibration across
other probabilities or future data. The larger experiment below shows why many cases and clear
denominators matter.
'''),code('''
warmup_predictions = np.full(10, 0.80)
warmup_outcomes = np.array([1, 1, 1, 1, 1, 1, 1, 1, 0, 0])
table(['Cases', 'Mean predicted yes probability', 'Observed yes outcomes', 'Observed yes frequency'],
      [[len(warmup_outcomes), f'{warmup_predictions.mean():.0%}',
        f'{warmup_outcomes.sum()} of {len(warmup_outcomes)}', f'{warmup_outcomes.mean():.0%}']])
'''),md('''**Predict a change:** if just one yes changes to no, the observed frequency is 70%.
That finite-group mismatch alone does not prove a model is miscalibrated. Read the reliability
diagram below as a pattern across bins, while keeping their sample sizes in view.
''')]

    if number == '01':
        for cell in cells:
            if cell.cell_type == 'markdown' and 'A useful abstract view is' in cell.source:
                cell.source = cell.source.replace('A useful abstract view is',
                    'First read this as: “How likely is each allowed answer, given the evidence and the question?” '
                    'The formula below is optional. A useful abstract view is')
            if cell.cell_type == 'markdown' and '### 3. Score:' in cell.source:
                cell.source += '\n\n**In everyday words:** multiply each level by its probability, then add. '
                cell.source += 'A 70% chance of level 2 contributes 1.4 to the final score. You can follow the worked numbers without memorizing the formula.'
        idx = next(i for i,c in enumerate(cells) if c.cell_type=='markdown' and '## Checks' in c.source)
        cells[idx:idx] = [md('''
### Your turn: change only the policy
Keep the same invented probabilities and try two thresholds. Predict the output before running.
This practice cell uses its own variables, so it does not change the earlier checks.
'''), code('''
practice_probabilities = {'technical': 0.90, 'billing': 0.06, 'other': 0.04}
practice_queue = max(practice_probabilities, key=practice_probabilities.get)
for practice_threshold in [0.85, 0.95]:
    practice_action = practice_queue if practice_probabilities[practice_queue] >= practice_threshold else 'review'
    print(f'Threshold {practice_threshold:.2f}: {practice_action}')
'''), md('**Expected observation:** 0.85 routes to `technical`; 0.95 sends it to `review`. The estimated topic did not change.')]

    # Mark the point at which optional extensions start; running remains top-to-bottom.
    markers = {'02':'### 6. Keep track', '03':'### 5. Repair', '04':'### 5. Rewrite', '05':'### 5. Inspect'}
    if number in markers:
        for i,cell in enumerate(cells):
            if cell.cell_type=='markdown' and markers[number] in cell.source:
                cells.insert(i,md('> **Optional deeper practice.** You can stop reading here on your first pass. '
                                   'If you run the notebook, use Run All so the later checks still have their inputs.'))
                break
    if number in RECAPS:
        recap = '\n'.join(f'- {point}' for point in RECAPS[number])
        cells.append(md(f'## Take three ideas with you\n\n{recap}\n\n**You are ready to move on when:** {done}'))
    cells.append(md(f'''## Check your understanding

{question}

Pause and explain your answer before opening the explanation.

<details>
<summary>Show the explanation</summary>
<p>{answer}</p>
</details>

For a short next step, try the [practice questions](PRACTICE.md).
For runnable exercises, use the [worked exercises](08_exercises_and_solutions.ipynb).

[Assignments](assignments/README.md) · [Quick reference](QUICK_REFERENCE.md) · [Course outline](COURSE.md)
'''))
    # Make the default notebook navigation useful in GitHub's Markdown/notebook viewer.
    for cell in cells:
        if cell.cell_type == 'markdown':
            cell.source = cell.source.replace('(index.html)', '(README.md)')
            cell.source = cell.source.replace('[Interactive playground](playground.html)', '[Calibration examples](03_calibration_and_decisions.ipynb)')
            cell.source = cell.source.replace('[playground](playground.html)', '[optional playground setup](SETUP.md)')
            cell.source = cell.source.replace('[interactive playground](playground.html)', '[optional playground setup](SETUP.md)')
    # Stable IDs reduce noisy notebook diffs when the public course is rebuilt.
    seen = {}
    for cell in cells:
        digest=hashlib.sha256((name+cell.cell_type+cell.source).encode()).hexdigest()[:12]
        count=seen.get(digest,0);seen[digest]=count+1
        cell.id=f'{digest}-{count}'
    return cells
