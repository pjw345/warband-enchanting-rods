"""Create a synthetic installer test payload; contains no client/game data."""
import hashlib
import json
import pathlib
import shutil
import sys

source = pathlib.Path(__file__).resolve().parent.parent
root = pathlib.Path(sys.argv[1]).resolve()
root.mkdir(parents=True, exist_ok=False)
(root/'Data').mkdir()
(root/'Data/patch-Z.MPQ').write_bytes(b'Synthetic installer payload, not an MPQ')
addon = root/'Interface/AddOns/WarbandEnchantingRods'
addon.mkdir(parents=True)
for name in ['WarbandEnchantingRods.lua', 'WarbandEnchantingRods.toc']:
    shutil.copyfile(source/'WarbandEnchantingRods'/name, addon/name)
(addon/'Recipes.lua').write_text('-- Synthetic installer fixture only\n')
shutil.copyfile(source/'Install.ps1', root/'Install.ps1')
digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
manifest = {
    'client_exe_sha256': '', 'spell_source': 'fixture.MPQ',
    'source_archive_sha256': '', 'client_archives': [],
    'mpq_sha256': digest(root/'Data/patch-Z.MPQ'),
    'addon_sha256': {p.name: digest(p) for p in addon.iterdir()},
}
(root/'manifest.json').write_text(json.dumps(manifest))
