import os

REPLACEMENTS = {
    'text-[#0A0E1A]': 'text-ink',
    'text-[#3A4A5E]': 'text-text-ghost',
    'bg-[rgba(232,168,56,0.1)]': 'bg-gold/10',
    'bg-[rgba(14,207,177,0.1)]': 'bg-teal/10',
    'border-[var(--teal)]': 'border-teal',
    'text-[var(--teal)]': 'text-teal',
    'hover:border-[#F0EDE6]': 'hover:border-text-primary',
    'bg-[var(--ink-soft)]': 'bg-ink-soft',
    'peer-checked:bg-[var(--gold)]': 'peer-checked:bg-gold',
    'after:bg-[#F0EDE6]': 'after:bg-text-primary',
    'text-[#E8A838]': 'text-gold',
    'text-[#1E2A3A]': 'text-ink-border',
    'bg-[#1E2A3A]': 'bg-ink-border',
    'hover:border-[#E8A838]': 'hover:border-gold',
    'group-hover:border-[#E8A838]': 'group-hover:border-gold',
    'group-hover:text-[#E8A838]': 'group-hover:text-gold',
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
