from fastapi import Depends, HTTPException
from app.services.peloton import PelotonAPI

def get_peloton_client(username: str, password: str):
# def get_peloton_client():
    """
    Dependency to get an authenticated Peloton API client.
    """
    try:
        client = PelotonAPI(username=username, password=password)
        client.authenticate()
        return client
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")
