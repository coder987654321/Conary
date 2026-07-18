# Conary Universal Installation Guide
> "High level and low level coding combined"

This manual provides a single, cross-platform workflow to globally install the Conary scripting language environment on Windows, macOS, or Linux.

---

## 🏗️ Step 1: Install Python 3 & PIP (System Layer)

Ensure your machine has a functioning Python environment before proceeding:

* **Windows:** Download the installer from python.org. Run it, and ensure you check "Add python.exe to PATH" before clicking install.
* **macOS:** Open a terminal and install via Homebrew: brew install python
* **Linux (Ubuntu/Debian):** Open a terminal and run: sudo apt update && sudo apt install python3 python3-pip -y

---

## 🚀 Step 2: Download, Bind, and Run Conary Globally

Once Python is verified on your system, execute the following commands sequence in your terminal app to clone the codebase and link the interpreter script globally:

1. Fetch your language source distribution from the cloud server:
   git clone https://github.com/coder978654321/Conary.git
   cd Conary

2. Bind the engine to your global system path configuration terminal:
   pip install -e .

3. Test the active runtime engine initialization framework:
   conary

If configured properly, your machine will instantly respond with your language's verification signature:
"Conary Runtime Active. (High level and low level coding combined)"