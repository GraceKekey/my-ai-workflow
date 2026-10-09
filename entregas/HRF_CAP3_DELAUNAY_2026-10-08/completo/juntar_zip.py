from pathlib import Path
import hashlib
root = Path(__file__).resolve().parent
parts = sorted(root.glob("HRF_COMPLETO.zip.[0-9][0-9][0-9]"))
if len(parts) != 18:
    raise SystemExit("Baixe as 18 partes na mesma pasta deste script.")
out = root / "HRF_CAP3_DELAUNAY_COMPLETO.zip"
h = hashlib.sha256()
with out.open("wb") as target:
    for p in parts:
        with p.open("rb") as source:
            for block in iter(lambda: source.read(1024*1024), b""):
                target.write(block)
                h.update(block)
if h.hexdigest() != "d29940699b7abda51582963e25350972188bd7b26ed187efe81b3a871c279e1a":
    raise SystemExit("Integridade incorreta: alguma parte está ausente ou danificada.")
print("ZIP completo reconstruído e SHA-256 verificado:", out)
