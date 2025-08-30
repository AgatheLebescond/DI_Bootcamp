import pandas as pd
import base64
from io import BytesIO
from PIL import Image
import os

def create_html_visualization():
    """Create an HTML visualization of the Parquet dataset."""
    
    # Load both Parquet files
    df1 = pd.read_parquet('out_test/train-00000-of-n.parquet')
    df2 = pd.read_parquet('out_test/train-00001-of-n.parquet')
    df = pd.concat([df1, df2], ignore_index=True)
    
    print(f"Loading {len(df)} entries from Parquet files...")
    
    # Start HTML
    html_content = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dataset PDF-to-Parquet - Visualisation</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            padding: 30px;
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .entry {
            border: 1px solid #ddd;
            border-radius: 8px;
            margin: 20px 0;
            overflow: hidden;
            background: white;
        }
        .entry-header {
            background: #3498db;
            color: white;
            padding: 15px;
            font-weight: bold;
        }
        .entry-content {
            display: grid;
            grid-template-columns: 1fr 300px;
            gap: 20px;
            padding: 20px;
        }
        .query-text {
            background: #f8f9fa;
            padding: 15px;
            border-left: 4px solid #3498db;
            border-radius: 4px;
            font-style: italic;
        }
        .image-container {
            text-align: center;
        }
        .page-image {
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .metadata {
            background: #e9ecef;
            padding: 10px;
            border-radius: 4px;
            margin-top: 10px;
            font-size: 0.9em;
        }
        .filter-buttons {
            text-align: center;
            margin: 20px 0;
        }
        .filter-btn {
            background: #3498db;
            color: white;
            border: none;
            padding: 10px 20px;
            margin: 0 5px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
        }
        .filter-btn:hover {
            background: #2980b9;
        }
        .filter-btn.active {
            background: #e74c3c;
        }
        @media (max-width: 768px) {
            .entry-content {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Dataset PDF-to-Parquet : Sondage Politique 2025</h1>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{total_entries}</div>
                <div>Entrées Total</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{total_pages}</div>
                <div>Pages PDF</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">4</div>
                <div>Types de Requêtes</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">FR</div>
                <div>Langue</div>
            </div>
        </div>
        
        <div class="filter-buttons">
            <button class="filter-btn active" onclick="filterEntries('all')">Toutes</button>
            <button class="filter-btn" onclick="filterEntries('budget')">Budget</button>
            <button class="filter-btn" onclick="filterEntries('visual')">Visuelles</button>
            <button class="filter-btn" onclick="filterEntries('multimodal')">Multimodales</button>
        </div>
        
        <div id="entries-container">
"""
    
    # Add statistics
    html_content = html_content.format(
        total_entries=len(df),
        total_pages=len(df) // 4
    )
    
    # Process and add entries (limit to first 20 for HTML size)
    sample_entries = df.head(20)
    
    for idx, row in sample_entries.iterrows():
        # Convert image to base64 for HTML display
        try:
            image_bytes = row['image']['bytes']
            image_b64 = base64.b64encode(image_bytes).decode('utf-8')
            
            # Determine query type
            query = row['query'].lower()
            query_type = 'budget' if any(word in query for word in ['budget', 'politique', 'gouvernement']) else \
                        'visual' if any(word in query for word in ['graphique', 'diagramme', 'visuel']) else \
                        'multimodal' if any(word in query for word in ['multimodal', 'complexe', 'sémantique']) else 'other'
            
            html_content += f"""
        <div class="entry" data-type="{query_type}">
            <div class="entry-header">
                Entrée #{idx + 1} - Type: {query_type.title()}
            </div>
            <div class="entry-content">
                <div>
                    <div class="query-text">
                        "{row['query']}"
                    </div>
                    <div class="metadata">
                        <strong>Langue:</strong> {row['language']}<br>
                        <strong>Type:</strong> {query_type.title()}<br>
                        <strong>Taille image:</strong> {len(image_bytes):,} bytes
                    </div>
                </div>
                <div class="image-container">
                    <img src="data:image/jpeg;base64,{image_b64}" 
                         alt="Page PDF {idx + 1}" 
                         class="page-image">
                </div>
            </div>
        </div>
            """
        except Exception as e:
            print(f"Error processing entry {idx}: {e}")
            continue
    
    # Close HTML
    html_content += """
        </div>
    </div>
    
    <script>
        function filterEntries(type) {
            const entries = document.querySelectorAll('.entry');
            const buttons = document.querySelectorAll('.filter-btn');
            
            // Update button states
            buttons.forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            
            // Filter entries
            entries.forEach(entry => {
                if (type === 'all' || entry.dataset.type === type) {
                    entry.style.display = 'block';
                } else {
                    entry.style.display = 'none';
                }
            });
        }
        
        // Add click handlers for images (zoom)
        document.querySelectorAll('.page-image').forEach(img => {
            img.addEventListener('click', function() {
                window.open(this.src, '_blank');
            });
            img.style.cursor = 'pointer';
            img.title = 'Cliquer pour agrandir';
        });
    </script>
</body>
</html>
"""
    
    # Save HTML file
    with open('dataset_visualization.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Visualisation HTML créée: dataset_visualization.html")
    print(f"📊 {len(df)} entrées au total, {len(sample_entries)} affichées")
    
    return html_content

if __name__ == "__main__":
    create_html_visualization()