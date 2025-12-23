# Troubleshooting Guide

Common issues and solutions for Pool Stroke Trainer.

## 📋 Table of Contents

- [Camera Issues](#camera-issues)
- [Detection Issues](#detection-issues)
- [Performance Issues](#performance-issues)
- [Browser Issues](#browser-issues)
- [Deployment Issues](#deployment-issues)
- [Configuration Issues](#configuration-issues)

---

## 📷 Camera Issues

### Camera Not Working

**Symptoms:**
- "Camera permission denied" message
- Black screen instead of video feed
- Camera button stays disabled

**Solutions:**

1. **Check Browser Permissions**
   - Chrome: Click padlock icon → Camera → Allow
   - Firefox: Click camera icon in address bar → Allow
   - Safari: Settings → Websites → Camera → Allow
   - Edge: Settings → Site permissions → Camera → Allow

2. **Check System Permissions**
   - **macOS:** System Preferences → Security & Privacy → Camera → Enable for browser
   - **Windows:** Settings → Privacy → Camera → Allow apps to access camera
   - **Linux:** Check browser has camera access permissions

3. **Camera In Use by Another Application**
   - Close other applications using camera (Zoom, Teams, Skype)
   - Restart browser
   - Restart computer if issue persists

4. **HTTPS Requirement**
   - Camera API requires HTTPS connection
   - Local development: `http://localhost:7860` works
   - Production: Must use HTTPS URL

**Still Not Working?**
- Try different browser (Chrome recommended)
- Check if camera works in other applications
- Update browser to latest version
- Check for browser extensions blocking camera
- Disable VPN/proxy temporarily

---

### Wrong Camera Selected

**Symptoms:**
- Front camera activates instead of back camera on mobile
- External webcam not being used

**Solutions:**

1. **Mobile Devices**
   - App requests "environment" facing camera (back camera)
   - Some devices may default to front camera
   - Solution: Manually switch camera in browser settings

2. **Multiple Webcams**
   - Edit `static/js/app.js`:
   ```javascript
   // Specify exact camera device
   stream = await navigator.mediaDevices.getUserMedia({
       video: {
           deviceId: { exact: "your-device-id-here" }
       }
   });
   ```

3. **List Available Cameras**
   - Open browser console
   - Run:
   ```javascript
   navigator.mediaDevices.enumerateDevices()
       .then(devices => console.log(devices.filter(d => d.kind === 'videoinput')));
   ```

---

## 🎯 Detection Issues

### Cue Tip Not Detected

**Symptoms:**
- Status shows "No Tip Detected"
- Red marker visible but not tracked
- Detection intermittent

**Solutions:**

1. **Improve Marker Visibility**
   - ✅ Use bright, vivid red tape
   - ✅ Ensure high contrast with background
   - ✅ Replace faded or worn markers
   - ❌ Avoid dark red, pink, or orange

2. **Optimize Lighting**
   - ✅ Bright, even lighting
   - ✅ Multiple light sources to reduce shadows
   - ✅ Indoor lighting with lamps
   - ❌ Avoid direct sunlight (washes out colors)
   - ❌ Avoid backlighting (camera facing windows)
   - ❌ Avoid colored lights (affects HSV detection)

3. **Adjust Camera Position**
   - Ensure marker is in frame
   - Try different angles
   - Avoid extreme angles
   - Keep reasonable distance (1-3 meters)

4. **Adjust Detection Sensitivity**
   
   Edit `stroke_analyzer.py` HSV color ranges:
   ```python
   # More permissive detection (wider range)
   self.color_lower = np.array([0, 80, 80])     # Lower saturation/value
   self.color_upper = np.array([15, 255, 255])  # Wider hue range
   
   self.color_lower2 = np.array([165, 80, 80])  # Lower bounds
   self.color_upper2 = np.array([180, 255, 255])
   ```

5. **Adjust Minimum Contour Size**
   
   Edit `stroke_analyzer.py`:
   ```python
   # In detect_cue_tip method
   if cv2.contourArea(largest) < 30:  # Reduce from 50 to 30
       return None
   ```

---

### False Detections

**Symptoms:**
- Detection on wrong objects
- Multiple detection points
- Erratic tracking

**Solutions:**

1. **Remove Red Objects from Background**
   - Cover or remove red items in view
   - Use plain background
   - Avoid red clothing

2. **Tighten Detection Sensitivity**
   ```python
   # More restrictive detection (narrower range)
   self.color_lower = np.array([0, 120, 120])   # Higher saturation/value
   self.color_upper = np.array([8, 255, 255])   # Narrower hue range
   ```

3. **Increase Minimum Contour Size**
   ```python
   # In detect_cue_tip method
   if cv2.contourArea(largest) < 100:  # Increase from 50
       return None
   ```

---

## ⚡ Performance Issues

### Slow Frame Rate

**Symptoms:**
- Laggy video feed
- Delayed response
- Choppy visualization

**Solutions:**

1. **Reduce Frame Rate**
   
   Edit `static/js/app.js`:
   ```javascript
   const FRAME_RATE = 5;  // Reduce from 10 to 5 FPS
   ```

2. **Reduce Image Quality**
   ```javascript
   // In captureAndProcess function
   const imageData = canvas.toDataURL('image/jpeg', 0.6);  // Reduce from 0.8
   ```

3. **Reduce Canvas Resolution**
   ```javascript
   // In startCamera function, after setting canvas dimensions
   canvas.width = video.videoWidth / 2;   // Half resolution
   canvas.height = video.videoHeight / 2;
   ```

4. **Close Other Applications**
   - Close unnecessary browser tabs
   - Close CPU-intensive applications
   - Disable browser extensions

5. **Server Performance**
   - Check server CPU usage
   - Restart application: `python app.py`
   - Use production WSGI server (gunicorn):
   ```bash
   gunicorn -w 4 -b 0.0.0.0:7860 app:app
   ```

---

### High CPU Usage

**Symptoms:**
- Fan noise increases
- Device gets hot
- Battery drains quickly

**Solutions:**

1. **Lower Frame Rate** (see above)

2. **Pause When Inactive**
   - App already pauses when browser tab hidden
   - Close app when not in use

3. **Mobile Optimization**
   - Enable battery saver mode
   - Reduce screen brightness
   - Use lower resolution setting

---

### Memory Issues

**Symptoms:**
- Application crashes after extended use
- "Out of memory" errors
- Browser becomes unresponsive

**Solutions:**

1. **Reduce Tracking Points**
   ```python
   # In app.py
   analyzer = PoolStrokeAnalyzer(max_points=20)  # Reduce from 30
   ```

2. **Regular Reset**
   - Click "Reset" button periodically
   - Clears accumulated tracking data

3. **Restart Browser**
   - Close and reopen browser
   - Clears accumulated memory

---

## 🌐 Browser Issues

### Browser Compatibility

**Supported Browsers:**
- ✅ Chrome 90+
- ✅ Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+ (macOS/iOS)
- ❌ Internet Explorer (not supported)

**Solutions:**

1. **Update Browser**
   - Use latest version of supported browser
   - Chrome recommended for best compatibility

2. **Enable Required Features**
   - JavaScript must be enabled
   - Cookies must be enabled (for sessions)
   - WebRTC must be enabled (for camera)

3. **Check Browser Console**
   - Press F12 to open developer tools
   - Check Console tab for errors
   - Report errors in GitHub issues

---

### CORS Errors

**Symptoms:**
- "CORS policy blocked" errors in console
- API requests failing

**Solutions:**

1. **Same-Origin Access**
   - Ensure accessing app from same domain
   - Use `http://localhost:7860`, not `http://127.0.0.1:7860`

2. **Configure CORS (if needed)**
   ```python
   # In app.py, add after app initialization
   from flask_cors import CORS
   CORS(app, origins=['https://yourdomain.com'])
   ```

---

## 🚀 Deployment Issues

### Docker Build Failures

**Symptoms:**
- Docker build fails with errors
- Image size too large

**Solutions:**

1. **Check Dockerfile Syntax**
   - Verify all dependencies listed
   - Check for typos in commands

2. **Build with No Cache**
   ```bash
   docker build --no-cache -t pool-stroke-trainer .
   ```

3. **Check System Dependencies**
   - Ensure OpenCV dependencies included
   - Verify Python version matches

---

### Hugging Face Spaces Issues

**Symptoms:**
- Space fails to build
- Application not accessible
- Health check fails

**Solutions:**

1. **Verify README Metadata**
   ```yaml
   ---
   title: Pool Stroke Trainer
   sdk: docker
   app_port: 7860
   ---
   ```

2. **Check Build Logs**
   - View logs in HF Spaces interface
   - Look for error messages
   - Verify all dependencies install

3. **Environment Variables**
   - Set `PORT=7860` if needed
   - Configure `SECRET_KEY` in settings

4. **File Size Limits**
   - HF Spaces has file size limits
   - Keep models and data small
   - Use `.gitignore` for large files

---

### Port Already in Use

**Symptoms:**
- "Address already in use" error
- Cannot start application

**Solutions:**

1. **Find Process Using Port**
   ```bash
   # Linux/Mac
   lsof -i :7860
   
   # Windows
   netstat -ano | findstr :7860
   ```

2. **Kill Process**
   ```bash
   # Linux/Mac
   kill -9 <PID>
   
   # Windows
   taskkill /PID <PID> /F
   ```

3. **Use Different Port**
   ```bash
   export PORT=8080
   python app.py
   ```

---

## ⚙️ Configuration Issues

### Incorrect Metrics

**Symptoms:**
- Metrics seem inaccurate
- Straight strokes marked as not straight
- Inconsistent results

**Solutions:**

1. **Adjust Deviation Threshold**
   ```python
   # In app.py - Make more lenient
   analyzer = PoolStrokeAnalyzer(deviation_threshold=20.0)  # Increase from 15.0
   ```

2. **Increase Tracking Points**
   ```python
   # More points = more stable metrics
   analyzer = PoolStrokeAnalyzer(max_points=40)  # Increase from 30
   ```

3. **Calibration**
   - Test with known straight object (ruler, level)
   - Adjust threshold based on results
   - Document your calibration settings

---

### Session Issues

**Symptoms:**
- Data lost between refreshes
- Multiple users interfering
- Tracking resets unexpectedly

**Solutions:**

1. **Session Cookies**
   - Ensure cookies enabled in browser
   - Check browser not in incognito mode

2. **Server Restart**
   - Sessions cleared on server restart
   - Normal behavior for in-memory storage

3. **Production Session Storage**
   ```python
   # Use Redis for persistent sessions (production)
   from flask_session import Session
   app.config['SESSION_TYPE'] = 'redis'
   ```

---

## 🆘 Getting Help

If issue persists after trying these solutions:

1. **Check GitHub Issues**
   - [Search existing issues](https://github.com/scott-ai-maker/pool-straight-stroke-app/issues)
   - Similar problem may be documented

2. **Create New Issue**
   - Use issue template
   - Include error messages
   - Describe steps to reproduce
   - Share screenshots if helpful

3. **Contact Support**
   - 📧 Email: scott.aiengineer@outlook.com
   - Include detailed information
   - Attach relevant logs

---

## 📊 Diagnostic Commands

Run these to gather information:

```bash
# Python version
python --version

# Installed packages
pip list

# OpenCV info
python -c "import cv2; print(cv2.__version__)"

# Flask info
python -c "import flask; print(flask.__version__)"

# System info
python -c "import platform; print(platform.platform())"
```

---

## 📝 Logging

Enable detailed logging:

```python
# In app.py, at top
import logging
logging.basicConfig(level=logging.DEBUG)
```

Check logs for detailed error messages.

---

**Still having issues? Don't hesitate to reach out!** 🎱
