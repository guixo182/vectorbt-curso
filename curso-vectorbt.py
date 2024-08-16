import vectorbt as vbt 
import yfinance as yfinance

# Conf de layout
vbt.settings.set_theme("dark")
vbt.settings['plotting']['layout']['width'] = 1200
vbt.settings['plotting']['layout']['height'] = 600

# Download dos dados no formato pandas de varios dados: open, close, high, low etc
dados = vbt.YFData.download(["USDBRL=X"],
                            start="2024-08-01",
                            end = "2024-08-14",
                            interval="5m",
                            missing_index='drop'
                            ).get()

# Gerando variaveis a partir dos dados
dados_fech = dados['Close']

# Imprementando indicadores
media_rapida = vbt.MA.run(dados_fech, 9)
media_lenta = vbt.MA.run(dados_fech, 21)
macd_t = vbt.MACD.run(dados_fech, fast_window=12, slow_window=26, signal_window=9)

# Criando as logicas de entrada e saida
entradas = media_rapida.ma_crossed_above(media_lenta)
saidas = media_rapida.ma_crossed_below(media_lenta) 

# Portifolio é a estrutura para fazer testes, otimizacoes e dash
pf = vbt.Portfolio.from_signals(dados_fech, entradas, saidas)
#print(pf.stats())
#pf.plot().show()

# Plotando info no grafico
fig = dados_fech.vbt.plot(trace_kwargs=dict(name='Preço',line=dict(color='green')))
fig = media_rapida.ma.vbt.plot(trace_kwargs=dict(name='Media Rapida',line=dict(color='blue')), fig=fig)
fig = media_lenta.ma.vbt.plot(trace_kwargs=dict(name='Media Lenta',line=dict(color='red')), fig=fig)
fig = entradas.vbt.signals.plot_as_entry_markers(dados_fech, fig=fig)
fig = saidas.vbt.signals.plot_as_exit_markers(dados_fech, fig=fig)
#fig.show() 


dados_max = dados['High']
dados_min = dados['Low']
max_20_candles = dados_max.shift(1).rolling(20).max()
min_10_candles = dados_min.shift(1).rolling(10).min()
atr = vbt.ATR.run(dados_max, dados_min, dados_fech, window=20)

print(atr.atr)

entradas2 = dados_fech > max_20_candles
saidas2 = (dados_fech < min_10_candles)

pf2 = vbt.Portfolio.from_signals(
    dados_fech, 
    entradas2,
    saidas,
    sl_stop=2*(atr.atr/dados_fech))
 
pf2.plot().show()
print(pf.stats())


fig2 = dados_fech.vbt.plot(trace_kwargs=dict(name='Preço',line=dict(color='green')))
fig2 = max_20_candles.vbt.plot(trace_kwargs=dict(name='Max 20 Candles',line=dict(color='blue')), fig=fig2)
fig2 = min_10_candles.vbt.plot(trace_kwargs=dict(name='Min 20 Candles',line=dict(color='yellow')), fig=fig2)
fig2 = entradas2.vbt.signals.plot_as_entry_markers(dados_fech, fig=fig2)
fig2 = saidas2.vbt.signals.plot_as_exit_markers(dados_fech, fig=fig2)

#fig2.show()