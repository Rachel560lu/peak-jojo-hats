"""Package only this mod's runtime files; never bundle local game/dependency DLLs."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    manifest = json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))
    catalog = json.loads((ROOT / 'assets/catalog.json').read_text(encoding='utf-8'))
    version = manifest['version_number']
    assert version == catalog['version'] == '0.4.2'
    assert len(catalog['hats']) == 6
    dll = ROOT / 'bin/Release/netstandard2.1/JojoHats.dll'
    if not dll.is_file():
        raise SystemExit('Build Release first using scripts/build.ps1.')

    files = [(ROOT / name, name) for name in ('manifest.json', 'icon.png', 'CHANGELOG.md')]
    files.append((ROOT / 'docs/RELEASE-README.md', 'README.md'))
    for name in ('install-jojo-only.ps1', 'allow-empty-bundles.ps1'):
        files.append((ROOT / 'scripts' / name, 'scripts/' + name))
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

    assert len(files) == len({name for _, name in files}) == 21
    for source, _ in files:
        if not source.is_file():
            raise SystemExit(f'Missing required input: {source.relative_to(ROOT)}')
    target = ROOT / 'dist' / f"{manifest['name']}-{version}.zip"
    target.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for source, name in files:
            archive.write(source, name)
    with zipfile.ZipFile(target) as archive:
        assert archive.testzip() is None
        dlls = [name for name in archive.namelist() if name.lower().endswith('.dll')]
        assert dlls == [plugin + 'JojoHats.dll']
        assert not any(name.lower().endswith(('.pcab', '.pdb')) for name in archive.namelist())
    print(f'Created {target.name}: {target.stat().st_size:,} bytes, {len(files)} entries')
    print('SHA256 ' + hashlib.sha256(target.read_bytes()).hexdigest())


if __name__ == '__main__':
    main()
