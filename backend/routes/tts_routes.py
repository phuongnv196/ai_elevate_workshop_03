from flask import Blueprint, jsonify, request, send_file
import os
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Create blueprint for TTS routes
tts_bp = Blueprint('tts', __name__)

@tts_bp.route('/info', methods=['GET'])
def get_tts_info():
    """Get TTS model information"""
    try:
        # Import TTS service only when needed
        from services.tts_service import tts_service
        info = tts_service.get_model_info()
        return jsonify({
            'success': True,
            'data': info,
            'message': 'TTS model information retrieved successfully'
        })
    except Exception as e:
        logger.error(f"TTS info error: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to retrieve TTS model information'
        }), 500

@tts_bp.route('/convert', methods=['POST'])
def text_to_speech():
    """Convert text to speech"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'success': False,
                'message': 'Text is required in request body'
            }), 400
        
        text = data.get('text', '').strip()
        output_filename = data.get('filename', None)
        
        if not text:
            return jsonify({
                'success': False,
                'message': 'Text cannot be empty'
            }), 400
        
        # Import TTS service only when needed
        from services.tts_service import tts_service
        
        # Convert text to speech
        result = tts_service.text_to_speech(text, output_filename)
        
        if result['success']:
            # Remove file_path from response for security
            response_data = {k: v for k, v in result.items() if k != 'file_path'}
            return jsonify({
                'success': True,
                'data': response_data,
                'message': 'Text converted to speech successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Unknown error'),
                'message': 'Failed to convert text to speech'
            }), 500
            
    except Exception as e:
        logger.error(f"TTS conversion error: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to process text-to-speech request'
        }), 500

@tts_bp.route('/download/<filename>', methods=['GET'])
def download_audio(filename):
    """Download generated audio file"""
    try:
        # Validate filename
        if not filename.endswith('.wav'):
            return jsonify({
                'success': False,
                'message': 'Invalid file format'
            }), 400
        
        # Import TTS service only when needed
        from services.tts_service import tts_service
        
        # Construct file path
        file_path = os.path.join(tts_service.output_dir, filename)
        
        # Check if file exists
        if not os.path.exists(file_path):
            return jsonify({
                'success': False,
                'message': 'File not found'
            }), 404
        
        # Send file
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='audio/wav'
        )
        
    except Exception as e:
        logger.error(f"TTS download error: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to download audio file'
        }), 500

@tts_bp.route('/cleanup', methods=['POST'])
def cleanup_audio_files():
    """Clean up old audio files"""
    try:
        data = request.get_json() or {}
        max_age_hours = data.get('max_age_hours', 24)
        
        # Import TTS service only when needed
        from services.tts_service import tts_service
        
        result = tts_service.cleanup_old_files(max_age_hours)
        
        if result['success']:
            return jsonify({
                'success': True,
                'data': result,
                'message': 'Cleanup completed successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Unknown error'),
                'message': 'Failed to cleanup files'
            }), 500
            
    except Exception as e:
        logger.error(f"TTS cleanup error: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to cleanup audio files'
        }), 500
