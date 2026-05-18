import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "api"))

from lib.tools import dispatch_tool


def test_book_appointment_missing_name():
    result = dispatch_tool("book_appointment", {"date": "2026-05-18", "time": "10:00", "service": "oil change", "phone": "555-1234"})
    assert "name" in result.lower()


def test_book_appointment_missing_date():
    result = dispatch_tool("book_appointment", {"customer_name": "Alex", "time": "10:00", "service": "oil change", "phone": "555-1234"})
    assert "date" in result.lower()


def test_book_appointment_missing_time():
    result = dispatch_tool("book_appointment", {"customer_name": "Alex", "date": "2026-05-18", "service": "oil change", "phone": "555-1234"})
    assert "time" in result.lower()


def test_book_appointment_missing_service():
    result = dispatch_tool("book_appointment", {"customer_name": "Alex", "date": "2026-05-18", "time": "10:00", "phone": "555-1234"})
    assert "service" in result.lower()


def test_book_appointment_missing_phone():
    result = dispatch_tool("book_appointment", {"customer_name": "Alex", "date": "2026-05-18", "time": "10:00", "service": "oil change"})
    assert "phone" in result.lower()


def test_book_appointment_empty_strings():
    result = dispatch_tool("book_appointment", {"customer_name": "  ", "date": "", "time": "", "service": "", "phone": ""})
    assert "name" in result.lower()


def test_submit_inquiry_missing_name():
    result = dispatch_tool("submit_inquiry", {"message": "Fleet pricing?", "contact": "555-9876"})
    assert "name" in result.lower()


def test_submit_inquiry_missing_message():
    result = dispatch_tool("submit_inquiry", {"customer_name": "Jordan", "contact": "555-9876"})
    assert "inquiry" in result.lower() or "about" in result.lower()


def test_submit_inquiry_missing_contact():
    result = dispatch_tool("submit_inquiry", {"customer_name": "Jordan", "message": "Fleet pricing?"})
    assert "phone" in result.lower() or "email" in result.lower() or "reach" in result.lower()


def test_submit_inquiry_empty_strings():
    result = dispatch_tool("submit_inquiry", {"customer_name": "  ", "message": "", "contact": ""})
    assert "name" in result.lower()


def test_unknown_tool():
    result = dispatch_tool("nonexistent_tool", {})
    assert "unknown" in result.lower()
