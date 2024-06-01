from app import *
import plotly.graph_objects as go
import pandas as pd
from dash import html, dcc, Input, Output
from dash_bootstrap_templates import ThemeSwitchAIO, load_figure_template
import datetime
import pdb

df = pd.read_csv('crypto_combine.csv')
df['Date'] = df['Date'].apply(lambda x: pd.to_datetime(x))
df.dropna(inplace=True)
df['Media'] = (df['High'] + df['Low']) / 2

template_theme1 = 'superhero'
template_theme2 = 'zephyr'
theme1 = dbc.themes.SUPERHERO
theme2 = dbc.themes.ZEPHYR

###### Style config ########
graph_config = {'showTips': False, 'displayModeBar':False}
card_style = {'height': '100%'}
main_config = {
    'hovermode': 'x unified',
    'legend': {'yanchor':'top',
               'y':0.9,
               'xanchor':'left',
               'x':0.1,
               'title': {'text': None},
               'font': {'color': 'white'},
               'bgcolor': 'rgba(0, 0, 0, 0.5)'},
    'margin':{'l':0, 'r':0, 't':10, 'b':0}
}

main_config2 = {
    'margin':{'l':0, 'r':0, 't':40, 'b':0},
}


######### Layout ##########
app.layout = dbc.Container([
    dcc.Store(id='base-df', data=df.to_dict()),
    dcc.Store(id='date-filtered-df'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.Legend('Criptocurrency Analysis', style={'text-align': 'center', 'font-size': '20px'})
                ]),
                dbc.CardBody([
                    ThemeSwitchAIO(aio_id='theme-swich', themes=[theme1, theme2]),
                    dcc.DatePickerRange(
                        start_date=datetime.date(2018, 1, 1),
                        end_date=datetime.date(2023, 5, 31),
                        start_date_placeholder_text=datetime.date(2018, 1, 1),
                        end_date_placeholder_text=datetime.date(2023, 5, 31),
                        min_date_allowed=datetime.date(2018, 1, 1),
                        max_date_allowed=datetime.date(2023, 5, 31),
                        clearable=False,
                        className='dbc',
                        id='date-range'
                    )
                ])
            ], style=card_style)
        ], md=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Legend('Comparação Direta', style={'text-align': 'center'}),
                    dbc.Row([
                        dbc.Col([
                            dcc.Dropdown(
                                options=df['Crypto'].unique(),
                                value=df['Crypto'].unique()[0],
                                multi=False,
                                clearable=False,
                                id='cripto1_comparation', 
                                className='dbc'
                                )
                        ]),
                        dbc.Col([
                            dcc.Dropdown(
                                options=df['Crypto'].unique(),
                                value=df['Crypto'].unique()[1],
                                multi=False,
                                clearable=False,
                                id='cripto2_comparation',
                                className='dbc'
                                )
                        ])
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id='direct-comparison-graph', config=graph_config, style={'margin-top':'25px'})
                        ])
                    ])
                ])
            ], style=card_style)
        ], md=6),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='growth-bitcoin-graph', config=graph_config)
                        ])
                    ])
                ],sm=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='growth-etherium-graph', config=graph_config)
                        ])
                    ])
                ],sm=6)
            ], className='g-2 my-auto'),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='growth-ripple-graph', config=graph_config)
                        ])
                    ])
                ], sm=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='growth-litecoin-graph', config=graph_config)
                        ])
                    ])
                ], sm=6)
            ], className='g-2 my-auto')
        ], md=4)
    ], className='g-2 my-auto'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Legend('Evolução individual das CriptoMoedas', style={'text-align': 'center'}),
                    dcc.Dropdown(
                        options=df['Crypto'].unique(),
                        value=df['Crypto'].unique()[0],
                        multi=False,
                        clearable=False,
                        className='dbc',
                        id='crypto-individual-comparation',
                        style={'margin-left': '20px', 'margin-right':'500px', 'margin-bottom': '10px', 'text-align': 'center'}
                    ),
                    dcc.Graph(id='candlesticks-graph', config=graph_config)
                ])
            ], style=card_style)
        ], md=7),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Legend('Evolução Geral das CriptoMoedas', style={'text-align':'center'}),
                    dcc.Graph(id='general-graph', config=graph_config)
                ])
            ],style=card_style)
        ], md=5)
    ], className='g-2 my-auto')
], fluid=True)


########## Callbacks ##################
@app.callback(
    Output('date-filtered-df', 'data'),
    Input('base-df', 'data'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date')
)
def filtrando_dataframe_por_data(dataframe, start, end):
    df = pd.DataFrame(dataframe)
    df_filtered = df[(pd.to_datetime(df['Date']) >= pd.to_datetime(start)) & (pd.to_datetime(df['Date']) <= pd.to_datetime(end))]
    return df_filtered.to_dict()


@app.callback(
    Output('direct-comparison-graph', 'figure'),
    Input('date-filtered-df', 'data'),
    Input('cripto1_comparation', 'value'),
    Input('cripto2_comparation', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme-swich'), 'value')
)
def comparacao_direta(dataframe, cripto1, cripto2, toggle):
    template = template_theme1 if toggle else template_theme2
    df = pd.DataFrame(dataframe)
    df_final = pd.DataFrame()
    df_crypto1 = df[df['Crypto'].isin([cripto1])]
    df_crypto2 = df[df['Crypto'].isin([cripto2])]

    #pdb.set_trace()
    df_crypto1['Ano-Mes'] = pd.to_datetime(df['Date']).apply(lambda x: ''.join([str(x.year), '-', str(x.month)]))
    df_crypto1['Ano-Mes'] = df_crypto1['Ano-Mes'].apply(lambda x: pd.to_datetime(x).strftime('%Y/%m')).sort_values()
    df_crypto2['Ano-Mes'] = pd.to_datetime(df['Date']).apply(lambda x: ''.join([str(x.year), '-', str(x.month)]))
    df_crypto2['Ano-Mes'] = df_crypto2['Ano-Mes'].apply(lambda x: pd.to_datetime(x).strftime('%Y/%m')).sort_values()

    df_final1 = df_crypto1.groupby('Ano-Mes')['Media'].mean().round(1)
    df_final2 = df_crypto2.groupby('Ano-Mes')['Media'].mean().round(1)
    
    fig = go.Figure()

    fig.add_scattergl(name=cripto1, x=df_final1.index, y=df_final1.values)
    fig.add_scattergl(name=cripto2, x=df_final2.index, y=df_final2.values)
    
    fig.update_layout(main_config, height=200, template=template)

    return fig
    
# Indicator do Bitcoin
@app.callback(
    Output('growth-bitcoin-graph', 'figure'),
    Input('date-filtered-df', 'data'),
    Input(ThemeSwitchAIO.ids.switch('theme-swich'), 'value')
)
def card1(dataframe, toggle):
    template = template_theme1 if toggle else template_theme2

    df = pd.DataFrame(dataframe)
    df_final = df[df['Crypto'] == 'BTC']
    df_final['Ano'] = df_final['Date'].apply(lambda x: pd.to_datetime(x).year)
    medias_anuais = df_final.groupby(by="Ano")['Media'].mean().round(2)
    
    fig = go.Figure()
    fig.add_trace(go.Indicator(
            mode='number+delta',
            title={'text': f'<span style="size:60%">Bitcoin</span><br><span style="font-size:0.7rem">{medias_anuais.index[0]} - {medias_anuais.index[-1]}</span>'},
            value=medias_anuais.iloc[-1],
            number= {'prefix': '$', 'valueformat': '.2f'},
            delta= {'relative': True, 'valueformat': '.1%', 'reference': medias_anuais.iloc[0]},
    ))
    fig.update_layout(main_config2, height=150, template=template)
    
    return fig

# Indicator Etherium
@app.callback(
    Output('growth-etherium-graph', 'figure'),
    Input('date-filtered-df', 'data'),
    Input(ThemeSwitchAIO.ids.switch('theme-swich'), 'value')
)
def card2(dataframe, toggle):
    template = template_theme1 if toggle else template_theme2

    df = pd.DataFrame(dataframe)
    df_final = df[df['Crypto'] == 'ETH']
    df_final['Ano'] = df_final['Date'].apply(lambda x: pd.to_datetime(x).year)
    medias_anuais = df_final.groupby(by="Ano")['Media'].mean().round(2)
    
    fig = go.Figure()
    fig.add_trace(go.Indicator(
            mode='number+delta',
            title={'text': f'<span style="size:60%">Etherium</span><br><span style="font-size:0.7rem">{medias_anuais.index[0]} - {medias_anuais.index[-1]}</span>'},
            value=medias_anuais.iloc[-1],
            number= {'prefix': '$', 'valueformat': '.2f'},
            delta= {'relative': True, 'valueformat': '.1%', 'reference': medias_anuais.iloc[0]},
    ))
    fig.update_layout(main_config2, height=150, template=template)
    
    return fig

@app.callback(
    Output('growth-ripple-graph', 'figure'),
    Input('date-filtered-df', 'data'),
    Input(ThemeSwitchAIO.ids.switch('theme-swich'), 'value')
)
def card3(dataframe, toggle):
    template = template_theme1 if toggle else template_theme2

    df = pd.DataFrame(dataframe)
    df_final = df[df['Crypto'] == 'XRP']
    df_final['Ano'] = df_final['Date'].apply(lambda x: pd.to_datetime(x).year)
    medias_anuais = df_final.groupby(by="Ano")['Media'].mean().round(2)
    
    fig = go.Figure()
    fig.add_trace(go.Indicator(
            mode='number+delta',
            title={'text': f'<span style="size:60%">Ripple</span><br><span style="font-size:0.7rem">{medias_anuais.index[0]} - {medias_anuais.index[-1]}</span>'},
            value=medias_anuais.iloc[-1],
            number= {'prefix': '$', 'valueformat': '.2f'},
            delta= {'relative': True, 'valueformat': '.1%', 'reference': medias_anuais.iloc[0]},
    ))
    fig.update_layout({'margin':{'l':0, 'r':0, 't':50, 'b':0}}, height=160, template=template)
    
    return fig

@app.callback(
    Output('growth-litecoin-graph', 'figure'),
    Input('date-filtered-df', 'data'),
    Input(ThemeSwitchAIO.ids.switch('theme-swich'), 'value')
)
def card4(dataframe, toggle):
    template = template_theme1 if toggle else template_theme2

    df = pd.DataFrame(dataframe)
    df_final = df[df['Crypto'] == 'LTC']
    df_final['Ano'] = df_final['Date'].apply(lambda x: pd.to_datetime(x).year)
    medias_anuais = df_final.groupby(by="Ano")['Media'].mean().round(2)
    
    fig = go.Figure()
    fig.add_trace(go.Indicator(
            mode='number+delta',
            title={'text': f'<span style="size:60%">Litecoin</span><br><span style="font-size:0.7rem">{medias_anuais.index[0]} - {medias_anuais.index[-1]}</span>'},
            value=medias_anuais.iloc[-1],
            number= {'prefix': '$', 'valueformat': '.2f'},
            delta= {'relative': True, 'valueformat': '.1%', 'reference': medias_anuais.iloc[0]},
    ))
    fig.update_layout({'margin':{'l':0, 'r':0, 't':40, 'b':0}}, height=160, template=template)

    return fig


@app.callback(
    Output('candlesticks-graph', 'figure'),
    Input('crypto-individual-comparation', 'value'),
    Input('date-filtered-df', 'data'),
    Input(ThemeSwitchAIO.ids.switch('theme-swich'), 'value')
)
def individual_analysis(cripto, dataframe, toggle):
    template = template_theme1 if toggle else template_theme2
    df = pd.DataFrame(dataframe)
    df_filtrado = df[df['Crypto'] == cripto]

    fig = go.Figure()
    fig.add_trace(go.Candlestick(close=df_filtrado['Close'], open=df_filtrado['Open'], high=df_filtrado['High'], low=df_filtrado['Low'], x=df_filtrado['Date']))
    fig.update_layout(main_config, height=250, template=template)

    return fig


@app.callback(
    Output('general-graph', 'figure'),
    Input('date-filtered-df', 'data'),
    Input(ThemeSwitchAIO.ids.switch('theme-swich'), 'value')
)
def general_graph(dataframe, toggle):
    template = template_theme1 if toggle else template_theme2
    df = pd.DataFrame(dataframe)
    df['Ano-Mes'] = pd.to_datetime(df['Date']).apply(lambda x: ''.join([str(x.year), '-', str(x.month)]))
    df['Ano-Mes'] = df['Ano-Mes'].apply(lambda x: pd.to_datetime(x).strftime('%Y/%m')).sort_values()
    Medias = df.groupby('Ano-Mes')['Media'].sum().round(2)

    fig = go.Figure()
    fig.add_trace(go.Scattergl(x=Medias.index, y=Medias.values))
    fig.update_layout(main_config, height=250, template=template)
    fig.add_annotation(text=f'Evolução da soma do valor<br>de 1 unidade de cada Crypto',
                       xref='paper', yref='paper',
                       font=dict(
                        family='Courier New, monospace',
                        size=12,
                        color='#ffffff'
                       ),
                       align='center', bgcolor='rgba(0,0,0,0.5)', opacity=0.8,
                       x=0.05, y=0.95, showarrow=False)

    return fig

if __name__ == '__main__':
    app.run(debug=False, port='8080', host='0.0.0.0')