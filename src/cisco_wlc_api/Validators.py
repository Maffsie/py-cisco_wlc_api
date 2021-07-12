from .Decorators import validator
import re

class URL:
	@validator
	def Base(url: str):
		assert re.match('^https?://', url), \
			f"Base URL parameter ('{url}') must begin with http(s)://"
		assert not url.endswith('/'), \
			f"Base URL parameter ('{url}') must not end with a forward-slash"


class Credentials:
	@validator
	def Type(credentials: tuple):
		assert type(credentials) is tuple, \
			f"Credentials parameter must be a tuple, but given object was actually a {type(credentials)}"
		assert len(credentials) == 2, \
			f"Credentials parameter must contain a username and a password, but given object contained {len(credentials)} item(s)"
