# -*- mode: python -*-

block_cipher = None


a = Analysis(['ui.py'],
             pathex=['c:\\Program Files (x86)\\Python36-32\\lib', 'C:\\Users\\dimirie\\OneDrive - montgomerycollege.edu\\Coding\\py\\PycharmProjects\\gui_subnet_calc'],
             binaries=[],
             datas=[('logo2.gif', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='ui',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
