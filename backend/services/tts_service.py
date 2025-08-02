import os
import uuid
import tempfile
from datetime import datetime
from typing import Optional, Tuple, Dict
import logging

# Configure logging
logger = logging.getLogger(__name__)

class TTSService:
    """Text-to-Speech service using Meta's MMS-TTS model"""
    
    def __init__(self):
        """Initialize the TTS service with the model and tokenizer"""
        self.model_name = "facebook/mms-tts-eng"
        self.tokenizer = None
        self.model = None
        self.output_dir = os.path.join(tempfile.gettempdir(), "tts_outputs")
        self.is_available = False
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Try to load model
        self._load_model()
    
    def _load_model(self):
        """Load the tokenizer and model with error handling"""
        try:
            # Check if required packages are available
            self._check_dependencies()
            
            logger.info("Loading TTS model...")
            from transformers import AutoTokenizer, AutoModelForTextToWaveform
            
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForTextToWaveform.from_pretrained(self.model_name)
            self.is_available = True
            logger.info("TTS model loaded successfully!")
            
        except ImportError as e:
            logger.warning(f"TTS dependencies not available: {e}")
            self.is_available = False
        except Exception as e:
            logger.error(f"Error loading TTS model: {str(e)}")
            self.is_available = False
    
    def _check_dependencies(self):
        """Check if all required dependencies are available"""
        required_modules = ['torch', 'transformers', 'scipy', 'numpy']
        missing = []
        
        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                missing.append(module)
        
        if missing:
            raise ImportError(f"Missing required modules: {', '.join(missing)}")
    
    def text_to_speech(self, text: str, output_filename: Optional[str] = None) -> Dict:
        """
        Convert text to speech and save as WAV file
        
        Args:
            text (str): The text to convert to speech
            output_filename (str, optional): Custom filename for output
            
        Returns:
            dict: Result containing success status, file path, and metadata
        """
        if not self.is_available:
            return {
                'success': False,
                'error': 'TTS service is not available. Missing dependencies: torch, transformers, scipy, numpy',
                'text': text
            }
        
        try:
            import torch
            import scipy.io.wavfile
            import numpy as np
            
            if not text or not text.strip():
                raise ValueError("Text cannot be empty")
            
            # Validate text length (reasonable limit)
            if len(text) > 5000:
                raise ValueError("Text is too long. Please limit to 5000 characters.")
            
            # Generate unique filename if not provided
            if not output_filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                unique_id = str(uuid.uuid4())[:8]
                output_filename = f"tts_{timestamp}_{unique_id}.wav"
            
            # Ensure filename has .wav extension
            if not output_filename.endswith('.wav'):
                output_filename += '.wav'
            
            output_path = os.path.join(self.output_dir, output_filename)
            
            # Tokenize the input text
            inputs = self.tokenizer(text, return_tensors="pt")
            
            # Generate waveform
            with torch.no_grad():
                output = self.model(**inputs)
            
            # Extract waveform
            waveform = output.waveform[0].cpu().numpy()
            
            # Normalize waveform to prevent clipping
            waveform = self._normalize_waveform(waveform)
            
            # Save to WAV file
            scipy.io.wavfile.write(
                output_path, 
                rate=self.model.config.sampling_rate, 
                data=waveform
            )
            
            # Get file size
            file_size = os.path.getsize(output_path)
            
            return {
                'success': True,
                'file_path': output_path,
                'filename': output_filename,
                'text': text,
                'duration_seconds': len(waveform) / self.model.config.sampling_rate,
                'sampling_rate': self.model.config.sampling_rate,
                'file_size_bytes': file_size,
                'created_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'text': text if 'text' in locals() else None
            }
    
    def _normalize_waveform(self, waveform):
        """
        Normalize waveform to prevent clipping and improve audio quality
        
        Args:
            waveform (np.ndarray): Input waveform
            
        Returns:
            np.ndarray: Normalized waveform
        """
        import numpy as np
        
        # Find the maximum absolute value
        max_val = np.max(np.abs(waveform))
        
        # Normalize to prevent clipping (leave some headroom)
        if max_val > 0:
            waveform = waveform / max_val * 0.95
        
        # Convert to 16-bit integer format
        waveform = (waveform * 32767).astype(np.int16)
        
        return waveform
    
    def cleanup_old_files(self, max_age_hours: int = 24):
        """
        Clean up old generated audio files
        
        Args:
            max_age_hours (int): Maximum age of files to keep in hours
        """
        try:
            current_time = datetime.now()
            deleted_count = 0
            
            for filename in os.listdir(self.output_dir):
                if filename.endswith('.wav'):
                    file_path = os.path.join(self.output_dir, filename)
                    file_time = datetime.fromtimestamp(os.path.getctime(file_path))
                    age_hours = (current_time - file_time).total_seconds() / 3600
                    
                    if age_hours > max_age_hours:
                        os.remove(file_path)
                        deleted_count += 1
            
            return {
                'success': True,
                'deleted_files': deleted_count,
                'message': f'Cleaned up {deleted_count} old files'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_model_info(self) -> Dict:
        """
        Get information about the loaded model
        
        Returns:
            dict: Model information
        """
        try:
            return {
                'model_name': self.model_name,
                'sampling_rate': self.model.config.sampling_rate if self.model else None,
                'is_loaded': self.is_available and self.model is not None and self.tokenizer is not None,
                'is_available': self.is_available,
                'output_directory': self.output_dir,
                'status': 'Ready' if self.is_available else 'Dependencies missing'
            }
        except Exception as e:
            return {
                'model_name': self.model_name,
                'error': str(e),
                'is_loaded': False,
                'is_available': False,
                'output_directory': self.output_dir,
                'status': 'Error'
            }

# Create global instance with error handling
try:
    tts_service = TTSService()
    logger.info(f"TTS Service initialized - Available: {tts_service.is_available}")
except Exception as e:
    logger.error(f"Failed to initialize TTS Service: {e}")
    # Create a dummy service that will return appropriate error messages
    class DummyTTSService:
        def __init__(self):
            self.is_available = False
            self.output_dir = os.path.join(tempfile.gettempdir(), "tts_outputs")
            os.makedirs(self.output_dir, exist_ok=True)
        
        def text_to_speech(self, text, output_filename=None):
            return {
                'success': False,
                'error': 'TTS service is not available due to initialization error',
                'text': text
            }
        
        def get_model_info(self):
            return {
                'model_name': 'facebook/mms-tts-eng',
                'is_loaded': False,
                'is_available': False,
                'status': 'Service unavailable',
                'error': 'Failed to initialize TTS service'
            }
        
        def cleanup_old_files(self, max_age_hours=24):
            return {
                'success': False,
                'error': 'TTS service is not available'
            }
    
    tts_service = DummyTTSService()
