"""Optional public primary-reference retrieval on GitHub; no fitting or credentials."""
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen,Request
from pathlib import Path
import hashlib,json,re
ROOT=Path(__file__).resolve().parent
URLS={'neutrino_primary':'https://arxiv.org/abs/1803.05901','PREM_primary_metadata':'https://ds.iris.edu/ds/products/emc-prem/','PREM_crossref':'https://api.crossref.org/works/10.1016%2F0031-9201%2881%2990046-7','Slichter_crossref':'https://api.crossref.org/works/10.1073%2Fpnas.47.2.186'}

def fetch(item):
    name,url=item
    try:
        with urlopen(Request(url,headers={'User-Agent':'C5B-QW03-reproducible-research/1.0'}),timeout=15) as response:
            raw=response.read(1000000);content_type=response.headers.get('Content-Type','')
        text=raw.decode('utf-8','replace')
        if 'crossref' in name:
            m=json.loads(text)['message'];extract={'title':m.get('title'),'DOI':m.get('DOI'),'authors':[a.get('family') for a in m.get('author',[])]}
        else:
            clean=re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',text))
            # Archive factual provenance, not redundant full webpage/abstract copies.
            channels=[label for pattern,label in [('mass of the Earth','Earth mass'),('moment of inertia','Moment of inertia'),('mass of the Earth&#39;s core','Core mass'),('seismological','Complementarity with seismology')] if re.search(pattern,clean,re.I)]
            extract={'identified_observables':channels,'raw_likelihood_available':False,'numerical_precision_adopted':None}
        return {'name':name,'url':url,'available':True,'sha256':hashlib.sha256(raw).hexdigest(),'content_type':content_type,'extract':extract,'used_for_parameter_fit':False}
    except Exception as e:return {'name':name,'url':url,'available':False,'error':str(e),'used_for_parameter_fit':False}

if __name__=='__main__':
    rows=list(ThreadPoolExecutor(4).map(fetch,URLS.items()))
    (ROOT/'data/source_access_cloud.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps([{'name':a['name'],'available':a['available']} for a in rows]))
