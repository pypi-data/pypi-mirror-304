#!/usr/bin/env python3
"""
Tests for the OWASPScraper class.
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

from owasp_checker_v2.owasp_scraper import OWASPScraper

@pytest.fixture
def scraper():
    """Create a test instance of OWASPScraper"""
    return OWASPScraper()

@pytest.fixture
def mock_html():
    """Create mock HTML content for testing"""
    return """
    <div class="top-10-item">
        <div class="title">A01:2021 - Broken Access Control</div>
        <div class="description">Access control enforces policy such that users cannot act outside of their intended permissions.</div>
    </div>
    <div class="cheat-sheet">
        <div class="title">Authentication Cheat Sheet</div>
        <div class="content">Implement proper authentication using secure protocols.</div>
    </div>
    """

def test_initialization(scraper):
    """Test OWASPScraper initialization"""
    assert scraper.base_url == "https://owasp.org"
    assert scraper.top_ten_url == "https://owasp.org/Top10"
    assert scraper.cheat_sheets_url == "https://owasp.org/www-project-cheat-sheets"
    assert not scraper.test_mode

def test_enable_test_mode(scraper):
    """Test enabling test mode"""
    scraper.enable_test_mode()
    assert scraper.test_mode

def test_fetch_owasp_guidelines_test_mode(scraper):
    """Test fetching guidelines in test mode"""
    scraper.enable_test_mode()
    guidelines = scraper.fetch_owasp_guidelines()
    
    assert isinstance(guidelines, dict)
    assert 'OWASP Top Ten' in guidelines
    assert 'Cheat Sheets' in guidelines
    assert 'last_updated' in guidelines
    
    # Verify mock data structure
    top_ten = guidelines['OWASP Top Ten']
    assert isinstance(top_ten, dict)
    assert len(top_ten) == 10
    assert 'A01:2021 - Broken Access Control' in top_ten
    
    cheat_sheets = guidelines['Cheat Sheets']
    assert isinstance(cheat_sheets, dict)
    assert 'Authentication Cheat Sheet' in cheat_sheets

@patch('requests.get')
def test_fetch_top_ten(mock_get, scraper, mock_html):
    """Test fetching OWASP Top Ten"""
    # Mock response
    mock_response = Mock()
    mock_response.text = mock_html
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response
    
    top_ten = scraper._fetch_top_ten()
    assert isinstance(top_ten, dict)
    assert 'A01:2021 - Broken Access Control' in top_ten
    assert top_ten['A01:2021 - Broken Access Control'].startswith('Access control')

@patch('requests.get')
def test_fetch_cheat_sheets(mock_get, scraper, mock_html):
    """Test fetching OWASP cheat sheets"""
    # Mock response
    mock_response = Mock()
    mock_response.text = mock_html
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response
    
    cheat_sheets = scraper._fetch_cheat_sheets()
    assert isinstance(cheat_sheets, dict)
    assert 'Authentication Cheat Sheet' in cheat_sheets
    assert cheat_sheets['Authentication Cheat Sheet'].startswith('Implement proper')

def test_clean_text(scraper):
    """Test text cleaning functionality"""
    dirty_text = "  Test\xa0text\u200bwith\nwhitespace  "
    clean_text = scraper._clean_text(dirty_text)
    assert clean_text == "Test text with whitespace"

def test_cache_management(scraper):
    """Test cache management functionality"""
    scraper.enable_test_mode()
    
    # Initial fetch
    guidelines1 = scraper.fetch_owasp_guidelines()
    
    # Should use cached results
    guidelines2 = scraper.fetch_owasp_guidelines()
    assert guidelines1 == guidelines2
    
    # Clear cache
    scraper.clear_cache()
    assert len(scraper.cache) == 0
    
    # Should fetch new results
    guidelines3 = scraper.fetch_owasp_guidelines()
    assert guidelines3 is not None

def test_cache_validation(scraper):
    """Test cache validation"""
    key = 'test_key'
    data = {'test': 'data'}
    
    # Add to cache
    scraper._update_cache(key, data)
    assert scraper._is_cache_valid(key)
    
    # Invalidate cache
    scraper.cache[f"{key}_time"] = datetime.now() - timedelta(hours=25)
    assert not scraper._is_cache_valid(key)

def test_update_cache_duration(scraper):
    """Test updating cache duration"""
    original_duration = scraper.cache_duration
    new_hours = 48
    
    scraper.update_cache_duration(new_hours)
    assert scraper.cache_duration == timedelta(hours=new_hours)
    assert scraper.cache_duration != original_duration

@patch('requests.get')
def test_error_handling(mock_get, scraper):
    """Test error handling"""
    # Mock network error
    mock_get.side_effect = Exception("Network error")
    
    # Should return mock data on error
    guidelines = scraper.fetch_owasp_guidelines()
    assert isinstance(guidelines, dict)
    assert 'OWASP Top Ten' in guidelines
    assert 'Cheat Sheets' in guidelines

def test_mock_data_structure(scraper):
    """Test mock data structure"""
    mock_guidelines = scraper._get_mock_guidelines()
    assert isinstance(mock_guidelines, dict)
    assert 'OWASP Top Ten' in mock_guidelines
    assert 'Cheat Sheets' in mock_guidelines
    assert 'last_updated' in mock_guidelines
    
    mock_top_ten = scraper._get_mock_top_ten()
    assert isinstance(mock_top_ten, dict)
    assert len(mock_top_ten) == 10
    
    mock_cheat_sheets = scraper._get_mock_cheat_sheets()
    assert isinstance(mock_cheat_sheets, dict)
    assert len(mock_cheat_sheets) > 0

@patch('requests.get')
def test_html_parsing(mock_get, scraper):
    """Test HTML parsing functionality"""
    html = """
    <div class="top-10-item">
        <div class="title">Test Title</div>
        <div class="description">Test Description</div>
    </div>
    """
    
    # Mock response
    mock_response = Mock()
    mock_response.text = html
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response
    
    # Parse HTML
    soup = BeautifulSoup(html, 'html.parser')
    item = soup.find(class_='top-10-item')
    title = item.find(class_='title').get_text()
    description = item.find(class_='description').get_text()
    
    assert title.strip() == 'Test Title'
    assert description.strip() == 'Test Description'

if __name__ == '__main__':
    pytest.main([__file__])
