import streamlit as st, pandas as pd, os, pydeck as pdk, matplotlib.pyplot as plt, numpy as np
from translatepy import Translator

def df_to_sorted_dict(df):
    d = dict()
    for i, row in df.iterrows():
        for variable, valor in row.items():
            d[variable] = valor
    return dict(sorted(d.items(), key=lambda item: item[1], reverse=True))

def best_countries_by_variable(df):
    # Esta función debe recibir un dataframe y una lista con los países recomendados,
    # y devolver un diccionario del tipo {variable: [pais1, pais2, pais3]}
    d = dict()
    for column in df.columns[1:]:
        df.sort_values(column, ascending = False, inplace = True)
        # Añade los tres primeros países a la lista
        d[column] = df.head(3)['Country'].tolist()
    return d

def df_country_to_dict(df, pais):
	# Esta función recibe un df con todos los países y sus valores, y devuelve un diccionario del tipo {variable: valor} para el país buscado como parámetro
	d = dict()
	for i, row in df.iterrows():
		if row['Country'] == pais:
			for variable, valor in row.items():
				if variable != 'Country':
					d[variable] = float(valor)
			break
		else:
			continue

	return d

def traducir_pal(str, salida = 'Spanish'):
    # Esta función recibe un string y un diccionario de entrada y otro de salida, y traduce el string de entrada al de salida
    translator = Translator()
    try:
        traduccion = translator.translate(str, salida)
        return traduccion.result
    except:
        return str

def traducir_lista(lista, salida = 'Spanish'):
    # Esta función recibe una lista de strings y un diccionario de entrada y otro de salida, y traduce la lista de entrada al de salida
    try:
        return [traducir_pal(i, salida) for i in lista]
    except:
        return lista

def traducir_variable(variable):
    d = {'Education': 'Educación', 'Jobs': 'Trabajo', 'Income': 'Finanzas', 'Housing': 'Alojamiento', 'Safety': 'Seguridad', 'Health': 'Salud','Environment': 'Medio Ambiente',
        'Civic Engagement': 'Compromiso Civil', 'Access to Services': 'Acceso a Servicios', 'Community': 'Comunidad', 'Life satisfaction': 'Satisfacción con la vida'}
    try:
        return d[variable]
    except:
        return traducir_pal(variable)

def graficar_histograma(input, dic_pais, pais):
    del dic_pais['Life satisfaction']
    claves = input.keys()
    valores_usuario = np.array([k for k in input.values()])
    valores_pais = np.array([k for k in dic_pais.values()])
    plt.figure()
    plt.bar(claves, valores_usuario / 2, label='Usuario', color = 'navy')
    plt.bar(claves, abs(valores_pais - valores_usuario) / 2, label=pais, bottom=(valores_usuario / 2), color = 'powderblue')
    plt.xticks(rotation = 90)
    plt.yticks([])
    plt.ylim(0, 10)
    plt.xlabel('Variables')
    plt.ylabel('Valores')
    plt.title(f'Comparación de valores entre {traducir_pal(pais)} y el input del usuario.')
    plt.legend()
    # Mostrar
    st.pyplot(plt)

def results(path, top, probs, user_input):
    if st.button('📈 Ver resultados'):
        # Carga los datos
        df = pd.read_csv(os.path.join(path, "csv", "BetterLife_clean.csv"))
        uni = pd.read_csv(os.path.join(path, "csv", "UniversityRanks_clean.csv"))
        coords_df = pd.read_csv(os.path.join(path, "csv", "CountryCoords.csv"))
        
        # Crea el diccionario con los países y sus universidades
        dicUni = {}
        for _, row in uni.iterrows():
            if row["Country"] in top and row["Country"] not in dicUni:
                dicUni[row["Country"]] = (row["Institution Name"],
                row["QS Overall Score"],
                row["2025 Rank"],
                os.path.join(path, "svg", f"{row['Location'].lower()}.svg"),
                df[df["Country"] == row["Country"]]["Life satisfaction"].values)

        # UI top 3
        for i in range(3):
            country = top[i]
            university, score, rank, flag_path, life_satisfaction = dicUni[country]
            try:
                pais = traducir_pal(str(country))
                universidad = traducir_pal(str(university))
            except:
                pais = country
                universidad = university
            try: 
                with st.container():
                    card = st.columns([1, 2, 6],vertical_alignment="center",gap="medium")
                    
                    with card[0]:
                        st.image(flag_path, width=200)

                    with card[1]:
                        st.markdown(f"""
                            <div style='padding: 00px 0px; font-size: 1.1rem; margin-bottom:15px'>
                            <h4 style='margin-bottom: -8px;'>{i+1}. {pais}:</h4>
                            <p style='margin: 0px;'>
                            🏫 <b>{universidad}</b><br>
                            ⭐ Puntuación: <b>{score}</b><br>
                            📊 Ranking Mundial: <b>{rank}</b></p></div>""", unsafe_allow_html=True)
                    
                    with card[2]:
                        satisfaction_percent = float(life_satisfaction)
                        stroke_width = 3
                        radius = 15.9155
                        circumference = 2 * 3.1416 * radius
                        offset = circumference * (1 - satisfaction_percent / 10)

                        st.markdown(f"""<div style="display: flex; flex-direction: column; align-items: left;">
                                <div style="position: relative; width: 80px; height: 80px;margin-left:10px">
                                <svg width="80" height="80" viewBox="0 0 36 36">
                                <circle cx="18" cy="18" r="{radius}" 
                                fill="none" stroke="#444" stroke-width="{stroke_width}" />
                                <circle cx="18" cy="18" r="{radius}"
                                fill="none" stroke="#FFD700" stroke-width="{stroke_width}"
                                stroke-dasharray="{circumference:.2f}"
                                stroke-dashoffset="{offset:.2f}"
                                stroke-linecap="round"
                                transform="rotate(-90 18 18)" /></svg>
                                <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
                                font-size: 1em; color: white;">
                                {satisfaction_percent:.1f}/10</div></div>
                                <div style="margin-top: 5px; color: white;"><b>Calidad de Vida</b></div></div>""", unsafe_allow_html=True)

                        st.markdown("<hr style='margin-top: 10px; margin-bottom: 30px;'>", unsafe_allow_html=True)
            except:
                st.write("Ha habido un error en el sistema.")

        # Compara 
        best = best_countries_by_variable(df) # diccionario del tipo {variable: [pais1, pais2, pais3]}
        dic_top_en_best = dict()
        for variable, valor in best.items():
            for country in top:
                if country in valor:
                    if country not in dic_top_en_best:
                        dic_top_en_best[traducir_pal(country)] = [traducir_variable(variable)]
                    else:
                        dic_top_en_best[traducir_pal(country)].append(traducir_variable(variable))
        
        if dic_top_en_best != {}:
            st.markdown(f"## 🏆 Comparación de las recomendaciones respecto a los mejores países en cada variable:")
            for pais, l_variables in dic_top_en_best.items():
                if len(l_variables) == 1:
                    st.markdown(f"**{pais}** está entre los mejores países en {l_variables[0]}.")
                elif len(l_variables) == 2:
                    st.markdown(f"**{pais}** está entre los mejores países en {l_variables[0]} y {l_variables[1]}.")
                elif len(l_variables) == 3:
                    st.markdown(f"**{pais}** está entre los mejores países en {l_variables[0]}, {l_variables[1]} y {l_variables[2]}.")
                elif len(l_variables) > 3:
                    st.markdown(f"**{pais}** está entre los mejores países en {l_variables[0]}, {l_variables[1]} y {len(l_variables)-2} variables más.")

        # Gráfico de puntos donde aparezca el input del usuario, y uno de los países recomendados
        input = df_to_sorted_dict(user_input) # diccionario del tipo {variable: valor}
        st.markdown("## 📊 Comparación de variables entre el input del usuario y los países recomendados:")
        with st.container():
            col1, col2, col3 = st.columns([3, 3, 3], gap = 'medium')
            dic_top1 = df_country_to_dict(df, top[0])
            dic_top2 = df_country_to_dict(df, top[1])
            dic_top3 = df_country_to_dict(df, top[2])
            with col1:
                graficar_histograma(input, dic_top1, top[0])
            with col2:
                graficar_histograma(input, dic_top2, top[1])
            with col3:
                graficar_histograma(input, dic_top3, top[2])
            st.markdown("""
                        **¿Qué significan estos gráficos?**
                        
                        <p style='text-indent: 30px;'>
                        Estos gráficos de barras dibujan en azul marino el input que has introducido al inicio en orden descendente. Luego, sobre las propias barras de ese diagrama, se dibuja en azul celeste la diferencia entre el valor que tú has introducido, y el valor que tiene el país recomendado en cada variable. De esta forma, puedes ver de un vistazo qué variables son las que más se diferencian entre tu input y el país recomendado. Por tanto, el objetivo es que en estos diagramas aparezca el mínimo color azul celeste posible, pues esto significa que el país recomendado tiene un valor similar al tuyo en esas variables.
                        </p>
                        """, unsafe_allow_html=True)

        # Mapa
        try:
            map_data = []
            for country in top:
                coord_row = coords_df[coords_df["Country"] == country]
                if not coord_row.empty:
                    map_data.append({"Country": country,
                                    "lat": coord_row.iloc[0]["lat"],
                                    "lon": coord_row.iloc[0]["lon"],
                                    "University": dicUni[country][0],
                                    "Satisfaction": float(dicUni[country][4])})
                            
            top_coords_df = pd.DataFrame(map_data)
            st.markdown("## 🗺️ Ubicación de Países Recomendados:")
            st.pydeck_chart(pdk.Deck(map_style="mapbox://styles/mapbox/dark-v10",
                                    initial_view_state=pdk.ViewState(latitude=top_coords_df["lat"].mean(),
                                                                    longitude=top_coords_df["lon"].mean(),
                                                                    zoom=1, pitch=30),
                                    layers=[pdk.Layer("ScatterplotLayer",
                                            data=top_coords_df,
                                            get_position='[lon, lat]',
                                            get_color='[255, 140, 0, 160]',
                                            get_radius=500000,
                                            pickable=True)],
                                    tooltip={"html": "<b>{Country}</b><br/>🏫 {University}<br/>😊 Calidad de Vida: {Satisfaction}<br/>", "style": {"color": "white"}}))
        except:
            st.write("Ha habido un error con la generación del mapa.")
