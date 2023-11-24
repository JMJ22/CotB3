import os
import pandas as pd

# Pasta onde os arquivos estão localizados
caminho = r'C:\Users\caminho_dos_seus_arquivos_cotahist'

# Lista das ações que você quer analisar
acoes = ['ALOS3', 'ALPA4', 'ABEV3', 'ARZZ3', 'ASAI3', 'AZUL4', 'B3SA3', 'BBSE3', 'BBDC3', 'BBDC4', 'BRAP4', 'BBAS3', 'BRKM5', 'BRFS3', 'BPAC11', 'CRFB3', 'BHIA3', 'CCRO3', 'CMIG4', 'CIEL3', 'COGN3', 'CPLE6', 'CSAN3', 'CPFE3', 'CMIN3', 'CVCB3', 'CYRE3', 'DXCO3', 'ELET3', 'ELET6', 'EMBR3', 'ENGI11', 'ENEV3', 'EGIE3', 'EQTL3', 'EZTC3', 'FLRY3', 'GGBR4', 'GOAU4', 'GOLL4', 'NTCO3', 'SOMA3', 'HAPV3', 'HYPE3', 'IGTI11', 'IRBR3', 'ITSA4', 'ITUB4', 'JBSS3', 'KLBN11', 'RENT3', 'LWSA3', 'LREN3', 'MGLU3', 'MRFG3', 'BEEF3', 'MRVE3', 'MULT3', 'PCAR3', 'PETR3', 'PETR4', 'RECV3', 'PRIO3', 'PETZ3', 'RADL3', 'RAIZ4', 'RDOR3', 'RAIL3', 'RRRP3', 'SBSP3', 'SANB11', 'SMTO3', 'CSNA3', 'SLCE3', 'SUZB3', 'TAEE11', 'VIVT3', 'TIMS3', 'TOTS3', 'UGPA3', 'USIM5', 'VALE3', 'VAMO3', 'VBBR3', 'WEGE3', 'YDUQ3']

# Dicionário para armazenar os dados de cada ação
dados_acoes = {}

for acao in acoes:
    dados_acao = []
    for arquivo in os.listdir(caminho):
        if arquivo.endswith('.TXT') and arquivo.startswith('COTAHIST_A'):
            with open(os.path.join(caminho, arquivo), 'r') as file:
                linhas = file.readlines()
                for linha in linhas:
                    if linha[12:24].strip() == acao:
                        # Processar os dados da linha conforme a estrutura do arquivo
                        # Aqui você precisará extrair os dados relevantes, como data e valor de fechamento
                        # e armazená-los na lista dados_acao
                        # Exemplo:
                        data = linha[2:10].strip()  # Ajuste conforme a posição correta nos seus arquivos
                        fechamento = float(linha[108:121].strip()) / 100  # Ajuste conforme a posição correta nos seus arquivos
                        dados_acao.append([data, fechamento])
    
    # Transformar os dados em um DataFrame do Pandas para facilitar a análise
    df = pd.DataFrame(dados_acao, columns=['Data', 'Fechamento'])
    df['Data'] = pd.to_datetime(df['Data'], format='%Y%m%d')
    
    if not df.empty:  # Verifica se há dados no DataFrame antes de calcular as métricas
        # Calcular as métricas desejadas
        data_mais_antiga = df['Data'].min()
        valor_fechamento_antigo = df.loc[df['Data'] == data_mais_antiga, 'Fechamento'].values[0]
        data_mais_recente = df['Data'].max()
        valor_fechamento_recente = df.loc[df['Data'] == data_mais_recente, 'Fechamento'].values[0]
        variacao_percentual = ((valor_fechamento_recente / valor_fechamento_antigo) - 1) * 100
        desvio_padrao = df['Fechamento'].std()
        
        # Armazenar os resultados no dicionário dados_acoes
        dados_acoes[acao] = {
            'Data mais antiga': data_mais_antiga.strftime('%d/%m/%y'),
            'Valor de fechamento mais antigo': valor_fechamento_antigo,
            'Data mais recente': data_mais_recente.strftime('%d/%m/%y'),
            'Valor de fechamento mais recente': valor_fechamento_recente,
            'Variação percentual': variacao_percentual,
            'Desvio Padrão': desvio_padrao
        }

# Imprimir os resultados
for acao, dados in dados_acoes.items():
    print(f'\=================================================================================================')
    print(f'{acao} - de {dados["Data mais antiga"]} Vlr = {dados["Valor de fechamento mais antigo"]:.2f} - ate {dados["Data mais recente"]} Vlr {dados["Valor de fechamento mais recente"]:.2f} - Osc% = {dados["Variação percentual"]:.2f}% - DesvPad%  = {dados["Desvio Padrão"]:.2f}')
    print(f'==================================================================================================')
