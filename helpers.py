import pandas as pd
import tree


def calculate_result(df):
    ti_len = len(df['ti'])
    prods = {"ε1":[tree.sum_product(df, 'pti', 'ε1')], 
             "ε2":[tree.sum_product(df, 'pti', 'ε2')],
             "ε3":[tree.sum_product(df, 'pti', 'ε3')]}
    for eps in range(1, len(prods)+1):
        for ti in range(0, ti_len):
            prods[f"ε{eps}"].append(df['pti'][ti]*df[f'ε{eps}'][ti]/prods[f"ε{eps}"][0])
    
    df = pd.DataFrame(prods).T.round(4).reset_index()
    df.columns = ['ε', 'p(ε)'] + [f'ϑ{x+1}' for x in range(ti_len)]
    return df

def parse(el):
    return float(el.get('data').get('label'))
