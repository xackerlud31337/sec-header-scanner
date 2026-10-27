from project import check_headers


def test_all_headers_present():
    headers = {
        "Content-Security-Policy": "default-src 'self'",
        "Strict-Transport-Security": "max-age=31536000",
        "X-Frame-Options": "DENY",
        "X-Content-Type-Options": "nosniff",
    }
    assert check_headers(headers) == {"missing": [], "leaks": []}


def test_all_headers_missing():
    result = check_headers({})
    assert result["missing"] == [
        "Content-Security-Policy",
        "Strict-Transport-Security",
        "X-Frame-Options",
        "X-Content-Type-Options",
    ]
    assert result["leaks"] == []


def test_leaks_reported_with_value():
    result = check_headers({"Server": "Apache/2.4.29", "X-Powered-By": "PHP/7.2.24"})
    assert result["leaks"] == ["Server: Apache/2.4.29", "X-Powered-By: PHP/7.2.24"]
