import cv2

cap = cv2.VideoCapture(0)
while(1):
    # get a frame
    ret, frame = cap.read()
    # show a frame
    cv2.imshow("capture", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite(r'C:\Users\ZhangJiankai\Desktop\14.jpg', frame)
        break
cap.release()
cv2.destroyAllWindows()