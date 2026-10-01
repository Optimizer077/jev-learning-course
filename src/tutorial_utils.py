"""Plot style and a small HTML table helper; no model or network calls."""
from html import escape
from pathlib import Path
import matplotlib.pyplot as plt
from IPython.display import HTML, display

BLUE, ORANGE, GREY = '#2563a6', '#c46b20', '#444444'

def setup():
    plt.rcParams.update({'figure.figsize': (8, 4), 'figure.dpi': 120,
                         'font.size': 11, 'axes.spines.top': False,
                         'axes.spines.right': False, 'axes.grid': False,
                         'figure.constrained_layout.use': True})

def show_figure(name):
    figures = Path(__file__).resolve().parents[1] / 'assets' / 'figures'
    figures.mkdir(parents=True, exist_ok=True)
    plt.gcf().savefig(figures / f'{name}.png', bbox_inches='tight')
    plt.show()
    plt.close()

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
    show_figure(name)

def table(headers, rows):
    head = ''.join(f'<th style="text-align:left;padding:8px">{escape(str(x))}</th>' for x in headers)
    body = ''.join('<tr>' + ''.join(f'<td style="text-align:left;padding:8px;border-top:1px solid #ddd">{escape(str(x))}</td>' for x in row) + '</tr>' for row in rows)
    display(HTML(f'<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>'))
