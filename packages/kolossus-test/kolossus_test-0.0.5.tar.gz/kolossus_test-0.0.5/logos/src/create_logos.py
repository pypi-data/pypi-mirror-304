# %%
import pandas as pd
import numpy as np 
import os 
import sys
import logomaker as lm
import matplotlib.pyplot as plt
import logging
from tqdm import tqdm
from IDmapping import main as IDmapping_main
logger = logging.getLogger(__name__)
from pythonjsonlogger import jsonlogger
import json 
from collections import Counter
os.chdir(os.path.dirname(os.path.abspath(__file__)))
print(f'setting working directory to: {(os.path.dirname(os.path.abspath(__file__)))}')

def get_background_distribution(substrates: pd.Index , position=None):
    symbols = ['A', 'R', 'N', 'D', 'C', 'E', 'Q', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']
    bkgrdCount = Counter(dict.fromkeys(symbols, int(0)))
    if position is not None:
        counts = substrates.str.upper().str[position].value_counts().astype(int).to_dict()
        bkgrdCount.update(counts)
    else:
        for i in range(15):
            currcounts = Counter(substrates.str.upper().str[i].value_counts().astype(int).to_dict())
            bkgrdCount = bkgrdCount + currcounts
    return dict(bkgrdCount)

def make_bkgrd_matrix(distributions:dict[dict], position_specific=True):
    dist = {int(pos)-7: distributions[pos] for pos in distributions if pos.isdigit()}
    matrix = pd.DataFrame.from_records(dist).T
    matrix.replace(0, np.NaN, inplace=True)
    bkgrd_probs = get_probability(matrix)
    bkgrd_probs.drop(columns=[x for x in bkgrd_probs if x not in symbols], inplace=True)
    return bkgrd_probs


def assertPhosphosite(kinasename, matrix, accession):
    ## log json = assert positions are correct?
    psite = {site: ratio for site, ratio in matrix.iloc[7].items() if ratio!=0}
    passertion = [duelKinase.loc[accession, 'STYD']]
    ttal = np.fromiter(psite.values(), dtype=float).sum()
    for ps, r in psite.items():
        duelKinase.loc[accession, f'KS_{ps}'] = 100*(r/ttal) ## if ratio is greater than 1 std above mean.
    duelKinase.loc[accession, [x for x in duelKinase.columns if 'KS' in x]] = duelKinase.loc[accession, \
                                                                            [x for x in duelKinase.columns\
                                                                            if 'KS' in x]].fillna(False)


def sanityCheck(kinasedata, pos=0.75):
    posk = kinasedata>= pos
    psiter = {p: 0  for p in ['S','T', 'Y']}
    posi = kinasedata[posk]
    for s, _ in psiter.items():
        posmask = posi.index.str[7].str.lower().str.contains(s.lower())
        pmean = posi[posmask].values.mean()
        psiter[s] = pmean*posmask.sum()
    print('finished!', kinasedata.name)
    logger.info(f'{kinasedata.name}_{pos}p', extra=psiter)
    return


def make_logo(kinasename, matrix, pos, accession):
    set_max = max(matrix.where(matrix >0).sum(axis=1))
    plt.figure(figsize=(42,30))
    COLORSCHEME = 'charge'
    STACKORDER='big_on_top'
    matrix = matrix.apply(lambda x: x.astype(float).fillna(0))
    logo = lm.Logo(matrix, color_scheme = COLORSCHEME,# font_name= 'Arial Rounded MT Bold', 
                        shade_below=0.3,
                        fade_below=0.2, 
                        flip_below=False,
                        # allow_nan=True,
                stack_order=STACKORDER)
    plt.gca().set_facecolor('white')
    plt.gcf().set_facecolor('white')
    plt.gca().set_xlabel('Position', color='black')
    plt.gca().set_ylabel('Relative Entropy', color='black') #
    plt.gcf().suptitle(f'{ORGANISM.capitalize()} kinase {kinasename} Substrate Motif', color='black', fontsize=18, y = 1) ## name to be workshopped
    plt.gca().spines['left'].set_color('black')
    plt.ylim(top=set_max)
    # plt.gca().set_title(f'{accession}',y=0.8 )
    plt.tick_params(axis='both', colors='black')  # Set the tick color
    plt.xticks(color='black')
    plt.yticks(color='black')
    filesave = f'../data/relative_entropy/{ORGANISM}_{str(pos).replace(".", "")}/{kinasename}.png'
    os.makedirs(os.path.dirname(filesave), exist_ok=True)
    plt.savefig(filesave,
            dpi=300, bbox_inches='tight', facecolor='white')
    return f'saved to {filesave}'


def get_probability(matrix):
    frequency = matrix.apply(lambda pos: pos.apply(lambda v: v/pos.sum()), axis=1)
    return frequency


def get_bits(matrix):
    norm = matrix * np.log2(len(matrix.columns) * matrix)
    norm = norm.apply(lambda x : x.astype(float).fillna(0))
    return norm


def scale_phosphosite(matrix): # parsing in KL divergence output
    masked = np.ones(matrix.shape[0], dtype=bool)
    masked[7]  = False  
    mx = (matrix[matrix[masked]>0].sum(axis=1)).max()
    scalar = mx/matrix.iloc[7].sum()
    matrix.iloc[7] = matrix.iloc[7] *scalar
    return matrix 


def kl_divergence(kin_dist, bkgrd_dist):
    significant_probabilities = kin_dist * np.log2(kin_dist/ bkgrd_dist)
    return significant_probabilities


def analyze_eachKinase(kinase, kinasedata, accession, bkgrd, pos=0.75):
    print('evaluating kinase: ', kinase, file=sys.stdout)
    symbols = ['A', 'R', 'N', 'D', 'C', 'E', 'Q', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']
    count = pd.DataFrame(0, columns=symbols, index=range(-7, 8))
    posk = kinasedata[kinasedata>=pos]
    os.makedirs(f'../substrates/{ORGANISM}_{str(pos).replace(".", "")}', exist_ok=True)
    with open(f'../substrates/{ORGANISM}_{str(pos).replace(".", "")}/{kinase}.txt', 'wt') as f:
        for x in posk.index:
            print(f'>{x}', file = f)
            print(f'{x}', file=f)
    valid = posk[posk.index.str[7].str.upper().str.contains(r'S|T|Y')]
    logging.basicConfig(filename=f'{pos}{ORGANISM}.log', level=logging.INFO, format='%(message)s')
    logger.info(f'{kinase}:\tpos_substrates-{posk.shape[0]}')    
    for sub, pred in valid.items():
        for i, aa in enumerate(sub):
            if aa in ['_', 'X']:
                continue
            count.loc[i-7, aa.upper()] += 1*pred ## account for val
    count = count.apply(lambda x: x.astype(float).fillna(0))
    obs_frequency = get_probability(count) # p(i)
    bkgrd_frequency = make_bkgrd_matrix(bkgrd) # q(i)
    ## kl divergence == sum( p(k) * log2(p(k)/q(k)))  , individual is wihtout summation
    klDivergence = kl_divergence(obs_frequency, bkgrd_frequency)
    ## skip for position7
    klDivergence.iloc[7] = obs_frequency.iloc[7]
    scalednp = scale_phosphosite(klDivergence)
    print(make_logo(kinase, scalednp, pos, accession))
    if ORGANISM.lower() == 'human':
        assertPhosphosite(kinase, scalednp, accession)
    sanityCheck(kinasedata)
    return f'made logo for {kinase}'


global ORGANISM
ORGANISM = 'human'
taxID = {'human': 9606, 'mouse': 10090}
infile = f'../data/KS_genome_preds/cleaned_{ORGANISM.lower()}_kinase_substrate_predictions.csv'
data = pd.read_csv(infile, index_col=0)
uniprot2gene = IDmapping_main(data.columns.to_list(), 'UniProtKB_AC-ID', 'Gene_Name')
data = data.rename(columns={x: y for x, y in uniprot2gene.items() if y is not None})
global duelKinase
duelKinase = pd.read_excel(f'../data/Logos_STYE_KinaseNames_finalkeyV2_dualkinases.xlsx', 
                        sheet_name=0, index_col=0)
symbols = ['A', 'R', 'N', 'D', 'C', 'E', 'Q', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']
## get background distributions
if os.path.exists(f'../data/{ORGANISM.lower()}_bkgrdDistrbutions.json'):
    allDistributions = json.load(open(f'../data/{ORGANISM.lower()}_bkgrdDistrbutions.json'))
else:
    print(f'creating background for {ORGANISM}, in file ../data/{ORGANISM.lower()}_bkgrdDistrbutions.json')
    allDistributions= {}
    substrates = data.index[data.index.str[7].str.upper().isin(['S','T','Y'])]
    with open(f'../data/{ORGANISM.lower()}_bkgrdDistrbutions.json', 'w') as writer:
        for ps in range(15):
            allDistributions[str(ps)] = get_background_distribution(substrates, position=ps)
        allDistributions['all']  =  get_background_distribution(substrates, position=None)
        json.dump(allDistributions, writer, indent=4)

logger           = logging.getLogger()
logger.setLevel(logging.INFO)
logHandler       = logging.FileHandler(f'{ORGANISM}.log')
formatter        = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

for i, col in tqdm(enumerate(data.columns), total = len(data.columns)):
    for v, x in enumerate(pd.DataFrame(data[col]).columns):
        if pd.DataFrame(data[col]).iloc[:, v].name not in ['Substrate', 'GENE', 'ACC_ID', 'MOD_RSD']: 
            curracc = [ac for ac, g in uniprot2gene.items() if g == x][v]
            kinasedata = pd.DataFrame(data[col]).iloc[:, v]
            out = analyze_eachKinase(kinasedata.name, kinasedata, curracc, allDistributions)

if ORGANISM.lower() == 'human':
    duelKinase.to_excel('../data/Logos_STYE_KinaseNames_finalkeyV2_dualkinases.xlsx')

