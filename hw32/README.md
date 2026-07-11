Installation guide

1. **To install requirements enter in your terminal command below:**
    
    `pip install -r requirements.txt`


2. **Install Ollama** from https://ollama.com/download

3. **Download the AI model:**

   `ollama pull llama3`

   To verify that the model is installed:

   `ollama list`

4. **Create a `.env` file in the project directory with:**

   - BOT_TOKEN=`YOUR_BOTFATHER_BOT_TOKEN`
   - OLLAMA_MODEL=`llama3`

5. **Run the bot:**

   `python main.py`