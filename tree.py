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

def add_basic_calcs(value, cost):
    return [{
        'data': {'id': 'label2', 'label': str('Without experiment or analysis')},
        'classes': 'whiteSmoke'
    },{
        'data': {'id': 'total3', 'label': str(value), 'parent': 'label2'},
        'position': {'x': 500, 'y': 150}, 'classes': 'gold'
    },{
        'data': {'id': 'label3', 'label': str('Analysis without experiment')},
        'classes': 'whiteSmoke'
    },{
        'data': {'id': 'total4', 'label': str(value-cost), 'parent': 'label3'},
        'position': {'x': 500, 'y': 300}, 'classes': 'gold'
    }]

def build_tree_no_analysis(df):
    nodes = []
    nodes.append({
        'data': {'id': 'label_no_an', 'label': str('Without analysis')},
        'classes': 'whiteSmoke'
    })
    for i in range(0, len(df['v1'])):
        nodes.append({
        'data': {'id': f'ti{i}', 'label': str(df['v1'][i]), 'parent': 'label_no_an'},
        'position': {'x': 100, 'y': float(120 + 70 * i)}, 'classes': 'blue'
    })
    total = sum_product(df, 'v1', 'pti')
    nodes.append({
        'data': {'id': 'total1', 'label': str(total), 'parent': 'label_no_an'},
        'position': {'x': 300, 'y': 120 + 70 * len(df['v1'])/2}, 'classes': 'gold'
    })

    edges = [
        {'data': {'source': f'ti{i}', 'target': 'total1'}, 'classes': 'blue'}
        for i in range(0, len(df['v1']))
        ]

    return nodes + edges

def build_tree_analysis(df, calc_df, cost, glob_offset):
    nodes = [] 
    edges = []
    successor = None
    successors = []
    offset = 70 * len(df['v1'])
    eps_offset = offset * VCount
    res = calc_df.set_index('ε').T.reset_index()\
                .set_index('index').add_suffix('_res')
    res.index.names = ['ti']
    res = pd.merge(df, res, on='ti')
    eps_count = len(calc_df['ε'])
    nodes.append({
        'data': {'id': 'label_an', 'label': str('With analysis')},
        'classes': 'whiteSmoke'
    })
    # Iterate for each epsilon
    for e in range(eps_count):
        # Iterate for each V
        for v in range(VCount):
            # Iterate for each theta 
            for i in range(0, len(df[f'v{v+1}'])):
                val = df[f'v{v+1}'][i]
                nodes.append({
                    'value': val,
                    'data': {'id': f'ti{i}v{v+1}e{e}', 'label': str(val), 'parent': 'label_an'},
                    'position': {'x': 100, 'y': float(120 + 70 * i + v * offset + eps_offset * e + glob_offset)},
                    'classes': 'blue'
                })
            val = sum_product(res, f'v{v+1}', f'ε{e+1}_res')
            node = {
                'value': val,
                'data': {'id': f'prod{v+1}e{e}', 'label': str(val), 'parent': 'label_an'},
                'position': {'x': 300, 'y': 120 + 70 * (len(df[f'v{v+1}']+1)/2-0.5) + offset * v + eps_offset * e + glob_offset}
            }
            if not successor or val > successor.get('value'):
                if successor:
                    successor['classes'] = 'red'                
                successor = node
                node['classes'] = 'green'
            else:
                node['classes'] = 'red'

            nodes.append(node)

            edges += [
                {'data': {'source': f'ti{i}v{v+1}e{e}', 'target': f'prod{v+1}e{e}'}, 'classes': 'blue'}
                for i in range(0, len(df[f'v{v+1}']))
            ]
        successors.append({'id': f'ε{e+1}','value': successor.get('value')})
        nodes.append({'data': {'id': f'successor{e}', 'label': str(successor.get('value')), 'parent': 'label_an'},
                      'position': {'x': 500, 'y': eps_offset * e + 365 + glob_offset},
                      'classes': 'green'
                      })    
        edges.append({'data': {'source': successor.get('data').get('id'), 'target': f'successor{e}'}, 'classes': 'green'})
        successor = None
    sdf = pd.DataFrame(successors).set_index('id')
    sdf.index.names = ['ε']
    sdf = pd.merge(sdf, calc_df.set_index('ε')['p(ε)'].T, on='ε')
    final = sum_product(sdf, 'value', 'p(ε)')
    final_offset = eps_offset * (eps_count/2) + 100
    nodes.append({'data': {'id': f'final', 'label': str(final), 'parent': 'label_an'},
                'position': {'x': 900, 'y': final_offset + glob_offset},
                'classes': 'green'
                })
    edges += [
                {'data': {'source': f'successor{i}', 'target': f'final'}, 'classes': 'green'}
                for i in range(0, len(successors))
            ]
    nodes.append({'data': {'id': f'final_exp', 'label': str(cost), 'parent': 'label_an'},
                'position': {'x': 900, 'y': final_offset + 100 + glob_offset},
                'classes': 'red'
                })
    edges.append({'data': {'source': 'final', 'target': 'total2'}, 'classes': 'green'})
    nodes.append({'data': {'id': f'total2', 'label': str(final-cost), 'parent': 'label_an'},
                'position': {'x': 1000, 'y': final_offset + 50 + glob_offset},
                'classes': 'gold'
                })
    edges.append({'data': {'source': 'final_exp', 'target': 'total2'}, 'classes': 'red'})
    
    return nodes + edges

def find_successor(nodes):
    best = nodes[0]
    for node in nodes:
        if node.get('value') > best.get('value'):
            best = node
    return best

def sum_product(df, col1, col2):
    sum = pd.Series.sum(df[col1] * df[col2])
    return sum
