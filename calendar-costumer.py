import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import calplot

# 1. Lê apenas as colunas necessárias
df = pd.read_csv('novo_arquivo.csv', names=['Inicio', 'Fim'], header=None)

# 2. Converte os campos para datetime
df['Inicio'] = pd.to_datetime(df['Inicio'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
df['Fim'] = pd.to_datetime(df['Fim'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
df = df.dropna(subset=['Inicio', 'Fim'])

# 3. Recebe as datas do usuário
data_inicio_str = input("Informe a data de início (dd/mm/aaaa): ")
data_fim_str = input("Informe a data de fim (dd/mm/aaaa): ")

# 4. Converte para datetime
inicio_intervalo = datetime.strptime(data_inicio_str, '%d/%m/%Y')
fim_intervalo = datetime.strptime(data_fim_str, '%d/%m/%Y') + timedelta(days=1) - timedelta(seconds=1)

# 5. Calcula tempo de uso dentro do intervalo
total_duracao = timedelta(0)
dias_uso = pd.Series(dtype=int)

print("\nConexões dentro do intervalo informado:\n")
for idx, row in df.iterrows():
    inicio = max(row['Inicio'], inicio_intervalo)
    fim = min(row['Fim'], fim_intervalo)
    if inicio < fim:
        total_duracao += fim - inicio
        dias = pd.date_range(inicio.date(), fim.date(), freq='D')
        for dia in dias:
            dias_uso.at[dia] = dias_uso.get(dia, 0) + 1
        print(f"Linha {idx + 1}: Início = {row['Inicio'].strftime('%d/%m/%Y')}, Fim = {row['Fim'].strftime('%d/%m/%Y')}")

# 6. Converte para dias inteiros
dias_totais = int(total_duracao.total_seconds() / (60 * 60 * 24))
print(f"\nUso total entre {data_inicio_str} e {data_fim_str}: {dias_totais} dias")

# 7. Plota o calendário com os números visíveis
calplot.calplot(
    dias_uso,
    cmap='YlGn',
    textformat='{:.0f}',  # mostra número inteiro de sessões por dia
    suptitle='Dias de Uso por Conexão'
)
plt.show()
