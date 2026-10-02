"""Write the explicitly authored synthetic sentence task; no downloads or model calls."""
import json
import sys
from course_paths import ROOT

sys.path.insert(0, str(ROOT/'src'))
from torch_lab import make_toy_rows, validate_toy_rows

rows = make_toy_rows()
counts = validate_toy_rows(rows)
(ROOT/'data'/'torch_toy.json').write_text(json.dumps(rows, indent=2)+'\n', encoding='utf-8')
print(f'Authored {len(rows)} synthetic sentences in fixed paired splits: {dict(counts)}')
