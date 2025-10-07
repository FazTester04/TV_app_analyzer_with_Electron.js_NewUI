import shutil, os
root = os.path.abspath(os.path.dirname(__file__))
out = os.path.join(root, 'tv-test-analyzer-electron.zip')
if os.path.exists(out):
    os.remove(out)
shutil.make_archive('tv-test-analyzer-electron', 'zip', root)
print('Created', out)
