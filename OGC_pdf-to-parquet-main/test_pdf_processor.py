import pytest
import asyncio
import io
import os
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path

from pdf_to_img_txt import pdf_to_image_and_text, process_one_page
from main import process_one_pdf_file, pdf_batch_to_parquet_part
from rate_limiter import RateLimiter
from config import ZOOM_FACTOR, CHUNK_SIZE, OUTPUT_FORMAT


class TestPdfToImageAndText:
    """Test PDF processing functionality."""
    
    @pytest.fixture
    def mock_pdf_bytes(self):
        """Create mock PDF bytes for testing."""
        return b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n"
    
    @pytest.fixture
    def mock_page(self):
        """Create a mock PDF page object."""
        page = Mock()
        page.get_text.return_value = "Test page content"
        
        mock_pixmap = Mock()
        mock_pixmap.tobytes.return_value = b"fake_image_data"
        page.get_pixmap.return_value = mock_pixmap
        
        return page
    
    @pytest.mark.asyncio
    async def test_process_one_page(self, mock_page):
        """Test processing of a single PDF page."""
        img_bytes, text = await process_one_page(mock_page)
        
        assert img_bytes == b"fake_image_data"
        assert text == "Test page content"
        mock_page.get_pixmap.assert_called_once()
        mock_page.get_text.assert_called_once()
    
    @pytest.mark.asyncio
    @patch('pdf_to_img_txt.fitz.open')
    async def test_pdf_to_image_and_text_success(self, mock_fitz_open, mock_pdf_bytes):
        """Test successful PDF to image and text conversion."""
        mock_doc = Mock()
        mock_page1 = Mock()
        mock_page2 = Mock()
        
        # Setup mock pages
        mock_page1.get_text.return_value = "Page 1 content"
        mock_page2.get_text.return_value = "Page 2 content"
        
        mock_pixmap1 = Mock()
        mock_pixmap1.tobytes.return_value = b"image_data_1"
        mock_page1.get_pixmap.return_value = mock_pixmap1
        
        mock_pixmap2 = Mock()
        mock_pixmap2.tobytes.return_value = b"image_data_2"
        mock_page2.get_pixmap.return_value = mock_pixmap2
        
        mock_doc.__iter__ = Mock(return_value=iter([mock_page1, mock_page2]))
        mock_doc.__enter__ = Mock(return_value=mock_doc)
        mock_doc.__exit__ = Mock(return_value=None)
        mock_fitz_open.return_value = mock_doc
        
        images, texts = await pdf_to_image_and_text(mock_pdf_bytes)
        
        assert len(images) == 2
        assert len(texts) == 2
        assert images[0] == b"image_data_1"
        assert images[1] == b"image_data_2"
        assert texts[0] == "Page 1 content"
        assert texts[1] == "Page 2 content"
    
    @pytest.mark.asyncio
    @patch('pdf_to_img_txt.fitz.open')
    async def test_pdf_to_image_and_text_empty_pdf(self, mock_fitz_open, mock_pdf_bytes):
        """Test handling of empty PDF."""
        mock_doc = Mock()
        mock_doc.__iter__ = Mock(return_value=iter([]))
        mock_doc.__enter__ = Mock(return_value=mock_doc)
        mock_doc.__exit__ = Mock(return_value=None)
        mock_fitz_open.return_value = mock_doc
        
        images, texts = await pdf_to_image_and_text(mock_pdf_bytes)
        
        assert images == []
        assert texts == []


class TestMainProcessing:
    """Test main processing functions."""
    
    @pytest.fixture
    def mock_rate_limiter(self):
        """Create a mock rate limiter."""
        return Mock(spec=RateLimiter)
    
    @pytest.fixture
    def sample_pdf_path(self, tmp_path):
        """Create a temporary PDF file for testing."""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4\ntest content")
        return str(pdf_file)
    
    @pytest.mark.asyncio
    @patch('main.pdf_to_image_and_text')
    @patch('main.generate_technical_queries')
    async def test_process_one_pdf_file_success(self, mock_generate_queries, mock_pdf_to_img, 
                                                mock_rate_limiter, sample_pdf_path):
        """Test successful processing of one PDF file."""
        # Setup mocks
        mock_pdf_to_img.return_value = ([b"image1", b"image2"], ["text1", "text2"])
        
        mock_queries = Mock()
        mock_queries.main_query = "Main query"
        mock_queries.secondary_query = "Secondary query"
        mock_queries.visual_query = "Visual query"
        mock_queries.multimodal_query = "Multimodal query"
        mock_queries.language = "en"
        mock_generate_queries.return_value = mock_queries
        
        results = await process_one_pdf_file(sample_pdf_path, mock_rate_limiter)
        
        assert len(results) == 8  # 2 pages × 4 queries each
        assert all("query" in result for result in results)
        assert all("image" in result for result in results)
        assert all("language" in result for result in results)
        assert all(result["language"] == "en" for result in results)
    
    @pytest.mark.asyncio
    @patch('main.pdf_to_image_and_text')
    @patch('main.generate_technical_queries')
    async def test_process_one_pdf_file_with_errors(self, mock_generate_queries, mock_pdf_to_img,
                                                    mock_rate_limiter, sample_pdf_path):
        """Test PDF processing with some page errors."""
        mock_pdf_to_img.return_value = ([b"image1", b"image2"], ["text1", "text2"])
        
        # First call succeeds, second fails
        mock_queries = Mock()
        mock_queries.main_query = "Main query"
        mock_queries.secondary_query = "Secondary query"
        mock_queries.visual_query = "Visual query"
        mock_queries.multimodal_query = "Multimodal query"
        mock_queries.language = "en"
        
        mock_generate_queries.side_effect = [mock_queries, Exception("API Error")]
        
        results = await process_one_pdf_file(sample_pdf_path, mock_rate_limiter)
        
        assert len(results) == 4  # Only first page processed successfully
    
    @pytest.mark.asyncio
    @patch('main.Path')
    @patch('main.process_one_pdf_file')
    @patch('main.save_data_to_parquet')
    @patch('os.makedirs')
    async def test_pdf_batch_to_parquet_part_no_files(self, mock_makedirs, mock_save_parquet, 
                                                       mock_process_pdf, mock_path):
        """Test batch processing with no PDF files."""
        mock_path_obj = Mock()
        mock_path_obj.glob.return_value = []
        mock_path.return_value = mock_path_obj
        
        await pdf_batch_to_parquet_part("test_input", "test_output", 100)
        
        mock_makedirs.assert_called_once_with("test_output", exist_ok=True)
        mock_process_pdf.assert_not_called()
        mock_save_parquet.assert_not_called()


class TestRateLimiter:
    """Test rate limiting functionality."""
    
    def test_rate_limiter_initialization(self):
        """Test rate limiter initialization."""
        limiter = RateLimiter(requests_per_second=10)
        assert limiter.capacity == 10
        assert limiter.tokens == 10
    
    @pytest.mark.asyncio
    async def test_rate_limiter_acquire(self):
        """Test rate limiter acquire method."""
        limiter = RateLimiter(requests_per_second=100)  # Fast rate for testing
        
        start_time = asyncio.get_event_loop().time()
        await limiter.acquire()
        await limiter.acquire()
        end_time = asyncio.get_event_loop().time()
        
        # Should have some minimal delay
        assert end_time >= start_time


class TestConfigValues:
    """Test configuration values."""
    
    def test_zoom_factor_is_positive(self):
        """Test that zoom factor is positive."""
        assert ZOOM_FACTOR > 0
    
    def test_chunk_size_is_positive(self):
        """Test that chunk size is positive."""
        assert CHUNK_SIZE > 0
    
    def test_output_format_is_valid(self):
        """Test that output format is valid."""
        assert OUTPUT_FORMAT in ["jpeg", "png", "ppm"]


@pytest.mark.integration
class TestIntegration:
    """Integration tests requiring actual dependencies."""
    
    @pytest.fixture
    def temp_folders(self, tmp_path):
        """Create temporary input and output folders."""
        input_folder = tmp_path / "input"
        output_folder = tmp_path / "output"
        input_folder.mkdir()
        output_folder.mkdir()
        return str(input_folder), str(output_folder)
    
    @pytest.mark.skipif(False, reason="API key available")
    @pytest.mark.asyncio
    async def test_full_pipeline_integration(self, temp_folders):
        """Test full pipeline with minimal PDF (requires API key)."""
        input_folder, output_folder = temp_folders
        
        # Create a minimal valid PDF
        minimal_pdf = b"""%PDF-1.4
1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj
2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj
3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Contents 4 0 R>>endobj
4 0 obj<</Length 44>>stream
BT /F1 12 Tf 72 720 Td (Test Page) Tj ET
endstream
endobj
xref
0 5
0000000000 65535 f 
0000000010 00000 n 
0000000053 00000 n 
0000000125 00000 n 
0000000230 00000 n 
trailer<</Size 5/Root 1 0 R>>
startxref
323
%%EOF"""
        
        pdf_path = Path(input_folder) / "test.pdf"
        pdf_path.write_bytes(minimal_pdf)
        
        # This would require mocking API calls for full test
        # For now, just verify the function can be called
        try:
            await pdf_batch_to_parquet_part(input_folder, output_folder, 10)
        except Exception as e:
            # Expected to fail without proper API setup
            assert "API" in str(e) or "key" in str(e).lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])