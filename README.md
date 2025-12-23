# Pool Straight Stroke Trainer 🎱

A web-based computer vision application to help pool players achieve a perfectly straight stroke. Uses real-time video analysis accessible from any device including mobile phones.

## ✨ Features

- **Mobile-Friendly**: Works on smartphones, tablets, and desktops
- **Real-time Analysis**: Instant feedback on stroke quality
- **Computer Vision**: Automatic cue tip tracking
- **Comprehensive Metrics**:
  - Deviation from ideal straight line
  - Stroke smoothness/consistency
  - Angle measurement
  - Stroke speed calculation
- **Visual Feedback**: Color-coded path visualization
- **Session-based**: Each user gets independent tracking

## 🏗️ Architecture

### Backend (Python/Flask)
- Frame processing with OpenCV
- Session management for multi-user support
- RESTful API for client communication

### Frontend (HTML/CSS/JavaScript)
- HTML5 camera access via getUserMedia API
- Canvas-based rendering for processed frames
- Responsive design with mobile-first approach
- Real-time metrics display

### Deployment
- Docker containerized for easy deployment
- Optimized for Hugging Face Spaces
- Health check endpoint for monitoring

## 📋 Requirements

- Python 3.10+
- Webcam/phone camera
- Red marker or tape for cue tip tracking

## 🚀 Local Development

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd pool-straight-stroke-app
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
python app.py
```

### 5. Open in browser
Navigate to `http://localhost:7860`

## 🐳 Docker Deployment

### Build the image
```bash
docker build -t pool-stroke-trainer .
```

### Run the container
```bash
docker run -p 7860:7860 pool-stroke-trainer
```

## 🤗 Deploy to Hugging Face Spaces

### Method 1: Direct Docker Deployment

1. Create a new Space on Hugging Face
   - Select "Docker" as the SDK
   - Choose "Public" or "Private"

2. Clone your Space locally:
```bash
git clone https://huggingface.co/spaces/<your-username>/<space-name>
cd <space-name>
```

3. Copy all project files to the Space directory

4. Create a `README.md` in the Space with:
```yaml
---
title: Pool Stroke Trainer
emoji: 🎱
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
app_port: 7860
---
```

5. Commit and push:
```bash
git add .
git commit -m "Initial deployment"
git push
```

### Method 2: GitHub Integration

1. Push your code to GitHub
2. Create a new Space on HF
3. Connect your GitHub repository
4. HF Spaces will automatically deploy from Dockerfile

## 📱 Usage Instructions

1. **Mark your cue tip** with red tape or a bright red marker
2. **Open the app** on your mobile device or computer
3. **Click "Start Camera"** and allow camera permissions
4. **Position camera** to capture your stroke motion
   - Landscape orientation recommended
   - Ensure good lighting
   - Plain background helps tracking
5. **Click "Start Tracking"** when ready to practice
6. **Watch the feedback**:
   - Green path = straight stroke ✅
   - Orange path = needs work ⚠️
7. **Review metrics** for detailed analysis

## 🎯 Tips for Best Results

### Lighting
- Bright, even lighting works best
- Avoid backlighting (don't face windows)
- Indoor lighting is usually ideal

### Camera Position
- Mount phone/tablet for stable view
- Capture full stroke motion
- Try different angles to find what works

### Marker
- Use bright red tape on cue tip
- Ensure marker is visible throughout stroke
- Replace if it fades or peels

### Practice
- Start with slow, controlled strokes
- Focus on consistency over speed
- Use metrics to track improvement

## 🔧 Customization

### Adjust Sensitivity
Edit [stroke_analyzer.py](stroke_analyzer.py):
```python
analyzer = PoolStrokeAnalyzer(
    max_points=30,              # Number of tracked points
    deviation_threshold=15.0    # Pixels for "straight" classification
)
```

### Change Detection Color
Modify HSV color ranges in [stroke_analyzer.py](stroke_analyzer.py):
```python
self.color_lower = np.array([0, 100, 100])    # Red lower
self.color_upper = np.array([10, 255, 255])   # Red upper
```

### Adjust Frame Rate
Edit [static/js/app.js](static/js/app.js):
```javascript
const FRAME_RATE = 10; // Frames per second
```

## 🏛️ Project Structure

```
pool-straight-stroke-app/
├── app.py                    # Flask application
├── stroke_analyzer.py        # Computer vision logic
├── templates/
│   └── index.html           # Main page
├── static/
│   ├── css/
│   │   └── style.css        # Styles
│   └── js/
│       └── app.js           # Client logic
├── Dockerfile               # Container definition
├── requirements.txt         # Python dependencies
├── pool-straight-stroke-app.py  # Original desktop version
└── README.md
```

## 📚 Learning Resources

This project demonstrates several concepts:

### Backend
- Flask routing and session management
- OpenCV color detection and line fitting
- Base64 image encoding/decoding
- RESTful API design

### Frontend
- HTML5 getUserMedia API
- Canvas manipulation
- Async/await patterns
- Mobile-responsive design
- CSS custom properties

### DevOps
- Multi-stage Docker builds
- Container optimization
- Health checks
- Environment variables

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Alternative tracking methods (MediaPipe, YOLO)
- Historical session data and progress tracking
- Multiple cue tip color support
- Advanced metrics (acceleration, jerk)
- Social features (sharing results)

## 📄 License

MIT License - feel free to use and modify!

## 🙏 Acknowledgments

Built for pool players looking to perfect their technique through technology.

---

**Happy practicing! May your strokes be straight and your runs be long! 🎱**
# pool-straight-stroke-app
