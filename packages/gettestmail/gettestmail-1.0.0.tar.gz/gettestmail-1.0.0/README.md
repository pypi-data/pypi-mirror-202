# python-sdk
Python SDK for GetTestMail

This Python client library allows you to interact with the GetTestMail API, which provides a simple way to create temporary email addresses and receive messages sent to them.

## Usage

```python
from gettestmail.client import GetTestMailClient

# optional parameters
expires_at = "2023-04-01T00:00:00Z"

client = GetTestMailClient("your-api-key")
test_mail = client.create_new()
print(test_mail.emailAddress)

# This will wait for a message to be received up until expires_at time
test_mail = client.wait_for_message(test_mail.emailAddress)
print(test_mail.message)

```

## API Documentation

TODO

## License

This project is licensed under the MIT License. See the LICENSE file for details.