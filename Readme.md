**Remarks:**
1. Should be run on linux server. (vllm installation issue)
2. 2 ports are required. The model is served on 8128, fastapi listen to 10928. You can change them in runModel.sh and config.py

**Dependencies:**
1. Ten-VAD: Detect speech activities:
   https://github.com/TEN-framework/ten-vad
2. vLLM: Deploy whisper models
   https://github.com/vllm-project/vllm

**Deployment:**

1. Install Dependencies:
   ```
   pip install -r requirements.txt
   ```
   
2. Run script to start VLLM and download the whisper model
   ```
   sh runModel.sh
   ```
3. Run the application server
   ```
   python server.py
   ```
4. Test the result with the sample in sample/sample_web_client.html
   Results should be shown in console of server.py
   Change path if need:
   ```
   ws = new WebSocket('ws://localhost:10928/transcribe/stream');
   ```

6. Modify config.py if you want to finetune the results
