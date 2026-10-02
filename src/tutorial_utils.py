"""Plot style and a small HTML table helper; no model or network calls."""
from html import escape
from pathlib import Path
import matplotlib.pyplot as plt
from IPython.display import HTML, Image, display

BLUE, ORANGE, GREY = '#2563a6', '#c46b20', '#444444'

def setup():
    plt.rcParams.update({'figure.figsize': (8, 4), 'figure.dpi': 120,
                         'font.size': 11, 'axes.spines.top': False,
                         'axes.spines.right': False, 'axes.grid': False,
                         'figure.constrained_layout.use': True})

def show_figure(name, description=None):
    """Save and embed a chart, including when a headless backend is active."""
    figures = Path(__file__).resolve().parents[1] / 'assets' / 'figures'
    figures.mkdir(parents=True, exist_ok=True)
    figure = plt.gcf()
    image = figures / f'{name}.png'
    try:
        figure.savefig(image, bbox_inches='tight')
        if description is None:
            titles = [text.get_text() for text in figure.texts] + [axis.get_title() for axis in figure.axes]
            description = '; '.join(dict.fromkeys(title for title in titles if title)) or name.replace('_', ' ')
        display(Image(filename=str(image), embed=True, alt=description), metadata={'alt': description})
    finally:
        plt.close(figure)


def show_diagram(name, description):
    """Embed the course artwork in saved outputs for GitHub, Colab, and offline reading."""
    image = Path(__file__).resolve().parents[1] / 'assets' / f'{name}.png'
    if not image.is_file():
        raise FileNotFoundError('Keep the complete course folder, including assets, together.')
    # Preserve descriptions for notebook viewers and the course's HTML export.
    display(Image(filename=str(image), width=540, alt=description), metadata={'alt': description})

def flow_diagram(labels, name, title):
    """A readable conceptual flow; boxes do not claim neural-network internals."""
    fig, ax = plt.subplots(figsize=(11, 2.4))
    ax.set(xlim=(0, len(labels)), ylim=(0, 1))
    ax.axis('off')
    for i, label in enumerate(labels):
        ax.text(i + .5, .5, label, ha='center', va='center', fontsize=11,
                bbox=dict(boxstyle='round,pad=.7', facecolor='#edf3fa', edgecolor=BLUE))
        if i < len(labels)-1:
            ax.annotate('', xy=(i+1.1,.5), xytext=(i+.88,.5),
                        arrowprops=dict(arrowstyle='->',color=GREY,lw=1.5))
    ax.set_title(title, pad=12)
    show_figure(name, title + ': ' + ' → '.join(label.replace('\n', ' ') for label in labels))

def table(headers, rows):
    head = ''.join(f'<th style="text-align:left;padding:8px">{escape(str(x))}</th>' for x in headers)
    body = ''.join('<tr>' + ''.join(f'<td style="text-align:left;padding:8px;border-top:1px solid #ddd">{escape(str(x))}</td>' for x in row) + '</tr>' for row in rows)
    display(HTML(f'<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>'))
