import asyncio
import os
from dataclasses import dataclass
from typing import List, Dict, Any

from dotenv import load_dotenv
import pandas as pd
from tqdm import tqdm

from config import settings
from utils import (
    render_pdf_page_to_image_bytes,
    extract_text_from_pdf,
    detect_language_from_pages,
    image_bytes_to_b64,
)


load_dotenv()


@dataclass
class PageResult:
    image_b64: str
    page_index: int
    pdf_name: str
    language: str
    main_query: str
    secondary_query: str
    visual_query: str
    multimodal_query: str


async def fake_gemini_generate_queries(page_image_b64: str, page_text: str, language: str) -> Dict[str, str]:
    # Placeholder: replace with actual Gemini/OpenRouter call
    return {
        "main": f"Principales informations techniques ({language})",
        "secondary": "Détails techniques secondaires",
        "visual": "Éléments visuels à analyser",
        "multimodal": "Requête multimodale complexe",
    }


async def process_pdf(pdf_path: str) -> List[PageResult]:
    pdf_name = os.path.basename(pdf_path)
    pages_text = extract_text_from_pdf(pdf_path)
    language = detect_language_from_pages(pages_text)

    results: List[PageResult] = []
    sem = asyncio.Semaphore(settings.CHUNK_SIZE)

    async def process_page(idx: int):
        async with sem:
            img_bytes = render_pdf_page_to_image_bytes(pdf_path, idx, settings.ZOOM_FACTOR)
            img_b64 = image_bytes_to_b64(img_bytes)
            queries = await fake_gemini_generate_queries(img_b64, pages_text[idx], language)
            results.append(
                PageResult(
                    image_b64=img_b64,
                    page_index=idx,
                    pdf_name=pdf_name,
                    language=language,
                    main_query=queries["main"],
                    secondary_query=queries["secondary"],
                    visual_query=queries["visual"],
                    multimodal_query=queries["multimodal"],
                )
            )

    await asyncio.gather(*[process_page(i) for i in range(len(pages_text))])
    results.sort(key=lambda r: r.page_index)
    return results


def write_parquet_chunk(rows: List[PageResult], output_dir: str, file_prefix: str, chunk_index: int):
    records = [
        {
            "image_b64": r.image_b64,
            "pdf_name": r.pdf_name,
            "page_index": r.page_index,
            "language": r.language,
            "main_query": r.main_query,
            "secondary_query": r.secondary_query,
            "visual_query": r.visual_query,
            "multimodal_query": r.multimodal_query,
        }
        for r in rows
    ]
    df = pd.DataFrame.from_records(records)
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, f"{file_prefix}_{chunk_index:05d}.parquet")
    df.to_parquet(out_path)
    return out_path


async def main():
    input_dir = settings.INPUT_FOLDER
    output_dir = settings.OUTPUT_FOLDER
    file_prefix = settings.FILE_NAMES
    parquet_size = settings.PARQUET_SIZE

    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    pdf_files = [
        os.path.join(input_dir, f)
        for f in os.listdir(input_dir)
        if f.lower().endswith(".pdf")
    ]

    if not pdf_files:
        print(f"Aucun PDF trouvé dans {input_dir}. Ajoutez des fichiers et relancez.")
        return

    all_rows: List[PageResult] = []
    for pdf in tqdm(pdf_files, desc="Traitement des PDFs"):
        rows = await process_pdf(pdf)
        all_rows.extend(rows)

        # write in chunks
        while len(all_rows) >= parquet_size:
            chunk = all_rows[:parquet_size]
            all_rows = all_rows[parquet_size:]
            idx = len([p for p in os.listdir(output_dir) if p.endswith('.parquet')])
            out = write_parquet_chunk(chunk, output_dir, file_prefix, idx)
            print(f"Écrit: {out}")

    # remaining
    if all_rows:
        idx = len([p for p in os.listdir(output_dir) if p.endswith('.parquet')])
        out = write_parquet_chunk(all_rows, output_dir, file_prefix, idx)
        print(f"Écrit: {out}")


if __name__ == "__main__":
    asyncio.run(main())
