"""Create self-contained vector artwork for the GitHub course landing page."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from course_paths import ROOT

ASSETS = ROOT / 'assets'
INK, TEAL, VIOLET, CORAL = '#13243b', '#0d9488', '#7356cf', '#c45137'
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


def save(fig, name):
    ASSETS.mkdir(exist_ok=True)
    vector = ASSETS/f'{name}.svg'
    fig.savefig(vector, facecolor=fig.get_facecolor(), metadata={'Date': None})
    vector.write_text('\n'.join(line.rstrip() for line in vector.read_text(encoding='utf-8').splitlines())+'\n',
                      encoding='utf-8')
    # A local raster preview permits inspection without opening a webpage.
    preview = ROOT / 'dist' / 'visual-previews'
    preview.mkdir(parents=True, exist_ok=True)
    fig.savefig(preview/f'{name}.png', dpi=150, facecolor=fig.get_facecolor())
    plt.close(fig)


def build_visuals():
    fig, ax = canvas(1200, 430, INK)
    ax.plot([0, 1200], [424, 424], color='#3dd8c6', linewidth=8)
    label(ax, 48, 361, 'AN INDEPENDENT, HANDS-ON COURSE', 12, '#70e0d1', 'bold')
    label(ax, 48, 287, 'Learn Jev.', 43, 'white', 'bold')
    label(ax, 48, 224, 'One focused decision at a time.', 21, '#e1e9f4')
    label(ax, 48, 174, 'Read the evidence. Predict. Run. Explain.', 15, '#afc4df')
    for x, width, text, fill in [(48, 176, '10 notebooks', '#235557'),
                                (238, 180, '3 assignments', '#493e72'),
                                (432, 192, 'CPU-friendly labs', '#553c3b')]:
        box(ax, x, 64, width, 49, fill)
        label(ax, x+width/2, 89, text, 11.5, 'white', 'bold', ha='center')
    for y, title, subtitle, color in [(290, '01  EVIDENCE', 'A support message', '#3dd8c6'),
                                      (176, '02  TYPED ANSWER', 'Choice · Score · Noul', '#c2afff'),
                                      (62, '03  ACTION RULE', 'Route or ask for review', '#ffb29e')]:
        box(ax, 811, y, 338, 88, '#1e3551', '#425670')
        label(ax, 834, y+61, title, 11, color, 'bold')
        label(ax, 834, y+29, subtitle, 13, '#f4f7fc')
        if y > 62:
            ax.annotate('', xy=(980, y-18), xytext=(980, y-3),
                        arrowprops={'arrowstyle':'->', 'color':'#96acc9', 'lw':2})
    save(fig, 'course-banner')

    fig, ax = canvas(1200, 272, '#f5f7fc')
    tracks = [
        ('01  UNDERSTAND', '00 → 01 → 04', 'Evidence, answer types, workflows', TEAL, '#e5f6f2'),
        ('02  EXPERIMENT', '02 → 03', 'Training, probabilities, review costs', VIOLET, '#eee9fc'),
        ('03  BUILD', '07 → 09', 'Route text, evaluate, compare', CORAL, '#fceee9'),
    ]
    for i, (title, lessons, subtitle, color, fill) in enumerate(tracks):
        x = 22 + 397*i
        box(ax, x, 25, 362, 222, 'white', '#d9e2f0')
        box(ax, x+17, 185, 328, 42, fill)
        label(ax, x+32, 206, title, 11, color, 'bold')
        label(ax, x+24, 137, lessons, 24, INK, 'bold')
        label(ax, x+24, 87, subtitle, 11.2, '#405671')
        label(ax, x+24, 49, ['Explain a decision', 'Change one thing', 'Inspect the failures'][i],
              10.5, color, 'bold')
    save(fig, 'learning-path')


if __name__ == '__main__':
    build_visuals()
