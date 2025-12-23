# Quick Start Guide

Get up and running with Pool Stroke Trainer in 5 minutes!

## 🎯 What You'll Need

- **Python 3.10+** installed on your system
- **Webcam** or smartphone camera
- **Red marker/tape** for your cue tip (bright red works best)
- **Good lighting** (indoor lighting ideal)

## 🚀 Installation (5 Minutes)

### Option 1: Automated Setup (Recommended)

```bash
# 1. Clone repository
git clone https://github.com/scott-ai-maker/pool-straight-stroke-app.git
cd pool-straight-stroke-app

# 2. Run setup script
chmod +x setup.sh
./setup.sh

# 3. Start application
python app.py
```

### Option 2: Manual Setup

```bash
# 1. Clone repository
git clone https://github.com/scott-ai-maker/pool-straight-stroke-app.git
cd pool-straight-stroke-app

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate    # Windows

# 4. Install dependencies
pip install -r requirements.txt

# 5. Start application
python app.py
```

### Option 3: Docker (One Command)

```bash
# Build and run
docker build -t pool-stroke-trainer . && docker run -p 7860:7860 pool-stroke-trainer
```

## 🎮 First Use (2 Minutes)

### Step 1: Open Application

Open your browser and go to:
```
http://localhost:7860
```

### Step 2: Start Camera

1. Click the **"📷 Start Camera"** button
2. Click **"Allow"** when browser asks for camera permission
3. Wait for "Camera ready" status

**Troubleshooting:**
- If camera doesn't start, check browser permissions
- Try Chrome or Edge for best compatibility
- Make sure no other app is using the camera

### Step 3: Prepare Cue

1. Get bright **red tape** or marker
2. Apply to your **cue tip**
3. Make sure it's **clearly visible**

**Tips:**
- Electrical tape works great
- Red sports tape also works
- Avoid dark red or pink

### Step 4: Position Camera

1. **Mount** your device (phone stand, tripod, etc.)
2. Use **landscape orientation**
3. Position to capture **full stroke path**
4. Ensure good **lighting**

**Ideal Setup:**
```
         [Camera]
            |
            v
    +---------------+
    |               |
    |  Stroke Path  |
    |   <------->   |
    |               |
    +---------------+
```

### Step 5: Start Practicing

1. Click **"▶️ Start Tracking"** button
2. Perform your **practice stroke**
3. Watch **real-time feedback**:
   - **Green path** = Excellent! ✅
   - **Orange path** = Needs work ⚠️

### Step 6: Review Metrics

After each stroke, check your metrics:

- **Deviation:** How straight was your stroke
  - ✅ < 15px = Excellent
  - ⚠️ 15-25px = Good
  - ❌ > 25px = Needs work

- **Smoothness:** How consistent
  - Lower = Better

- **Angle:** Stroke direction
  - Should be ~0° or ~180° for horizontal

- **Speed:** Stroke velocity
  - Track consistency over time

### Step 7: Reset and Repeat

1. Click **"🔄 Reset"** button
2. Start new stroke analysis
3. Compare metrics over multiple strokes

## 📱 Mobile Quick Start

### iOS/Safari

1. Open **Safari** browser
2. Navigate to app URL
3. Tap **"📷 Start Camera"**
4. Tap **"Allow"** for camera
5. **Rotate to landscape** for best view

**Note:** Safari may ask permission twice - allow both times

### Android/Chrome

1. Open **Chrome** browser
2. Navigate to app URL
3. Tap **"📷 Start Camera"**
4. Tap **"Allow"** for camera
5. **Rotate to landscape**

**Tip:** Tap "Add to Home Screen" for app-like experience!

## 🎯 Getting Good Results

### Lighting Setup (1 minute)

```
✅ GOOD:
   [Lamp] --- Light --→ [Cue] ←-- Light --- [Lamp]
   
   Two lamps, even lighting, no shadows

❌ BAD:
   [Window] ===== Bright Light ====→ [Cue] → [Camera]
   
   Backlighting washes out colors
```

### Camera Position (1 minute)

**Try These Angles:**

1. **Side View** (Recommended for beginners)
   ```
   Camera →  [Cue moving ↑↓]
   ```

2. **Top-Down View** (Advanced)
   ```
        Camera
          ↓
   [Cue moving ←→]
   ```

3. **Angled View** (Good compromise)
   ```
       Camera
         ↘
     [Cue moving ↗↙]
   ```

### Marker Visibility (30 seconds)

Test your marker:
1. Apply red tape to cue tip
2. Move it in camera view
3. Check if status shows **"Tip Detected"**
4. If not detected → Use brighter red marker

## ⚡ Quick Tips

### For Best Tracking:
- ✅ **Bright red** marker (electrical tape ideal)
- ✅ **Even lighting** (no harsh shadows)
- ✅ **Stable camera** (mount phone/tablet)
- ✅ **Plain background** (avoid red objects)
- ✅ **Slow strokes** at first (build consistency)

### For Best Practice:
- 📊 Record metrics for 10 strokes
- 📈 Track improvement over time
- 🎯 Focus on consistency, not speed
- 🔄 Reset between stroke attempts
- 💪 Start slow, increase speed gradually

## 🐛 Quick Troubleshooting

### Camera Won't Start
- Check browser permissions (click padlock icon)
- Close other apps using camera
- Try different browser

### Tip Not Detected
- Use brighter red marker
- Improve lighting
- Check marker is visible in frame

### Laggy Performance
- Reduce frame rate (see Configuration)
- Close other browser tabs
- Try on different device

### Metrics Seem Wrong
- Ensure camera is stable (not handheld)
- Check lighting is even
- Verify marker stays visible throughout stroke

## 📚 Next Steps

Now that you're up and running:

1. **Practice Consistently**
   - Track 10-20 strokes per session
   - Note your best deviation score
   - Work to beat it each session

2. **Experiment with Settings**
   - Try different camera angles
   - Adjust sensitivity (see API.md)
   - Find what works for you

3. **Learn More**
   - Read full [README.md](README.md)
   - Check [API Documentation](API.md)
   - Review [Troubleshooting](TROUBLESHOOTING.md)

4. **Share Feedback**
   - Report issues on GitHub
   - Suggest improvements
   - Share your results!

## 🎓 Understanding Your Metrics

### Deviation (Most Important)
- **What it means:** Average distance from perfect straight line
- **Goal:** < 15 pixels
- **How to improve:** Slow down, focus on smooth motion

### Smoothness
- **What it means:** Consistency of your stroke
- **Goal:** Lower numbers
- **How to improve:** Avoid jerky movements, relax grip

### Angle
- **What it means:** Direction of your stroke
- **Goal:** 0° or 180° for horizontal table
- **How to improve:** Check your stance and alignment

### Speed
- **What it means:** How fast cue tip moves
- **Goal:** Consistent speed across strokes
- **How to improve:** Practice rhythm and tempo

## 🏆 Achievement Goals

Set these goals for yourself:

**Beginner:**
- ✅ Get first "Excellent Stroke" (deviation < 15px)
- ✅ Complete 10 consecutive tracked strokes
- ✅ Understand all metrics

**Intermediate:**
- ✅ Average deviation < 12px over 10 strokes
- ✅ Smoothness < 5px
- ✅ Consistent speed (variation < 20%)

**Advanced:**
- ✅ Average deviation < 10px over 20 strokes
- ✅ Smoothness < 3px
- ✅ Angle within ±2° of target

## 📞 Need Help?

**Quick Links:**
- 🐛 [Troubleshooting Guide](TROUBLESHOOTING.md)
- 📖 [Full Documentation](README.md)
- 🤝 [Contributing](CONTRIBUTING.md)
- 📧 Email: scott.aiengineer@outlook.com

## 🎉 Success!

You're now ready to improve your pool stroke!

**Remember:**
- 🎯 Consistency over speed
- 📊 Track your progress
- 💪 Practice regularly
- 🎱 Have fun!

---

**Happy practicing! May your strokes be straight! 🎱**
