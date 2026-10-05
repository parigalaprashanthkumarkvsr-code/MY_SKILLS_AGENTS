"""Build an organized index of generated artwork and archived image references."""
import hashlib
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
inventory = json.loads((ROOT / 'inventory.json').read_text(encoding='utf-8'))
cover = 'assets/images/generated/skills-overview-blue-white-v1.png'
data = (ROOT / cover).read_bytes()
width, height = struct.unpack('>II', data[16:24])
metadata = {
    'schema_version': 1,
    'generated_on': '2026-10-05',
    'tool': 'built-in imagegen',
    'asset': cover,
    'dimensions': {'width': width, 'height': height},
    'palette': ['white', 'navy blue', 'cobalt blue', 'ice blue'],
    'purpose': 'README overview of the six skill groups',
    'skills': len(inventory['skills']),
    'agent_interfaces': len(inventory['agent_interfaces']),
    'generation_prompt': 'assets/images/prompts/skills-overview-blue-white-v1.txt',
    'correction_prompt': 'assets/images/prompts/skills-overview-blue-white-v1-correction.txt',
    'sha256': hashlib.sha256(data).hexdigest(),
}
(ROOT / 'assets/images/metadata.json').write_text(json.dumps(metadata, indent=2) + '\n', encoding='utf-8')

images = [item for item in inventory['files'] if Path(item['path']).suffix.lower() in {'.png', '.jpg', '.jpeg', '.webp', '.svg', '.gif'}]
references = [item for item in images if 'reference' in Path(item['path']).name]
previews = [item for item in images if Path(item['path']).name == 'preview.png']
icons = [item for item in images if item not in references + previews]
lines = [
    '# Image reference library', '',
    'Repository artwork uses a blue-and-white palette. Original upstream images retain their source appearance and location.', '',
    '## Repository overview', '',
    f'![Blue-and-white illustration of all six skill groups](../{cover})', '',
    f'**34 skills · 28 agent interfaces · {width} × {height} PNG.** Generated with the built-in imagegen tool on October 5, 2026.', '',
    '| Resource | Location |', '| --- | --- |',
    f'| Final overview | [PNG](../{cover}) |',
    '| Generation prompt | [Prompt](../assets/images/prompts/skills-overview-blue-white-v1.txt) |',
    '| Palette correction | [Edit prompt](../assets/images/prompts/skills-overview-blue-white-v1-correction.txt) |',
    '| Provenance and checksum | [Metadata](../assets/images/metadata.json) |', '',
    'The artwork illustrates Creative (1), Core tools (5), Sites (4), ChatGPT Pets (3), Plugin management (1), and Document templates (20). See the [skill catalog](CATALOG.md) for the complete inventory.', '',
    '## Creative reference', '',
    'Original material and lighting reference for `dark-tech-cover`. This reference retains its original dark appearance; the repository cover uses the requested blue-and-white palette.', '',
]
for item in references:
    lines += [f"![Original creative reference](../{item['path']})", '', f"[Source file](../{item['path']})", '']
lines += ['## Document template previews', '',
          'These original preview images accompany the 20 template skills. Their reference documents stay in the same package assets directories.', '',
          '| Template skill | Preview |', '| --- | --- |']
for item in previews:
    name = Path(item['path']).parent.parent.name
    skill = next(s for s in inventory['skills'] if s['name'] == name)
    lines.append(f"| [{name.removeprefix('artifact-template-').replace('-', ' ').title()}](../{skill['path']}) | <img src=\"../{item['path']}\" alt=\"{name} preview\" width=\"240\"> |")
lines += ['', '## Package icons and supporting images', '',
          'Original interface icons and supporting images are indexed here without duplicating them.', '',
          '| Image | Original package path |', '| --- | --- |']
for item in icons:
    lines.append(f"| {Path(item['path']).name} | [View image](../{item['path']}) |")
lines += ['', '## Maintenance', '',
          'Run `python scripts/catalog_images.py` after refreshing the skill inventory or replacing the overview artwork. Preserve original package paths and bundled source terms. The generated cover checksum is recorded in `assets/images/metadata.json`; archived image checksums are recorded in `inventory.json`.', '']
(ROOT / 'docs/IMAGES.md').write_text('\n'.join(lines), encoding='utf-8')
print(f'Indexed one generated cover and {len(images)} archived images: {len(references)} references, {len(previews)} previews, {len(icons)} supporting images.')
