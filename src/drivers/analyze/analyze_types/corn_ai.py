from base_ai import BaseAnalyze
class CornAnalyze(BaseAnalyze):
    def __init__(self, image_service):
        super().__init__(image_service)
        self.min_area = 400
        self.max_area = 1200
        self.min_avg_area = 400
        self.max_avg_area = 1200
        self.contour_colors = {
            'good': (0, 255, 0),
            'burned': (0, 0, 255),
            'greenish': (255, 255, 0),
            'bad_detection': (128, 128, 128),
            'small': (0, 255, 255),
            'unknown': (255, 0, 255)
        }
        
    def _average_contour_area(self, contours: list) -> None:
        if not contours:
            raise ValueError("No contours found to calculate average area.")
        
        total_area = 0
        count_valid = 0

        for contour in contours:
            area = self.cv2.contourArea(contour)
            if self.min_area <= area <= self.max_area:
                total_area += area
                count_valid += 1

        if count_valid == 0:
            raise ValueError("No valid contours to calculate average area.")

        average_area = total_area / count_valid
        self.min_avg_area = average_area * 0.75
        self.max_avg_area = average_area * 1.75
    
    def _classify_corn(self, contour_area: float, grain_image) -> tuple:
        if contour_area < self.min_avg_area:
            return ("small", "area too small (noise)")
        if contour_area > self.max_avg_area:
            return ("bad_detection", "area too large (probably multiple grains)")
        
        hsv = self.cv2.cvtColor(grain_image, self.cv2.COLOR_BGR2HSV)
        h_mean = self.np.mean(hsv[:, :, 0])
        s_mean = self.np.mean(hsv[:, :, 1])
        v_mean = self.np.mean(hsv[:, :, 2])
        
        if v_mean < 90 and s_mean < 60:
            return ("burned", f"dark grain (H={h_mean:.1f}, S={s_mean:.1f}, V={v_mean:.1f})")

        if 40 <= h_mean <= 80:
            return ("greenish", f"green hue (H={h_mean:.1f})")

        if 18 <= h_mean <= 35 and v_mean > 100:
            return ("good", f"healthy yellow grain (H={h_mean:.1f})")

        return ("unknown", f"undefined color pattern (H={h_mean:.1f})")
    
    def ai(self, payload, save_path) -> tuple:
        image = self.cv2.imread(save_path)
        gray = self.cv2.cvtColor(image, self.cv2.COLOR_BGR2GRAY)
        blur = self.cv2.GaussianBlur(gray, (5, 5), 0)
        
        _, thresh = self.cv2.threshold(blur, 165, 255, self.cv2.THRESH_BINARY)
        morphologyEx = self.cv2.morphologyEx(thresh, self.cv2.MORPH_CLOSE, self.np.ones((5, 5), self.np.uint8))
        kernel = self.cv2.getStructuringElement(self.cv2.MORPH_RECT, (3, 3))
        eroded = self.cv2.erode(morphologyEx, kernel, iterations=1)
        
        contours, _ = self.cv2.findContours(eroded, self.cv2.RETR_EXTERNAL, self.cv2.CHAIN_APPROX_SIMPLE)
        self._average_contour_area(contours)

        result = {
            "good_grains": 0,
            "burned": 0,
            "greenish": 0,
            "small": 0,
            "bad_detection": 0,
            "unknown": 0,
        }
        
        for idx, contour in enumerate(contours):
            x, y, w, h = self.cv2.boundingRect(contour)
            grain_image = image[y:y+h, x:x+w]
            
            contour_area = w * h
            classification, reason = self._classify_corn(contour_area, grain_image)
            result[classification] += 1

        return result, {
            "total_grains": len(contours),
            "min_avg_area": self.min_avg_area,
            "max_avg_area": self.max_avg_area
        }
    