"""Importa o PREM anterior sem copiar/alterar coeficientes."""
import hashlib
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREM_PATH = ROOT.parent / "c5b_qo" / "study.py"
EXPECTED_SHA256 = "637d641a905960f4c789e0f6327e5a6b0a407c5dde1a4943e8675ef16678c1f1"


def source_hash():
    if not PREM_PATH.is_file():
        raise FileNotFoundError(f"PREM anterior ausente: {PREM_PATH}; não inventar dados.")
    return hashlib.sha256(PREM_PATH.read_bytes()).hexdigest()


spec = importlib.util.spec_from_file_location("qw01_previous_prem", PREM_PATH)
prem = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prem)
G, C, M, R = prem.G, prem.C, prem.M, prem.R


def verify_source():
    if source_hash() != EXPECTED_SHA256:
        raise RuntimeError("O PREM não corresponde ao arquivo anterior fixado neste ensaio.")
    return True
