from transformers import PegasusForConditionalGeneration, AutoTokenizer
import os
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

def download_model():
    print(Fore.YELLOW + "Starting model download...")
    
    # Create cache directory if it doesn't exist
    cache_dir = "cache_dir/transformers/google/xsum"
    os.makedirs(cache_dir, exist_ok=True)
    
    print(Fore.YELLOW + "Downloading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained("google/pegasus-xsum", cache_dir=cache_dir)
    tokenizer.save_pretrained(cache_dir)
    print(Fore.GREEN + "Tokenizer downloaded and saved successfully!")
    
    print(Fore.YELLOW + "Downloading model...")
    model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-xsum", cache_dir=cache_dir)
    model.save_pretrained(cache_dir)
    print(Fore.GREEN + "Model downloaded and saved successfully!")
    
    print(Fore.GREEN + f"\nModel and tokenizer have been saved to: {cache_dir}")

if __name__ == "__main__":
    download_model() 