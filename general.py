import streamlit as st, pandas as pd, matplotlib.pyplot as plt, seaborn as sns, os

df = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'csv', 'BetterLife_clean.csv'))

# Meter cada gráfica en una pestaña (tab) diferente???


def general():
    inicio, distribucion, correlacion = st.tabs(['Inicio', 'Estudio de distribuciones', 'Estudio de relaciones'])
    
    with inicio:
        st.markdown('Para empezar, aquí hay un resumen de los datos que tenemos en el dataset.')
        st.markdown('---')

        st.dataframe(df.describe())

        st.markdown('---')
        
        st.markdown('### **Conclusiones:**')
        st.markdown("""
                    - El conteo de todas las variables es 36, lo que muestra el trabajo realizado "limpiando" el dataset de valores faltantes.
                    - Se puede observar fácilmente que la media de las variables se encuentran alrededor de los 6 puntos, con la media más alta en seguridad, y la más baja en ingresos.
                    - También se observa una gran variedad entre los países respecto al Compromiso civil y la Salud, con desviaciones estándar cercanas a 2.8 puntos.
                    - Pese a que el rango de muchas de las variables sea elevado, esto es porque, como se dice en la pestaña de 'Acerca de', los datos han sido transformados a una escala del 0 al 10 para facilitar la comparación de variables y la entrada del usuario.
                    """)
    
    with distribucion:
        # Introducción
        st.markdown('Estudiemos las distribuciones de las variables. Para ello disponemos de:')
        st.markdown('En primer lugar, un gráfico de violín que nos muestra la densidad de datos de cada variable.')
        st.markdown('Después, un Box & Whisker múltiple que nos permite analizar la distribución de cada variable, al igual que los valores en los que se encuentra.')
        st.markdown('---')
        
        # Crear los gráficos
        fig, ax = plt.subplots(figsize = (6, 4))
        sns.violinplot(data=df, ax=ax)
        plt.title('Gráfico de violín de cada variable')
        plt.xticks(rotation=90)
        ax.tick_params(axis = 'both', labelsize = 7)
        
        fig2, ax2 = plt.subplots(figsize = (6, 4))
        sns.boxplot(data=df, ax=ax2)
        plt.title('Box & Whisker de cada variable')
        plt.xticks(rotation=90)
        ax2.tick_params(axis = 'both', labelsize = 7)
        
        # Mostrarlos centrados
        col1, col2, col3 = st.columns([0.1, 2, 0.1], gap="small")
        with col2:
            st.pyplot(fig)
            st.markdown('---')
            st.pyplot(fig2)
            st.markdown('---')
        st.markdown('### **Conclusiones:**')
        st.markdown("""
                    - Se puede observar la asimetría en la distribución de varias variables, tales como 'Seguridad' o 'Comunidad'.
                    - También vemos como la variable Ingresos, como se ha previsto en la tabla descriptiva de la pestaña anterior, tiene en general unos valores inferiores.
                    - Se puede destacar la asimetría negativa que tiene el violín de la variable Educación.
                    - En general, destacan los outliers presentes en la mayoría de las variables. Esto se podría explicar, en parte, por la transformación aplicada a los datos.
                    """)
    
    with correlacion:
        # Introducción
        st.markdown('A continuación se muestran dos matrices:')
        st.markdown('En la primera, la diagonal muestra un histograma de cada variable y el resto de la matriz muestra la relación entre cada par de variables.')
        st.markdown('En la segunda, se muestra una matriz de correlación que muestra la correlación de Pearson entre cada par de variables numéricas.')
        st.markdown('---')
        
        # Crear los gráficos
        fig3, ax3 = plt.subplots(figsize = (5, 3))
        fig3 = sns.pairplot(df, diag_kind='kde')
        plt.tick_params(axis = 'both', labelsize = 7) 
        plt.title('**Relaciones e histogramas de cada variable**')
        
        fig4, ax4 = plt.subplots(figsize = (6, 4))
        sns.heatmap(df.corr(numeric_only = True), annot=True, fmt=".2f", cmap='coolwarm', ax=ax4)
        ax4.tick_params(axis = 'both', labelsize = 7)
        plt.title('Matriz de correlación')
        
        # Mostrarlos centrados
        col1, col2, col3 = st.columns([0.1, 2, 0.1], gap="small")
        with col2:
            st.pyplot(fig3)
            st.markdown('---')
            st.pyplot(fig4)
            st.markdown('---')
        
        st.markdown('### **Conclusiones:**')
        st.markdown("""
                    - Estos gráficos nos permiten detectar las correlaciones presentes entre las variables, así como la fuerte correlación entre Comunidad y Satisfacción de vida, lo que indica que, en general, la conexión y apoyo social son factores importantes para la satisfacción personal.
                    - Se observa también una correlación consolidada entre Educación y Trabajo, que demuestra la importancia de una buena educación base para la posterior inserción laboral. Además, Educación también está correlacionada con Seguridad.
                    - Seguridad mantiene una correlación significativa con Acceso a servicios, lo que puede indicar que una buena infraestructura de transporte y servicios públicos puede contribuir a la percepción de seguridad en un país.
                    - En general, se observa una correlación positiva entre todas las variables, lo que indica que un país con un buen nivel en una variable tiende a tener buenos niveles en las demás.
                    """)