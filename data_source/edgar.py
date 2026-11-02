


from config import MY_EMAIL
from edgar import set_identity, Company


def _get_financials(ticker: str):
    if not MY_EMAIL:
        raise ValueError("MY_EMAIL is required for SEC EDGAR identity")
    set_identity(MY_EMAIL)
    return Company(ticker).get_financials()