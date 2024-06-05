import os
from deepface import DeepFace


class FacialRecognition:
    TARGET_FOLDER = None
    pass



    def __init__(self, targetFolder: str):
        FacialRecognition.TARGET_FOLDER = targetFolder
    #end

    def recognizeFace(self, imagePath: str, studentId: str):
        studentId = studentId + '.png'
        targetImagePath = os.path.join(os.path.dirname(__name__), FacialRecognition.TARGET_FOLDER, studentId)
        targetImage = os.open(targetImagePath, mode = 'r')
        checkImage = os.open(imagePath, mode = 'r')

        try:
            if DeepFace.verify(checkImage, targetImage.copy())['verified']:
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
    print("hello")
    target_folder = "../../Targets"
    imagePath = "../../Targets/D1166597.png"
    studentId = "D1166597"
    facialRecognition = FacialRecognition(target_folder)



    print(facialRecognition.recognizeFace(imagePath, studentId))
#end
