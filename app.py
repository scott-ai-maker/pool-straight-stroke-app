"""
Flask Web Application for Pool Stroke Trainer.

A real-time computer vision application that helps pool players perfect their
straight stroke technique through visual feedback and quantitative metrics.

Author: Scott Gordon
Email: scott.aiengineer@outlook.com
License: MIT
"""

from flask import Flask, render_template, request, jsonify, session
import cv2
import numpy as np
import base64
from stroke_analyzer import PoolStrokeAnalyzer
import secrets
import os
import logging
from typing import Optional, Dict, Any, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask application
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(16))

# Session-based analyzer storage
# Each user session maintains its own analyzer instance for independent tracking
# Note: For production with multiple workers, consider using Redis or similar
analyzers: Dict[str, PoolStrokeAnalyzer] = {}


def get_analyzer() -> PoolStrokeAnalyzer:
    """Get or create analyzer instance for the current user session.
    
    Each user session maintains its own PoolStrokeAnalyzer instance to provide
    independent tracking across multiple concurrent users. Session IDs are
    securely generated using cryptographic random tokens.
    
    Returns:
        PoolStrokeAnalyzer: The analyzer instance for the current session.
        
    Note:
        This implementation works well for single-worker deployments (like HF Spaces).
        For multi-worker production environments, consider using Redis or similar
        for shared session storage.
    """
    try:
        if 'session_id' not in session:
            session['session_id'] = secrets.token_hex(8)
        
        session_id = session['session_id']
        
        if session_id not in analyzers:
            analyzers[session_id] = PoolStrokeAnalyzer(
                max_points=30,
                deviation_threshold=15.0
            )
            logger.info(f"Created new analyzer for session: {session_id}")
        
        return analyzers[session_id]
        
    except Exception as e:
        logger.error(f"Error getting analyzer: {str(e)}")
        raise


def decode_image(base64_string: str) -> Optional[np.ndarray]:
    """Decode base64-encoded image string to OpenCV format.
    
    Converts a base64-encoded image (typically sent from the client as a data URL)
    into a NumPy array that OpenCV can process. Handles both raw base64 strings
    and data URLs with MIME type headers.
    
    Args:
        base64_string: Base64-encoded image string, optionally with data URL header
                      (e.g., 'data:image/jpeg;base64,...').
                      
    Returns:
        NumPy array in BGR format (OpenCV standard), or None if decoding fails.
        
    Raises:
        ValueError: If the base64 string is invalid or cannot be decoded.
    """
    try:
        # Remove data URL header if present (e.g., 'data:image/jpeg;base64,')
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]
        
        # Decode base64 string to raw bytes
        img_bytes = base64.b64decode(base64_string)
        
        # Convert bytes to NumPy array
        nparr = np.frombuffer(img_bytes, np.uint8)
        
        # Decode to OpenCV BGR image
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            raise ValueError("Failed to decode image data")
            
        return img
        
    except Exception as e:
        logger.error(f"Error decoding image: {str(e)}")
        raise ValueError(f"Invalid image data: {str(e)}")


def encode_image(img: np.ndarray, quality: int = 85) -> str:
    """Encode OpenCV image to base64 data URL for client transmission.
    
    Converts a NumPy array (OpenCV image) to a base64-encoded JPEG data URL
    that can be embedded directly in HTML or sent via JSON.
    
    Args:
        img: OpenCV image as NumPy array in BGR format.
        quality: JPEG compression quality (0-100). Default is 85.
                 Higher values = better quality but larger size.
                 
    Returns:
        Complete data URL string: 'data:image/jpeg;base64,...'
        
    Raises:
        ValueError: If image encoding fails.
    """
    try:
        # Encode image to JPEG format with specified quality
        success, buffer = cv2.imencode(
            '.jpg',
            img,
            [cv2.IMWRITE_JPEG_QUALITY, quality]
        )
        
        if not success:
            raise ValueError("Failed to encode image to JPEG")
        
        # Convert buffer to base64 string
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        
        # Return as data URL for direct embedding
        return f"data:image/jpeg;base64,{img_base64}"
        
    except Exception as e:
        logger.error(f"Error encoding image: {str(e)}")
        raise ValueError(f"Image encoding failed: {str(e)}")


@app.route('/')
def index():
    """Render the main application page.
    
    Serves the single-page application that provides the camera interface,
    real-time stroke analysis, and metrics visualization.
    
    Returns:
        Rendered HTML template for the main application page.
    """
    return render_template('index.html')


@app.route('/api/process_frame', methods=['POST'])
def process_frame() -> Tuple[Dict[str, Any], int]:
    """Process a video frame and return annotated image with stroke metrics.
    
    This endpoint receives a base64-encoded image frame from the client,
    performs cue tip detection and tracking, annotates the frame with
    visual feedback, and returns comprehensive stroke quality metrics.
    
    Expected JSON payload:
        {
            "image": "data:image/jpeg;base64,...",  # Base64-encoded frame
            "tracking": true/false                   # Whether to add points to stroke path
        }
    
    Returns:
        JSON response containing:
            - image: Base64-encoded annotated frame with visual overlays
            - tip_detected: Boolean indicating if cue tip was found
            - metrics: Stroke quality metrics (deviation, smoothness, angle, speed, etc.)
            
    Status Codes:
        200: Success - frame processed successfully
        400: Bad Request - missing or invalid image data
        500: Internal Server Error - processing failure
    """
    try:
        # Validate request has JSON body
        if not request.is_json:
            logger.warning("Request missing JSON content-type")
            return jsonify({'error': 'Content-Type must be application/json'}), 400
            
        data = request.json
        
        # Extract and validate parameters
        image_data = data.get('image')
        is_tracking = data.get('tracking', False)
        
        if not image_data:
            logger.warning("Request missing image data")
            return jsonify({'error': 'No image provided'}), 400
        
        # Decode image from base64
        try:
            frame = decode_image(image_data)
        except ValueError as e:
            logger.error(f"Image decode error: {str(e)}")
            return jsonify({'error': f'Invalid image data: {str(e)}'}), 400
        
        if frame is None:
            return jsonify({'error': 'Failed to decode image'}), 400
        
        # Get analyzer for current session
        analyzer = get_analyzer()
        
        # Detect cue tip position in frame
        cue_tip = analyzer.detect_cue_tip(frame)
        
        # Add point to tracking path if tracking is enabled and tip detected
        if is_tracking and cue_tip:
            analyzer.add_point(cue_tip)
            logger.debug(f"Added tracking point: {cue_tip}")
        
        # Generate annotated frame with visualization and compute metrics
        annotated_frame, metrics = analyzer.draw_visualization(frame)
        
        # Draw cue tip detection indicator
        if cue_tip:
            cv2.circle(annotated_frame, cue_tip, 10, (0, 0, 255), 2)
            cv2.putText(
                annotated_frame,
                "TIP DETECTED",
                (cue_tip[0] - 50, cue_tip[1] - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 255),
                2
            )
        
        # Encode annotated frame to base64
        try:
            result_image = encode_image(annotated_frame)
        except ValueError as e:
            logger.error(f"Image encode error: {str(e)}")
            return jsonify({'error': 'Failed to encode result image'}), 500
        
        # Prepare successful response
        response = {
            'image': result_image,
            'tip_detected': cue_tip is not None,
            'metrics': metrics.to_dict() if metrics else None
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        logger.exception(f"Unexpected error processing frame: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@app.route('/api/reset', methods=['POST'])
def reset() -> Tuple[Dict[str, Any], int]:
    """Reset stroke tracking data for the current session.
    
    Clears all accumulated tracking points and timestamps, allowing the user
    to start fresh stroke analysis. This is useful when switching between
    different practice sessions or after completing a stroke.
    
    Returns:
        JSON response with success status and message.
        
    Status Codes:
        200: Success - tracking data cleared
        500: Internal Server Error - reset operation failed
    """
    try:
        analyzer = get_analyzer()
        analyzer.reset()
        logger.info("Tracking reset successfully")
        return jsonify({
            'success': True,
            'message': 'Tracking reset successfully'
        }), 200
    
    except Exception as e:
        logger.exception(f"Error resetting tracking: {str(e)}")
        return jsonify({
            'error': 'Failed to reset tracking',
            'message': str(e)
        }), 500


@app.route('/api/config', methods=['GET', 'POST'])
def config() -> Tuple[Dict[str, Any], int]:
    """Get or update analyzer configuration settings.
    
    GET: Retrieve current configuration parameters for the session's analyzer.
    POST: Update configuration parameters with new values.
    
    Configuration Parameters:
        - max_points (int): Maximum number of tracking points to maintain (5-100)
        - deviation_threshold (float): Maximum deviation in pixels for 'straight' classification (5.0-50.0)
    
    GET Response:
        {
            "max_points": 30,
            "deviation_threshold": 15.0
        }
    
    POST Request Body:
        {
            "max_points": 40,              # Optional
            "deviation_threshold": 20.0    # Optional
        }
    
    Returns:
        JSON response with current configuration or success confirmation.
        
    Status Codes:
        200: Success - configuration retrieved or updated
        400: Bad Request - invalid configuration values
        500: Internal Server Error - operation failed
    """
    try:
        analyzer = get_analyzer()
        
        if request.method == 'GET':
            return jsonify({
                'max_points': analyzer.max_points,
                'deviation_threshold': analyzer.deviation_threshold
            }), 200
        
        else:  # POST
            if not request.is_json:
                return jsonify({'error': 'Content-Type must be application/json'}), 400
                
            data = request.json
            
            # Validate and update deviation threshold
            if 'deviation_threshold' in data:
                threshold = float(data['deviation_threshold'])
                if not (5.0 <= threshold <= 50.0):
                    return jsonify({
                        'error': 'deviation_threshold must be between 5.0 and 50.0'
                    }), 400
                analyzer.deviation_threshold = threshold
                logger.info(f"Updated deviation_threshold to {threshold}")
            
            # Validate and update max points
            if 'max_points' in data:
                max_points = int(data['max_points'])
                if not (5 <= max_points <= 100):
                    return jsonify({
                        'error': 'max_points must be between 5 and 100'
                    }), 400
                analyzer.max_points = max_points
                logger.info(f"Updated max_points to {max_points}")
            
            return jsonify({
                'success': True,
                'max_points': analyzer.max_points,
                'deviation_threshold': analyzer.deviation_threshold
            }), 200
    
    except (ValueError, TypeError) as e:
        logger.error(f"Invalid configuration value: {str(e)}")
        return jsonify({'error': f'Invalid value: {str(e)}'}), 400
    
    except Exception as e:
        logger.exception(f"Error updating configuration: {str(e)}")
        return jsonify({'error': 'Configuration update failed'}), 500


@app.route('/health')
def health() -> Tuple[Dict[str, Any], int]:
    """Health check endpoint for monitoring and orchestration systems.
    
    This endpoint is used by deployment platforms (like Hugging Face Spaces)
    and monitoring tools to verify the application is running and responsive.
    Returns basic service information and status.
    
    Returns:
        JSON response with health status and service metadata.
        
    Status Code:
        200: Service is healthy and operational
    """
    return jsonify({
        'status': 'healthy',
        'service': 'pool-stroke-trainer',
        'version': '1.0.0'
    }), 200


if __name__ == '__main__':
    """Application entry point for local development.
    
    Configuration:
        - PORT: Configurable via environment variable (default: 7860 for HF Spaces)
        - HOST: Binds to 0.0.0.0 for external access
        - DEBUG: Disabled for production safety
    
    Note: In production deployments (e.g., Hugging Face Spaces), the hosting
    platform typically overrides these settings with their own WSGI server.
    """
    port = int(os.environ.get('PORT', 7860))
    logger.info(f"Starting Pool Stroke Trainer on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
