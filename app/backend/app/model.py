"""Model loading and translation inference."""
import os
import tensorflow as tf
from transformers import AutoTokenizer, TFAutoModelForSeq2SeqLM
from .config import MODEL_PATH, MAX_LENGTH, NUM_BEAMS

# Set TensorFlow to use legacy Keras
os.environ['TF_USE_LEGACY_KERAS'] = '1'

# Global variables for model and tokenizer
_model = None
_tokenizer = None


def load_model():
    """Load the translation model and tokenizer."""
    global _model, _tokenizer
    
    if _model is None or _tokenizer is None:
        print(f"Loading model from {MODEL_PATH}...")
        try:
            _tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
            _model = TFAutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH)
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    
    return _model, _tokenizer


def translate_text(text: str) -> str:
    """
    Translate English text to Spanish.
    
    Args:
        text: English text to translate
        
    Returns:
        Translated Spanish text
    """
    global _model, _tokenizer
    
    # Load model if not already loaded
    if _model is None or _tokenizer is None:
        _model, _tokenizer = load_model()
    
    try:
        # Tokenize input
        inputs = _tokenizer(
            text,
            return_tensors="tf",
            max_length=MAX_LENGTH,
            truncation=True,
            padding=True
        )
        
        # Generate translation
        outputs = _model.generate(
            inputs["input_ids"],
            max_length=MAX_LENGTH,
            num_beams=NUM_BEAMS,
            early_stopping=True
        )
        
        # Decode output
        translation = _tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Remove leading inverted question mark if present
        if translation.startswith('¿'):
            translation = translation[1:].lstrip()
        
        return translation
        
    except Exception as e:
        raise Exception(f"Translation error: {str(e)}")

