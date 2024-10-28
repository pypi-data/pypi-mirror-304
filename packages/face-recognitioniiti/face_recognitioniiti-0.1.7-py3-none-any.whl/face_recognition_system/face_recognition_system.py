import cv2
import numpy as np
from ultralytics import YOLO
from arcface import ArcFace
import requests
import pickle
import os
from datetime import datetime
import torch



class FaceRecognitionSystem:
    def __init__(self, database_path="face_database.pkl", confidence_threshold=0.5, similarity_threshold=2):
        # Initialize YOLO for face detection
        self.yolo_model = YOLO('https://github.com/akanametov/yolo-face/releases/download/v0.0.0/yolov11s-face.pt').to('cpu')
        model_path = "model/model.tflite"
        model_url = "https://huggingface.co/spaces/Warlord-K/FaceRecognition-InterIIT/resolve/main/model.tflite?download=true"

        # Check if the model file already exists locally
        if not os.path.exists(model_path):
            print("Downloading model...")
            response = requests.get(model_url)
            response.raise_for_status()  # Ensure download was successful

            # Create the model directory if it doesn't exist
            os.makedirs(os.path.dirname(model_path), exist_ok=True)

            # Write the model file locally
            with open(model_path, "wb") as f:
                f.write(response.content)

            print("Model downloaded and saved locally.")

        # Load the model into TensorFlow Lite Interpreter
        self.face_rec = ArcFace.ArcFace(model_path)
        # Initialize ArcFace for face recognition
        #self.face_rec = ArcFace.ArcFace("https://huggingface.co/spaces/Warlord-K/FaceRecognition-InterIIT/resolve/main/model.tflite?download=true")
        
        # Thresholds
        self.confidence_threshold = confidence_threshold
        self.similarity_threshold = similarity_threshold
        
        # Load or create face database
        self.database_path = database_path
        self.face_database = self.load_database()
        
    def load_database(self):
        if os.path.exists(self.database_path):
            with open(self.database_path, 'rb') as f:
                return pickle.load(f)
            
        return {}
    
    def save_database(self):
        with open(self.database_path, 'wb') as f:
            pickle.dump(self.face_database, f)
    
    def add_face_to_database(self, name, frame):
        """Add a new face to the database"""
        try:
            embedding = self.face_rec.calc_emb(frame)
            self.face_database[name] = embedding
            self.save_database()
            return True
        except Exception as e:
            print(f"Error adding face to database: {e}")
            return False
    
    def find_closest_match(self, embedding):
        """Find the closest matching face in the database"""
        if not self.face_database:
            return "Unknown", 1.0
            
        min_distance = 10000
        closest_name = "Unknown"
        
        for name, stored_embedding in self.face_database.items():
            distance = self.face_rec.get_distance_embeddings(embedding, stored_embedding)
            if distance < min_distance:
                min_distance = distance
                closest_name = name
        
        return closest_name, min_distance
    
    def process_frame(self, frame):
        """Process a single frame"""
        # Run YOLO detection
        if isinstance(frame, torch.Tensor):
             frame = frame.to('cpu')

# Run the model with the frame on CPU
        results = self.yolo_model(frame, verbose=False)[0]

        
        # Process each detected face
        for detection in results.boxes.data:
            x1, y1, x2, y2, conf, _ = detection
            
            if conf < self.confidence_threshold:
                continue
                
            # Convert coordinates to integers
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
            
            # Extract face region
            face_region = frame[y1:y2, x1:x2]
            
            try:
                # Calculate face embedding
                embedding = self.face_rec.calc_emb(face_region)
                
                # Find closest match
                name, distance = self.find_closest_match(embedding)
                
                # Determine if match is close enough
                if distance > self.similarity_threshold:
                    name = "Unknown"
                
                # Draw rectangle and name
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{name} ({conf:.2f})", 
                           (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.5, (0, 255, 0), 2)
                
            except Exception as e:
                print(f"Error processing face: {e}")
                
        return frame
    
    def run(self):
        """Run the face recognition system on webcam feed"""
        cap = cv2.VideoCapture(0)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            # Process the frame
            processed_frame = self.process_frame(frame)
            
            # Display the result
            cv2.imshow('Face Recognition', processed_frame)
            
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
            elif key == ord('a'):
                # Add new face to database
                name = input("Enter name for new face: ")
                if self.add_face_to_database(name, frame):
                    print(f"Successfully added {name} to database")
                else:
                    print("Failed to add face to database")
        
        cap.release()
        cv2.destroyAllWindows()
def main():
    face_system = FaceRecognitionSystem()
    face_system.run()

if __name__ == "__main__":
    main()
