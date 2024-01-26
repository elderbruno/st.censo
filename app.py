import streamlit as st
import pandas as pd
import plotly.express as px

# Função para carregar dados do dataset
@st.cache_data
def load_data():
    return pd.read_csv('DadosCenso.csv')

# Carregando os dados e criando uma cópia 
dados_censo_original = load_data()
dados_censo = dados_censo_original.copy()



# Criando a coluna 'Evasao' com base na coluna 'CO_ALUNO_SITUACAO'
dados_censo['Evasao'] = dados_censo['CO_ALUNO_SITUACAO'] == 0.0

# Menu de navegação lateral
with st.sidebar:
    st.title('Menu')
    page = st.radio('Escolha uma análise:', ['Introdução', 'Análise Demográfica', 'Modalidade de Ensino', 'Carga Horária', 'Ano de Ingresso', 'Apoio e Atividades'])

# Container para o cabeçalho principal
with st.container():
    st.header('Análise de Tendências de :blue[Evasão] :blue[acadêmica]', divider='rainbow')
    
# Definindo as seções do app
if page == 'Introdução':
    st.subheader('Bem-vindo! :school:')
    st.image('imagem.jpg', caption='Evasão Acadêmcia')
    st.markdown('Esta aplicação web tem como objetivo fornecer uma análise detalhada das tendências de evasão acadêmica/universitária utilizando dados do Censo da Educação Superior.')

# Implementação de cada página de análise
if page == 'Análise Demográfica':  

    # Seção de Análise Demográfica    
    st.header('Análise de Evasão por Características Demográficas')

    # Seletor para escolher a característica demográfica
    opcao_demografica = st.selectbox('Escolha uma Característica Demográfica:', ['SEXO', 'IDADE', 'RAÇA/COR'])

    # Processamento dos dados para a análise demográfica
    if opcao_demografica == 'SEXO':
        evasao_por_demografia = dados_censo.groupby('SEXO')['Evasao'].mean().reset_index()
        coluna_demografica = 'SEXO'

    elif opcao_demografica == 'IDADE':        
        dados_censo['Faixa Etária'] = pd.cut(dados_censo['NU_IDADE_ALUNO'], bins=[0, 20, 30, 40, 50, 100], labels=['0-20', '21-30', '31-40', '41-50', '51+'])
        evasao_por_demografia = dados_censo.groupby('Faixa Etária')['Evasao'].mean().reset_index()
        coluna_demografica = 'Faixa Etária'
        
    elif opcao_demografica == 'RAÇA/COR':        
        evasao_por_demografia = dados_censo.groupby('CO_COR_RACA_ALUNO')['Evasao'].mean().reset_index()
        coluna_demografica = 'CO_COR_RACA_ALUNO'

    # Vamos obter a paleta de cores do primeiro gráfico. Suponha que seja uma sequência de cores Plotly.
    cores_categoricas = px.colors.qualitative.Plotly

    # Criando o gráfico interativo com Plotly para a análise demográfica
    fig_demografia = px.bar(
        evasao_por_demografia, 
        x=coluna_demografica, 
        y='Evasao',
        title=f'Taxa de Evasão por {opcao_demografica}',
        labels={'Evasao': 'Taxa de Evasão (%)'},
        text='Evasao',
        color='Evasao',
        color_continuous_scale=px.colors.sequential.Viridis  
    )

    # Ajustando a escala de cores para refletir os valores de evasão como porcentagens
    max_evasao = evasao_por_demografia['Evasao'].max()
    fig_demografia.update_layout(
        coloraxis_colorbar=dict(
            title='Taxa de Evasão (%)',
            tickvals=[i * max_evasao / 5 for i in range(6)],  # Cria 6 pontos na escala de cores
            ticktext=[f'{i * max_evasao / 5:.0%}' for i in range(6)]  # Formata os pontos como porcentagens
        )
    )

    # Ajustando o layout do gráfico para análise demográfica
    fig_demografia.update_layout(
        xaxis_title=opcao_demografica,
        yaxis_title='Taxa de Evasão (%)',
        legend_title='Legenda',
        margin=dict(l=20, r=20, t=40, b=20),
        hovermode='closest',
        template='plotly_white'
    )

    # Ajustando o formato do eixo Y para exibir porcentagens e o texto nas barras
    fig_demografia.update_traces(
        texttemplate='%{y:.2%}',
        hovertemplate='<b>%{x}:</b> %{y:.2%}<extra></extra>'
    )
    fig_demografia.update_layout(yaxis_tickformat='.2%')

    # Exibindo o gráfico na aplicação
    st.plotly_chart(fig_demografia, use_container_width=True)
    

elif page == 'Modalidade de Ensino':
    # ... Seu código para Modalidade de Ensino ...
    # Seção para Análise do Impacto da Modalidade de Ensino na Evasão
    st.header('Impacto da Modalidade de Ensino na Evasão')

    # Agrupando os dados por modalidade de ensino
    evasao_por_modalidade = dados_censo.groupby('CO_MODALIDADE_ENSINO')['Evasao'].mean().reset_index()

    # Substitua os códigos numéricos pelas descrições correspondentes
    # Isso depende do seu conjunto de dados específico. Aqui é um exemplo genérico:
    modalidades = {1: 'Presencial', 2: 'EAD', 3: 'Híbrido'}
    evasao_por_modalidade['CO_MODALIDADE_ENSINO'] = evasao_por_modalidade['CO_MODALIDADE_ENSINO'].map(modalidades)

    # Criando o gráfico interativo com Plotly para a análise por modalidade de ensino
    fig_modalidade = px.bar(
        evasao_por_modalidade,
        x='CO_MODALIDADE_ENSINO',
        y='Evasao',
        title='Taxa de Evasão por Modalidade de Ensino',
        labels={'Evasao': 'Taxa de Evasão (%)', 'CO_MODALIDADE_ENSINO': 'Modalidade de Ensino'},
        text='Evasao',
        color_discrete_sequence=['#636EFA']  # Escolha uma cor ou uma sequência de cores
    )

    # Ajustando o layout do gráfico para análise por modalidade de ensino
    fig_modalidade.update_layout(
        xaxis_title='Modalidade de Ensino',
        yaxis_title='Taxa de Evasão (%)',
        legend_title='Legenda',
        margin=dict(l=20, r=20, t=40, b=20),
        hovermode='closest',
        template='plotly_white'
    )

    # Ajustando o formato do eixo Y para exibir porcentagens e o texto nas barras
    fig_modalidade.update_traces(
        texttemplate='%{y:.2%}',
        hovertemplate='<b>%{x}:</b> %{y:.2%}<extra></extra>'
    )
    fig_modalidade.update_layout(yaxis_tickformat='.2%')

    # Exibindo o gráfico na aplicação
    st.plotly_chart(fig_modalidade, use_container_width=True)


elif page == 'Carga Horária':
    # ... Seu código para Carga Horária ...
    # Seção para Análise da Carga Horária
    st.header('Análise da Carga Horária')

    # Processando os dados para correlacionar carga horária e evasão
    # Você pode decidir agrupar a carga horária em faixas, ou usar a carga horária como um valor contínuo diretamente
    # Aqui, vamos criar faixas de carga horária para facilitar a visualização
    bins_carga_horaria = [0, 1000, 2000, 3000, 4000, 5000, dados_censo['QT_CARGA_HORARIA_TOTAL'].max()]
    labels_carga_horaria = ['Até 1000h', '1001-2000h', '2001-3000h', '3001-4000h', '4001-5000h', 'Mais de 5000h']
    dados_censo['Faixa Carga Horária'] = pd.cut(dados_censo['QT_CARGA_HORARIA_TOTAL'], bins=bins_carga_horaria, labels=labels_carga_horaria)

    evasao_por_carga_horaria = dados_censo.groupby('Faixa Carga Horária')['Evasao'].mean().reset_index()

    # Criando o gráfico interativo com Plotly para a análise de carga horária
    fig_carga_horaria = px.bar(
        evasao_por_carga_horaria,
        x='Faixa Carga Horária',
        y='Evasao',
        title='Taxa de Evasão por Faixa de Carga Horária',
        labels={'Evasao': 'Taxa de Evasão (%)', 'Faixa Carga Horária': 'Carga Horária'},
        text='Evasao',
        color_discrete_sequence=['#EF553B']  # Escolha uma cor ou uma sequência de cores
    )

    # Ajustando o layout do gráfico para análise de carga horária
    fig_carga_horaria.update_layout(
        xaxis_title='Faixa de Carga Horária',
        yaxis_title='Taxa de Evasão (%)',
        legend_title='Legenda',
        margin=dict(l=20, r=20, t=40, b=20),
        hovermode='closest',
        template='plotly_white'
    )

    # Ajustando o formato do eixo Y para exibir porcentagens e o texto nas barras
    fig_carga_horaria.update_traces(
        texttemplate='%{y:.2%}',
        hovertemplate='<b>%{x}:</b> %{y:.2%}<extra></extra>'
    )
    fig_carga_horaria.update_layout(yaxis_tickformat='.2%')

    # Exibindo o gráfico na aplicação
    st.plotly_chart(fig_carga_horaria, use_container_width=True)


elif page == 'Ano de Ingresso':
    # ... Seu código para Ano de Ingresso ...
    # Seção para Análise da Influência do Ano de Ingresso na Evasão
    st.header('Influência do Ano de Ingresso na Evasão')

    # Agrupando os dados por ano de ingresso
    evasao_por_ano_ingresso = dados_censo.groupby('ANO_INGRESSO')['Evasao'].mean().reset_index()

    # Criando o gráfico interativo com Plotly para a análise do ano de ingresso
    fig_ano_ingresso = px.bar(
        evasao_por_ano_ingresso,
        x='ANO_INGRESSO',
        y='Evasao',
        title='Taxa de Evasão por Ano de Ingresso',
        labels={'Evasao': 'Taxa de Evasão (%)', 'ANO_INGRESSO': 'Ano de Ingresso'},
        text='Evasao',
        color_discrete_sequence=['#AB63FA']  # Escolha uma cor ou uma sequência de cores
    )

    # Ajustando o layout do gráfico para análise do ano de ingresso
    fig_ano_ingresso.update_layout(
        xaxis_title='Ano de Ingresso',
        yaxis_title='Taxa de Evasão (%)',
        legend_title='Legenda',
        margin=dict(l=20, r=20, t=40, b=20),
        hovermode='closest',
        template='plotly_white'
    )

    # Ajustando o formato do eixo Y para exibir porcentagens e o texto nas barras
    fig_ano_ingresso.update_traces(
        texttemplate='%{y:.2%}',
        hovertemplate='<b>Ano de Ingresso:</b> %{x}<br><b>Taxa de Evasão:</b> %{y:.2%}<extra></extra>'
    )
    fig_ano_ingresso.update_layout(yaxis_tickformat='.2%')

    # Exibindo o gráfico na aplicação
    st.plotly_chart(fig_ano_ingresso, use_container_width=True)


elif page == 'Apoio e Atividades':
    # Seção para Análise de Apoio Social e Atividades Extracurriculares
    # Seção para Análise de Apoio Social e Atividades Extracurriculares
    st.header('Análise de Apoio Social e Atividades Extracurriculares')

    # Apoio Social
    apoio_social_evasao = dados_censo.groupby('IN_APOIO_SOCIAL')['Evasao'].mean().reset_index()
    apoio_social_evasao['IN_APOIO_SOCIAL'] = apoio_social_evasao['IN_APOIO_SOCIAL'].map({0: 'Sem Apoio', 1: 'Com Apoio'})

    # Atividades Extracurriculares
    atividades_extracurriculares_evasao = dados_censo.groupby('IN_ATIVIDADE_EXTRACURRICULAR')['Evasao'].mean().reset_index()
    atividades_extracurriculares_evasao['IN_ATIVIDADE_EXTRACURRICULAR'] = atividades_extracurriculares_evasao['IN_ATIVIDADE_EXTRACURRICULAR'].map({0: 'Sem Atividades', 1: 'Com Atividades'})

    # Criando gráficos interativos com Plotly
    fig_apoio_social = px.bar(
        apoio_social_evasao,
        x='IN_APOIO_SOCIAL',
        y='Evasao',
        title='Taxa de Evasão e Apoio Social',
        labels={'Evasao': 'Taxa de Evasão (%)', 'IN_APOIO_SOCIAL': 'Apoio Social'},
        color_discrete_sequence=['#FFA15A']  # Escolha uma cor
    )

    fig_atividades_extracurriculares = px.bar(
        atividades_extracurriculares_evasao,
        x='IN_ATIVIDADE_EXTRACURRICULAR',
        y='Evasao',
        title='Taxa de Evasão e Atividades Extracurriculares',
        labels={'Evasao': 'Taxa de Evasão (%)', 'IN_ATIVIDADE_EXTRACURRICULAR': 'Atividades Extracurriculares'},
        color_discrete_sequence=['#00CC96']  # Escolha uma cor
    )

    # Ajustando o layout dos gráficos
    for fig in [fig_apoio_social, fig_atividades_extracurriculares]:
        fig.update_layout(
            xaxis_title='Categoria',
            yaxis_title='Taxa de Evasão (%)',
            legend_title='Legenda',
            margin=dict(l=20, r=20, t=40, b=20),
            hovermode='closest',
            template='plotly_white'
        )
        fig.update_traces(
            texttemplate='%{y:.2%}',
            hovertemplate='<b>%{x}:</b> %{y:.2%}<extra></extra>'
        )
        fig.update_layout(yaxis_tickformat='.2%')

    # Exibindo os gráficos na aplicação
    st.plotly_chart(fig_apoio_social, use_container_width=True)
    st.plotly_chart(fig_atividades_extracurriculares, use_container_width=True)



# Seção de visualização de dados brutos
if st.checkbox('Mostrar dados brutos'):
    with st.expander("Ver dados brutos"):
        st.write(dados_censo)

    # Criando um botão de download de CSV
    # Função para converter DataFrame para CSV
    def convert_df_to_csv(df):
        return df.to_csv(index=False).encode('utf-8')

    csv = convert_df_to_csv(dados_censo)

    # Botão para download
    st.download_button(
       label="Baixar dados como CSV",
       data=csv,
       file_name='dados_censo.csv',
       mime='text/csv',
    )

# Links externos e informações adicionais
st.markdown('Para mais informações, visite [INEP](https://www.gov.br/inep/pt-br).')