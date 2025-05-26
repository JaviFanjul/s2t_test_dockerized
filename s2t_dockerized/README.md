#  Real-Time Multi-Speaker Transcription & Sentiment Analyzer

This system records audio from two independent input devices, transcribes speech in real time using Whisper models, and analyzes customer satisfaction through LLMs. A simple Tkinter UI displays the live transcription and satisfaction score.

---

##  Features

- Multi-device audio recording with VAD filtering  
- Real-time transcription using FasterWhisper  
- Chronological transcription sorting  
- Customer satisfaction analysis via LLM (Groq API)  
- Live UI for monitoring conversation and sentiment  

---

##  Requirements

- Python 3.8+
- PyAudio
- numpy, scipy, pydub
- litellm
- tkinter (built-in on most systems)
- whisper-compatible model
- Groq API key

Install dependencies:

```bash
pip install -r requirements.txt
```

---

##  Configuration

All parameters are set in `config.py`, including:

- Audio device IDs
- Recording thresholds
- Whisper model configuration
- VAD parameters
- LLM prompts and API key

---

##  How to Run

```bash
python main.py
```

This will:

1. Initialize and clean environment.
2. Launch background threads for:
   - Dual audio recording
   - Transcription
   - Sorting
   - Sentiment analysis
   - UI updates
3. Open a Tkinter window with real-time feedback.

---

##  Architecture Overview

```
┌────────────┐     ┌──────────────┐
│ VoiceRec 1 │     │ VoiceRec 2   │
└────┬───────┘     └────┬─────────┘
     ▼                  ▼
┌────────────┐   ┌──────────────┐
│ Transcriber│   │ Transcriber  │
└────┬───────┘   └────┬─────────┘
     ▼                  ▼
        ┌──────────────────┐
        │    SinkWriter     │
        └────────┬─────────┘
                 ▼
          transcription.txt
                 ▼
  ┌──────────────┴───────────────┐
  │ TranscriptionSorter          │
  │ SatisfactionMonitor          │
  │ SentimentAnalyzerUI (Tkinter)│
  └──────────────────────────────┘
```

---

##  Example Prompts

**System prompt:**
```
You are an expert in customer satisfaction analysis.
```

**User template:**
```
Analyze the following conversation between a customer and an agent...
```

---

##  License

This project is for academic and experimental use only.
# s2t_dockerized
