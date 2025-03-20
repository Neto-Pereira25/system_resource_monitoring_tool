# **📊 SysCheck**  

Uma aplicação Streamlit para monitoramento de recursos do sistema (CPU, memória, disco) em tempo real.  

## **Funcionalidades**  

- Monitoramento em tempo real do uso da CPU (geral e por núcleo).  
- Rastreamento do uso da memória com métricas detalhadas.  
- Análise do uso do disco em todas as partições.  
- Visualização de dados históricos com gráficos interativos.  
- Personalização do intervalo de atualização e do tamanho do histórico.  

## **Instalação**  

1. Clone este repositório.  
2. Crie um ambiente virtual e ative-o:  

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate      # Windows
```  

3. Instale as dependências necessárias:  

```bash
pip install -r requirements.txt
```  

4. Execute a aplicação:  

```bash
streamlit run app.py
```  

## **Uso**  

1. Abra a aplicação no seu navegador (geralmente em [http://localhost:8501](http://localhost:8501)).  
2. Use a barra lateral para ajustar as configurações:  
   - **Intervalo de atualização:** Define a frequência de atualização dos dados (em segundos).  
   - **Tamanho do histórico:** Define quantos pontos de dados serão mantidos nos gráficos históricos.  

3. Visualize as métricas em tempo real:  
   - O **painel principal** exibe o uso atual de CPU, memória e disco com indicadores gráficos.  
   - As **abas detalhadas** mostram tendências históricas e métricas adicionais:  
     - **Aba CPU:** Mostra o uso por núcleo.  
     - **Aba Memória:** Exibe estatísticas detalhadas sobre o uso da memória.  
     - **Aba Disco:** Fornece um detalhamento do uso por partição.  

## **Requisitos**  

- Python 3.7+  
- Streamlit  
- psutil  
- plotly  
- pandas  
