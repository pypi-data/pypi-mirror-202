# Textoria API

Textoria API is a simple key-value store API that allows you to store, retrieve, update, and delete key-value pairs. It is built using aiohttp and provides an asynchronous interface for efficient and fast operations.

## Features

- Store key-value pairs
- Retrieve all key-value pairs
- Update the value of a specific key
- Delete a specific key-value pair

## Installation

To use the Textoria API, simply clone the repository and install the required dependencies:

```bash
git clone https://github.com/your_username/textoria-api.git
cd textoria-api
pip install -r requirements.txt
```

## Usage

First, you need to instantiate the `Textoria` class with the API URL:

```python
from textoria import Textoria

api_url = "https://example.com/api"
textoria = Textoria(api_url)
```

### Get all keys

To retrieve all the key-value pairs stored in the system, you can use the `get_all_keys` method:

```python
keys = await textoria.get_all_keys()
print(keys)
```

### Create a new key-value pair

To create a new key-value pair, use the `create_key` method with the key and value as arguments:

```python
new_key = "example_key"
new_value = "example_value"
response = await textoria.create_key(new_key, new_value)
print(response)
```

### Update an existing key-value pair

To update the value of an existing key, use the `update_key` method with the key and the new value as arguments:

```python
key = "example_key"
new_value = "updated_value"
response = await textoria.update_key(key, new_value)
print(response)
```

### Delete a key-value pair

To delete a specific key-value pair, use the `delete_key` method with the key as argument:

```python
key = "example_key"
response = await textoria.delete_key(key)
print(response)
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue to report bugs or suggest improvements.

## License

This project is released under the [MIT License](LICENSE).