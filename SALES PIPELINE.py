import pandas as pd
import zipfile

# =============================
# CONFIG
# =============================
zip_path = r"C:\Users\Allykiller\Documents\MEUS DASHBOARDS\SALES PIPELINE\DATA SET - SALES PIPELINE.zip"

# =============================
# EXTRAÇÃO
# =============================
with zipfile.ZipFile(zip_path) as z:
    print("Arquivos no ZIP:", z.namelist())

with zipfile.ZipFile(zip_path) as z:
    with z.open('sales_pipeline.csv') as f:
        df = pd.read_csv(f)

# =============================
# TRANSFORMAÇÃO
# =============================

# Datas
df['engage_date'] = pd.to_datetime(df['engage_date'])
df['close_date'] = pd.to_datetime(df['close_date'], errors='coerce')

# Valores
df['close_value'] = pd.to_numeric(df['close_value'], errors='coerce')

# Etapa do funil
df['etapa_funil'] = df['deal_stage'].apply(
    lambda x: 'Em negociação' if x == 'Engaging' else 'Fechado'
)

# Status
def status_map(x):
    if x == 'Won':
        return 'Ganho'
    elif x == 'Lost':
        return 'Perdido'
    else:
        return 'Em aberto'

df['status'] = df['deal_stage'].apply(status_map)

# Tempo de fechamento
df['tempo_dias'] = (df['close_date'] - df['engage_date']).dt.days

# Receita real
df['receita_real'] = df.apply(
    lambda row: row['close_value'] if row['deal_stage'] == 'Won' else 0,
    axis=1
)

# Nulos
df['account'] = df['account'].fillna('Não informado')

# =============================
# ANÁLISE
# =============================

print("\n===== VISÃO GERAL =====")
print(df.head())

# Conversão geral
total = len(df)
ganhos = df[df['status'] == 'Ganho'].shape[0]

conversao = ganhos / total if total > 0 else 0
print(f"\nTaxa de conversão geral: {conversao:.2%}")

# Status geral
print("\n===== STATUS =====")
print(df['status'].value_counts())

# Conversão real
ganhos = df[df['status'] == 'Ganho'].shape[0]
perdas = df[df['status'] == 'Perdido'].shape[0]

taxa_real = ganhos / (ganhos + perdas) if (ganhos + perdas) > 0 else 0
print(f"\nTaxa de conversão real: {taxa_real:.2%}")

# Receita total
receita_total = df['receita_real'].sum()
print(f"\nReceita total: R$ {receita_total:,.2f}")

# Tempo médio
tempo_medio = df[df['status'] == 'Ganho']['tempo_dias'].mean()
print(f"\nTempo médio de fechamento: {tempo_medio:.0f} dias")

# Top vendedores
print("\n===== TOP VENDEDORES =====")
print(
    df.groupby('sales_agent')['receita_real']
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

# =============================
# GARGALOS
# =============================

# Perdas por vendedor
print("\n===== PERDAS POR VENDEDOR =====")
perdas_vendedor = (
    df[df['status'] == 'Perdido']
    .groupby('sales_agent')
    .size()
    .sort_values(ascending=False)
)
print(perdas_vendedor.head(10))

# Conversão por produto
print("\n===== CONVERSÃO POR PRODUTO =====")
conversao_produto = (
    df.groupby('product')['status']
    .value_counts(normalize=True)
    .unstack()
)
print(conversao_produto.sort_values(by='Ganho', ascending=False))

# Perdas por produto
print("\n===== PERDAS POR PRODUTO =====")
perdas_produto = (
    df[df['status'] == 'Perdido']
    .groupby('product')
    .size()
    .sort_values(ascending=False)
)
print(perdas_produto.head(10))

# Matriz vendedor x produto
print("\n===== MATRIZ PERDAS (VENDEDOR X PRODUTO) =====")
matriz_perdas = (
    df[df['status'] == 'Perdido']
    .groupby(['sales_agent', 'product'])
    .size()
    .sort_values(ascending=False)
)
print(matriz_perdas.head(10))

# Conversão por vendedor
print("\n===== CONVERSÃO POR VENDEDOR =====")
conv_vendedor = (
    df.groupby('sales_agent')['status']
    .value_counts(normalize=True)
    .unstack()
)
print(conv_vendedor.sort_values(by='Ganho', ascending=False))