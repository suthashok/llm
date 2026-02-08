# Running Open-Source LLMs on Google Colab

A beginner-friendly guide to running your first open-source language model using Google Colab's free T4 GPU.

## What This Does

- Runs a 3B parameter language model (Llama 3.2) on Google Colab
- Uses GPU acceleration for fast inference (~30-60 tokens/second)
- Requires zero setup beyond a Google account
- Works entirely in your browser

## What You'll Learn

- How to enable GPU in Colab
- How to load and run quantized models with llama.cpp
- How to measure performance (tokens/sec, VRAM usage)
- How to interact with an LLM programmatically

## Prerequisites

- Google account (for Colab access)
- Basic Python knowledge
- Understanding of what LLMs are (helpful but not required)

## Quick Start (5 minutes)

### 1. Open Google Colab

Go to [colab.research.google.com](https://colab.research.google.com) and create a new notebook.

### 2. Enable GPU

- Click `Runtime` → `Change runtime type`
- Set `Hardware accelerator` to `T4 GPU`
- Click `Save`

### 3. Run the Setup

Copy and paste this into the first cell and run it:

```python
# Verify GPU is available
!nvidia-smi
```

You should see information about a T4 GPU with ~15GB memory.

### 4. Install Dependencies

```python
# Install llama.cpp with GPU support (takes ~2-3 minutes)
!CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python --no-cache-dir --force-reinstall --upgrade
!pip install huggingface_hub
```

### 5. Download the Model

```python
from huggingface_hub import hf_hub_download

model_path = hf_hub_download(
    repo_id="bartowski/Llama-3.2-3B-Instruct-GGUF",
    filename="Llama-3.2-3B-Instruct-Q4_K_M.gguf",
    local_dir="./models"
)

print(f"✓ Model downloaded to: {model_path}")
```

### 6. Load and Run

```python
from llama_cpp import Llama
import time

# Load model onto GPU
llm = Llama(
    model_path=model_path,
    n_gpu_layers=-1,      # Use GPU for all layers
    n_ctx=2048,           # Context window size
    verbose=True
)

# Test it
prompt = "Explain what a GPU is in one sentence."
start = time.time()

response = llm(
    prompt,
    max_tokens=100,
    temperature=0.7
)

# Show results
output = response['choices'][0]['text']
tokens = response['usage']['completion_tokens']
speed = tokens / (time.time() - start)

print(f"Response: {output}")
print(f"\nPerformance: {tokens} tokens in {speed:.1f} tokens/sec")
```

### 7. Check VRAM Usage

```python
!nvidia-smi --query-gpu=memory.used,memory.total --format=csv
```

Expected: ~2-3GB used out of 15GB available.

## Understanding the Components

### Platform: Google Colab
- Free cloud environment with GPU access
- T4 GPU: 15GB VRAM, good for models up to ~7B parameters (quantized)
- No installation needed, runs in browser

### Runtime: llama.cpp
- C++ implementation optimized for inference
- Supports quantized models (smaller, faster)
- GPU acceleration via CUDA

### Model: Llama 3.2 3B Instruct (Q4)
- **3B parameters**: Relatively small, fast model
- **Instruct-tuned**: Trained to follow instructions
- **Q4 quantized**: 4 bits per parameter (~2GB instead of ~12GB)
- **GGUF format**: Standard format for llama.cpp

## Key Parameters Explained

### Model Loading
```python
n_gpu_layers=-1     # -1 = use GPU for everything, 0 = CPU only
n_ctx=2048          # Max context length in tokens (~1500 words)
verbose=True        # Show loading details
```

### Inference
```python
max_tokens=100      # Maximum response length
temperature=0.7     # Randomness: 0=deterministic, 1=creative
stop=["User:"]      # Tokens that end generation
```

## Performance Expectations

On Colab's free T4 GPU:

| Model Size | Quantization | Speed | VRAM Used |
|------------|--------------|-------|-----------|
| 3B params  | Q4           | 40-60 tok/s | ~2-3GB |
| 7B params  | Q4           | 20-30 tok/s | ~4-5GB |
| 13B params | Q4           | 10-15 tok/s | ~8-9GB |

## Troubleshooting

### "CUDA not available" or very slow
- Make sure GPU is enabled: Runtime → Change runtime type → T4 GPU
- Check `n_gpu_layers=-1` is set when loading the model

### Out of memory errors
- Use a smaller model or lower quantization (Q4_K_S instead of Q4_K_M)
- Reduce `n_ctx` to 1024 or lower

### Model outputs gibberish
- Model file may be corrupted, try re-downloading
- Check you're using an "instruct" model, not a base model

### Colab disconnects
- Free tier has usage limits and timeouts
- Save your work regularly
- Consider Colab Pro for longer sessions

## Experimenting Further

### Try Different Models

Search [Hugging Face](https://huggingface.co/models?search=gguf) for "GGUF" models. Popular options:

```python
# Mistral 7B (smart, concise)
repo_id="TheBloke/Mistral-7B-Instruct-v0.2-GGUF"
filename="mistral-7b-instruct-v0.2.Q4_K_M.gguf"

# Phi-3 Mini (very efficient)
repo_id="bartowski/Phi-3-mini-128k-instruct-GGUF"
filename="Phi-3-mini-128k-instruct-Q4_K_M.gguf"
```

### Adjust Generation Parameters

```python
# More creative
response = llm(prompt, temperature=0.9, top_p=0.95)

# More focused/deterministic
response = llm(prompt, temperature=0.3, top_p=0.9)

# Longer responses
response = llm(prompt, max_tokens=500)
```

### Build a Simple Chatbot

```python
def chat(message):
    response = llm(
        f"User: {message}\nAssistant:",
        max_tokens=200,
        temperature=0.7,
        stop=["User:"]
    )
    return response['choices'][0]['text'].strip()

# Use it
print(chat("What's the capital of France?"))
print(chat("Tell me a joke about programming."))
```

## Migration to Cloud GPUs

This exact code works on other platforms. Just change the GPU:

| Platform | GPU Options | Notes |
|----------|-------------|-------|
| **RunPod** | A40, A100 | Pay per minute, very affordable |
| **Vast.ai** | Various | Cheapest option, community GPUs |
| **AWS EC2** | A10G, A100 | Enterprise-grade, more expensive |
| **Google Cloud** | T4, V100, A100 | Similar to AWS |

The code stays the same - just use a better GPU for larger models or higher throughput.

## Resources

- [llama.cpp documentation](https://github.com/ggerganov/llama.cpp)
- [Hugging Face GGUF models](https://huggingface.co/models?search=gguf)
- [Google Colab docs](https://colab.research.google.com/notebooks/intro.ipynb)

## License

This guide is MIT licensed. Models have their own licenses - check the model card on Hugging Face before commercial use.

## Contributing

Found an issue or have improvements? Feel free to open an issue or pull request!

---

**Note:** Google Colab's free tier has usage limits. If you get disconnected or can't access GPU, wait a few hours or consider Colab Pro ($10/month) for reliable access.
