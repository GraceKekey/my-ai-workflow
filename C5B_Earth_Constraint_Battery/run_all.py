"""Regression -> controls -> sequential A-K -> full validation and artifacts."""
import argparse,json,time,unittest,sys
from pathlib import Path
from core import *
from regression import run as regression
from stages import run_stage


def tests():
    suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'),pattern='test_*.py')
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    save_json('results/test_results.json',{'passed':result.wasSuccessful(),'tests_run':result.testsRun,'errors':len(result.errors),'failures':len(result.failures)})
    if not result.wasSuccessful():raise RuntimeError('Tests failed')


def main():
    start=time.time()
    if not regression():raise RuntimeError('QW02 regression failed')
    tests()
    save_json('results/stage_progress.json',[])
    for index in range(1,11):run_stage(index)
    from outputs import finish
    finish(start)

if __name__=='__main__':main()
