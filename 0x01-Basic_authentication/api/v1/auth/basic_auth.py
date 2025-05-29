printf '#!/usr/bin/env python3\n\
"""\n

BasicAuth class for Basic Authentication\n

"""\n

from api.v1.auth.auth import Auth\n

\n

\n

class BasicAuth(Auth):\n

"""\n

BasicAuth class inherits from Auth.\n

Extends Auth with methods specific to Basic Authentication.\n

"""\n

\n

def extract_base64_authorization_header(self, authorization_header: str) -> str:\n

"""\n

Extracts the Base64 encoded part of the Authorization header\n

for Basic Authentication.\n

\n

Args:\n

authorization_header (str): The value of the Authorization header.\n

\n

Returns:\n

str: The Base64 encoded part, or None if conditions are not met.\n

"""\n

if authorization_header is None:\n

return None\n

\n

if not isinstance(authorization_header, str):\n

return None\n

\n

# Check if the header starts with "Basic "\n

# The space after "Basic" is crucial as per the requirements\n

if not authorization_header.startswith("Basic "):\n

return None\n

\n

# Return the value after "Basic "\n

# The slice starts after "Basic " (which is 6 characters long)\n

return authorization_header[len("Basic "):]\n' > basic_auth.py
```
