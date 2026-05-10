import os

REPLACEMENTS = {
    'text-[#F0EDE6]': 'text-text-primary',
    'text-[#7B8CA8]': 'text-text-muted',
    'bg-[#0A0E1A]': 'bg-ink',
    'bg-[#0D1120]': 'bg-ink-soft',
    'border-[#1E2A3A]': 'border-ink-border',
    'bg-[rgba(255,255,255,0.02)]': 'bg-black/5 dark:bg-white/5',
    'bg-[rgba(255,255,255,0.04)]': 'bg-black/10 dark:bg-white/10',
    'hover:bg-[rgba(255,255,255,0.02)]': 'hover:bg-black/5 dark:hover:bg-white/5',
    'hover:bg-[rgba(255,255,255,0.04)]': 'hover:bg-black/10 dark:hover:bg-white/10',
    'border-[rgba(255,255,255,0.05)]': 'border-ink-border',
    'bg-[rgba(255,255,255,0.03)]': 'bg-black/5 dark:bg-white/5',
    'text-[var(--danger)]': 'text-red-500',
    'text-[var(--gold)]': 'text-gold',
    'border-[var(--gold)]': 'border-gold',
    'border-[var(--ink-border)]': 'border-ink-border',
    'hover:text-[#F0EDE6]': 'hover:text-text-primary',
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
