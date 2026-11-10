from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
meta=json.loads((root/'RELEASE.json').read_text())
actual={str(p.relative_to(root/'site')) for p in (root/'site').rglob('*') if p.is_file()}
assert actual==set(meta['files']),'Release files differ from approved ledger'
for name,wanted in meta['files'].items():
 p=root/'site'/name
 assert not p.is_symlink(),name
 assert hashlib.sha256(p.read_bytes()).hexdigest()==wanted,name
 assert p.stat().st_size<100*1024*1024,name
assert (root/'site/index.html').is_file()
assert (root/'site/licenses/ReplicaCAD.txt').read_text().startswith('CC BY-NC 4.0')
assert 'CC BY-NC 4.0' in (root/'site/licenses/ATTRIBUTION.txt').read_text()
print('Verified',len(actual),'static files; release',meta['release_id'])
