# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['pl\\savera\\grajdelko\\main\\main.py'],
             pathex=['F:\\grajdelko'],
             binaries=[],
             datas=[('ffmpeg.exe', '.'), ('F:\\grajdelko\\venv\\lib\\site-packages\\discord\\bin\\libopus-0.x64.dll', '.')],
             hiddenimports=['_cffi_backend'],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
