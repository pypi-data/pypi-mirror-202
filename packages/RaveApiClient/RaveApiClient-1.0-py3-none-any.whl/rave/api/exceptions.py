class APIError(Exception):
    ...


class Unknown(APIError):
	...


class SlowDown(APIError):
	...
	

def handle_exception(data: dict = None):
    raise {
        2015: SlowDown,
    }.get(data.get("error", {}).get("code", 666), Unknown)(data)
