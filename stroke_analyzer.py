"""
Pool Stroke Analyzer Module.

Provides computer vision-based analysis of pool cue strokes using OpenCV.
Tracks cue tip position over time and calculates straightness metrics using
linear regression and statistical analysis.

Author: Scott Gordon
Email: scott.aiengineer@outlook.com
License: MIT
"""

import cv2
import numpy as np
import time
import logging
from collections import deque
from dataclasses import dataclass, asdict
from typing import List, Tuple, Optional

# Configure module logger
logger = logging.getLogger(__name__)


@dataclass
class StrokeMetrics:
    """Quantitative metrics for evaluating pool stroke quality.
    
    Attributes:
        deviation: Average perpendicular distance from ideal straight line (pixels).
                   Lower values indicate straighter strokes.
        smoothness: Standard deviation of point deviations (pixels).
                    Lower values indicate more consistent motion.
        angle: Angle of stroke relative to horizontal axis (degrees).
               Ideally close to 0° or 180° for horizontal strokes.
        speed: Average velocity of cue tip during stroke (pixels/second).
               Useful for analyzing stroke tempo and consistency.
        is_straight: Boolean indicating if stroke meets straightness threshold.
                     True if deviation < deviation_threshold.
        point_count: Number of tracking points used in calculation.
                     More points generally provide more reliable metrics.
    """
    deviation: float
    smoothness: float
    angle: float
    speed: float
    is_straight: bool
    point_count: int
    
    def to_dict(self) -> dict:
        """Convert metrics to dictionary for JSON serialization.
        
        Returns:
            Dictionary representation of all metrics.
        """
        return asdict(self)


class PoolStrokeAnalyzer:
    """Analyzes pool cue strokes using computer vision and statistical methods.
    
    This class maintains state across video frames, tracking the cue tip position
    over time using color-based detection. It calculates stroke quality metrics
    by fitting a line through the tracked points and measuring deviations.
    
    The analyzer is stateful - each instance maintains its own tracking history.
    For multi-user applications, each user session should have its own instance.
    
    Detection Method:
        Uses HSV color space filtering to detect a red marker on the cue tip.
        HSV is preferred over RGB because it separates color information from
        brightness, making detection more robust under varying lighting conditions.
    
    Analysis Method:
        Applies least-squares linear regression (via cv2.fitLine) to find the
        best-fit line through tracked points, then calculates perpendicular
        distances to quantify straightness.
    
    Attributes:
        max_points: Maximum number of tracking points to retain.
        deviation_threshold: Maximum average deviation (pixels) to classify as 'straight'.
        points: Deque of tracked (x, y) coordinates.
        timestamps: Deque of corresponding timestamps for speed calculation.
        color_lower: HSV lower bound for red color detection (first range).
        color_upper: HSV upper bound for red color detection (first range).
        color_lower2: HSV lower bound for red color detection (second range, handles wrap-around).
        color_upper2: HSV upper bound for red color detection (second range).
    """
    
    def __init__(self, max_points: int = 30, deviation_threshold: float = 15.0):
        """Initialize the stroke analyzer.
        
        Args:
            max_points: Maximum tracking points to maintain (affects memory and smoothing).
                       Range: 5-100. Higher values provide smoother averaging but use more memory.
            deviation_threshold: Maximum average deviation in pixels to classify stroke as 'straight'.
                                Range: 5.0-50.0. Lower values require more precise strokes.
        
        Raises:
            ValueError: If parameters are outside valid ranges.
        """
        # Validate parameters
        if not (5 <= max_points <= 100):
            raise ValueError("max_points must be between 5 and 100")
        if not (5.0 <= deviation_threshold <= 50.0):
            raise ValueError("deviation_threshold must be between 5.0 and 50.0")
        
        self.max_points = max_points
        self.deviation_threshold = deviation_threshold
        self.points = deque(maxlen=max_points)
        self.timestamps = deque(maxlen=max_points)
        
        # HSV color ranges for red marker detection
        # Red in HSV wraps around (0° and 360° are both red), so we need two ranges:
        # Range 1: 0-10° (lower reds)
        self.color_lower = np.array([0, 100, 100])
        self.color_upper = np.array([10, 255, 255])
        # Range 2: 170-180° (upper reds)
        self.color_lower2 = np.array([170, 100, 100])
        self.color_upper2 = np.array([180, 255, 255])
        
        logger.info(f"PoolStrokeAnalyzer initialized: max_points={max_points}, threshold={deviation_threshold}")
        
    def detect_cue_tip(self, frame: np.ndarray) -> Optional[Tuple[int, int]]:
        """Detect cue tip position using HSV color-based detection.
        
        Detection Algorithm:
            1. Convert frame from BGR to HSV color space
            2. Create binary mask for red color (using two HSV ranges)
            3. Apply morphological operations to reduce noise
            4. Find contours in the binary mask
            5. Select the largest contour (assumed to be the cue tip)
            6. Calculate centroid of the contour
        
        Why Color Detection?
            - Fast and computationally efficient (works on mobile devices)
            - Simple implementation without ML models
            - Effective with proper lighting and marker
            - Downside: Requires colored marker and controlled environment
        
        Alternative Approaches:
            - Object detection (YOLO, SSD): More robust but computationally expensive
            - MediaPipe: Good for hand/pose tracking
            - Feature matching: Works without markers but slower
        
        Args:
            frame: Input image in BGR format (OpenCV standard).
            
        Returns:
            (x, y) tuple of cue tip centroid coordinates, or None if not detected.
            
        Note:
            Minimum contour area of 50 pixels is used to filter out noise.
            Adjust if detection is too sensitive or not sensitive enough.
        """
        try:
            # Convert BGR to HSV color space
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Create binary mask for red color (handles HSV wrap-around)
            mask1 = cv2.inRange(hsv, self.color_lower, self.color_upper)
            mask2 = cv2.inRange(hsv, self.color_lower2, self.color_upper2)
            mask = cv2.bitwise_or(mask1, mask2)
            
            # Apply morphological operations to reduce noise
            # Opening: erosion followed by dilation (removes small objects)
            # Closing: dilation followed by erosion (fills small holes)
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            
            # Find contours in the binary mask
            contours, _ = cv2.findContours(
                mask,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )
            
            if not contours:
                return None
            
            # Select the largest contour (assumes cue tip is most prominent red object)
            largest = max(contours, key=cv2.contourArea)
            
            # Filter out noise (contours too small to be the cue tip)
            if cv2.contourArea(largest) < 50:
                return None
                
            # Calculate centroid using image moments
            # Moments provide statistical properties of the contour
            M = cv2.moments(largest)
            if M["m00"] > 0:  # Avoid division by zero
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                return (cx, cy)
            
            return None
            
        except Exception as e:
            logger.error(f"Error detecting cue tip: {str(e)}")
            return None
    
    def add_point(self, point: Tuple[int, int]) -> None:
        """Add a tracking point to the stroke path.
        
        Appends the point to the tracking deque along with its timestamp.
        The deque automatically removes the oldest point when max_points is reached,
        implementing a sliding window for recent stroke history.
        
        Args:
            point: (x, y) tuple of pixel coordinates to add to the path.
        """
        self.points.append(point)
        self.timestamps.append(time.time())
        logger.debug(f"Added point: {point}, total points: {len(self.points)}")
    
    def calculate_metrics(self) -> Optional[StrokeMetrics]:
        """Calculate comprehensive stroke quality metrics using linear regression.
        
        Algorithm:
            1. Fit a line through all tracked points using least-squares method
            2. Calculate perpendicular distance from each point to the fitted line
            3. Compute statistical measures (mean, standard deviation)
            4. Calculate stroke angle and speed from timestamps
            5. Determine if stroke meets straightness threshold
        
        Mathematical Approach:
            Uses cv2.fitLine with DIST_L2 (least squares) method, which is equivalent
            to linear regression but robust to outliers. The fitted line is represented
            in parametric form: (x, y) = (x0, y0) + t * (vx, vy)
            
            Perpendicular distance formula:
                distance = |ax + by + c| / sqrt(a^2 + b^2)
            where the line is represented as ax + by + c = 0
        
        Returns:
            StrokeMetrics object with all calculated metrics, or None if insufficient points.
            
        Note:
            Requires at least 5 points for reliable metric calculation. With fewer points,
            linear regression may be unstable or produce misleading results.
        """
        if len(self.points) < 5:
            logger.debug(f"Insufficient points for metrics: {len(self.points)} < 5")
            return None
        
        try:
            points_array = np.array(list(self.points), dtype=np.float32)
            
            # Fit a line through points using least-squares linear regression
            # cv2.fitLine uses RANSAC-like method (DIST_L2) robust to outliers
            # Returns: (vx, vy) = direction vector, (x0, y0) = point on line
            vx, vy, x0, y0 = cv2.fitLine(
                points_array,
                cv2.DIST_L2,  # Least squares method
                0,            # Not used for DIST_L2
                0.01,         # Distance accuracy
                0.01          # Angle accuracy
            )
            
            # Calculate perpendicular distance from each point to fitted line
            # Formula: |ax + by + c| / sqrt(a² + b²)
            # Where line equation: (y - y0) / vy = (x - x0) / vx
            # Rearranged: vy * (x - x0) - vx * (y - y0) = 0
            deviations = []
            for point in points_array:
                # Calculate perpendicular distance
                distance = abs(
                    (point[1] - y0) * vx - (point[0] - x0) * vy
                ) / np.sqrt(vx**2 + vy**2)
                deviations.append(float(distance[0]))
            
            # Calculate statistical measures
            avg_deviation = np.mean(deviations)
            smoothness = np.std(deviations)  # Lower std = more consistent
            
            # Calculate stroke angle (degrees from horizontal)
            # Useful for checking if stroke is horizontal (ideal: 0° or 180°)
            angle = float(np.arctan2(vy[0], vx[0]) * 180 / np.pi)
            
            # Calculate average speed (pixels per second)
            speed = 0.0
            if len(self.timestamps) >= 2:
                # Sum distances between consecutive points
                total_distance = sum(
                    np.linalg.norm(points_array[i] - points_array[i-1])
                    for i in range(1, len(points_array))
                )
                # Calculate time span
                total_time = self.timestamps[-1] - self.timestamps[0]
                speed = float(total_distance / total_time if total_time > 0 else 0)
            
            # Determine if stroke meets straightness threshold
            is_straight = avg_deviation < self.deviation_threshold
            
            metrics = StrokeMetrics(
                deviation=float(avg_deviation),
                smoothness=float(smoothness),
                angle=angle,
                speed=speed,
                is_straight=is_straight,
                point_count=len(self.points)
            )
            
            logger.debug(f"Calculated metrics: deviation={avg_deviation:.2f}, is_straight={is_straight}")
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating metrics: {str(e)}")
            return None
    
    def draw_visualization(self, frame: np.ndarray) -> Tuple[np.ndarray, Optional[StrokeMetrics]]:
        """Draw stroke path visualization and annotations on the frame.
        
        Visualization Elements:
            - Tracked points: Colored circles at each tracked position
            - Stroke path: Lines connecting consecutive points
            - Fitted line: Best-fit straight line (purple) extending across frame
            - Color coding: Green = straight stroke, Orange = needs improvement
        
        Args:
            frame: Input image to annotate (not modified in-place).
            
        Returns:
            Tuple of (annotated_frame, metrics):
                - annotated_frame: Copy of input with visual overlays
                - metrics: Calculated StrokeMetrics object, or None if insufficient points
        """
        try:
            # Work on a copy to avoid modifying original frame
            annotated = frame.copy()
            
            # Calculate metrics for color coding
            metrics = self.calculate_metrics()
            
            # Determine path color based on stroke quality
            # Green = straight stroke, Orange = needs work
            path_color = (0, 255, 0) if metrics and metrics.is_straight else (0, 165, 255)
            
            # Draw tracked points and connecting lines
            for i, point in enumerate(self.points):
                # Draw point as filled circle
                cv2.circle(annotated, point, 5, path_color, -1)
                
                # Draw line to previous point
                if i > 0:
                    cv2.line(annotated, self.points[i-1], point, path_color, 3)
            
            # Draw fitted line if enough points available
            if len(self.points) >= 5:
                points_array = np.array(list(self.points), dtype=np.float32)
                vx, vy, x0, y0 = cv2.fitLine(points_array, cv2.DIST_L2, 0, 0.01, 0.01)
                
                # Extend line across entire frame width
                rows, cols = frame.shape[:2]
                lefty = int((-x0 * vy / vx) + y0)
                righty = int(((cols - x0) * vy / vx) + y0)
                
                # Draw fitted line in purple (255, 0, 255)
                cv2.line(annotated, (0, lefty), (cols - 1, righty), (255, 0, 255), 2)
            
            return annotated, metrics
            
        except Exception as e:
            logger.error(f"Error drawing visualization: {str(e)}")
            return frame, None
    
    def reset(self) -> None:
        """Clear all tracking data and metrics.
        
        Removes all tracked points and timestamps, resetting the analyzer to
        its initial state. Useful when starting a new practice session or
        after completing a stroke analysis.
        """
        point_count = len(self.points)
        self.points.clear()
        self.timestamps.clear()
        logger.info(f"Reset analyzer: cleared {point_count} points")
