import numpy as np

def get_match_score(face_box, body_box):
    """
    Calculates what percentage of the face_box is inside the body_box.
    Format: [xmin, ymin, xmax, ymax]
    """
    # 1. Determine the coordinates of the intersection rectangle
    x_left = max(face_box['x1'], body_box['x1'])
    y_top = max(face_box['y1'], body_box['y1'])
    x_right = min(face_box['x2'], body_box['x2'])
    y_bottom = min(face_box['y2'], body_box['y2'])

    if x_right < x_left or y_bottom < y_top:
        return 0.0  # No overlap at all

    # 2. Calculate area of intersection
    intersection_area = (x_right - x_left) * (y_bottom - y_top)

    # 3. Calculate area of the face box
    face_area = (face_box['x2']- face_box['x1']) * (face_box['y2'] - face_box['y1'])

    # 4. Return the ratio (how much of the face is inside the body)
    return intersection_area / face_area if face_area > 0 else 0

def match_behaviour_with_face(face_boxes, behavior_boxes):
    results = []
    for b_box in behavior_boxes:
        best_score = 0
        matched_body_idx = -1
        
        for i, f_box in enumerate(face_boxes):
            score = get_match_score(f_box, b_box)
            if score > best_score:
                best_score = score
                matched_body_idx = i
                
        if best_score > 0.8:
            face = face_boxes[matched_body_idx]
            results.append({
                'x1': b_box['x1'],
                'y1': b_box['y1'],
                'x2': b_box['x2'],
                'y2': b_box['y2'],
                'behavior': b_box['name'],
                'student_code': face['name']
            })
            
    return results
            