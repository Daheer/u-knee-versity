# U-Knee-Versity

<div align="center">
<img src="./kneegpt.png" alt="banner"/>
</div>

A user-friendly, highly customizable Python web app designed to help students learn about knee anatomy and surgery.

# Getting Started

You'll need a valid Google API key - save your API key under the environment variable `GOOGLE_API_KEY`:

```bash
export GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY" # replace me!
```

### 🧬 1. Clone the Repo

```bash
git clone https://github.com/Daheer/u-knee-versity.git
```

### 📦 2. Install Reflex

To get started with Reflex, you'll need:

- Python 3.7+
- Node.js 12.22.0+ \(No JavaScript knowledge required!\)
- Pip dependencies: `reflex`, `google.generativeai`

Install `pip` dependencies with the provided `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 🚀 3. Run the application

Initialize and run the app:

```
reflex init
reflex run
```

# Features

- 100% Python-based, including the UI, using Reflex
- Create and delete chat sessions
- The application is fully customizable and no knowledge of web dev is required to use it.
    - See https://reflex.dev/docs/styling/overview for more details 
- Easily swap out any LLM
- Responsive design for various devices
- Interactive 3D model of knee anatomy

# Contributing

We welcome contributions to improve and extend the U-Knee-Versity app. 
If you'd like to contribute, please do the following:
- Fork the repository and make your changes. 
- Once you're ready, submit a pull request for review.

# License

The following repo is licensed under the MIT License.
