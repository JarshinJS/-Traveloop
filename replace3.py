import os

REPLACEMENTS = {
    'text-text-primary': 'text-[var(--text-primary)]',
    'text-text-muted': 'text-[var(--text-muted)]',
    'text-text-ghost': 'text-[var(--text-ghost)]',
    'text-ink': 'text-[var(--ink)]',
    'text-ink-soft': 'text-[var(--ink-soft)]',
    'bg-ink': 'bg-[var(--ink)]',
    'bg-ink-soft': 'bg-[var(--ink-soft)]',
    'border-ink-border': 'border-[var(--ink-border)]',
    'bg-ink-border': 'bg-[var(--ink-border)]',
    'hover:border-text-primary': 'hover:border-[var(--text-primary)]',
    'hover:text-text-primary': 'hover:text-[var(--text-primary)]',
}

base_dir = r'd:\ODOO\Traveloop\templates'

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.html'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            orig = content
            for old, new in REPLACEMENTS.items():
                content = content.replace(old, new)
                
            if orig != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f'Updated {path}')
