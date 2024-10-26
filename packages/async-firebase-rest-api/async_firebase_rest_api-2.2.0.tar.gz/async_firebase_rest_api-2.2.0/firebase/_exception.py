
#   Copyright (c) 2022 Asif Arman Rahman
#   Licensed under MIT (https://github.com/AsifArmanRahman/firebase/blob/main/LICENSE)

# --------------------------------------------------------------------------------------

import requests.exceptions
import httpx

from firebase.exceptions import PermissionDenied


def raise_detailed_error(request_object):
	try:
		request_object.raise_for_status()
	except (httpx.HTTPError, requests.exceptions.HTTPError) as e:
		# raise detailed error message
		# Check if we get a { "error" : "Permission denied." } and handle automatically
		if request_object.status_code == httpx.codes.FORBIDDEN:
			try:
				data = request_object.json()
				if isinstance(data, list):
					data = data[0]
			except (ValueError, IndexError) as _:
				pass
			else:
				if data.get("error", {}).get("code") == 403:
					raise PermissionDenied(data["error"].get("message")) from e
		raise httpx.HTTPError(request_object.text) from e
