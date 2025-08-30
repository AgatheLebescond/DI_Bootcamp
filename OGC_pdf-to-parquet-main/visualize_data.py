import pandas as pd
import base64
from io import BytesIO
from PIL import Image
import os

def visualize_parquet_data():
    """Visualize the contents of the generated Parquet files."""
    
    # Load first Parquet file
    df = pd.read_parquet('out_test/train-00000-of-n.parquet')
    
    print("📊 DATASET OVERVIEW")
    print("=" * 50)
    print(f"Total entries: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    print()
    
    # Show sample queries
    print("🔍 SAMPLE QUERIES")
    print("=" * 50)
    for i in range(min(5, len(df))):
        print(f"Entry {i+1}:")
        print(f"  Query: {df.iloc[i]['query'][:100]}...")
        print(f"  Language: {df.iloc[i]['language']}")
        print()
    
    # Show query types distribution
    print("📈 QUERY ANALYSIS")
    print("=" * 50)
    
    # Analyze query patterns
    queries = df['query'].tolist()
    
    main_queries = [q for q in queries if 'budget' in q.lower() or 'politique' in q.lower()]
    visual_queries = [q for q in queries if 'graphique' in q.lower() or 'diagramme' in q.lower()]
    
    print(f"Budget/Political queries: {len(main_queries)}")
    print(f"Visual queries: {len(visual_queries)}")
    print(f"Languages: {df['language'].value_counts().to_dict()}")
    print()
    
    # Sample one image
    print("🖼️ SAMPLE IMAGE INFO")
    print("=" * 50)
    sample_image_bytes = df.iloc[0]['image']['bytes']
    print(f"Image size: {len(sample_image_bytes)} bytes")
    
    # Try to decode and show image properties
    try:
        image = Image.open(BytesIO(sample_image_bytes))
        print(f"Image dimensions: {image.size}")
        print(f"Image format: {image.format}")
        print(f"Image mode: {image.mode}")
        
        # Save a sample image for viewing
        sample_path = 'sample_page.png'
        image.save(sample_path)
        print(f"Sample image saved as: {sample_path}")
        
    except Exception as e:
        print(f"Error processing image: {e}")
    
    print("\n✅ Visualization complete!")
    
    return df

if __name__ == "__main__":
    df = visualize_parquet_data()