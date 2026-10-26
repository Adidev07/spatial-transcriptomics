"""Estimate masked fictional gene profiles using a spatial kernel and explicitly separate interpolation from extrapolation."""
from kit import *
TITLE='Spatial Gene Expression Interpolation'
LIVE=False

def tissue(seed,n=240):
    rng=np.random.default_rng(seed);xy=rng.uniform(0,1,(n,2));basis=np.column_stack([np.sin(4*xy[:,0]),np.cos(4*xy[:,1]),xy[:,0]*xy[:,1]]);mix=np.random.default_rng(9).normal(size=(3,12));expression=basis@mix+rng.normal(0,.08,(n,12));return xy,expression
def interpolate(ref_xy,ref_y,query,length):
    if length<=0 or len(ref_xy)==0:raise ValueError('Positive scale and observed spots required')
    logits=-np.sum((query[:,None]-ref_xy[None])**2,axis=2)/(2*length**2);weights=softmax(logits);return weights@ref_y
def run(d,a):
    xy,y=tissue(a.seed);candidates=[.05,.1,.2,.4];length=min(candidates,key=lambda l:rmse(y[170:],interpolate(xy[:170],y[:170],xy[170:],l)));xt,yt=tissue(a.seed+1);ref=np.arange(150);masked=np.arange(150,240);edge_ref=np.where(xt[:,0]<.7)[0];edge_test=np.where(xt[:,0]>=.7)[0]
    return dict(selected_length=length,masked_test_rmse=rmse(yt[masked],interpolate(xt[ref],yt[ref],xt[masked],length)),mean_baseline_rmse=rmse(yt[masked],np.tile(yt[ref].mean(axis=0),(len(masked),1))),edge_extrapolation_rmse=rmse(yt[edge_test],interpolate(xt[edge_ref],yt[edge_ref],xt[edge_test],length)),scope='Observed spots on test tissue are allowed references; masked targets remain hidden.'),dict(coordinates=xt,expression=yt,length=np.array(length))

if __name__=="__main__":main(run)
