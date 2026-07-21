import httpx


async def url_check(params: dict, url: str, timeout: float = 10.0):
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise ValueError(
        f"Open-Meteo has returned an error {exc.response.status_code}"
        ) from exc
    except httpx.RequestError as exc:
        raise ValueError(f"Unable to contact Open-Meteo : {exc}") from exc

    return response.json()