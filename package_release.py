"""Build an allowlisted install ZIP from a prepared candidate without installing it."""
import argparse
import json
import pathlib
import re
import zipfile
from build_patch import file_sha

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate', type=pathlib.Path, required=True)
    parser.add_argument('--output', type=pathlib.Path, required=True)
    args = parser.parse_args()
    candidate, output = args.candidate.resolve(), args.output.resolve()
    if output.exists() or output.with_suffix('.zip.sha256').exists():
        raise FileExistsError('Release destination already exists')
    source = pathlib.Path(__file__).resolve().parent
    manifest = json.loads((candidate/'manifest.json').read_text())
    version = manifest['version']
    if not re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+', version):
        raise ValueError('Invalid version')
    for entry in manifest['client_archives']:
        if not re.fullmatch(r'[a-fA-F0-9]{64}', entry.get('sha256', '')):
            raise ValueError('Every client archive requires a content hash')
    addon = 'Interface/AddOns/WarbandEnchantingRods/'
    assets = {
        'Install.ps1': candidate/'Install.ps1',
        'Data/patch-Z.MPQ': candidate/'Data/patch-Z.MPQ',
        **{addon+name: candidate/addon/name for name in
           ['Recipes.lua', 'WarbandEnchantingRods.lua', 'WarbandEnchantingRods.toc']},
        'README.md': source/'docs/INSTALL.md',
        'SOURCE.md': source/'SOURCE.md',
        'LICENSE': source/'LICENSE',
        'CHANGELOG.md': source/'CHANGELOG.md',
    }
    if file_sha(assets['Data/patch-Z.MPQ']) != manifest['mpq_sha256']:
        raise ValueError('Patch content hash differs')
    for name, digest in manifest['addon_sha256'].items():
        if addon+name not in assets or file_sha(assets[addon+name]) != digest:
            raise ValueError('Addon content hash differs')
    if set(manifest['addon_sha256']) != {'Recipes.lua', 'WarbandEnchantingRods.lua', 'WarbandEnchantingRods.toc'}:
        raise ValueError('Unexpected addon payload inventory')
    if file_sha(assets['Install.ps1']) != file_sha(source/'Install.ps1'):
        raise ValueError('Candidate installer does not match this source')
    manifest.pop('client_root', None)
    manifest['source_repository'] = 'https://github.com/pjw345/warband-enchanting-rods'
    prefix = 'WarbandEnchantingRods-'+version+'/'
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
        for name, path in sorted(assets.items()):
            archive.write(path, prefix+name)
        archive.writestr(prefix+'manifest.json', json.dumps(manifest, indent=2)+'\n')
    digest = file_sha(output)
    output.with_suffix('.zip.sha256').write_text(digest+'  '+output.name+'\n')
    print(json.dumps({'file': str(output), 'bytes': output.stat().st_size, 'sha256': digest, 'files': sorted(assets)+['manifest.json']}, indent=2))

if __name__ == '__main__':
    main()
