"""Build the postcompiler script."""
import os
from pathlib import Path


# Find the BSP transforms from HammerAddons.
try:
    hammer_addons = Path(os.environ['HAMMER_ADDONS']).resolve()
except KeyError:
    hammer_addons = Path('../HammerAddons/').resolve()
if not (hammer_addons / 'transforms').exists():
    raise ValueError(
        f'Invalid BSP transforms location "{hammer_addons}/transforms/"!\n'
        'Clone TeamSpen210/HammerAddons, or set the '
        'environment variable HAMMER_ADDONS to the location.'
    )

DATAS = [
    (str(file), str(file.relative_to(hammer_addons).parent))
    for file in (hammer_addons / 'transforms').rglob('*.py')
] + [
    (str(hammer_addons / 'crowbar_command/Crowbar.exe'), '.'),
    (str(hammer_addons / 'crowbar_command/FluentCommandLineParser.dll'), '.'),
]
print(DATAS)

a_post = Analysis(
    ['srctools/scripts/postcompiler.py'],
    binaries=[],
    datas=DATAS,
    hiddenimports=[
        # Ensure these modules are available for plugins.
        'abc', 'array', 'base64', 'binascii', 'binhex',
        'bisect', 'colorsys', 'collections', 'csv', 'datetime',
        'decimal', 'difflib', 'enum', 'fractions', 'functools',
        'io', 'itertools', 'json', 'math', 'random', 're',
        'statistics', 'string', 'struct', 'srctools',
    ],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    noarchive=False
)

a_fgd = Analysis(
    ['srctools/scripts/fgdfix.py'],
    binaries=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    noarchive=False
)

MERGE((a_post, 'postcompiler', 'postcompiler'), (a_fgd, 'fgdfix', 'fgdfix'))

pyz_post = PYZ(a_post.pure, a_post.zipped_data)
exe_post = EXE(
    pyz_post,
    a_post.scripts,
    [],
    exclude_binaries=True,
    name='postcompiler',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    icon="postcompiler.ico",
)
coll_post = COLLECT(
    exe_post,
    a_post.binaries,
    a_post.zipfiles,
    a_post.datas,
    strip=False,
    upx=True,
    name='postcompiler'
)

pyz_fgd = PYZ(a_fgd.pure, a_fgd.zipped_data)
exe_fgd = EXE(
    pyz_fgd,
    a_fgd.scripts,
    [],
    exclude_binaries=True,
    name='fgdfix',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    icon="postcompiler.ico",
)
coll_fgd = COLLECT(
    exe_fgd,
    a_fgd.binaries,
    a_fgd.zipfiles,
    a_fgd.datas,
    strip=False,
    upx=True,
    name='fgdfix'
)