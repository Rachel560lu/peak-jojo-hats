"""Package only this mod's runtime files; never bundle local game/dependency DLLs."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import struct
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='Optional ZIP output path')
    args = parser.parse_args()
    manifest = json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))
    catalog = json.loads((ROOT / 'assets/catalog.json').read_text(encoding='utf-8'))
    version = manifest['version_number']
    assert re.fullmatch(r'\d+\.\d+\.\d+', version), 'Expected a three-part package version'
    # Model revisions are independent: v0.5.0 deliberately retains v0.4.2 assets.
    assert re.fullmatch(r'\d+\.\d+\.\d+', catalog['version']), 'Invalid asset revision'
    assert len(catalog['hats']) == 6
    dll = ROOT / 'bin/Release/netstandard2.1/JojoHats.dll'
    if not dll.is_file():
        raise SystemExit('Build Release first using scripts/build.ps1.')

    files = [(ROOT / name, name) for name in ('manifest.json', 'icon.png', 'CHANGELOG.md')]
    files.append((ROOT / 'docs/RELEASE-README.md', 'README.md'))
    plugin = 'BepInEx/plugins/JojoHats/'
    files.append((dll, plugin + 'JojoHats.dll'))
    for name in ('catalog.json', 'palette.png'):
        files.append((ROOT / 'assets' / name, plugin + 'assets/' + name))
    for hat in catalog['hats']:
        identifier = hat['id']
        assert '/' not in identifier and '\\' not in identifier and '..' not in identifier
        for name in ('mesh.json', 'icon.png'):
            relative = f'assets/{identifier}/{name}'
            files.append((ROOT / relative, plugin + relative))

    assert len(files) == len({name for _, name in files}) == 19
    for source, _ in files:
        if not source.is_file():
            raise SystemExit(f'Missing required input: {source.relative_to(ROOT)}')
    icon = (ROOT / 'icon.png').read_bytes()
    assert icon[:8] == b'\x89PNG\r\n\x1a\n' and icon[12:16] == b'IHDR', 'icon.png must be a PNG'
    assert struct.unpack('>II', icon[16:24]) == (256, 256), 'Thunderstore icon must be 256 x 256'
    target = args.output or ROOT / 'dist' / f"{manifest['name']}-{version}.zip"
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for source, name in files:
            archive.write(source, name)
    with zipfile.ZipFile(target) as archive:
        assert archive.testzip() is None
        dlls = [name for name in archive.namelist() if name.lower().endswith('.dll')]
        assert dlls == [plugin + 'JojoHats.dll']
        assert not any(name.lower().endswith(('.pcab', '.pdb', '.ps1', '.bat', '.cmd')) for name in archive.namelist())
        assert not any(name.lower().startswith('scripts/') for name in archive.namelist())
    print(f'Created {target.name}: {target.stat().st_size:,} bytes, {len(files)} entries')
    print('SHA256 ' + hashlib.sha256(target.read_bytes()).hexdigest())


if __name__ == '__main__':
    main()
