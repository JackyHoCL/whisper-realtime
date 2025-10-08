#VLLM
VLLM_ADDR = 'localhost'   #Your vllm server ip
VLLM_PORT = '8128'          #Your vllm server port
VLLM_PATH = '/v1'
VLLM_KEY = ''             #Your vllm key
VLLM_PROTOCOL = 'http'
VLLM_MODEL_NAME = 'whisper-3'  #Should be the same name as the served-model-name or model name in runModel.sh
VLLM_DEFAULT_LANG = ''

#VAD
VAD_THRESHOLD = 0.5               #The threshold is used to determine whether it is a speech activity in a single hop
VAD_HOP_SIZE = 256
VAD_SILENT_THRESHOLD = 3         #How may frames should wait before send to whisper
VAD_SEND_THRESHOLD = 2000000      #Send if audio data accumulated number exceed threshold, 1000000 is around 5 seconds
VAD_AVG_SCORE_THRESHOLD = 0.1     #The threshold is used to determine whether it is a speech activity in a single speech frame by calculating the avg result return by VAD_THRESHOLD
                                  #eg. 100 hops in a frame, 90 of them are 1, 10 of them are 0, the avg_score should be (90+0)/100 = 0.9
                                  #The recording is start when exceed the score.
VAD_MIN_THRESHOLD = 50000        #Minimum length to transcribe

#SERVER
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 10928
SERVER_RELOAD = True             #For debug and dev purpose, suggest False in production environment

#AUDIO
AUDIO_SAMPLE_RATE = 16000            #Input audio sampling rate

#HALLUCINATION
HALLUCINATION_COLLECTOR = False     #Turn on hallucination collector to generate output.json? 
                                    #!DO NOT TURN ON UNLESS YOU CAN COLLECTING HALLUCINATIONS
                                    #If the data is record as hallucination in mistake, manually remove in util/hallucinations.json
