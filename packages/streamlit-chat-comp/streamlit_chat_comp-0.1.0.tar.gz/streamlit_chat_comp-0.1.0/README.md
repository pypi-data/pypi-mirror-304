Here is the entire content formatted as markdown code:

```markdown
# My Chat Package

## Overview

My Chat Package is a Streamlit component that allows users to seamlessly send both text and audio messages as base64 strings to chat applications. It's designed to enhance the interactivity of Streamlit apps by providing an intuitive chat interface.

## Features

- **Text Input**: Users can type and send text messages.
- **Audio Recording**: Users can record audio and send it as base64 strings.
- **Streamlit Integration**: Easily integrates with Streamlit applications.
- **Responsive Design**: Adaptable to different screen sizes.

## Why Use This Package?

1. **Enhanced User Interaction**: Allows users to communicate using both text and audio, enriching the chat experience.
2. **Easy Integration**: With Streamlit, adding interactive components is straightforward, making this package a quick addition to any app.
3. **Modern UI**: The component uses a sleek, modern design with responsive features to fit various devices.

## Installation

Install the package using pip:

```bash
pip install streamlit_chat_comp
```

## Usage

Here's a simple example of how to use the package in a Streamlit app:

```python
import streamlit as st
from streamlit_chat_comp.chat_component import chat_input

st.title("Chat Application")

chat_input()
```

## How It Works

- **Text Messages**: Users type a message and click the send button. The message is then sent to the Streamlit backend as a base64 encoded string.
- **Audio Messages**: Users can click the microphone icon to start recording. Once the recording is stopped, the audio is encoded in base64 and sent to the backend.

## Key Components

- **HTML Structure**: Provides a clean and organized interface for the chat input.
- **CSS Styling**: Ensures the chat component is visually appealing and responsive.
- **JavaScript Logic**: Handles the input events, audio recording, and data encoding.

## Detailed Example

```python
import streamlit as st
from streamlit_chat_comp.chat_component import chat_input

def main():
    st.title("Interactive Chat App")
    st.write("This app allows you to send text and audio messages.")

    chat_input()

if __name__ == "__main__":
    main()
```

## Handling Data in Streamlit

The package sends data to the Streamlit backend using `window.parent.postMessage`. On the Streamlit side, you can handle these messages by listening to the component's output.

## License

This package is distributed under the MIT License. See the LICENSE file for more information.

## Contributions

Contributions are welcome! Please fork the repository and submit a pull request with your improvements.

## Support

If you encounter any issues or have questions, feel free to open an issue in the GitHub repository.

---

This package is perfect for developers looking to add dynamic chat features to their Streamlit applications. Enjoy creating interactive and engaging apps with My Chat Package!
```

You can now copy and paste this markdown code directly into your README file. Let me know if you need anything else!


