import os
import glob
import pandas as pd
import streamlit as st
import base64

st.set_page_config(page_title="OGC PDF → Parquet Viewer", layout="wide")

st.title("OGC PDF → Parquet Viewer")
st.caption("Visualisez les paires image–requêtes générées")

out_dir = os.getenv("OUTPUT_FOLDER", "out_test")
parquet_files = sorted(glob.glob(os.path.join(out_dir, "*.parquet")))

if not parquet_files:
    st.warning(f"Aucun fichier Parquet trouvé dans '{out_dir}'. Lancez main.py d'abord.")
else:
    sel = st.selectbox("Fichier Parquet", parquet_files)
    engine = st.selectbox("Moteur de lecture", ["fastparquet", "pyarrow"], index=0)
    try:
        df = pd.read_parquet(sel, engine=engine)
    except Exception as e:
        st.error(f"Erreur lecture Parquet: {e}")
        st.stop()

    st.write(f"Lignes: {len(df)}")
    page = st.number_input("Index ligne", min_value=0, max_value=max(0, len(df)-1), value=0, step=1)
    row = df.iloc[int(page)] if len(df) else None

    if row is not None:
        col1, col2 = st.columns([1,1])
        with col1:
            st.subheader("Image")
            if "image_b64" in row and isinstance(row["image_b64"], str):
                try:
                    img_bytes = base64.b64decode(row["image_b64"])  # PNG bytes
                    st.image(img_bytes, caption=f"{row.get('pdf_name','')} - page {row.get('page_index','?')}")
                except Exception as e:
                    st.info(f"Impossible d'afficher l'image (base64). Erreur: {e}")
            else:
                st.info("Aucune image_b64 dans cette ligne")
        with col2:
            st.subheader("Requêtes")
            st.write("- Principale:")
            st.code(str(row.get("main_query", "")))
            st.write("- Secondaire:")
            st.code(str(row.get("secondary_query", "")))
            st.write("- Visuelle:")
            st.code(str(row.get("visual_query", "")))
            st.write("- Multimodale:")
            st.code(str(row.get("multimodal_query", "")))

    with st.expander("Aperçu DataFrame"):
        st.dataframe(df.head(200))
