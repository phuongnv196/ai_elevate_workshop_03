from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from config.config import Config
import logging
import sys
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Enable CORS for all routes
    CORS(app)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'Flask API is running successfully'
        })
    
    # Root endpoint
    @app.route('/')
    def root():
        return jsonify({
            'message': 'Welcome to Flask API with Text-to-Speech and Conversation',
            'version': '2.0.0',
            'endpoints': {
                'health': '/health',
                'api': '/api',
                'tts': {
                    'convert': '/api/tts/convert',
                    'download': '/api/tts/download/<filename>',
                    'info': '/api/tts/info',
                    'cleanup': '/api/tts/cleanup'
                },
                'conversation': {
                    'list': '/api/conversation/conversations',
                    'create': '/api/conversation/conversations',
                    'delete': '/api/conversation/conversations/<conversation_id>',
                    'update': '/api/conversation/conversations/<conversation_id>',
                    'messages': '/api/conversation/conversations/<conversation_id>/messages',
                    'chat': '/api/conversation/conversations/<conversation_id>/chat'
                }
            }
        })
    
    # Register API blueprints
    try:
        from routes.api_routes import api_bp
        app.register_blueprint(api_bp, url_prefix='/api')
        logger.info("✅ API routes registered successfully")
    except Exception as e:
        logger.warning(f"⚠️  Could not register API routes: {e}")
    
    # Register TTS blueprints
    try:
        from routes.tts_routes import tts_bp
        app.register_blueprint(tts_bp, url_prefix='/api/tts')
        logger.info("✅ TTS routes registered successfully")
    except Exception as e:
        logger.warning(f"⚠️  Could not register TTS routes: {e}")
    
    # Register Conversation blueprints
    try:
        from routes.conversation_router import conversation_bp
        app.register_blueprint(conversation_bp, url_prefix='/api/conversation')
        logger.info("✅ Conversation routes registered successfully")
    except Exception as e:
        logger.warning(f"⚠️  Could not register Conversation routes: {e}")
    
    return app

def check_tts_dependencies():
    """Check if TTS dependencies are available"""
    try:
        import torch
        import transformers
        import scipy
        import numpy
        logger.info("✅ All TTS dependencies are available")
        return True
    except ImportError as e:
        logger.warning(f"⚠️  TTS dependencies missing: {e}")
        logger.warning("TTS features will be disabled. Install with: pip install torch transformers scipy numpy")
        return False

def check_conversation_dependencies():
    """Check if Conversation dependencies are available"""
    try:
        import tinydb
        import openai
        import requests
        logger.info("✅ All Conversation dependencies are available")
        return True
    except ImportError as e:
        logger.warning(f"⚠️  Conversation dependencies missing: {e}")
        logger.warning("Conversation features will be disabled. Install with: pip install tinydb openai requests")
        return False

if __name__ == '__main__':
    logger.info("🚀 Starting Flask API with Text-to-Speech and Conversation support")
    
    # Check TTS dependencies
    tts_available = check_tts_dependencies()
    
    # Check Conversation dependencies
    conversation_available = check_conversation_dependencies()
    
    if tts_available:
        logger.info("🎤 TTS features enabled")
    else:
        logger.info("📝 TTS features disabled")
        
    if conversation_available:
        logger.info("💬 Conversation features enabled")
    else:
        logger.info("📝 Conversation features disabled")
    
    app = create_app()
    
    logger.info("🌐 Server starting at http://localhost:5000")
    logger.info("📚 API Documentation: Check /api/tts/info for TTS status")
    logger.info("📚 Conversation API: Check /api/conversation/conversations for conversation features")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        logger.info("👋 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Server error: {e}")
        sys.exit(1)
