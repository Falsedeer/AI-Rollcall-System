import os
from deepface import DeepFace
from icecream import ic


class FacialRecognitionClass:
    TARGET_FOLDER = None
    
    def __init__(self, targetFolder: str):
        FacialRecognitionClass.TARGET_FOLDER = targetFolder
    #end

    # Face detection function, needs image path of the face to be detected and the nid of the student. Returns true/false or ValueError
    def recognizeFace(self, imagePath: str, studentId: str) -> bool:
        checkImagePath = imagePath 
        #targetImagePath = os.path.join(os.path.dirname(__name__), FacialRecognition.TARGET_FOLDER, studentId)
        targetImagePath = FacialRecognitionClass.TARGET_FOLDER + "/" + studentId + ".png"

        ic(f"comparing {imagePath} to target {studentId}")
        
        try:
            if DeepFace.verify(checkImagePath, targetImagePath)['verified']:
                return True
            else:
                return False
            #end
        except ValueError:
            return False
        #end
    #end
#end

if __name__ == "__main__":
    target_folder = "../../Targets"
    imagePath = "../../Targets/D1166597.png"
    studentId = "D1166597"
    facialRecognition = FacialRecognitionClass(target_folder)



    print(facialRecognition.recognizeFace(imagePath, studentId))
#end
