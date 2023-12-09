import multiprocessing 
from multiprocessing import Process, Manager
import cv2
import dlib
from imutils import face_utils
import serial
import time
import goi_ham as gh
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

