from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
from matplotlib.colors import ListedColormap, BoundaryNorm
from PIL import Image
import json, textwrap, shutil

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
OUT = ROOT / 'outputs'
FIG = OUT / 'figures'
TAB = OUT / 'tables'
SUPP = OUT / 'supplementary'
for d in [OUT, FIG, TAB, SUPP]: d.mkdir(parents=True, exist_ok=True)

# Theme
NAVY = '#0B1F3A'
BLUE = '#1F5A94'
TEAL = '#1E7A78'
GOLD = '#C99A2E'
LIGHT = '#F4F7FA'
MID = '#D7E2EC'
RED = '#B64B4B'
GREEN = '#3B7D5B'
GRAY = '#667788'
WHITE = '#FFFFFF'

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'axes.titleweight': 'bold',
    'axes.titlesize': 13,
    'axes.labelsize': 10,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
})

integrated = pd.read_csv(DATA/'standardized_integrated_evidence_matrix.csv')
secure = pd.read_csv(DATA/'adjudicated_consensus_quality.csv')
sens = pd.read_csv(DATA/'sensitivity_consensus_scores.csv')
domain = pd.read_csv(DATA/'domain_profile.csv')
prisma = pd.read_csv(DATA/'prisma_operational_accounting.csv')
taxonomy = pd.read_csv(DATA/'reliability_taxonomy.csv')
sensitivity = pd.read_csv(DATA/'sensitivity_analysis_summary.csv')
reviews = pd.read_csv(DATA/'pilot_competing_reviews.csv')
quality_secure = secure.copy()
quality_sens = sens[['title','year','doi']+[f'Q{i}' for i in range(1,13)]+['consensus_total','consensus_band']].copy()
quality_sens = quality_sens.rename(columns={'title':'study'})
quality_all = pd.concat([quality_secure, quality_sens], ignore_index=True, sort=False)
quality_all['study_id'] = [f'S{i:02d}' for i in range(1,len(quality_all)+1)]

# Consolidate model families for visual taxonomy.
def broad_family(x):
    s = str(x).lower()
    if 'cnn' in s or 'convolution' in s: return 'CNN / convolutional hybrids'
    if 'transformer' in s: return 'Transformers / global-local hybrids'
    if 'graph' in s: return 'Graph / relational models'
    if 'gan' in s or 'generative' in s: return 'Generative / anomaly models'
    if 'autoencoder' in s or 'representation' in s or 'self-organizing' in s: return 'Autoencoder / representation learning'
    if 'ensemble' in s or 'boosting' in s or 'forest' in s: return 'Ensemble / boosting'
    if 'semi-supervised' in s or 'positive-unlabeled' in s or 'positive-unlabelled' in s: return 'PU / semi-supervised learning'
    if 'bayesian' in s or 'uncertainty' in s: return 'Bayesian / uncertainty-aware'
    if 'causal' in s: return 'Causal-aware models'
    if 'direction' in s: return 'Direction-aware models'
    return 'Other workflow / ML-DL studies'

integrated['broad_model_family'] = integrated['model_family'].map(broad_family)

# ---------- Graphical abstract ----------
fig, ax = plt.subplots(figsize=(16, 6.4), dpi=150)
ax.set_xlim(0, 16); ax.set_ylim(0, 6.4); ax.axis('off')
ax.add_patch(Rectangle((0,0),16,6.4,facecolor=LIGHT,edgecolor='none'))
ax.add_patch(FancyBboxPatch((0.35,5.55),15.3,0.55,boxstyle='round,pad=0.02,rounding_size=0.08',facecolor=NAVY,edgecolor=NAVY))
ax.text(8,5.83,'From architecture-first benchmarking to trustworthy mineral prospectivity mapping',ha='center',va='center',color=WHITE,fontsize=16,fontweight='bold')
steps = [
    ('Geoscience evidence','geology • geochemistry\ngeophysics • remote sensing'),
    ('Label audit','positive • negative\nunlabeled • bias'),
    ('Learning strategy','supervised • PU • SSL\ntransfer • unsupervised'),
    ('Spatial validation','random baseline → blocks\nclusters → external area'),
    ('Calibration & UQ','Brier • entropy • ensemble\nstability • workflow variance'),
    ('Geological trust','attribution • constraints\nfield consistency'),
    ('Decision-ready map','calibrated ranking\nuncertainty + target efficiency'),
]
xs = np.linspace(1.2,14.8,len(steps))
for i,((title,sub),x) in enumerate(zip(steps,xs),1):
    ax.add_patch(FancyBboxPatch((x-0.82,2.55),1.64,1.55,boxstyle='round,pad=0.05,rounding_size=0.12',facecolor=WHITE,edgecolor=BLUE,linewidth=1.8))
    ax.add_patch(Circle((x,3.75),0.22,facecolor=GOLD,edgecolor='none'))
    ax.text(x,3.75,str(i),ha='center',va='center',fontsize=10,fontweight='bold',color=NAVY)
    ax.text(x,3.42,title,ha='center',va='center',fontsize=10,fontweight='bold',color=NAVY)
    ax.text(x,2.95,sub,ha='center',va='center',fontsize=8.2,color=GRAY)
    if i < len(steps):
        ax.add_patch(FancyArrowPatch((x+0.86,3.33),(xs[i]-0.86,3.33),arrowstyle='-|>',mutation_scale=15,linewidth=1.6,color=TEAL))
cards = [('32','primary studies'),('4','strong spatial validation'),('25','no demonstrated spatial independence'),('6','strong label validity'),('9','strong calibration/UQ')]
card_x = np.linspace(1.3,14.7,len(cards))
for (num,label),x in zip(cards,card_x):
    ax.add_patch(FancyBboxPatch((x-1.05,0.65),2.1,0.95,boxstyle='round,pad=0.04,rounding_size=0.08',facecolor=NAVY,edgecolor='none'))
    ax.text(x,1.22,num,ha='center',va='center',fontsize=19,fontweight='bold',color=GOLD)
    ax.text(x,0.88,label,ha='center',va='center',fontsize=8.5,color=WHITE)
ax.text(8,0.25,'Eight-stage framework + minimum reporting standard for reliable, transferable and reproducible MPM',ha='center',va='center',fontsize=11,fontweight='bold',color=GREEN)
fig.tight_layout(pad=0)
ga_png = FIG/'Graphical_Abstract_2400x960.png'
fig.savefig(ga_png,dpi=150,bbox_inches='tight',pad_inches=0)
fig.savefig(FIG/'Graphical_Abstract.pdf',bbox_inches='tight',pad_inches=0)
plt.close(fig)
im = Image.open(ga_png).convert('RGB').resize((2400,960),Image.Resampling.LANCZOS)
im.save(FIG/'Graphical_Abstract_2400x960_300dpi.tif',dpi=(300,300),compression='tiff_lzw')
im.save(ga_png,dpi=(300,300))

# ---------- Figure 1 PRISMA ----------
fig, ax = plt.subplots(figsize=(9, 11), dpi=160)
ax.set_xlim(0,10); ax.set_ylim(0,14); ax.axis('off')
ax.text(5,13.55,'Study identification, screening and evidence architecture',ha='center',fontsize=15,fontweight='bold',color=NAVY)
boxes = [
    (5,12.4, '85 records/manifestations identified', '68 public-source + 9 recovery + 8 sensitivity'),
    (5,10.8, '10 duplicate/version manifestations removed', ''),
    (5,9.2, '75 unique records screened', ''),
    (2.5,7.5,'5 reviews diverted','competing-review inventory'),
    (5,7.5,'67 records retained','evidence architecture'),
    (7.5,7.5,'3 records not in primary corpus','2 out-of-domain + 1 watchlist'),
    (2.4,5.7,'25 secure core','method/results screened'),
    (5,5.7,'7 provisional core','not claim-bearing'),
    (7.6,5.7,'28 context/bridge','taxonomy and citation recovery'),
    (5,3.8,'7 current sensitivity additions','independently rescored'),
    (5,2.0,'32 integrated primary studies','manuscript synthesis'),
]
for x,y,t,s in boxes:
    w = 3.5 if y>=9 else (3.0 if y>=5 else 4.0)
    h = 1.0
    face = WHITE if y>2.1 else NAVY
    edge = BLUE if y>2.1 else NAVY
    ax.add_patch(FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle='round,pad=0.03,rounding_size=0.06',facecolor=face,edgecolor=edge,linewidth=1.6))
    ax.text(x,y+0.12,t,ha='center',va='center',fontsize=10,fontweight='bold',color=WHITE if y<=2.1 else NAVY)
    if s: ax.text(x,y-0.22,s,ha='center',va='center',fontsize=8,color=WHITE if y<=2.1 else GRAY)
for y1,y2 in [(11.9,11.3),(10.3,9.7)]:
    ax.add_patch(FancyArrowPatch((5,y1),(5,y2),arrowstyle='-|>',mutation_scale=14,color=TEAL,linewidth=1.5))
ax.add_patch(FancyArrowPatch((5,8.7),(5,8.05),arrowstyle='-|>',mutation_scale=14,color=TEAL,linewidth=1.5))
for x in [2.5,7.5]: ax.add_patch(FancyArrowPatch((5,8.7),(x,8.05),arrowstyle='-|>',mutation_scale=14,color=GRAY,linewidth=1.2))
for x in [2.4,5,7.6]: ax.add_patch(FancyArrowPatch((5,7.0),(x,6.25),arrowstyle='-|>',mutation_scale=14,color=TEAL,linewidth=1.4))
ax.add_patch(FancyArrowPatch((2.4,5.15),(4.35,4.25),arrowstyle='-|>',mutation_scale=14,color=TEAL,linewidth=1.4))
ax.add_patch(FancyArrowPatch((5,5.15),(5,4.35),arrowstyle='-|>',mutation_scale=14,color=TEAL,linewidth=1.4))
ax.add_patch(FancyArrowPatch((5,3.25),(5,2.55),arrowstyle='-|>',mutation_scale=14,color=TEAL,linewidth=1.6))
fig.tight_layout()
fig.savefig(FIG/'Figure_1_PRISMA_Flow.png',dpi=300,bbox_inches='tight')
fig.savefig(FIG/'Figure_1_PRISMA_Flow.pdf',bbox_inches='tight')
plt.close(fig)

# ---------- Figure 2 timeline ----------
years = sorted(integrated.year.astype(int).unique())
counts = integrated.year.astype(int).value_counts().sort_index()
full_years = list(range(min(years),max(years)+1))
vals = [int(counts.get(y,0)) for y in full_years]
cum = np.cumsum(vals)
fig, ax1 = plt.subplots(figsize=(10,5.8),dpi=160)
ax1.bar(full_years, vals, color=BLUE, edgecolor=NAVY, linewidth=0.6)
ax1.set_ylabel('Studies published per year')
ax1.set_xlabel('Publication year')
ax1.set_xticks(full_years)
ax1.grid(axis='y',alpha=0.2)
ax2=ax1.twinx(); ax2.plot(full_years,cum,marker='o',color=GOLD,linewidth=2.4); ax2.set_ylabel('Cumulative integrated studies')
for x,v in zip(full_years,vals):
    if v: ax1.text(x,v+0.3,str(v),ha='center',fontsize=8,fontweight='bold')
ax1.set_title('Rapid acceleration of deep-learning MPM evidence (2019–2026)')
fig.tight_layout()
fig.savefig(FIG/'Figure_2_Publication_Timeline.png',dpi=300,bbox_inches='tight')
fig.savefig(FIG/'Figure_2_Publication_Timeline.pdf',bbox_inches='tight')
plt.close(fig)

# ---------- Figure 3 reliability heatmap ----------
Q=[f'Q{i}' for i in range(1,13)]
mat=quality_all[Q].astype(int).values
rowlabels=[f"{sid} | {yr}" for sid,yr in zip(quality_all.study_id,quality_all.year)]
cmap=ListedColormap(['#E8B4B4','#F4D37A','#7BC5A5'])
norm=BoundaryNorm([-0.5,0.5,1.5,2.5],3)
fig, ax = plt.subplots(figsize=(12,11),dpi=160)
im=ax.imshow(mat,aspect='auto',cmap=cmap,norm=norm)
ax.set_xticks(range(12)); ax.set_xticklabels(Q,fontweight='bold')
ax.set_yticks(range(len(rowlabels))); ax.set_yticklabels(rowlabels,fontsize=7)
ax.set_xlabel('Reliability-appraisal domains (see Table 3)')
ax.set_title('Study-level trustworthiness matrix: strong methods are unevenly distributed')
for i in range(mat.shape[0]):
    for j in range(mat.shape[1]):
        ax.text(j,i,str(mat[i,j]),ha='center',va='center',fontsize=6.3,color=NAVY)
cbar=fig.colorbar(im,ax=ax,fraction=0.025,pad=0.02,ticks=[0,1,2]); cbar.ax.set_yticklabels(['Absent','Partial','Strong'])
ax.set_xticks(np.arange(-.5,12,1),minor=True); ax.set_yticks(np.arange(-.5,len(rowlabels),1),minor=True)
ax.grid(which='minor',color='white',linewidth=0.45); ax.tick_params(which='minor',bottom=False,left=False)
fig.tight_layout()
fig.savefig(FIG/'Figure_3_Reliability_Heatmap.png',dpi=300,bbox_inches='tight')
fig.savefig(FIG/'Figure_3_Reliability_Heatmap.pdf',bbox_inches='tight')
plt.close(fig)

# ---------- Figure 4 taxonomy ----------
family = integrated.broad_model_family.value_counts()
regime = integrated.learning_regime.copy()
def broad_regime(x):
    s=str(x).lower()
    if 'unsupervised' in s or 'anomaly' in s: return 'Unsupervised / anomaly / representation'
    if 'semi-supervised' in s or 'weak supervision' in s or 'positive' in s: return 'Semi-supervised / PU'
    if 'transfer' in s or 'fine-tuning' in s: return 'Transfer / regional refinement'
    if 'bayesian' in s or 'stochastic' in s: return 'Bayesian / stochastic'
    if 'ensemble' in s: return 'Supervised ensemble'
    return 'Supervised / hybrid'
reg=regime.map(broad_regime).value_counts()
fig, (ax1,ax2)=plt.subplots(1,2,figsize=(13,6),dpi=160)
wedges,texts,autotexts=ax1.pie(family.values,labels=None,autopct=lambda p:f'{p:.0f}%' if p>=6 else '',startangle=90,pctdistance=0.75,wedgeprops={'width':0.42,'edgecolor':'white'})
ax1.legend(wedges,[f'{k} (n={v})' for k,v in family.items()],loc='center left',bbox_to_anchor=(0.93,0.5),fontsize=8,frameon=False)
ax1.set_title('Model-family taxonomy')
reg=reg.sort_values()
ax2.barh(reg.index,reg.values,color=TEAL,edgecolor=NAVY,linewidth=0.5)
for y,v in enumerate(reg.values): ax2.text(v+0.15,y,str(v),va='center',fontweight='bold')
ax2.set_xlabel('Number of studies'); ax2.set_title('Learning regimes')
ax2.grid(axis='x',alpha=0.2)
fig.suptitle('Method diversity is high, but validation strength is not',fontsize=15,fontweight='bold',color=NAVY)
fig.tight_layout()
fig.savefig(FIG/'Figure_4_Model_and_Learning_Taxonomy.png',dpi=300,bbox_inches='tight')
fig.savefig(FIG/'Figure_4_Model_and_Learning_Taxonomy.pdf',bbox_inches='tight')
plt.close(fig)

# ---------- Figure 5 validation hierarchy ----------
validation_order=['Strong spatial/cross-cluster','Partial/spatially aware','Random/within-area or not demonstrated']
vc=integrated.validation_class.value_counts()
vals=[int(vc.get(x,0)) for x in validation_order]
fig, ax=plt.subplots(figsize=(10,5.5),dpi=160)
bars=ax.bar(['Strong spatial / cross-cluster','Partial spatial awareness','Random / within-area only'],vals,color=[GREEN,GOLD,RED],edgecolor=NAVY,linewidth=0.8)
for b,v in zip(bars,vals): ax.text(b.get_x()+b.get_width()/2,v+0.35,str(v),ha='center',fontweight='bold',fontsize=12)
ax.set_ylabel('Number of studies'); ax.set_ylim(0,max(vals)+4); ax.grid(axis='y',alpha=0.2)
ax.set_title('Validation hierarchy and permissible strength of generalization claims')
ax.text(0,0.8,'Geographic transfer claims\ncan be supported',ha='center',fontsize=9,color=GREEN,fontweight='bold')
ax.text(1,0.8,'Conditional / local\nspatial extrapolation',ha='center',fontsize=9,color='#8A6A12',fontweight='bold')
ax.text(2,0.8,'Within-area performance only;\ntransfer not demonstrated',ha='center',fontsize=9,color=RED,fontweight='bold')
fig.tight_layout()
fig.savefig(FIG/'Figure_5_Validation_Hierarchy.png',dpi=300,bbox_inches='tight')
fig.savefig(FIG/'Figure_5_Validation_Hierarchy.pdf',bbox_inches='tight')
plt.close(fig)

# ---------- Figure 6 domain coverage ----------
labels=domain.domain.tolist()
strong=domain.secure_strong_count.tolist()
partial=domain.secure_partial_count.tolist()
absent=domain.secure_absent_count.tolist()
y=np.arange(len(labels))
fig, ax=plt.subplots(figsize=(12,7.5),dpi=160)
ax.barh(y,strong,label='Strong',color=GREEN)
ax.barh(y,partial,left=strong,label='Partial',color=GOLD)
left2=np.array(strong)+np.array(partial)
ax.barh(y,absent,left=left2,label='Absent',color=RED)
ax.set_yticks(y); ax.set_yticklabels(labels,fontsize=8.4); ax.invert_yaxis(); ax.set_xlim(0,25)
ax.set_xlabel('Secure-core studies (n=25)'); ax.legend(ncol=3,loc='lower right'); ax.grid(axis='x',alpha=0.15)
ax.set_title('Reliability-domain coverage: documentation is strong upstream, weak at deployment gates')
fig.tight_layout()
fig.savefig(FIG/'Figure_6_Reliability_Domain_Coverage.png',dpi=300,bbox_inches='tight')
fig.savefig(FIG/'Figure_6_Reliability_Domain_Coverage.pdf',bbox_inches='tight')
plt.close(fig)

# ---------- Figure 7 competing review novelty matrix ----------
dims=['Architecture\ntaxonomy','Multisource\ndata','Scarcity &\nimbalance','Label\nvalidity','Spatial\nvalidation','Calibration\n& UQ','Transferability','Reproducibility','Claim-control\nframework']
review_names=['Yuan et al.\n2026','Sun et al.\n2024','Yang et al.\n2024','Lee & Moon\n2026','This review']
matrix=np.array([[2,2,2,1,1,1,1,1,0],[2,2,2,1,1,1,0,1,0],[2,2,2,1,1,1,1,1,0],[2,2,2,1,1,1,1,1,0],[1,2,2,2,2,2,2,2,2]])
cmap2=ListedColormap(['#EEF2F6','#F4D37A','#4E9F78']); norm2=BoundaryNorm([-0.5,0.5,1.5,2.5],3)
fig, ax=plt.subplots(figsize=(13,5),dpi=160)
im=ax.imshow(matrix,cmap=cmap2,norm=norm2,aspect='auto')
ax.set_xticks(range(len(dims))); ax.set_xticklabels(dims,fontsize=8)
ax.set_yticks(range(len(review_names))); ax.set_yticklabels(review_names,fontsize=9)
for i in range(matrix.shape[0]):
  for j in range(matrix.shape[1]): ax.text(j,i,['—','●','●●'][matrix[i,j]],ha='center',va='center',fontsize=10,color=NAVY)
ax.set_title('Competing-review landscape: novelty lies in operationalizing the full reliability chain')
cbar=fig.colorbar(im,ax=ax,fraction=0.025,pad=0.02,ticks=[0,1,2]); cbar.ax.set_yticklabels(['Not central','Discussed','Operationalized'])
fig.tight_layout()
fig.savefig(FIG/'Figure_7_Review_Novelty_Landscape.png',dpi=300,bbox_inches='tight')
fig.savefig(FIG/'Figure_7_Review_Novelty_Landscape.pdf',bbox_inches='tight')
plt.close(fig)

# ---------- Figure 8 framework + case-study translation ----------
fig, ax=plt.subplots(figsize=(12,9),dpi=160)
ax.set_xlim(0,12); ax.set_ylim(0,9); ax.axis('off')
ax.text(6,8.62,'Trustworthy MPM: eight reliability gates and their Chahargonbad experiment',ha='center',fontsize=15,fontweight='bold',color=NAVY)
stages=[('1','Problem & target domain','Porphyry-Cu decision scale; deployment domain'),('2','Evidence & label audit','Layer provenance; positive/negative/unlabeled designs'),('3','Scarcity strategy','Real-only vs augmentation vs PU/SSL/transfer'),('4','Architecture & fusion','ML baselines; CNN/DL; input and architecture ablations'),('5','Spatial validation','Random baseline; spatial blocks; deposit/cluster holdout'),('6','Calibration & uncertainty','Brier/calibration; ensembles; repeated-run stability'),('7','Geological consistency','Attribution; mineral-system checks; field evidence'),('8','Reproducibility','Code, folds, seeds, registries, checksums and release')]
ys=np.linspace(7.7,1.0,len(stages))
for num,t,s in stages:
    y=ys[int(num)-1]
    ax.add_patch(Circle((1.0,y),0.32,facecolor=GOLD,edgecolor=NAVY,linewidth=1))
    ax.text(1.0,y,num,ha='center',va='center',fontweight='bold',color=NAVY)
    ax.add_patch(FancyBboxPatch((1.55,y-0.42),3.5,0.84,boxstyle='round,pad=0.03,rounding_size=0.06',facecolor=WHITE,edgecolor=BLUE,linewidth=1.4))
    ax.text(1.75,y+0.12,t,ha='left',va='center',fontweight='bold',fontsize=10,color=NAVY)
    ax.text(1.75,y-0.17,s,ha='left',va='center',fontsize=8.2,color=GRAY)
    ax.add_patch(FancyArrowPatch((5.2,y),(6.25,y),arrowstyle='-|>',mutation_scale=15,color=TEAL,linewidth=1.3))
    ax.add_patch(FancyBboxPatch((6.4,y-0.42),4.6,0.84,boxstyle='round,pad=0.03,rounding_size=0.06',facecolor=LIGHT,edgecolor=TEAL,linewidth=1.2))
    right=['Freeze geological question and evaluation domain','Build auditable layer and label registries','Use identical folds and tuning budgets across scarcity regimes','Promote complexity only after stable spatial improvement','Separate interpolation from geographic generalization','Deliver prospectivity + uncertainty + target-area efficiency','Check stable explanations against porphyry-system expectations','Release executable package and decision logs'][int(num)-1]
    ax.text(6.65,y,right,ha='left',va='center',fontsize=8.8,color=NAVY)
ax.text(6,0.35,'Outcome: a decision-ready prospectivity product whose performance, uncertainty and deployment limits are explicit',ha='center',fontsize=10.5,fontweight='bold',color=GREEN)
fig.tight_layout()
fig.savefig(FIG/'Figure_8_Trustworthy_MPM_Framework.png',dpi=300,bbox_inches='tight')
fig.savefig(FIG/'Figure_8_Trustworthy_MPM_Framework.pdf',bbox_inches='tight')
plt.close(fig)

# ---------- Supplementary figures ----------
fig, ax=plt.subplots(figsize=(9,5.5),dpi=160)
ax.scatter(quality_all.year,quality_all.consensus_total,s=65,alpha=0.8,edgecolor=NAVY,linewidth=0.5)
for _,r in quality_all.iterrows(): ax.text(r.year+0.03,r.consensus_total+0.08,r.study_id,fontsize=6.5)
ax.set_xlabel('Publication year'); ax.set_ylabel('Consensus quality score (0–24)'); ax.set_ylim(7,24.5); ax.grid(alpha=0.2)
ax.set_title('Methodological support does not increase uniformly with publication year')
fig.tight_layout(); fig.savefig(FIG/'Figure_S1_Quality_vs_Year.png',dpi=300,bbox_inches='tight'); plt.close(fig)

ct=pd.crosstab(integrated.broad_model_family,integrated.validation_class)
ct=ct.reindex(columns=validation_order,fill_value=0)
fig,ax=plt.subplots(figsize=(10,7),dpi=160)
im=ax.imshow(ct.values,cmap='Blues',aspect='auto')
ax.set_xticks(range(len(ct.columns))); ax.set_xticklabels(['Strong','Partial','Random/within-area'],fontsize=8)
ax.set_yticks(range(len(ct.index))); ax.set_yticklabels(ct.index,fontsize=8)
for i in range(ct.shape[0]):
  for j in range(ct.shape[1]): ax.text(j,i,str(ct.iat[i,j]),ha='center',va='center',fontsize=8,color=NAVY)
ax.set_title('Model-family richness is concentrated in weak validation settings')
fig.colorbar(im,ax=ax,fraction=0.025,pad=0.02)
fig.tight_layout(); fig.savefig(FIG/'Figure_S2_Model_Family_by_Validation.png',dpi=300,bbox_inches='tight'); plt.close(fig)

fig, ax=plt.subplots(figsize=(11,6),dpi=160)
scens=sensitivity.scenario_id.tolist(); x=np.arange(len(scens)); width=0.17
metrics=[('strong_spatial_validation','Strong spatial'),('no_spatial_independence','No spatial independence'),('strong_label_validity','Strong labels'),('strong_calibration_uq','Strong UQ')]
for k,(col,label) in enumerate(metrics): ax.bar(x+(k-1.5)*width,sensitivity[col].astype(int),width,label=label)
ax.set_xticks(x); ax.set_xticklabels(scens,rotation=20,ha='right'); ax.set_ylabel('Studies'); ax.legend(ncol=2); ax.grid(axis='y',alpha=0.2)
ax.set_title('Headline conclusions remain stable across sensitivity scenarios')
fig.tight_layout(); fig.savefig(FIG/'Figure_S3_Sensitivity_Scenarios.png',dpi=300,bbox_inches='tight'); plt.close(fig)

bands=quality_all.consensus_band.value_counts().reindex(['HIGH_SUPPORT','MODERATE_SUPPORT','LOW_SUPPORT'],fill_value=0)
fig, ax=plt.subplots(figsize=(7,5),dpi=160)
ax.bar(['High','Moderate','Low'],bands.values,color=[GREEN,GOLD,RED],edgecolor=NAVY)
for i,v in enumerate(bands.values): ax.text(i,v+0.25,str(v),ha='center',fontweight='bold')
ax.set_ylabel('Studies'); ax.set_title('Methodological-support bands in the integrated corpus'); ax.grid(axis='y',alpha=0.2)
fig.tight_layout(); fig.savefig(FIG/'Figure_S4_Quality_Bands.png',dpi=300,bbox_inches='tight'); plt.close(fig)

# ---------- Tables ----------
corpus_rows=[('Records/manifestations identified',85),('Duplicate/version manifestations removed',10),('Unique records screened',75),('Competing reviews',5),('Secure claim-bearing studies',25),('Sensitivity additions',7),('Integrated primary studies',32),('Context/bridge records',28)]
pd.DataFrame(corpus_rows,columns=['Item','Count']).to_csv(TAB/'Table_1_Corpus_and_Selection.csv',index=False)
fam=integrated.broad_model_family.value_counts().rename_axis('Model family').reset_index(name='Studies')
fam['Share_%']=(fam.Studies/32*100).round(1)
fam.to_csv(TAB/'Table_2_Model_Taxonomy.csv',index=False)
cols=['domain_id','domain','secure_mean','secure_strong_count','secure_partial_count','secure_absent_count','interpretation']
domain[cols].to_csv(TAB/'Table_3_Reliability_Domain_Profile.csv',index=False)
valdf=pd.DataFrame({'Validation class':validation_order,'Studies':[vc.get(v,0) for v in validation_order],'Permitted claim':['Geographic/cross-cluster generalization','Conditional local spatial extrapolation','Within-area prediction only']})
valdf.to_csv(TAB/'Table_4_Validation_Hierarchy.csv',index=False)
strategies=[('Random/distance negatives','Simple supervised baseline','Label crossover; arbitrary buffers','Negative-sampling sensitivity and spatial continuity'),('Positive–unlabeled learning','Background treated as unlabeled','Class-prior and selection assumptions','AUPRC, Brier score, pseudo-negative stability'),('Recursive/dynamic annotation','Iterative negative refinement','Error reinforcement','Map continuity and iteration stability'),('Augmentation / SMOTE / GAN','Increase minority representation','Synthetic leakage and unrealistic samples','Fold-contained generation and realism checks'),('Semi-supervised anomaly learning','Use scarce positives and abundant unlabeled data','Unlabeled-domain bias','Spatially independent validation'),('Transfer / regional fine-tuning','Reuse source-domain representations','Covariate and concept shift','External target-domain test'),('Unsupervised representation learning','Avoid explicit negative labels','Evaluation still depends on known occurrences','Independent target-efficiency analysis')]
pd.DataFrame(strategies,columns=['Strategy','Primary purpose','Principal risk','Minimum evidence']).to_csv(TAB/'Table_5_Label_and_Scarcity_Strategies.csv',index=False)
uq=[('Calibration curves / Brier score','Probability reliability','Rare'),('Bayesian / MC dropout','Epistemic model uncertainty','Limited'),('Ensemble dispersion','Model variability','Emerging'),('Workflow perturbation','Pipeline stability','Limited'),('Repeated resampling','Repeatability','Emerging'),('Entropy / confidence maps','Prediction ambiguity','Emerging'),('Target-area efficiency','Exploration decision efficiency','Moderate')]
pd.DataFrame(uq,columns=['Practice','Decision question','Observed maturity']).to_csv(TAB/'Table_6_Uncertainty_Calibration_Practices.csv',index=False)
reporting=[('Geological decision problem','Deposit model, scale, spatial unit, deployment domain','No transfer/operational claim'),('Evidence provenance','Source, date, resolution, preprocessing, alignment','No reproducibility/input-comparability claim'),('Positive labels','Definition, source, representativeness, clustering','No class-validity claim'),('Negative/unlabeled samples','Sampling rule, buffers, PU/one-class assumptions, sensitivity','No reliable supervised-performance claim'),('Scarcity strategy','Rationale and leakage safeguards','No scarcity-robustness claim'),('Validation geometry','Random baseline plus blocks/clusters/area/external test','No geographic-generalization claim'),('Tuning/test separation','Nested or strict held-out test','No unbiased-performance claim'),('Decision metrics','Discrimination plus P–A/target-area efficiency','No exploration-utility claim'),('Calibration and uncertainty','Calibration/Brier plus uncertainty/stability','No probability-prioritization claim'),('Geological consistency','Attribution/ablation checked against independent geology','No mechanistic-interpretation claim'),('Reproducibility','Code, data lineage, folds, parameters, seeds, versions','No independent-replication claim')]
pd.DataFrame(reporting,columns=['Reporting item','Minimum requirement','Claim restricted if absent']).to_csv(TAB/'Table_7_Minimum_Reporting_Standard.csv',index=False)
translation=[('Evidence selection','Expert-selected layers vs full stack','Identical spatial folds and tuning budget','Generalization + target-area efficiency'),('Label design','Random negatives vs buffered vs PU/unlabeled','Same positives; repeated negative designs','Variance, continuity, calibration'),('Scarcity','Real-only vs augmentation vs SSL/PU/transfer','Augmentation inside training folds only','AUPRC, Brier, spatial test'),('Architecture','Transparent ML vs CNN/DL/graph/transformer','Fair baselines and ablations','Promotion only after stable spatial gain'),('Validation','Random, spatial blocks, deposit/cluster holdout, external area','Nested tuning','Transfer hierarchy'),('Uncertainty','Ensembles, MC dropout, workflow sensitivity','Repeated seeds and folds','Prospectivity + uncertainty products'),('Geological consistency','Attribution and mineral-system checks','Stable across folds','Field and deposit-model agreement'),('Reproducibility','Frozen registries, seeds, manifests, checksums','One-command rebuild','Auditable case-study package')]
pd.DataFrame(translation,columns=['Design axis','Required comparison','Control','Decision output']).to_csv(TAB/'Table_8_Chahargonbad_Case_Study_Translation.csv',index=False)

integrated.to_csv(SUPP/'Table_S1_Integrated_Study_Characteristics_32.csv',index=False)
quality_all.to_csv(SUPP/'Table_S2_Full_Quality_Matrix_32.csv',index=False)
pd.read_csv(DATA/'search_query_register.csv').to_csv(SUPP/'Table_S3_Search_Query_Register.csv',index=False)
pd.read_csv(DATA/'full_text_exclusion_register.csv').to_csv(SUPP/'Table_S4_Excluded_Studies.csv',index=False)
pd.read_csv(DATA/'sensitivity_analysis_summary.csv').to_csv(SUPP/'Table_S5_Sensitivity_Analysis.csv',index=False)
pd.read_csv(DATA/'reconciled_reference_register.csv').to_csv(SUPP/'Table_S6_Reference_Register.csv',index=False)
meta={'main_figures':8,'main_tables':8,'supplementary_figures':4,'supplementary_tables':8,'graphical_abstract_pixels':[2400,960],'graphical_abstract_dpi':300,'integrated_studies':32,'secure_core':25,'sensitivity_additions':7}
(OUT/'visual_assets_manifest.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
print('Visual assets created in', OUT)
