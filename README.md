---
title: Pool Stroke Trainer
emoji: 🎱
colorFrom: purple
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
license: mit
---

# Pool Stroke Trainer 🎱

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8.1-red.svg)](https://opencv.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

A professional, AI-powered web application that helps pool players perfect their straight stroke technique through real-time computer vision analysis and quantitative metrics.

**🎯 Live Demo:** [Coming Soon - Hugging Face Spaces]

## ✨ Features

- 📱 **Mobile-First Design** - Works on smartphones, tablets, and desktops
- ⚡ **Real-Time Analysis** - Instant feedback with 10 FPS processing
- 🎯 **Quantitative Metrics** - Deviation, smoothness, angle, and speed measurements
- 🎨 **Visual Feedback** - Color-coded stroke path visualization (green = excellent, orange = needs work)
- 🔒 **Privacy-First** - All processing in your session, no data stored
- 🖥️ **Computer Vision** - HSV color-space detection for reliable tracking
- 📊 **Statistical Analysis** - Linear regression-based straightness calculation

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/scott-ai-maker/pool-straight-stroke-app.git
cd pool-straight-stroke-app

# Run setup script
chmod +x setup.sh
./setup.sh

# Start application
python app.py
```

Open `http://localhost:7860` in your browser.

**For detailed instructions, see [QUICKSTART.md](QUICKSTART.md)**

## 📦 Installation

### Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

### Docker

```bash
# Build image
docker build -t pool-stroke-trainer .

# Run container
docker run -p 7860:7860 pool-stroke-trainer
```

## 🎮 Usage

### Basic Workflow

1. **Setup** - Mark your cue tip with red tape or marker
2. **Start Camera** - Click "Start Camera" and allow permissions
3. **Start Tracking** - Click "Start Tracking" when ready to practice
4. **Practice** - Perform strokes and watch real-time feedback
5. **Analyze** - Review metrics (deviation < 15px = excellent)
6. **Reset** - Click "Reset" to clear data for new session

### Tips for Best Results

**Lighting:**
- ✅ Bright, even indoor lighting
- ✅ Use lamps for consistent illumination
- ❌ Avoid direct sunlight
- ❌ Don't face windows (backlighting)

**Camera Position:**
- ✅ Mount phone/tablet for stability
- ✅ Landscape orientation recommended
- ✅ Capture full stroke path
- ✅ Experiment with different angles

**Marker:**
- ✅ Bright red tape on cue tip
- ✅ High contrast against background
- ✅ Replace if faded or peeling
- ❌ Avoid dark red or pink

## 🏗️ Architecture

### Technology Stack

**Backend:**
- Flask 3.0.0 (Python web framework)
- OpenCV 4.8.1 (Computer vision)
- NumPy 1.26.2 (Numerical computing)
- Python 3.10+

**Frontend:**
- HTML5 + CSS3 (Responsive design, purple theme)
- Vanilla JavaScript ES6+ (No frameworks)
- MediaStream API (Camera access)
- Canvas API (Frame processing)
- Fetch API (Server communication)

**DevOps:**
- Docker (Containerization)
- Hugging Face Spaces (Deployment platform)
- GitHub (Version control)

### System Design

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Client    │      │    Flask     │      │   OpenCV    │
│  (Browser)  │─────▶│   Server     │─────▶│  Analyzer   │
│             │◀─────│              │◀─────│             │
└─────────────┘      └──────────────┘      └─────────────┘
     │                      │                      │
     │ Video Frame          │ Base64 Image         │ Detection
     │ (10 FPS)            │                      │
     │                      │                      │
     │ Annotated Frame      │ Visualization        │ Metrics
     │ + Metrics            │                      │
```

### Project Structure

```
pool-straight-stroke-app/
├── app.py                      # Flask application & API routes
├── stroke_analyzer.py          # Computer vision & metrics calculation
├── requirements.txt            # Python dependencies (pinned versions)
├── Dockerfile                  # Container definition (HF Spaces optimized)
├── setup.sh                    # Automated setup script
├── .gitignore                  # Git ignore rules
├── .dockerignore              # Docker ignore rules
├── LICENSE                     # MIT License
├── README.md                   # This file
├── API.md                      # API documentation
├── CONTRIBUTING.md             # Contribution guidelines
├── TROUBLESHOOTING.md          # Common issues & solutions
├── QUICKSTART.md               # Quick start guide
├── CHANGELOG.md                # Version history
├── templates/
│   └── index.html             # Main application page
├── static/
│   ├── css/
│   │   └── style.css          # Purple theme styles
│   └── js/
│       └── app.js             # Client application logic
└── __pycache__/               # Python cache (git-ignored)
```

## 📡 API Documentation

### Core Endpoints

#### `POST /api/process_frame`
Process a video frame and return annotated image with metrics.

**Request:**
```json
{
  "image": "data:image/jpeg;base64,...",
  "tracking": true
}
```

**Response:**
```json
{
  "image": "data:image/jpeg;base64,...",
  "tip_detected": true,
  "metrics": {
    "deviation": 12.34,
    "smoothness": 5.67,
    "angle": -2.34,
    "speed": 245.67,
    "is_straight": true,
    "point_count": 25
  }
}
```

#### `POST /api/reset`
Reset tracking data for current session.

**Response:**
```json
{
  "success": true,
  "message": "Tracking reset successfully"
}
```

#### `GET /health`
Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "healthy",
  "service": "pool-stroke-trainer",
  "version": "1.0.0"
}
```

**For complete API documentation, see [API.md](API.md)**

## 🐳 Docker Deployment

### Build and Run

```bash
# Build image
docker build -t pool-stroke-trainer .

# Run container
docker run -p 7860:7860 pool-stroke-trainer

# Run with environment variables
docker run -p 7860:7860 \
  -e SECRET_KEY=your-secret-key \
  pool-stroke-trainer

# Run with volume mount
docker run -p 7860:7860 \
  -v $(pwd)/logs:/app/logs \
  pool-stroke-trainer
```

### Docker Compose

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "7860:7860"
    environment:
      - SECRET_KEY=${SECRET_KEY}
    restart: unless-stopped
```

## 🤗 Hugging Face Spaces Deployment

### Method 1: Direct Deployment

```bash
# Create Space at https://huggingface.co/spaces
# Select "Docker" SDK

# Clone your Space
git clone https://huggingface.co/spaces/<username>/pool-stroke-trainer
cd pool-stroke-trainer

# Copy project files
cp -r /path/to/pool-straight-stroke-app/* .

# Commit and push
git add .
git commit -m "Initial deployment"
git push
```

### Method 2: GitHub Integration

1. Push project to GitHub
2. Create new Space on Hugging Face
3. Connect GitHub repository
4. HF Spaces automatically builds and deploys

### Environment Variables

Set in Space settings:
- `SECRET_KEY` - Flask session secret (auto-generated if not set)
- `PORT` - Application port (default: 7860)

## ⚙️ Configuration

### Analyzer Parameters

Edit in `app.py`:
```python
PoolStrokeAnalyzer(
    max_points=30,           # Tracking points (5-100)
    deviation_threshold=15.0 # Straightness threshold px (5.0-50.0)
)
```

### Color Detection

Edit HSV ranges in `stroke_analyzer.py`:
```python
self.color_lower = np.array([0, 100, 100])    # Red lower bound
self.color_upper = np.array([10, 255, 255])   # Red upper bound
```

### Frame Rate

Edit in `static/js/app.js`:
```javascript
const FRAME_RATE = 10;  // Frames per second (1-30)
```

## 🐛 Troubleshooting

### Common Issues

**Camera not working:**
- Ensure browser has camera permissions
- Check if camera is in use by another app
- Try different browser (Chrome/Edge recommended)
- Check HTTPS connection (required for camera access)

**Cue tip not detected:**
- Verify red marker is bright and visible
- Improve lighting conditions
- Check marker hasn't faded
- Adjust HSV color ranges in configuration

**Slow performance:**
- Reduce frame rate (edit FRAME_RATE in app.js)
- Check network connection
- Close other applications
- Try on different device

**WebSocket/Connection errors:**
- Check firewall settings
- Verify port 7860 is available
- Restart the application

**For detailed troubleshooting, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)**

## 👨‍💻 Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/scott-ai-maker/pool-straight-stroke-app.git
cd pool-straight-stroke-app

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run in debug mode (optional)
export FLASK_DEBUG=1
python app.py
```

### Code Style

- **Python:** PEP 8 style guide
- **JavaScript:** ES6+ with consistent formatting
- **CSS:** BEM methodology for class naming
- **Docstrings:** Google style for Python
- **Comments:** JSDoc style for JavaScript

### Testing

```bash
# Python linting
flake8 app.py stroke_analyzer.py

# Type checking
mypy app.py stroke_analyzer.py

# Code formatting
black app.py stroke_analyzer.py
```

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on:
- Code of conduct
- Development workflow
- Pull request process
- Coding standards
- Issue reporting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2025 Scott Gordon

## 📞 Contact

**Scott Gordon**
- 📧 Email: scott.aiengineer@outlook.com
- 🐙 GitHub: [@scott-ai-maker](https://github.com/scott-ai-maker)
- 💼 Portfolio: [GitHub Profile](https://github.com/scott-ai-maker)

## 🙏 Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/) web framework
- Computer vision powered by [OpenCV](https://opencv.org/)
- Deployed on [Hugging Face Spaces](https://huggingface.co/spaces)
- Inspired by pool players everywhere striving to improve their game

## 🎯 Roadmap

Future enhancements:
- [ ] Historical session data and progress tracking
- [ ] Multiple color marker support (blue, green, yellow)
- [ ] Advanced metrics (acceleration, jerk, consistency score)
- [ ] Machine learning-based tracking (MediaPipe, YOLO)
- [ ] Social features (share results, leaderboards)
- [ ] Mobile native apps (iOS, Android)
- [ ] Multi-language support (Spanish, Chinese, French)
- [ ] Video recording and playback
- [ ] Coaching mode with tips and drills

## 📚 Learn More

- [Computer Vision Tutorial](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [Flask Documentation](https://flask.palletsprojects.com/en/3.0.x/)
- [MediaStream API](https://developer.mozilla.org/en-US/docs/Web/API/MediaStream_API)
- [Hugging Face Spaces Guide](https://huggingface.co/docs/hub/spaces)

---

**⭐ If you find this project helpful, please give it a star on GitHub!**

**🎱 Happy practicing! May your strokes be straight and your runs be long!**
