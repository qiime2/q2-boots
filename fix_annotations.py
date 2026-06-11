import re

files = [
    'q2_boots/_alpha.py',
    'q2_boots/_beta.py',
    'q2_boots/_core_metrics.py',
    'q2_boots/_kmer_diversity.py'
]

for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Remove parameter annotations
    content = re.sub(r'(\w+)\s*:\s*[\w\[\]\|,\s]+(?=[,=)])', r'\1', content)
    
    # Remove return type annotations
    content = re.sub(r'\s*->\s*[\w\[\]\|,\s]+:', ':', content)
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"Fixed {filepath}")
