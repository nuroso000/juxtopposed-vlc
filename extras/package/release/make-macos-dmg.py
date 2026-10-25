#!/usr/bin/env python3
"""Create a drag-to-Applications disk image from a verified macOS app bundle."""
import argparse
import hashlib
import json
from pathlib import Path
import plistlib
import subprocess
import tempfile


def run(*args):
    subprocess.run([str(arg) for arg in args], check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('app', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    source = args.app.resolve(strict=True)
    output = args.output.resolve()
    if source.suffix != '.app' or output.suffix != '.dmg':
        parser.error('Expected an .app input and a .dmg output')
    if output.exists():
        parser.error('The output already exists; choose a new output path')
    run('codesign', '--verify', '--deep', '--strict', source)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='vlc-dmg-') as temporary:
        root = Path(temporary) / 'VLC'
        root.mkdir()
        app = root / 'VLC.app'
        run('ditto', source, app)
        info_path = app / 'Contents/Info.plist'
        with info_path.open('rb') as stream:
            info = plistlib.load(stream)
        info.update(CFBundleName='VLC', CFBundleDisplayName='VLC')
        with info_path.open('wb') as stream:
            plistlib.dump(info, stream)
        # Only the outer bundle metadata changed; retain all nested code seals.
        run('codesign', '--force', '--sign', '-', '--timestamp=none', app)
        run('codesign', '--verify', '--deep', '--strict', app)
        (root / 'Applications').symlink_to('/Applications', target_is_directory=True)
        (root / 'Install VLC.txt').write_text(
            'Install VLC\n\n'
            '1. Quit VLC if it is running.\n'
            '2. Drag VLC.app onto Applications.\n'
            '3. Choose Replace when Finder asks about the existing VLC.app.\n'
            '4. Eject this disk image and open VLC from Applications.\n\n'
            'This replaces the app bundle. It does not remove your media or preferences.\n'
            'This community beta uses ad-hoc signing and is not Apple-notarized.\n',
            encoding='utf-8')
        run('hdiutil', 'create', '-volname', 'VLC', '-srcfolder', root,
            '-fs', 'HFS+', '-format', 'UDZO', output)
    run('hdiutil', 'verify', output)
    digest = hashlib.file_digest(output.open('rb'), 'sha256').hexdigest()
    output.with_suffix('.dmg.sha256').write_text(f'{digest}  {output.name}\n')
    source_commit = (source / 'Contents/Resources/SOURCE_COMMIT.txt').read_text().strip()
    packaging_commit = subprocess.check_output(
        ['git', '-C', str(Path(__file__).resolve().parents[3]), 'rev-parse', 'HEAD'],
        text=True).strip()
    output.with_suffix('.dmg.json').write_text(json.dumps({
        'asset_name': output.name, 'application_name': 'VLC.app',
        'source_commit': source_commit, 'packaging_commit': packaging_commit,
        'source_application': source.name, 'sha256': digest,
        'size': output.stat().st_size, 'installation': 'drag to Applications; confirm Replace',
        'minimum_macos': info['LSMinimumSystemVersion'],
        'signing': 'ad-hoc; no Developer ID or notarization',
    }, indent=2) + '\n')
    print(output)


if __name__ == '__main__':
    main()
