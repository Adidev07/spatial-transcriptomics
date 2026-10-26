
from pathlib import Path
import argparse, json, math, html, os, re
import numpy as np
ROOT=Path(__file__).resolve().parent
def options():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--mode',choices=['fixture','live'],default='fixture',help='Live requires a running local Ollama model for supported projects.')
    p.add_argument('--model',default=os.environ.get('OLLAMA_MODEL',''),help='Installed Ollama model name.')
    p.add_argument('--input',type=Path,help='Optional JSON input matching sample_input.json.')
    p.add_argument('--seed',type=int,default=42)
    return p.parse_args()
def data(args): return json.loads((args.input or ROOT/'sample_input.json').read_text(encoding='utf-8'))
def rmse(y,p): return float(np.sqrt(np.mean((np.asarray(y)-p)**2)))
def classification(y,p):
    y=np.asarray(y);p=np.asarray(p);tp=int(np.sum((y==1)&(p==1)));fp=int(np.sum((y==0)&(p==1)));fn=int(np.sum((y==1)&(p==0)));tn=int(np.sum((y==0)&(p==0)))
    precision=tp/max(1,tp+fp);recall=tp/max(1,tp+fn)
    return dict(accuracy=float(np.mean(y==p)),precision=precision,recall=recall,f1=2*precision*recall/max(1e-15,precision+recall),tp=tp,fp=fp,fn=fn,tn=tn)
def report(title,result,artifacts=None):
    out=ROOT/'results';out.mkdir(exist_ok=True)
    result={'project':title,**result}
    (out/'metrics.json').write_text(json.dumps(result,indent=2,allow_nan=False),encoding='utf-8')
    if artifacts:np.savez_compressed(out/'artifacts.npz',**artifacts)
    cards=[]
    for k,v in result.items():
        if isinstance(v,(int,float)) and not isinstance(v,bool):cards.append('<div class="card">'+html.escape(k.replace('_',' '))+'<b>'+str(round(v,5))+'</b></div>')
    body=html.escape(json.dumps(result,indent=2))
    (out/'report.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+html.escape(title)+'</title><style>body{font:16px system-ui;max-width:1100px;margin:40px auto;padding:20px;background:#101c2f;color:#e8f2ff}h1{color:#8ee7d1}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#182c46;padding:24px;border-radius:12px;line-height:1.5}.cards{display:flex;flex-wrap:wrap;gap:15px}.card{padding:20px;background:#213953;border-radius:10px;min-width:160px}b{display:block;font-size:26px;margin-top:10px}</style><h1>'+html.escape(title)+'</h1><p>Reproducible educational experiment. See README and model card for scope and limitations.</p><div class="cards">'+''.join(cards)+'</div><h2>Complete results</h2><pre>'+body+'</pre></html>',encoding='utf-8')
    print(json.dumps(result,indent=2,allow_nan=False))
def main(run):
    args=options()
    if args.mode=='live' and not run.__globals__['LIVE']:raise SystemExit('This project is a local algorithm experiment; use --mode fixture.')
    result,artifacts=run(data(args),args)
    report(run.__globals__['TITLE'],result,artifacts)

def standardize_fit(x):
    mean=x.mean(axis=0);scale=x.std(axis=0);return mean,np.where(scale<1e-10,1,scale)
def ridge(x,y,alpha=1.):
    z=np.column_stack([np.ones(len(x)),x]);reg=np.eye(z.shape[1])*alpha;reg[0,0]=0
    return np.linalg.solve(z.T@z+reg,z.T@y)
def ridge_predict(w,x):return np.column_stack([np.ones(len(x)),x])@w
def softmax(z):
    v=np.exp(z-z.max(axis=1,keepdims=True));return v/v.sum(axis=1,keepdims=True)
def fit_softmax(x,y,classes,epochs=350):
    z=np.column_stack([np.ones(len(x)),x]);w=np.zeros((z.shape[1],classes));truth=np.eye(classes)[y]
    for _ in range(epochs):w-=.15*(z.T@(softmax(z@w)-truth)/len(y)+.002*w)
    return w
def macro_f1(y,p,classes):return float(np.mean([classification(np.asarray(y)==k,np.asarray(p)==k)['f1'] for k in range(classes)]))
def group_split(groups,heldout):
    groups=np.asarray(groups);test=np.isin(groups,heldout);return np.where(~test)[0],np.where(test)[0]
def log_normalize(counts,target=10000):
    if np.any(counts<0) or counts.ndim!=2:raise ValueError('Nonnegative two-dimensional counts required')
    totals=counts.sum(axis=1,keepdims=True);return np.log1p(counts/np.maximum(totals,1)*target)
