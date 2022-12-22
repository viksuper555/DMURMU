import pandas as pd

VCount = 2

def get_nodes():
    nodes = [
    {
        'data': {'id': short, 'label': label},
        'position': {'x': 20 * lat, 'y': -20 * long}
    }
    for short, label, long, lat in (
        ('la', 'Los Angeles', 34.03, -118.25),
        ('nyc', 'New York', 40.71, -74),
        ('to', 'Toronto', 43.65, -79.38),
        ('mtl', 'Montreal', 45.50, -73.57),
        ('van', 'Vancouver', 49.28, -123.12),
        ('chi', 'Chicago', 41.88, -87.63),
        ('bos', 'Boston', 42.36, -71.06),
        ('hou', 'Houston', 29.76, -95.37)
    )]
    return nodes

def get_edges():
    edges = [
        {'data': {'source': source, 'target': target}}
        for source, target in (
            ('van', 'la'),
            ('la', 'chi'),
            ('hou', 'chi'),
            ('to', 'mtl'),
            ('mtl', 'bos'),
            ('nyc', 'bos'),
            ('to', 'hou'),
            ('to', 'nyc'),
            ('la', 'nyc'),
            ('nyc', 'bos')
        )]
    return edges

def get_style():
    default_stylesheet = [
    {
        'selector': 'node',
        'style': {
            'background-color': '#BFD7B5',
            'label': 'data(label)'
        }
    },
    {
        'selector': 'edge',
        'style': {
            'line-color': '#A3C4BC'
        }
    }]
    return default_stylesheet

def build_tree_no_analysis(df):
    nodes = []
    for i in range(0, len(df['v1'])):
        nodes.append({
        'data': {'id': f'ti{i}', 'label': str(df['v1'][i])},
        'position': {'x': 100, 'y': float(120 + 70 * i)}
    })
    prod = sum_product(df, 'v1', 'pti')
    nodes.append({
        'data': {'id': 'prod', 'label': str(prod)},
        'position': {'x': 300, 'y': 120 + 70 * len(df['v1'])/2}
    })

    edges = [
        {'data': {'source': f'ti{i}', 'target': 'prod'}}
        for i in range(0, len(df['v1']))
        ]

    return nodes + edges

def build_tree_analysis(df, calc_df):
    nodes = [] 
    edges = []
    successor = None
    offset = 70 * len(df['v1'])
    eps_offset = offset * VCount
    res = calc_df.set_index('ε').T.reset_index()\
                .set_index('index').add_suffix('_res')
    res.index.names = ['ti']
    res = pd.merge(df, res, on='ti')

    # Iterate for each epsilon
    for e in range(len(calc_df['ε'])):
        # Iterate for each V
        for v in range(VCount):
            # Iterate for each theta 
            for i in range(0, len(df[f'v{v+1}'])):
                val = df[f'v{v+1}'][i]
                nodes.append({
                    'value': val,
                    'data': {'id': f'ti{i}v{v+1}e{e}', 'label': str(val)},
                    'position': {'x': 100, 'y': float(120 + 70 * i + v * offset + eps_offset * e)}
                })
            val = sum_product(res, f'v{v+1}', f'ε{e+1}_res')
            node = {
                'value': val,
                'data': {'id': f'prod{v+1}e{e}', 'label': str(val)},
                'position': {'x': 300, 'y': 120 + 70 * (len(df[f'v{v+1}']+1)/2-0.5) + offset * v + eps_offset * e}
            }
            nodes.append(node)
            if not successor or val > successor.get('value'):
                successor = node

            edges += [
                {'data': {'source': f'ti{i}v{v+1}e{e}', 'target': f'prod{v+1}e{e}'}}
                for i in range(0, len(df[f'v{v+1}']))
            ]
        # nodes.append({
        #         'data': {'id': f'prod{v+1}e{e}', 'label': str(sum_product(res, f'v{v+1}', f'ε{e+1}_res'))},
        #         'position': {'x': 300, 'y': 120 + 70 * (len(df[f'v{v+1}']+1)/2-0.5) + offset * v + eps_offset * e}
        #     })

        # edges.append[
        #     {'data': {'source': f'ti{i}v{v+1}e{e}', 'target': f'prod{v+1}e{e}'}}
        # ]
        
    return nodes + edges




def sum_product(df, col1, col2):
    sum = pd.Series.sum(df[col1] * df[col2])
    return sum
