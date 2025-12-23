/**
 * Pool Stroke Trainer - Client Application
 * 
 * Handles camera access, real-time frame capture, server communication,
 * and user interface updates for pool stroke analysis.
 * 
 * Features:
 * - Camera access via MediaStream API
 * - Frame-by-frame processing at configurable rate
 * - RESTful API communication
 * - Real-time metrics visualization
 * - Mobile-responsive interaction
 * 
 * @author Scott Gordon
 * @email scott.aiengineer@outlook.com
 * @license MIT
 */

// IIFE (Immediately Invoked Function Expression) to avoid global scope pollution
(function() {
    'use strict';
    
    // ============================================================================
    // DOM ELEMENTS
    // ============================================================================
    
    const video = document.getElementById('video');
    const canvas = document.getElementById('videoCanvas');
    const ctx = canvas.getContext('2d');
    
    const startCameraBtn = document.getElementById('startCameraBtn');
    const toggleTrackingBtn = document.getElementById('toggleTrackingBtn');
    const resetBtn = document.getElementById('resetBtn');
    
    const statusIndicator = document.getElementById('statusIndicator');
    const statusText = document.getElementById('statusText');
    const metricsPanel = document.getElementById('metricsPanel');
    
    // ============================================================================
    // STATE MANAGEMENT
    // ============================================================================
    
    let stream = null;
    let isTracking = false;
    let animationId = null;
    let frameInterval = null;
    
    // ============================================================================
    // CONFIGURATION
    // ============================================================================
    
    const FRAME_RATE = 10;  // Frames per second to process
    const FRAME_INTERVAL = 1000 / FRAME_RATE;  // Milliseconds between frames
    
    // ============================================================================
    // CAMERA MANAGEMENT
    // ============================================================================
    
    /**
     * Initialize and start the camera stream.
     * 
     * Requests user permission for camera access and configures the video stream
     * with optimal settings for stroke analysis. Prefers back camera on mobile devices.
     * 
     * @async
     * @throws {NotAllowedError} User denied camera permission
     * @throws {NotFoundError} No camera device found
     */
    async function startCamera() {
        try {
            updateStatus('Requesting camera access...', 'loading');
            
            // Request camera access with optimized constraints
            stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    facingMode: 'environment',  // Back camera on mobile
                    width: { ideal: 1280 },
                    height: { ideal: 720 }
                },
                audio: false
            });
            
            // Attach stream to video element
            video.srcObject = stream;
            
            // Wait for video metadata to load
            await new Promise((resolve) => {
                video.onloadedmetadata = () => {
                    resolve();
                };
            });
            
            // Set canvas dimensions to match video
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            
            // Update UI state
            startCameraBtn.textContent = '📷 Camera Active';
            startCameraBtn.disabled = true;
            toggleTrackingBtn.disabled = false;
            resetBtn.disabled = false;
            
            updateStatus('Camera ready', 'success');
            
            // Begin frame processing
            startFrameProcessing();
            
        } catch (error) {
            console.error('Camera access error:', error);
            
            let message = 'Failed to access camera';
            if (error.name === 'NotAllowedError') {
                message = 'Camera permission denied';
            } else if (error.name === 'NotFoundError') {
                message = 'No camera found';
            } else if (error.name === 'NotReadableError') {
                message = 'Camera is in use by another application';
            }
            
            updateStatus(message, 'error');
            alert(`${message}. Please check your camera settings and try again.`);
        }
    }
    
    /**
     * Stop camera stream and release resources.
     * 
     * Important for mobile devices: Releasing camera saves battery and allows
     * other applications to access the camera.
     */
    function stopCamera() {
        if (frameInterval) {
            clearInterval(frameInterval);
            frameInterval = null;
        }
        
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
            stream = null;
        }
        
        if (video.srcObject) {
            video.srcObject = null;
        }
        
        console.log('Camera stopped and resources released');
    }
    
    // ============================================================================
    // FRAME PROCESSING
    // ============================================================================
    
    /**
     * Start continuous frame processing at configured interval.
     * 
     * Uses setInterval instead of requestAnimationFrame because:
     * - Fixed rate (10 FPS) reduces network traffic
     * - Server processing is slower than display refresh rate (60 FPS)
     * - 10 FPS provides smooth enough feedback for stroke analysis
     */
    function startFrameProcessing() {
        frameInterval = setInterval(() => {
            captureAndProcess();
        }, FRAME_INTERVAL);
        console.log(`Frame processing started at ${FRAME_RATE} FPS`);
    }
    
    /**
     * Capture current video frame and send to server for processing.
     * 
     * Process:
     * 1. Draw current video frame to canvas
     * 2. Convert canvas to base64 JPEG
     * 3. Send to server via POST request
     * 4. Display processed frame with annotations
     * 5. Update metrics display
     * 
     * @async
     */
    async function captureAndProcess() {
        if (!video.videoWidth) return;
        
        try {
            // Draw current video frame to canvas
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
            
            // Convert canvas to base64 image (JPEG at 80% quality for efficiency)
            const imageData = canvas.toDataURL('image/jpeg', 0.8);
            
            // Send frame to server for processing
            const response = await fetch('/api/process_frame', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    image: imageData,
                    tracking: isTracking
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const result = await response.json();
            
            // Display processed frame with annotations
            displayProcessedFrame(result.image);
            
            // Update metrics display if available
            if (result.metrics) {
                updateMetrics(result.metrics);
                metricsPanel.style.display = 'block';
            }
            
            // Update status based on detection and tracking state
            if (isTracking) {
                if (result.tip_detected) {
                    updateStatus('Tracking - Tip Detected', 'tracking');
                } else {
                    updateStatus('Tracking - No Tip Detected', 'warning');
                }
            } else {
                updateStatus(result.tip_detected ? 'Tip Detected' : 'Ready', 'success');
            }
            
        } catch (error) {
            console.error('Frame processing error:', error);
            updateStatus('Processing error - check connection', 'error');
        }
    }
    
    /**
     * Display processed frame from server on canvas.
     * 
     * The server returns the frame with annotations (stroke path, metrics, etc.)
     * that we want to display instead of the raw camera feed.
     * 
     * @param {string} base64Image - Base64-encoded JPEG image with data URL prefix
     */
    function displayProcessedFrame(base64Image) {
        const img = new Image();
        img.onload = () => {
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        };
        img.onerror = () => {
            console.error('Failed to load processed frame');
        };
        img.src = base64Image;
    }
    
    // ============================================================================
    // USER INTERACTIONS
    // ============================================================================
    
    /**
     * Toggle stroke tracking on/off.
     * 
     * When tracking is enabled, detected cue tip positions are added to the
     * stroke path for analysis. When disabled, detection continues but points
     * are not recorded.
     */
    function toggleTracking() {
        isTracking = !isTracking;
        
        if (isTracking) {
            toggleTrackingBtn.textContent = '⏸️ Stop Tracking';
            toggleTrackingBtn.classList.remove('btn-success');
            toggleTrackingBtn.classList.add('btn-danger');
            updateStatus('Tracking active', 'tracking');
        } else {
            toggleTrackingBtn.textContent = '▶️ Start Tracking';
            toggleTrackingBtn.classList.remove('btn-danger');
            toggleTrackingBtn.classList.add('btn-success');
            updateStatus('Tracking stopped', 'success');
        }
        
        console.log(`Tracking ${isTracking ? 'enabled' : 'disabled'}`);
    }
    
    /**
     * Reset tracking data on the server.
     * 
     * Clears all accumulated tracking points and metrics, allowing the user
     * to start a fresh analysis session.
     * 
     * @async
     */
    async function resetTracking() {
        try {
            const response = await fetch('/api/reset', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (!response.ok) {
                throw new Error('Reset request failed');
            }
            
            const result = await response.json();
            
            // Clear metrics display
            metricsPanel.style.display = 'none';
            
            updateStatus('Reset complete', 'success');
            console.log('Tracking reset successfully');
            
        } catch (error) {
            console.error('Reset error:', error);
            alert('Failed to reset tracking. Please try again.');
        }
    }
    
    // ============================================================================
    // UI UPDATES
    // ============================================================================
    
    /**
     * Update metrics display with current stroke analysis data.
     * 
     * @param {Object} metrics - Stroke metrics from server
     * @param {number} metrics.deviation - Average deviation from straight line
     * @param {number} metrics.smoothness - Consistency measure
     * @param {number} metrics.angle - Stroke angle in degrees
     * @param {number} metrics.speed - Average speed in pixels/second
     * @param {boolean} metrics.is_straight - Whether stroke meets threshold
     */
    function updateMetrics(metrics) {
        const { deviation, smoothness, angle, speed, is_straight } = metrics;
        
        // Update individual metric values
        document.getElementById('metricDeviation').textContent = deviation.toFixed(2);
        document.getElementById('metricSmoothness').textContent = smoothness.toFixed(2);
        document.getElementById('metricAngle').textContent = angle.toFixed(1);
        document.getElementById('metricSpeed').textContent = speed.toFixed(1);
        
        // Update stroke quality indicator
        const qualityElement = document.getElementById('strokeQuality');
        const qualityText = document.getElementById('qualityText');
        
        if (is_straight) {
            qualityText.textContent = '✅ EXCELLENT STROKE!';
            qualityElement.classList.remove('needs-work');
            qualityElement.classList.add('excellent');
        } else {
            qualityText.textContent = '⚠️ NEEDS WORK';
            qualityElement.classList.remove('excellent');
            qualityElement.classList.add('needs-work');
        }
    }
    
    /**
     * Update status indicator with message and styling.
     * 
     * @param {string} message - Status message to display
     * @param {string} type - Status type: 'success', 'error', 'tracking', 'loading', 'warning'
     */
    function updateStatus(message, type = 'info') {
        statusText.textContent = message;
        
        // Remove all status classes
        statusIndicator.classList.remove('tracking', 'error', 'loading', 'warning');
        
        // Add new status class if applicable
        if (type !== 'success' && type !== 'info') {
            statusIndicator.classList.add(type);
        }
    }
    
    // ============================================================================
    // EVENT LISTENERS
    // ============================================================================
    
    startCameraBtn.addEventListener('click', startCamera);
    toggleTrackingBtn.addEventListener('click', toggleTracking);
    resetBtn.addEventListener('click', resetTracking);
    
    // Cleanup on page unload (important for mobile)
    window.addEventListener('beforeunload', () => {
        stopCamera();
    });
    
    // Handle page visibility changes (mobile background/foreground)
    // Pause processing when app is in background to save battery and bandwidth
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            // Page hidden - pause processing
            if (frameInterval) {
                clearInterval(frameInterval);
                frameInterval = null;
                console.log('Frame processing paused (page hidden)');
            }
        } else {
            // Page visible - resume processing
            if (stream && !frameInterval) {
                startFrameProcessing();
                console.log('Frame processing resumed (page visible)');
            }
        }
    });
    
    // ============================================================================
    // INITIALIZATION
    // ============================================================================
    
    updateStatus('Click "Start Camera" to begin', 'info');
    console.log('Pool Stroke Trainer initialized');
    console.log(`Configuration: ${FRAME_RATE} FPS processing rate`);
    
})();
