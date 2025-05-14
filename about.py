import streamlit as st

def aboutus():
    st.title("ℹ️ Acerca de esta App")

    st.markdown("""
        Bienvenido a **Optimizando tu destino: Análisis de tu lugar ideal** 🌍

        Esta aplicación utiliza tus preferencias personales en áreas como educación, seguridad, salud y más, para recomendarte los mejores países donde podrías considerar estudiar.
        
        Todo está basado en un estudio de los índices de Calidad de Vida de varias fuentes: **OECD**, **Eurostat** e **INE**.
        
        Es importante mencionar que los datos han sido transformados a un rango de 0 a 10 para facilitar la comparación entre diferentes variables y la entrada del usuario, asumiendo así cierta pérdida de precisión en la predicción. Esto significa que un valor 0 indica el peor país del que disponemos datos (países de la OECD), mientras que un 10 es el mejor de ellos. Por tanto, un valor de 5 indica que el país está en la media de los países de la OECD.

        ---

        ### ¿Qué hace esta aplicación?
        - Esta aplicación utiliza un algoritmo de *Random Forest* para predecir los mejores países según sus preferencias.
        - Sobre estos países, se muestran estadísticas de universidades destacadas, sus rankings y además puedes verlos en un mapa interactivo.
        - También puedes ver un análisis general de los datos, incluyendo distribuciones y correlaciones entre variables, al igual que algunas conclusiones

        ---

        ### Tecnologías utilizadas:
        - **Python** como lenguaje de programación.
        - **Pandas** y **NumPy** para manejo de datos.
        - **Matplotlib** y **Seaborn** para la generación de gráficas
        - **Streamlit** para la interfaz.
        - **Scikit-learn** para la predicción con modelo *Random Forest*.
        - **Pydeck** para mapas.
        - **Joblib** y **os** para la optimización del código.

        ---

        Desarrollado por Chafik Laslouni, Juan López, Juanjo Fernández, Alejandro Ruiz y Álvaro Santafé, estudiantes de la Universidad Politécnica de Valencia.

        """)