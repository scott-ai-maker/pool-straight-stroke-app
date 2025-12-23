"""
Pool Straight Stroke Trainer
A computer vision application to help pool players achieve a perfectly straight stroke.
"""

import cv2
import numpy as np
import time
from collections import deque
from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass
class StrokeMetrics:
    """Metrics for evaluating stroke quality"""
    deviation: float  # Average deviation from ideal straight line
    smoothness: float  # Consistency of motion
    angle: float  # Angle of stroke relative to horizontal
    speed: float  # Average speed of stroke
    is_straight: bool  # Whether stroke meets threshold


class PoolStrokeAnalyzer:
    """Analyzes pool cue stroke from video input"""
    
    def __init__(self, max_points: int = 30, deviation_threshold: float = 15.0):
        self.max_points = max_points
        self.deviation_threshold = deviation_threshold
        self.points = deque(maxlen=max_points)
        self.timestamps = deque(maxlen=max_points)
        self.color_lower = np.array([0, 100, 100])  # Red lower bound (HSV)
        self.color_upper = np.array([10, 255, 255])  # Red upper bound (HSV)
        
    def detect_cue_tip(self, frame: np.ndarray) -> Optional[Tuple[int, int]]:
        """Detect the cue tip (assumes red marker or bright tip)"""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create mask for red color
        mask = cv2.inRange(hsv, self.color_lower, self.color_upper)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Get largest contour
            largest = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest)
            if M["m00"] > 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                return (cx, cy)
        
        return None
    
    def add_point(self, point: Tuple[int, int]):
        """Add a tracked point to the stroke path"""
        self.points.append(point)
        self.timestamps.append(time.time())
    
    def calculate_metrics(self) -> Optional[StrokeMetrics]:
        """Calculate stroke quality metrics"""
        if len(self.points) < 5:
            return None
        
        points_array = np.array(list(self.points))
        
        # Fit a line through the points
        vx, vy, x0, y0 = cv2.fitLine(points_array, cv2.DIST_L2, 0, 0.01, 0.01)
        
        # Calculate deviation from the fitted line
        deviations = []
        for point in points_array:
            # Distance from point to line
            distance = abs((point[1] - y0) * vx - (point[0] - x0) * vy) / np.sqrt(vx**2 + vy**2)
            deviations.append(distance[0])
        
        avg_deviation = np.mean(deviations)
        smoothness = np.std(deviations)
        
        # Calculate angle
        angle = np.arctan2(vy, vx) * 180 / np.pi
        
        # Calculate speed
        if len(self.timestamps) >= 2:
            total_distance = sum(
                np.linalg.norm(np.array(self.points[i]) - np.array(self.points[i-1]))
                for i in range(1, len(self.points))
            )
            total_time = self.timestamps[-1] - self.timestamps[0]
            speed = total_distance / total_time if total_time > 0 else 0
        else:
            speed = 0
        
        is_straight = avg_deviation < self.deviation_threshold
        
        return StrokeMetrics(
            deviation=avg_deviation,
            smoothness=smoothness,
            angle=float(angle[0]),
            speed=speed,
            is_straight=is_straight
        )
    
    def draw_feedback(self, frame: np.ndarray, metrics: Optional[StrokeMetrics]) -> np.ndarray:
        """Draw visual feedback on the frame"""
        overlay = frame.copy()
        
        # Draw tracked points
        for i, point in enumerate(self.points):
            color = (0, 255, 0) if metrics and metrics.is_straight else (0, 165, 255)
            radius = 5
            cv2.circle(overlay, point, radius, color, -1)
            
            # Draw line between consecutive points
            if i > 0:
                cv2.line(overlay, self.points[i-1], point, color, 2)
        
        # Draw the ideal fitted line if we have enough points
        if len(self.points) >= 5:
            points_array = np.array(list(self.points))
            vx, vy, x0, y0 = cv2.fitLine(points_array, cv2.DIST_L2, 0, 0.01, 0.01)
            
            # Extend line across visible area
            lefty = int((-x0 * vy / vx) + y0)
            righty = int(((frame.shape[1] - x0) * vy / vx) + y0)
            cv2.line(overlay, (0, lefty), (frame.shape[1] - 1, righty), (255, 0, 255), 1)
        
        # Display metrics
        if metrics:
            y_offset = 30
            cv2.putText(overlay, f"Deviation: {metrics.deviation:.2f}px", 
                       (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            y_offset += 30
            
            cv2.putText(overlay, f"Smoothness: {metrics.smoothness:.2f}", 
                       (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            y_offset += 30
            
            cv2.putText(overlay, f"Angle: {metrics.angle:.1f} deg", 
                       (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            y_offset += 30
            
            cv2.putText(overlay, f"Speed: {metrics.speed:.1f} px/s", 
                       (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            y_offset += 30
            
            status = "STRAIGHT!" if metrics.is_straight else "NEEDS WORK"
            color = (0, 255, 0) if metrics.is_straight else (0, 0, 255)
            cv2.putText(overlay, status, (10, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 3)
        
        # Blend overlay with original frame
        alpha = 0.7
        return cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)
    
    def reset(self):
        """Reset tracking data"""
        self.points.clear()
        self.timestamps.clear()


class StrokeTrainerApp:
    """Main application class"""
    
    def __init__(self, camera_index: int = 0):
        self.camera_index = camera_index
        self.cap = None
        self.analyzer = PoolStrokeAnalyzer()
        self.is_tracking = False
        self.recording = False
        
    def initialize_camera(self) -> bool:
        """Initialize camera capture"""
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            print(f"Error: Could not open camera {self.camera_index}")
            return False
        
        # Set camera properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        return True
    
    def draw_instructions(self, frame: np.ndarray) -> np.ndarray:
        """Draw usage instructions"""
        instructions = [
            "Pool Straight Stroke Trainer",
            "",
            "Instructions:",
            "1. Mark your cue tip with red tape/marker",
            "2. Press SPACE to start/stop tracking",
            "3. Press 'r' to reset tracking",
            "4. Press 'q' to quit",
            "",
            f"Status: {'TRACKING' if self.is_tracking else 'STOPPED'}"
        ]
        
        y_offset = frame.shape[0] - 250
        for i, line in enumerate(instructions):
            cv2.putText(frame, line, (10, y_offset + i * 25), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return frame
    
    def run(self):
        """Main application loop"""
        if not self.initialize_camera():
            return
        
        print("Pool Straight Stroke Trainer Started")
        print("Press SPACE to start/stop tracking, 'r' to reset, 'q' to quit")
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("Error: Failed to capture frame")
                    break
                
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Detect cue tip
                cue_tip = self.analyzer.detect_cue_tip(frame)
                
                # If tracking and cue tip detected, add point
                if self.is_tracking and cue_tip:
                    self.analyzer.add_point(cue_tip)
                    # Draw current detection
                    cv2.circle(frame, cue_tip, 10, (0, 0, 255), -1)
                
                # Calculate metrics
                metrics = self.analyzer.calculate_metrics()
                
                # Draw feedback
                frame = self.analyzer.draw_feedback(frame, metrics)
                frame = self.draw_instructions(frame)
                
                # Display frame
                cv2.imshow('Pool Stroke Trainer', frame)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q'):
                    break
                elif key == ord(' '):
                    self.is_tracking = not self.is_tracking
                    if not self.is_tracking:
                        print(f"Tracking stopped. Final metrics: {metrics}")
                    else:
                        self.analyzer.reset()
                        print("Tracking started")
                elif key == ord('r'):
                    self.analyzer.reset()
                    print("Tracking reset")
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        print("Application closed")


def main():
    """Entry point"""
    app = StrokeTrainerApp(camera_index=0)
    app.run()


if __name__ == "__main__":
    main()
