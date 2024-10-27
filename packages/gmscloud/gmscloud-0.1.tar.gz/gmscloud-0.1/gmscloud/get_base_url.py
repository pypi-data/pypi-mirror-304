def get_base_url(company_code):
    """Mengembalikan base URL berdasarkan kode perusahaan."""
    if company_code.lower() == "gig":
        return "https://gig.example.com"
    elif company_code.lower() == "sg":
        return "https://app2.gmscloud.id"
    elif company_code.lower() == "bgs":
        return "https://bgs.example.com"
    elif company_code.lower() == "sga":
        return "https://sga.example.com"
    return "https://app2.gmscloud.id"  # Domain default
