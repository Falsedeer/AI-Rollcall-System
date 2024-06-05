import os
from deepface import DeepFace


class FacialRecognition:
    TARGET_FOLDER = None
    pass



    def __init__(self, targetFolder: str):
        FacialRecognition.TARGET_FOLDER = targetFolder
    #end

    def recognizeFace(self, imagePath: str, studentId: str):
        checkImagePath = imagePath 
        #targetImagePath = os.path.join(os.path.dirname(__name__), FacialRecognition.TARGET_FOLDER, studentId)
        targetImagePath = FacialRecognition.TARGET_FOLDER + "/"+ studentId + ".png"
        
        print(checkImagePath)
        print(targetImagePath)
        
        try:
            if DeepFace.verify(targetImagePath, targetImagePath)['verified']:
                return True
            else:
                return False
            #end
        except ValueError:
            raise ValueError
        #end
    #end
#end

if __name__ == "__main__":
    target_folder = "../../Targets"
    imagePath = "../../Targets/D1166597.png"
    studentId = "D1166597"
    facialRecognition = FacialRecognition(target_folder)



    print(facialRecognition.recognizeFace(imagePath, studentId))
#end
