# API Documentation

Complete REST API documentation for the Pool Stroke Trainer application.

## Base URL

**Local Development:**
```
http://localhost:7860
```

**Production (Hugging Face Spaces):**
```
https://huggingface.co/spaces/<username>/pool-stroke-trainer
```

## Authentication

No authentication required. Session-based tracking uses Flask sessions with secure cookies.

## Endpoints

### Main Application

#### `GET /`

Render the main application page.

**Response:**
- **Content-Type:** `text/html`
- **Status Code:** `200 OK`

**Example:**
```bash
curl http://localhost:7860/
```

---

### Frame Processing

#### `POST /api/process_frame`

Process a video frame and return annotated image with stroke analysis metrics.

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
  "tracking": true
}
```

**Parameters:**
- `image` (string, required): Base64-encoded JPEG image with data URL prefix
- `tracking` (boolean, optional): Whether to add detected points to stroke path. Default: `false`

**Response:**
```json
{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
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

**Response Fields:**
- `image` (string): Base64-encoded annotated frame with visual overlays
- `tip_detected` (boolean): Whether cue tip was detected in frame
- `metrics` (object|null): Stroke quality metrics, or null if insufficient data
  - `deviation` (float): Average perpendicular distance from ideal line (pixels)
  - `smoothness` (float): Standard deviation of point deviations (pixels)
  - `angle` (float): Stroke angle relative to horizontal (degrees)
  - `speed` (float): Average cue tip velocity (pixels/second)
  - `is_straight` (boolean): Whether stroke meets straightness threshold
  - `point_count` (integer): Number of tracking points used

**Status Codes:**
- `200 OK`: Frame processed successfully
- `400 Bad Request`: Invalid or missing image data
- `500 Internal Server Error`: Processing failure

**Example:**
```javascript
const response = await fetch('/api/process_frame', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    image: canvas.toDataURL('image/jpeg', 0.8),
    tracking: true
  })
});
const result = await response.json();
```

**cURL Example:**
```bash
curl -X POST http://localhost:7860/api/process_frame \
  -H "Content-Type: application/json" \
  -d '{"image":"data:image/jpeg;base64,...","tracking":true}'
```

---

### Tracking Management

#### `POST /api/reset`

Reset tracking data for the current session. Clears all accumulated points and timestamps.

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{}
```

**Response:**
```json
{
  "success": true,
  "message": "Tracking reset successfully"
}
```

**Response Fields:**
- `success` (boolean): Whether reset was successful
- `message` (string): Human-readable status message

**Status Codes:**
- `200 OK`: Reset successful
- `500 Internal Server Error`: Reset operation failed

**Example:**
```javascript
const response = await fetch('/api/reset', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' }
});
const result = await response.json();
```

**cURL Example:**
```bash
curl -X POST http://localhost:7860/api/reset \
  -H "Content-Type: application/json" \
  -d '{}'
```

---

### Configuration

#### `GET /api/config`

Get current analyzer configuration for the session.

**Response:**
```json
{
  "max_points": 30,
  "deviation_threshold": 15.0
}
```

**Response Fields:**
- `max_points` (integer): Maximum tracking points to maintain (5-100)
- `deviation_threshold` (float): Straightness threshold in pixels (5.0-50.0)

**Status Codes:**
- `200 OK`: Configuration retrieved successfully
- `500 Internal Server Error`: Configuration retrieval failed

**Example:**
```javascript
const response = await fetch('/api/config');
const config = await response.json();
```

**cURL Example:**
```bash
curl http://localhost:7860/api/config
```

---

#### `POST /api/config`

Update analyzer configuration for the session.

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "max_points": 40,
  "deviation_threshold": 20.0
}
```

**Parameters:**
- `max_points` (integer, optional): Maximum tracking points (5-100)
- `deviation_threshold` (float, optional): Straightness threshold px (5.0-50.0)

**Response:**
```json
{
  "success": true,
  "max_points": 40,
  "deviation_threshold": 20.0
}
```

**Response Fields:**
- `success` (boolean): Whether update was successful
- `max_points` (integer): Updated max points value
- `deviation_threshold` (float): Updated threshold value

**Status Codes:**
- `200 OK`: Configuration updated successfully
- `400 Bad Request`: Invalid parameter values
- `500 Internal Server Error`: Configuration update failed

**Validation:**
- `max_points` must be between 5 and 100
- `deviation_threshold` must be between 5.0 and 50.0

**Example:**
```javascript
const response = await fetch('/api/config', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    max_points: 40,
    deviation_threshold: 20.0
  })
});
const result = await response.json();
```

**cURL Example:**
```bash
curl -X POST http://localhost:7860/api/config \
  -H "Content-Type: application/json" \
  -d '{"max_points":40,"deviation_threshold":20.0}'
```

---

### Health Check

#### `GET /health`

Health check endpoint for monitoring and orchestration systems.

**Response:**
```json
{
  "status": "healthy",
  "service": "pool-stroke-trainer",
  "version": "1.0.0"
}
```

**Response Fields:**
- `status` (string): Service health status ("healthy" or "unhealthy")
- `service` (string): Service identifier
- `version` (string): Application version

**Status Codes:**
- `200 OK`: Service is healthy and operational

**Example:**
```javascript
const response = await fetch('/health');
const health = await response.json();
```

**cURL Example:**
```bash
curl http://localhost:7860/health
```

---

## Error Responses

All endpoints may return error responses in the following format:

```json
{
  "error": "Error type or category",
  "message": "Detailed error message"
}
```

### Common Error Codes

- `400 Bad Request`: Invalid request parameters or malformed data
- `404 Not Found`: Endpoint does not exist
- `405 Method Not Allowed`: HTTP method not supported for endpoint
- `500 Internal Server Error`: Server-side processing error

### Error Examples

**Missing Required Field:**
```json
{
  "error": "No image provided"
}
```

**Invalid Image Data:**
```json
{
  "error": "Invalid image data: Failed to decode image"
}
```

**Configuration Validation Error:**
```json
{
  "error": "max_points must be between 5 and 100"
}
```

**Internal Server Error:**
```json
{
  "error": "Internal server error",
  "message": "Failed to process frame: Connection timeout"
}
```

---

## Rate Limiting

Currently, no rate limiting is implemented. For production deployments, consider:
- Implementing rate limiting at the API gateway level
- Using Flask-Limiter extension
- Setting up CDN with rate limiting rules

**Recommended Limits:**
- `/api/process_frame`: 20 requests/second per session
- `/api/reset`: 5 requests/minute per session
- `/api/config`: 10 requests/minute per session

---

## Session Management

The application uses Flask sessions to maintain user state:
- Each user gets a unique session ID (16-byte random hex)
- Session data is stored server-side in memory
- Session cookies are HTTP-only and secure (in production)
- No authentication required

**Session Storage:**
- Single-worker deployments: In-memory dictionary
- Multi-worker deployments: Consider Redis or similar

---

## CORS Policy

Default CORS policy:
- Same-origin requests only
- No cross-origin requests allowed by default

To enable CORS for specific origins, add to `app.py`:
```python
from flask_cors import CORS
CORS(app, origins=['https://your-domain.com'])
```

---

## WebSocket Support

Currently not implemented. All communication uses HTTP REST API with polling at 10 FPS.

Future consideration: WebSocket for real-time bidirectional communication.

---

## SDK Examples

### Python Client

```python
import requests
import base64

# Load image
with open('frame.jpg', 'rb') as f:
    image_data = base64.b64encode(f.read()).decode('utf-8')

# Process frame
response = requests.post('http://localhost:7860/api/process_frame', json={
    'image': f'data:image/jpeg;base64,{image_data}',
    'tracking': True
})

result = response.json()
print(f"Deviation: {result['metrics']['deviation']:.2f}px")
```

### JavaScript/TypeScript

```typescript
interface ProcessFrameResponse {
  image: string;
  tip_detected: boolean;
  metrics: {
    deviation: number;
    smoothness: number;
    angle: number;
    speed: number;
    is_straight: boolean;
    point_count: number;
  } | null;
}

async function processFrame(imageData: string, tracking: boolean): Promise<ProcessFrameResponse> {
  const response = await fetch('/api/process_frame', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ image: imageData, tracking })
  });
  
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }
  
  return await response.json();
}
```

---

## Changelog

### v1.0.0 (2025-12-22)
- Initial API release
- Frame processing endpoint
- Reset and configuration endpoints
- Health check endpoint

---

## Support

For API questions or issues:
- 📧 Email: scott.aiengineer@outlook.com
- 🐙 GitHub Issues: [Create Issue](https://github.com/scott-ai-maker/pool-straight-stroke-app/issues)
- 📖 Documentation: [README.md](README.md)
