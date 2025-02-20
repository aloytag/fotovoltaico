import datetime
import io

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

with st.sidebar:
    st.write('**CONFIGURACIÓN**')
    N = st.number_input('Cantidad de paneles', min_value=1,
                        max_value=1000, value=12, step=1)
    Ppico = st.number_input('Pot. pico del panel (W)', min_value=50,
                        max_value=1000, value=240, step=10)
    kp = st.number_input('Coef. de pot.-temp. (1/°C)', min_value=-0.01,
                        max_value=0., value=-0.0044, step=0.001, format="%0.4f")
    eta = st.number_input('Rendimiento global (p.u.)', min_value=0.,
                        max_value=1., value=0.97, step=0.05, format="%0.2f")

tab1, tab2 = st.tabs(['Carga de datos', 'Resultados'])

with tab1:
    """
    # Título

    ## Subtítulo

    ### Sub-subtítulo


    referferfref
    grgt4g4gg

    $ I = \cfrac{V}{R} $
    """

    arch = st.file_uploader('Cargar archivo de datos', type='xlsx',
                            accept_multiple_files=False)

    if arch:
        df = pd.read_excel(arch, index_col=0)
        G, T = df.columns
        Tc = df[T] + 0.031 * df[G]
        df['Potencia (kW)'] = N * df[G]/1000 * Ppico * (1 + (Tc - 25)) * eta * 1e-3  # kW
        st.success('¡ARCHIVO CARGADO EXITOSAMENTE!')
        st.dataframe(df)
    else:
        st.warning('¡FALTA EL ARCHIVO DE DATOS!', icon="⚠️")

with tab2:
    d = st.date_input("Seleccionar día", value=datetime.date(2019, 1, 15),
                      max_value=datetime.date(2019, 12, 31),
                      min_value=datetime.date(2019, 1, 1),
                      format="DD/MM/YYYY")
    if arch:
        tabla_filtrada = df.loc[f'{d.year}-{d.month}-{d.day}', :]
        st.dataframe(tabla_filtrada)

        st.line_chart(data=tabla_filtrada, y='Potencia (kW)', x_label='Hora',
                      y_label='Pot. (kW)',
                      color='#ffaa0088', width=10, height=None, use_container_width=True)
        
        f, ax = plt.subplots(1, 1, figsize=(10, 5), dpi=50)
        tabla_filtrada.plot(y='Potencia (kW)', kind='line', ax=ax)
        f
        
        col1, col2 = st.columns(2)
        with col1:
            st.line_chart(data=tabla_filtrada, y=T, x_label='Hora',
                          y_label='Temperatura (°C)')
            
        with col2:
            st.line_chart(data=tabla_filtrada, y=G, x_label='Hora',
                          y_label=G)
        
        nuevo_archivo = io.BytesIO()
        tabla_filtrada.to_excel(nuevo_archivo)
        st.download_button('Descargar resultados', data=nuevo_archivo,
                           file_name='Tabla_resultados.xlsx')
