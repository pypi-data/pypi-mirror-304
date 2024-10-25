# Infin8t

Infin8t is a Python package for integrating AI-powered chatbots into web applications.

## Installation

You can install Infin8t using pip:

```
pip install infin8t
```

## Usage

Here's a basic example of how to use Infin8t:

```python
from infin8t import Infin8t

# Initialize the chatbot with your API key
chatbot = Infin8t(api_key='YOUR_API_KEY')

# Send a message to the chatbot
response = chatbot.send_message('Hello, chatbot!')
print(response)

# Get the script tag for web integration
script_tag = chatbot.get_script_tag()
print(script_tag)
```

## Features

- Easy integration with web applications
- Customizable chatbot behavior
- Support for multiple AI models

## Documentation

For more detailed information, please refer to our [official documentation](https://infin8t.tech/docs).

## Contributing

We welcome contributions! Please see our [contributing guidelines](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, please file an issue on our [GitHub issue tracker](https://github.com/yourusername/infin8t/issues).

## About

Infin8t is developed and maintained by the Infin8t Team. For more information, visit our [website](https://infin8t.tech).
