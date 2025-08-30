import pandas as pd
import base64

def create_html_visualization():
    # Load data
    df1 = pd.read_parquet('out_test/train-00000-of-n.parquet')
    df2 = pd.read_parquet('out_test/train-00001-of-n.parquet')
    df = pd.concat([df1, df2], ignore_index=True)
    
    print(f"Loading {len(df)} entries from Parquet files...")
    
    # Create HTML
    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dataset Sondage Politique 2025</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }}
        h1 {{ color: #2c3e50; text-align: center; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        .stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin: 30px 0; }}
        .stat-card {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; }}
        .stat-number {{ font-size: 2em; font-weight: bold; margin-bottom: 5px; }}
        .entry {{ border: 1px solid #ddd; margin: 20px 0; border-radius: 8px; overflow: hidden; }}
        .entry-header {{ background: #3498db; color: white; padding: 15px; font-weight: bold; }}
        .entry-content {{ display: grid; grid-template-columns: 1fr 300px; gap: 20px; padding: 20px; }}
        .query-text {{ background: #f8f9fa; padding: 15px; border-left: 4px solid #3498db; border-radius: 4px; }}
        .image-container {{ text-align: center; }}
        .page-image {{ max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 4px; cursor: pointer; }}
        .metadata {{ background: #e9ecef; padding: 10px; border-radius: 4px; margin-top: 10px; font-size: 0.9em; }}
        @media (max-width: 768px) {{ .entry-content {{ grid-template-columns: 1fr; }} .stats {{ grid-template-columns: repeat(2, 1fr); }} }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Dataset PDF-to-Parquet : Sondage Politique 2025</h1>
        
        <div class="stats">
            <div class="stat-card"><div class="stat-number">{len(df)}</div><div>Entrées Total</div></div>
            <div class="stat-card"><div class="stat-number">{len(df) // 4}</div><div>Pages PDF</div></div>
            <div class="stat-card"><div class="stat-number">4</div><div>Types de Requêtes</div></div>
            <div class="stat-card"><div class="stat-number">FR</div><div>Langue</div></div>
        </div>"""
    
    # Add sample entries
    for idx, row in df.head(15).iterrows():
        try:
            image_bytes = row['image']['bytes']
            image_b64 = base64.b64encode(image_bytes).decode('utf-8')
            
            query = row['query'][:200] + "..." if len(row['query']) > 200 else row['query']
            
            html += f"""
        <div class="entry">
            <div class="entry-header">Entrée #{idx + 1}</div>
            <div class="entry-content">
                <div>
                    <div class="query-text">"{query}"</div>
                    <div class="metadata">
                        <strong>Langue:</strong> {row['language']}<br>
                        <strong>Taille image:</strong> {len(image_bytes):,} bytes
                    </div>
                </div>
                <div class="image-container">
                    <img src="data:image/jpeg;base64,{image_b64}" alt="Page PDF {idx + 1}" class="page-image" onclick="window.open(this.src, '_blank')">
                </div>
            </div>
        </div>"""
        except Exception as e:
            print(f"Error processing entry {idx}: {e}")
    
    html += """
    </div>
    <script>
        document.querySelectorAll('.page-image').forEach(img => {
            img.title = 'Cliquer pour agrandir';
        });
    </script>
</body>
</html>"""
    
    # Save file
    with open('dataset_visualization.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("✅ Visualisation HTML créée: dataset_visualization.html")

if __name__ == "__main__":
    create_html_visualization()