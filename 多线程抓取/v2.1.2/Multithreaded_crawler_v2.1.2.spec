# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['C:\\Users\\x550\\Desktop\\Multithreaded_crawler_v2.1.2.py'],
             pathex=['C:\\Users\\x550\\AppData\\Local\\Programs\\Python\\Python38\\Lib\\site-packages\\lxml,C:\\Users\\x550\\AppData\\Local\\Programs\\Python\\Python38\\Lib\\site-packages\\bs4,C:\\Users\\x550\\AppData\\Local\\Programs\\Python\\Python38\\Lib\\site-packages\\requests', 'H:\\0_我的\\Python\\网络爬虫\\多线程抓取\\v2.1.2'],
             binaries=[],
             datas=[],
             hiddenimports=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='Multithreaded_crawler_v2.1.2',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , icon='C:\\Users\\x550\\AppData\\Local\\Programs\\Python\\Python38\\DLLs\\py.ico')
