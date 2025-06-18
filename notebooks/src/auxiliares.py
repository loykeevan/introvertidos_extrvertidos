import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import seaborn as sns
from scipy.stats import (
    f_oneway,
    friedmanchisquare,
    kruskal,
    levene,
    mannwhitneyu,
    shapiro,
    ttest_ind,
    ttest_rel,
    wilcoxon,
)

def tabela_distribuicao_frequencia(dataframe, column, frequency_column=False):
    """
    Cria uma tabela de :
    Frequência: Somatório de Valores
    Frequência Relativa: Que é a Frequência em porcentagem da frequência acima;
    Frequência Acumulada: Somatório das Frequências sendo acumuladas de cada um dos itens;
    Frequência Relativa Acumulada: Somatório das Frequências em porcentagens sendo acumuladas de cada um dos itens;

    dataframe: pd.DataFrame
        DataFrame com os dados

    column: str
        Coluna do DataFrame a ser analisada

    frequency_column: Bool
        Informa se a coluna passada já é com os valores de Frequência ou nao
        Padrao: False

    Returns:
    _ _ _ _ 

    pd.DataFrame
        DataFrame da tabela com a distribuiçao de frequências informadas acima

    _ _ _ _

    """

    df_estatistica = pd.DataFrame()

    if frequency_column:
        df_estatistica['Frequencia'] = dataframe[column]
        df_estatistica['FrequenciaRelativa'] = df_estatistica['Frequencia'] / df_estatistica['Frequencia'].sum()
    else:
        df_estatistica['Frequencia'] = dataframe[column].value_counts().sort_index()
        df_estatistica['FrequenciaRelativa'] = dataframe[column].value_counts(normalize=True).sort_index()

    df_estatistica['FrequenciaAcumulada'] = df_estatistica['Frequencia'].cumsum()
    df_estatistica['FrequenciaRelativaAcumulada'] = df_estatistica['FrequenciaRelativa'].cumsum()
    
    return df_estatistica

def frequencia_quantitativa_continua(dataframe, column, amplitude):
    """
    dataframe: pd.DataFrame
    Dataframe a ser analisado

    column: str
    Coluna Quantitativa Contínua a ser analisada
    
    Amplitude: number int
     Faixa de valor a ser dividida a sua coluna
    """
    tamanho_intervalo = (dataframe[column].max() - dataframe[column].min()) / amplitude #Cálculo do tamanho de intervalos a serem divididos os dados

    # Cáldulo da quantidade de faixas de acordo com o valor mínimo da coluna, o valor máximo da coluna e a faixa de valor a ser dividido o DataFrame
    numero_de_zeros = np.ceil(tamanho_intervalo) 

    # Faz um array com número de Zeros de acordo com a faixa de valor estipulada
    array_numero_de_faixas = np.zeros(int(numero_de_zeros) + 1) 
    array_numero_de_faixas[1:] = np.ceil(amplitude)

    # Cálculo do bins para a fórmula do pd.cut
    bins = dataframe[column].min() + np.cumsum(array_numero_de_faixas)

    # Fazendo um DataFrame para os dados coletados
    freq = pd.cut(dataframe[column], bins=bins, right=False).value_counts().sort_index().to_frame()

    return freq



def grafico_pareto(dataframe, titulo, string=False):
    """
    dataframe = DataFrame
    Dataframe a ser utilizado

    título: str
    Título em string do gráfico

    string: Bool
    corresponde ao valor do índice, se precisa ser transformado em string para obter o gráfico
    Padrao False


    """
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax2 = ax.twinx()
    if string:
        ax.bar(dataframe.index.astype(str), dataframe["Frequencia"], color="C0")
    
        ax.bar(dataframe.index.astype(str), dataframe["Frequencia"], color="C0")

        ax2.plot(dataframe.index.astype(str), dataframe["FrequenciaRelativaAcumulada"], color="C1", marker="o")
    else:
        ax.bar(dataframe.index, dataframe["Frequencia"], color="C0")
    
        ax.bar(dataframe.index, dataframe["Frequencia"], color="C0")

        ax2.plot(dataframe.index, dataframe["FrequenciaRelativaAcumulada"], color="C1", marker="o")

    ax.bar_label(ax.containers[0], color="C0", fontweight="bold")

    for i, percentual in enumerate(dataframe["FrequenciaRelativaAcumulada"]):
        ax2.annotate(f"{percentual:.0%}", 
                     (i, percentual), 
                     xytext=(0,10), 
                     textcoords="offset points",
                     ha="center",
                     color="C1",
                     fontweight="bold")

    ax.tick_params(axis="y", left=False, labelleft=False)
    ax.tick_params(axis="x", rotation=90, size=0)
    ax2.tick_params(axis="y", right=False, labelright=False)

    for spine in ax.spines.values():
        spine.set_visible(False)
    for spine in ax2.spines.values():
        spine.set_visible(False)

    fig.suptitle(titulo)
    
    plt.show()
    

def grafico_boxplot_histograma(dataframe, column):
    fig, (ax1, ax2) = plt.subplots(
    nrows=2,
    ncols=1,
    sharex=True,
    gridspec_kw={
        "height_ratios": (0.15, 0.85),
        "hspace": 0.02
    }
    )

    sns.boxplot(
        data=dataframe,
        x=column,
        showmeans=True,
        meanline=True,
        meanprops={"color": "C1", "linewidth": 1.5, "linestyle": "--"},
        medianprops={"color": "C2", "linewidth": 1.5, "linestyle": "--"},
        ax=ax1,
    )

    sns.histplot(data=dataframe, x=column, kde=True, bins="sturges", ax=ax2)

    for ax in (ax1, ax2):
        ax.grid(True, linestyle="--", color="gray", alpha=0.5)
        ax.set_axisbelow(True)

    ax2.axvline(dataframe[column].mean(), color="C1", linestyle="--", label="Média")
    ax2.axvline(dataframe[column].median(), color="C2", linestyle="--", label="Mediana")
    ax2.axvline(dataframe[column].mode()[0], color="C3", linestyle="--", label="Moda")

    ax2.legend()

    plt.show()


def analise_shapiro(dataframe, alfa=0.05):
    print("Teste de Shapiro-Wilk")
    for coluna in dataframe.columns:
        estatistica_shapirowilk, pvalue_shapirowilk = shapiro(dataframe[coluna], nan_policy="omit")
        print(f'Estatística: {estatistica_shapirowilk=:.3f}')
        if pvalue_shapirowilk > alfa:
            print(f'{coluna} segue uma distribuição Normal (valor P: {pvalue_shapirowilk:.3f})')
        else: 
            print(f'{coluna} não segue uma distribuição Normal (valor P: {pvalue_shapirowilk:.3f})')

def analise_levene(dataframe, alfa=0.05 ,centro="mean"):
    print("Teste de Levene")
    estatistica_levene, pvalue_levene = levene(
        *[dataframe[coluna] for coluna in dataframe.columns], 
        center=centro, 
        nan_policy="omit")
    print(f"{estatistica_levene=:.3f}")
    if pvalue_levene > alfa:
        print(f'Variânicas Iguais (valor P: {pvalue_levene:.3f})')
    else: 
        print(f'Ao menos uma variância é diferente (valor P: {pvalue_levene:.3f})')

def analises_shapiro_levene(dataframe, alfa=0.05, centro="mean"):
    analise_shapiro(dataframe, alfa)

    print()

    analise_levene(dataframe, alfa, centro)

def analise_ttest_ind(
    dataframe,
    alfa=0.05,
    variancias_iguais=True,
    alternativa="two-sided",
    ):
    print("Teste t de Student")
    estatistica_ttest, valor_p_ttest = ttest_ind(
        *[dataframe[coluna] for coluna in dataframe.columns],
        equal_var=variancias_iguais,
        alternative=alternativa,
        nan_policy="omit",
    )

    print(f"{estatistica_ttest=:.3f}")
    if valor_p_ttest > alfa:
        print(f"Não rejeita a hipótese nula (valor p: {valor_p_ttest:.3f})")
    else:
        print(f"Rejeita a hipótese nula (valor p: {valor_p_ttest:.3f})")


def analise_ttest_rel(
    dataframe,
    alfa=0.05,
    alternativa="two-sided",
):
    print("Teste t de Student")
    estatistica_ttest, valor_p_ttest = ttest_rel(
        *[dataframe[coluna] for coluna in dataframe.columns],
        alternative=alternativa,
        nan_policy="omit",
    )

    print(f"{estatistica_ttest=:.3f}")
    if valor_p_ttest > alfa:
        print(f"Não rejeita a hipótese nula (valor p: {valor_p_ttest:.3f})")
    else:
        print(f"Rejeita a hipótese nula (valor p: {valor_p_ttest:.3f})")


def analise_anova_one_way(
    dataframe,
    alfa=0.05,
):

    print("Teste ANOVA one way")
    estatistica_f, valor_p_f = f_oneway(
        *[dataframe[coluna] for coluna in dataframe.columns], nan_policy="omit"
    )

    print(f"{estatistica_f=:.3f}")
    if valor_p_f > alfa:
        print(f"Não rejeita a hipótese nula (valor p: {valor_p_f:.3f})")
    else:
        print(f"Rejeita a hipótese nula (valor p: {valor_p_f:.3f})")

def analise_wilcoxon(
    dataframe,
    alfa=0.05,
    alternativa="two-sided",
):

    print("Teste de Wilcoxon")
    estatistica_wilcoxon, valor_p_wilcoxon = wilcoxon(
        *[dataframe[coluna] for coluna in dataframe.columns],
        nan_policy="omit",
        alternative=alternativa,
    )

    print(f"{estatistica_wilcoxon=:.3f}")
    if valor_p_wilcoxon > alfa:
        print(f"Não rejeita a hipótese nula (valor p: {valor_p_wilcoxon:.3f})")
    else:
        print(f"Rejeita a hipótese nula (valor p: {valor_p_wilcoxon:.3f})")


def analise_mannwhitneyu(
    dataframe,
    alfa=0.05,
    alternativa="two-sided",
):

    print("Teste de Mann-Whitney")
    estatistica_mw, valor_p_mw = mannwhitneyu(
        *[dataframe[coluna] for coluna in dataframe.columns],
        nan_policy="omit",
        alternative=alternativa,
    )

    print(f"{estatistica_mw=:.3f}")
    if valor_p_mw > alfa:
        print(f"Não rejeita a hipótese nula (valor p: {valor_p_mw:.3f})")
    else:
        print(f"Rejeita a hipótese nula (valor p: {valor_p_mw:.3f})")


def analise_friedman(
    dataframe,
    alfa=0.05,
):

    print("Teste de Friedman")
    estatistica_friedman, valor_p_friedman = friedmanchisquare(
        *[dataframe[coluna] for coluna in dataframe.columns],
        nan_policy="omit",
    )

    print(f"{estatistica_friedman=:.3f}")
    if valor_p_friedman > alfa:
        print(f"Não rejeita a hipótese nula (valor p: {valor_p_friedman:.3f})")
    else:
        print(f"Rejeita a hipótese nula (valor p: {valor_p_friedman:.3f})")


def analise_kruskal(
    dataframe,
    alfa=0.05,
):

    print("Teste de Kruskal")
    estatistica_kruskal, valor_p_kruskal = kruskal(
        *[dataframe[coluna] for coluna in dataframe.columns],
        nan_policy="omit",
    )

    print(f"{estatistica_kruskal=:.3f}")
    if valor_p_kruskal > alfa:
        print(f"Não rejeita a hipótese nula (valor p: {valor_p_kruskal:.3f})")
    else:
        print(f"Rejeita a hipótese nula (valor p: {valor_p_kruskal:.3f})")
        
def remover_outliers(dados, faixa_outlier=1.5):
    quartil_1 = dados.quantile(0.25)
    quartil_3 = dados.quantile(0.75)
    fiq = quartil_3 - quartil_1

    return dados[(dados >= quartil_1 - faixa_outlier * fiq) & (dados <= quartil_3 + faixa_outlier * fiq)]
