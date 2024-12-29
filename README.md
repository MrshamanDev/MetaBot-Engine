# MetaBot Engine

**MetaBot Engine** is a powerful Python-based automation tool that simulates human-like browsing behavior. This tool allows users to perform tasks such as traffic simulation, proxy management, and performance monitoring with ease and efficiency.

---

## • Features

- **Human-like Behavior Simulation**: Simulates real user interactions, including clicks, scrolling, and mouse movements.
- **Multi-Tab Support**: Enables running multiple browser tabs simultaneously for realistic browsing experiences.
- **Traffic Source Simulation**: Mimics traffic from search engines, social media platforms, and referral sources.
- **Proxy Support**: Integrates proxies to mask IP addresses and manage traffic effectively.
- **Performance Monitoring**: Tracks CPU, memory, and network usage in real-time during operations.
- **Customizable View Duration**: Adjust minimum and maximum time spent on websites.
- **Logging & Console Output**: Maintains detailed logs for debugging and monitoring purposes.
- **Dark Mode**: Offers a light and dark mode for the user interface.

---

## • Requirements

Ensure you have the following installed:

- Python 3.6+
- pip (Python package installer)
- Chrome (or any Chromium-based browser)

---

## • Installation

Follow these steps to install and set up MetaBot Engine:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/MrshamanDev/MetaBot-Engine.git
   cd MetaBot-Engine
   ```

2. **Create a virtual environment (optional but recommended):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Install the Chrome WebDriver:**

   Use the `webdriver-manager` package to automate WebDriver management:

   ```bash
   pip install webdriver-manager
   ```

   Alternatively, download the correct WebDriver version manually from [ChromeDriver](https://chromedriver.chromium.org/).

---

## • Usage

1. **Run the application:**

   Start the software with:

   ```bash
   python main.py
   ```

2. **Interact with the application:**

   - **Main Tab:** Enter the website URL, configure tab settings, and start the bot.
   - **Settings Tab:** Adjust proxy settings, traffic source simulation, and view durations.
   - **Performance Tab:** Monitor resource usage in real-time.

3. **Stop the bot:**

   Use the "Stop" button to halt operations when needed.

---

## • Customization

To tailor MetaBot Engine to your specific needs, modify the `config` files or scripts as necessary. This includes:

- Adjusting bot behavior settings.
- Updating traffic simulation parameters.
- Changing logging levels for more detailed output.

---

## 🚨 Educational Use Only

**MetaBot Engine is strictly for educational purposes.**

The creator, Shaman Siddiqui, assumes no responsibility for misuse or malicious intent. Ensure you comply with applicable laws and website terms of service when using this tool.

---


## • Contributing

To contribute to this project:

1. Fork the repository.
2. Create a new branch:

   ```bash
   git checkout -b feature/YourFeature
   ```

3. Commit your changes:

   ```bash
   git commit -m 'Add YourFeature'
   ```

4. Push the branch:

   ```bash
   git push origin feature/YourFeature
   ```

---

## © Copyright

Copyright (c) 2024 Shaman Siddiqui. All rights reserved.

