import os
import glob
import pandas as pd

OUT_DIR = os.getenv("OUTPUT_FOLDER", "out_test")
OUT_HTML = os.path.join(OUT_DIR, "viewer.html")

def main():
    files = sorted(glob.glob(os.path.join(OUT_DIR, "*.parquet")))
    if not files:
        print(f"Aucun Parquet dans {OUT_DIR}")
        return
    path = files[-1]
    try:
        df = pd.read_parquet(path, engine="fastparquet")
    except Exception:
        df = pd.read_parquet(path)

    rows = []
    for _, r in df.iterrows():
        img = r.get("image_b64", "")
        pdf_name = r.get("pdf_name", "")
        page_idx = r.get("page_index", "")
        main_q = r.get("main_query", "")
        sec_q = r.get("secondary_query", "")
        vis_q = r.get("visual_query", "")
        mul_q = r.get("multimodal_query", "")
        rows.append(f"""
        <div class='card'>
          <div class='left'>
            <img src='data:image/png;base64,{img}' alt='page' />
            <div class='meta'>{pdf_name} — page {page_idx}</div>
          </div>
          <div class='right'>
            <h4>Principale</h4><pre>{main_q}</pre>
            <h4>Secondaire</h4><pre>{sec_q}</pre>
            <h4>Visuelle</h4><pre>{vis_q}</pre>
            <h4>Multimodale</h4><pre>{mul_q}</pre>
          </div>
        </div>
        """)

    html = f"""
    <!doctype html>
    <html>
    <head>
      <meta charset='utf-8' />
      <title>Dataset Viewer</title>
      <style>
        body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; margin: 0; background: #0b0c10; color: #eaf0f1; }}
        header {{ padding: 16px 24px; background: #14161a; border-bottom: 1px solid #222; position: sticky; top: 0; }}
        h1 {{ font-size: 18px; margin: 0; }}
        .wrap {{ padding: 24px; display: grid; gap: 16px; }}
        .card {{ display: grid; grid-template-columns: 420px 1fr; gap: 16px; background: #111316; border: 1px solid #222; border-radius: 12px; overflow: hidden; }}
        .left {{ background: #0f1114; padding: 12px; display: flex; flex-direction: column; align-items: center; }}
        img {{ width: 100%; height: auto; border-radius: 8px; border: 1px solid #222; }}
        .meta {{ font-size: 12px; opacity: .8; margin-top: 8px; }}
        .right {{ padding: 12px 16px; display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
        h4 {{ margin: 8px 0 4px; font-size: 13px; color: #a1cdf1; }}
        pre {{ white-space: pre-wrap; background: #0b0c10; padding: 10px; border: 1px solid #222; border-radius: 8px; }}
      </style>
    </head>
    <body>
      <header>
        <h1>{os.path.basename(path)} — {len(df)} lignes</h1>
      </header>
      <div class='wrap'>
        {''.join(rows)}
      </div>
    </body>
    </html>
    """

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    print(OUT_HTML)


if __name__ == "__main__":
    main()
