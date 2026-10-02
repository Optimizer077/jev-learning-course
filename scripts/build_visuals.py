"""Create vector course artwork and portable PNGs for saved notebook outputs."""
from collections import Counter
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from course_paths import ROOT

sys.path.insert(0, str(ROOT / 'src'))
from lab_core import WORD_ORDER_PAIR, load_tickets, tokenise, vocabulary
from model_history import HISTORY_TRACKS

ASSETS = ROOT / 'assets'
INK, TEAL, VIOLET, CORAL = '#13243b', '#0d766f', '#6245b7', '#b7432b'
plt.rcParams['svg.hashsalt'] = 'jev-learning-course'


def canvas(width, height, background):
    fig = plt.figure(figsize=(width/100, height/100), dpi=100, facecolor=background)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set(xlim=(0, width), ylim=(0, height))
    ax.axis('off')
    return fig, ax


def box(ax, x, y, w, h, fill, edge=None):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0,rounding_size=18',
                              facecolor=fill, edgecolor=edge or fill, linewidth=1.3))


def label(ax, x, y, text, size, color, weight='normal', **kwargs):
    ax.text(x, y, text, fontsize=size, color=color, fontweight=weight,
            fontfamily='DejaVu Sans', va='center', **kwargs)


def save(fig, name, description=''):
    ASSETS.mkdir(exist_ok=True)
    vector = ASSETS/f'{name}.svg'
    fig.savefig(vector, facecolor=fig.get_facecolor(), metadata={'Date': None})
    from html import escape
    source = vector.read_text(encoding='utf-8')
    position = source.index('>', source.index('<svg '))+1
    # Keep vector graphics understandable when opened directly, as well as embedded.
    title_id, description_id = f'{name}-title', f'{name}-description'
    source = (source[:position-1]+f' role="img" aria-labelledby="{title_id} {description_id}">'+
              f'\n <title id="{title_id}">{escape(name.replace("-", " "))}</title>\n'
              f' <desc id="{description_id}">{escape(description)}</desc>'+source[position:])
    vector.write_text('\n'.join(line.rstrip() for line in source.splitlines())+'\n', encoding='utf-8')
    # A local raster preview permits inspection without opening a webpage.
    preview = ROOT / 'dist' / 'visual-previews'
    preview.mkdir(parents=True, exist_ok=True)
    fig.savefig(preview/f'{name}.png', dpi=150, facecolor=fig.get_facecolor())
    if name in {'decision-flow', 'question-types', 'calibration-counts', 'data-splits', 'word-order', 'model-history-mobile'}:
        fig.savefig(ASSETS/f'{name}.png', dpi=150, facecolor=fig.get_facecolor())
    if name.endswith('-mobile') or name in {'decision-flow', 'question-types', 'calibration-counts', 'data-splits', 'word-order'}:
        fig.savefig(preview/f'{name}-360.png', dpi=360/fig.get_figwidth(), facecolor=fig.get_facecolor())
    plt.close(fig)


def build_visuals():
    fig, ax = canvas(1200, 430, INK)
    ax.plot([0, 1200], [424, 424], color='#3dd8c6', linewidth=8)
    label(ax, 48, 361, 'AN INDEPENDENT, HANDS-ON COURSE', 12, '#70e0d1', 'bold')
    label(ax, 48, 287, 'Learn Jev.', 43, 'white', 'bold')
    label(ax, 48, 224, 'One focused decision at a time.', 21, '#e1e9f4')
    label(ax, 48, 174, 'Read the evidence. Predict. Run. Explain.', 15, '#afc4df')
    for x, width, text, fill in [(48, 176, '11 notebooks', '#235557'),
                                (238, 180, '4 assignments', '#493e72'),
                                (432, 192, 'CPU-friendly labs', '#553c3b')]:
        box(ax, x, 64, width, 49, fill)
        label(ax, x+width/2, 89, text, 11.5, 'white', 'bold', ha='center')
    for y, title, subtitle, color in [(290, '01  EVIDENCE + QUESTION', 'A message and clear criteria', '#3dd8c6'),
                                      (176, '02  TYPED ANSWER', 'Choice · Score · Noul', '#c2afff'),
                                      (62, '03  ACTION RULE', 'Route or ask for review', '#ffb29e')]:
        box(ax, 811, y, 338, 88, '#1e3551', '#425670')
        label(ax, 834, y+61, title, 11, color, 'bold')
        label(ax, 834, y+29, subtitle, 13, '#f4f7fc')
        if y > 62:
            ax.annotate('', xy=(980, y-18), xytext=(980, y-3),
                        arrowprops={'arrowstyle':'->', 'color':'#96acc9', 'lw':2})
    save(fig, 'course-banner', 'Evidence and a focused question lead to a typed estimate; application code chooses an action.')

    fig, ax = canvas(540, 525, INK)
    ax.plot([0,540],[520,520],color='#3dd8c6',lw=7)
    label(ax,30,477,'AN INDEPENDENT LEARNING COURSE',10.5,'#70e0d1','bold')
    label(ax,30,419,'Learn Jev.',35,'white','bold')
    label(ax,30,371,'One decision at a time.',19,'#e1e9f4')
    label(ax,30,333,'11 notebooks · 4 assignments · CPU labs',11.5,'#afc4df')
    for y, title, subtitle, color in [(230,'EVIDENCE + QUESTION','A message and clear criteria','#70e0d1'),
                                     (132,'TYPED ANSWER','Choice · Score · Noul','#c2afff'),
                                     (34,'YOUR ACTION RULE','Route or ask for review','#ffb29e')]:
        box(ax,26,y,488,82,'#1e3551','#425670')
        label(ax,46,y+55,title,12,color,'bold')
        label(ax,46,y+26,subtitle,13,'white')
    save(fig,'course-banner-mobile','Evidence, question, typed estimate, and application action. Mobile version of the course header.')

    fig, ax = canvas(1200, 272, '#f5f7fc')
    tracks = [
        ('01  UNDERSTAND', '00 → 01 → 04', 'Evidence, answer types, workflows', TEAL, '#e5f6f2'),
        ('02  EXPERIMENT', '02 → 03', 'Training, probabilities, review costs', VIOLET, '#eee9fc'),
        ('03  BUILD', '07 → 09', 'Optional 10: train with PyTorch', CORAL, '#fceee9'),
    ]
    for i, (title, lessons, subtitle, color, fill) in enumerate(tracks):
        x = 22 + 397*i
        box(ax, x, 25, 362, 222, 'white', '#d9e2f0')
        box(ax, x+17, 185, 328, 42, fill)
        label(ax, x+32, 206, title, 11, color, 'bold')
        label(ax, x+24, 137, lessons, 24, INK, 'bold')
        label(ax, x+24, 87, subtitle, 11.2, '#405671')
        label(ax, x+24, 49, ['Explain a decision', 'After lesson 01', 'After lessons 02 and 03'][i],
              10.5, color, 'bold')
    save(fig, 'learning-path', 'Understand: 00, 01, 04. Experiment: 02, 03 after 01. Build: 07, 09 after 02 and 03. Add optional lesson 10 to train small models with PyTorch.')
    fig, ax = canvas(440, 735, '#f5f7fc')
    for i, (title, lessons, subtitle, color, fill) in enumerate(tracks):
        y = 503-240*i
        box(ax,18,y,404,213,'white','#d9e2f0')
        box(ax,34,y+155,372,40,fill)
        label(ax,49,y+175,title,13,color,'bold')
        label(ax,42,y+110,lessons,27,INK,'bold')
        short = ['Evidence, types, workflows','Training, probabilities, costs','Optional 10: PyTorch models'][i]
        label(ax,42,y+62,short,13,'#405671')
        label(ax,42,y+29,['No coding needed','After lesson 01','After lessons 02 and 03'][i],12,color,'bold')
    save(fig,'learning-path-mobile','Three learning paths and their prerequisites, stacked for narrow screens. Optional lesson 10 adds PyTorch training after 07 and 09.')

    build_teaching_visuals()
    build_project_visuals()
    build_history_visuals()


def build_teaching_visuals():
    fig, ax = canvas(660, 854, '#f5f7fc')
    label(ax,30,813,'ONE TICKET, FOUR CLEAR STEPS',17,INK,'bold')
    steps = [
        ('01  EVIDENCE','“The export button crashes.\nI cannot finish my report.”',TEAL),
        ('02  QUESTION + CRITERIA','Which queue fits?\nTechnical, billing, or other.',VIOLET),
        ('03  ILLUSTRATIVE ESTIMATE','Technical 90% · Billing 6% · Other 4%\nThese numbers are invented, not a Jev call.',TEAL),
        ('04  APPLICATION RULE','At threshold 0.85: route to technical.\nAt threshold 0.95: ask for review.',CORAL),
    ]
    for i,(title,body,color) in enumerate(steps):
        y = 605-169*i
        box(ax,26,y,608,143,'white','#d9e2f0')
        ax.plot([27,27],[y+20,y+123],color=color,lw=5)
        label(ax,47,y+111,title,13,color,'bold')
        label(ax,47,y+58,body,13.5,INK,linespacing=1.7)
        if i<3:
            ax.annotate('',xy=(330,y-20),xytext=(330,y-3),arrowprops={'arrowstyle':'->','color':'#405671','lw':2})
    label(ax,30,41,'Estimate ≠ action. Permissions remain separate.',12,INK,'bold')
    save(fig,'decision-flow','Invented probabilities: technical 90%, billing 6%, other 4%. Thresholds 0.85 and 0.95 produce routing and review. A model estimate does not grant permission.')

    fig, ax = canvas(600, 984, '#f5f7fc')
    label(ax,26,947,'SAME EVIDENCE, DIFFERENT QUESTIONS',15,INK,'bold')
    for y,title,color in [(637,'CHOICE · named alternatives',TEAL),
                           (349,'SCORE · ordered levels',VIOLET),
                           (61,'NOUL · yes / no judgment',CORAL)]:
        box(ax,22,y,556,266,'white','#d9e2f0')
        label(ax,43,y+228,title,16,color,'bold')
    label(ax,43,824,'Which support queue fits?',14,INK)
    for y,name,p in [(776,'Technical',.90),(732,'Billing',.06),(688,'Other',.04)]:
        label(ax,43,y,name,12.5,'#405671')
        ax.plot([191,467],[y,y],lw=14,color='#e5f6f2',solid_capstyle='butt')
        ax.plot([191,191+276*p],[y,y],lw=14,color=TEAL,solid_capstyle='butt')
        label(ax,489,y,f'{p:.0%}',13,INK,'bold')
    label(ax,192,655,'Bar scale: 0 to 100%',10.5,'#405671')
    label(ax,43,536,'How disrupted is work on a 0–2 rubric?',13,INK)
    label(ax,43,489,'0: no disruption     1: partial     2: blocked',11.5,'#405671')
    label(ax,43,443,'5% at 0  +  25% at 1  +  70% at 2',13,INK)
    score = sum(level*p for level,p in enumerate([.05,.25,.70]))
    label(ax,43,398,f'Expected level = {score:.2f}',21,VIOLET,'bold')
    label(ax,43,247,'Is a refund explicitly requested?',14,INK)
    label(ax,43,194,'Illustrative probability of yes',12.5,'#405671')
    label(ax,43,136,'12%',30,CORAL,'bold')
    label(ax,184,135,'A probability, not a permission.',11.5,INK)
    label(ax,26,26,'Authored illustrations · no model call',11.5,'#405671')
    save(fig,'question-types','Choice: technical 90%, billing 6%, other 4%. Score: probabilities 5%, 25%, 70% for levels 0, 1, 2 give expected level 1.65. Noul: illustrative yes probability 12%.')

    fig, ax = canvas(600, 426, 'white')
    label(ax,24,391,'CALIBRATION STARTS WITH OUTCOMES',14,INK,'bold')
    outcomes = [1]*8+[0]*2
    cases, yes = len(outcomes), sum(outcomes)
    label(ax,24,343,'Ten cases each receive a predicted yes probability of 80%.',10.8,'#405671')
    for i,outcome in enumerate(outcomes):
        x,y = 69+113*(i%5), 266-76*(i//5)
        ax.scatter([x],[y],s=1050,marker='o' if outcome else 'X',
                   color=TEAL if outcome else CORAL)
        label(ax,x,y,'Y' if outcome else 'N',12,'white','bold',ha='center')
    label(ax,24,119,f'{yes} yes / {cases} cases = {yes/cases:.0%}',23,INK,'bold')
    label(ax,24,73,'One agreeing group does not prove calibration.',12,VIOLET,'bold')
    label(ax,24,30,'Invented outcomes · circle Y = yes · cross N = no',10.5,'#405671')
    save(fig,'calibration-counts','Ten authored outcomes: eight yes and two no. Mean predicted probability is 80%; observed yes frequency is 8/10, or 80%. One group does not establish calibration.')


def build_project_visuals():
    rows = load_tickets()
    counts = Counter(row['split'] for row in rows)
    fig, ax = canvas(540, 892, '#f5f7fc')
    label(ax, 24, 854, 'KEEP THE EXAMPLES SEPARATE', 16, INK, 'bold')
    label(ax, 24, 809, 'Each group has a different job.', 14, '#405671')
    stages = [
        ('train', '01  TRAIN', 'Learn the vocabulary and weights.',
         'Labels are targets, never text features.', TEAL, '#e5f6f2'),
        ('validation', '02  VALIDATE', 'Choose temperature and review cutoff.',
         'Freeze these choices before testing.', VIOLET, '#eee9fc'),
        ('test', '03  TEST', 'Assess the frozen system once.',
         'Tuning here uses up the test set.', CORAL, '#fceee9'),
        ('stress', '04  STRESS', 'Inspect deliberately difficult cases.',
         'Report separately from test accuracy.', INK, '#edf1f7'),
    ]
    for i, (split, title, purpose, note, color, fill) in enumerate(stages):
        y = 610 - 170*i
        box(ax, 22, y, 496, 147, 'white', '#d9e2f0')
        box(ax, 38, y+93, 464, 38, fill)
        label(ax, 50, y+112, title, 13, color, 'bold')
        label(ax, 490, y+112, f'{counts[split]} cases', 13, color, 'bold', ha='right')
        label(ax, 42, y+66, purpose, 13.5, INK)
        label(ax, 42, y+29, note, 12.5, '#405671')
        if i < 2:
            ax.annotate('', xy=(270, y-20), xytext=(270, y-3),
                        arrowprops={'arrowstyle': '->', 'color': '#405671', 'lw': 2})
    label(ax, 24, 62, f'{len(rows)} fictional tickets. A learning exercise.', 13, INK, 'bold')
    label(ax, 24, 27, 'Small authored sets do not establish reliability.', 12, '#405671')
    save(fig, 'data-splits',
         f"Counts from data/tickets.json: {dict(counts)}. Fit on training; choose settings on validation; assess a frozen system on test; inspect stress cases separately.")

    # Use the same messages as lessons 07/09 and the vocabulary fitted on training only.
    vocab = vocabulary([row['text'] for row in rows if row['split'] == 'train'])
    bags = [set(tokenise(message)) for message, _ in WORD_ORDER_PAIR]
    assert bags[0] == bags[1]
    known = sorted(bags[0].intersection(vocab))
    unseen = sorted(bags[0].difference(vocab))
    fig, ax = canvas(540, 948, '#f5f7fc')
    label(ax, 24, 910, 'WHEN WORD ORDER DISAPPEARS', 15.5, INK, 'bold')
    label(ax, 24, 868, 'Same words. Different problems.', 14, '#405671')
    for i, (message, reference) in enumerate(WORD_ORDER_PAIR):
        y = 653-185*i
        box(ax, 22, y, 496, 159, 'white', '#d9e2f0')
        label(ax, 43, y+127, f'MESSAGE {"AB"[i]}', 12.5, TEAL if i == 0 else CORAL, 'bold')
        first, second = message.split(', ')
        label(ax, 43, y+78, first+',\n'+second, 16, INK, linespacing=1.45)
        label(ax, 43, y+24, f'Intended primary queue: {reference}', 12.5, INK, 'bold')
    box(ax, 22, 218, 496, 217, 'white', '#d9e2f0')
    label(ax, 43, 403, 'COMPARE THE BINARY INPUTS', 13, VIOLET, 'bold')
    positions = [140 + i*(320/max(len(known)-1, 1)) for i in range(len(known))]
    for x, word in zip(positions, known):
        label(ax, x, 359, word, 13, INK, 'bold', ha='center')
        for y in (316, 276):
            label(ax, x, y, '1', 17, VIOLET, 'bold', ha='center')
    label(ax, 48, 316, 'A', 14, INK, 'bold')
    label(ax, 48, 276, 'B', 14, INK, 'bold')
    dropped = ', '.join(unseen)
    label(ax, 42, 241, f'Unseen in training: {dropped}. These words are dropped.', 10.8, '#405671')
    label(ax, 24, 170, 'Identical inputs → identical predictions.', 14, INK, 'bold')
    label(ax, 24, 125, 'At least one primary queue must be wrong.', 13, CORAL, 'bold')
    label(ax, 24, 77, 'A new threshold cannot restore missing word order.', 12, '#405671')
    label(ax, 24, 32, 'A limitation of our local baseline; no Jev call.', 12, '#405671')
    save(fig, 'word-order',
         f'Authored messages: {WORD_ORDER_PAIR}. Both have active training-vocabulary words {known}; unseen words {unseen} are dropped. Identical binary features cannot yield different deterministic classifier outputs.')


def build_history_visuals():
    description = ('Selected publication milestones grouped into probability evaluation, input '
                   'representation, and task adaptation. Brier 1950, Chow 1970, Guo 2017; '
                   'backpropagation 1986, term weighting 1988, CNN and GRU 2014, Transformer 2017; '
                   'BERT, RoBERTa, Sentence-BERT and entailment-based classification 2019; '
                   'SetFit preprint 2022. This does not establish Jev\'s internal ancestry.')
    fig, ax = canvas(1200, 700, '#f5f7fc')
    label(ax, 24, 666, 'A SHORT HISTORY OF THE IDEAS', 20, INK, 'bold')
    label(ax, 24, 628, 'Three threads to follow while reading the course papers.', 14, '#405671')
    for column, (title, color, fill, milestones) in enumerate(HISTORY_TRACKS):
        x = 22 + 397*column
        label(ax, x+9, 581, title, 16, color, 'bold')
        for row, (year, heading, detail) in enumerate(milestones):
            y = 415-161*row
            box(ax, x, y, 362, 143, 'white', '#d9e2f0')
            box(ax, x+16, y+103, 150, 27, fill)
            label(ax, x+29, y+117, year, 11.5, color, 'bold')
            label(ax, x+19, y+83, heading, 14, INK, 'bold')
            label(ax, x+19, y+37, detail, 12.4, '#405671', linespacing=1.35)
    label(ax, 24, 54, 'Publication milestones; spacing is schematic. Follow the linked papers for details.', 12, '#405671')
    label(ax, 24, 24, 'Jev\'s internal model lineage is unspecified in the reviewed documentation.', 12, INK)
    save(fig, 'model-history', description)

    fig, ax = canvas(540, 1520, '#f5f7fc')
    label(ax, 24, 1483, 'A SHORT HISTORY OF THE IDEAS', 18, INK, 'bold')
    label(ax, 24, 1447, 'Three threads. Selected papers.', 14, '#405671')
    label(ax, 24, 1420, 'Dates identify publications.', 12.5, '#405671')
    for group, (title, color, fill, milestones) in enumerate(HISTORY_TRACKS):
        top = 1390-425*group
        label(ax, 26, top, title.upper(), 16, color, 'bold')
        for row, (year, heading, detail) in enumerate(milestones):
            y = top-150-126*row
            box(ax, 22, y, 496, 118, 'white', '#d9e2f0')
            label(ax, 42, y+96, year, 12.5, color, 'bold')
            label(ax, 42, y+65, heading, 15.5, INK, 'bold')
            label(ax, 42, y+26, detail, 13.5, '#405671', linespacing=1.25)
    label(ax, 24, 77, 'Publication dates; spacing is schematic.', 12.5, '#405671')
    label(ax, 24, 40, 'Jev\'s internal lineage is unspecified.', 12.5, INK)
    save(fig, 'model-history-mobile', description)


if __name__ == '__main__':
    build_visuals()
