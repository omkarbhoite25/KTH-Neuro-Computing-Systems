;; Auto-generated. Do not edit!


(when (boundp 'single_motor::GetPosition)
  (if (not (find-package "SINGLE_MOTOR"))
    (make-package "SINGLE_MOTOR"))
  (shadow 'GetPosition (find-package "SINGLE_MOTOR")))
(unless (find-package "SINGLE_MOTOR::GETPOSITION")
  (make-package "SINGLE_MOTOR::GETPOSITION"))
(unless (find-package "SINGLE_MOTOR::GETPOSITIONREQUEST")
  (make-package "SINGLE_MOTOR::GETPOSITIONREQUEST"))
(unless (find-package "SINGLE_MOTOR::GETPOSITIONRESPONSE")
  (make-package "SINGLE_MOTOR::GETPOSITIONRESPONSE"))

(in-package "ROS")





(defclass single_motor::GetPositionRequest
  :super ros::object
  :slots (_id ))

(defmethod single_motor::GetPositionRequest
  (:init
   (&key
    ((:id __id) 0)
    )
   (send-super :init)
   (setq _id (round __id))
   self)
  (:id
   (&optional __id)
   (if __id (setq _id __id)) _id)
  (:serialization-length
   ()
   (+
    ;; uint8 _id
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint8 _id
       (write-byte _id s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint8 _id
     (setq _id (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;;
   self)
  )

(defclass single_motor::GetPositionResponse
  :super ros::object
  :slots (_position ))

(defmethod single_motor::GetPositionResponse
  (:init
   (&key
    ((:position __position) 0)
    )
   (send-super :init)
   (setq _position (round __position))
   self)
  (:position
   (&optional __position)
   (if __position (setq _position __position)) _position)
  (:serialization-length
   ()
   (+
    ;; uint16 _position
    2
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint16 _position
       (write-word _position s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint16 _position
     (setq _position (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;;
   self)
  )

(defclass single_motor::GetPosition
  :super ros::object
  :slots ())

(setf (get single_motor::GetPosition :md5sum-) "fa82be1deaeed2877bd58e858d4dcf23")
(setf (get single_motor::GetPosition :datatype-) "single_motor/GetPosition")
(setf (get single_motor::GetPosition :request) single_motor::GetPositionRequest)
(setf (get single_motor::GetPosition :response) single_motor::GetPositionResponse)

(defmethod single_motor::GetPositionRequest
  (:response () (instance single_motor::GetPositionResponse :init)))

(setf (get single_motor::GetPositionRequest :md5sum-) "fa82be1deaeed2877bd58e858d4dcf23")
(setf (get single_motor::GetPositionRequest :datatype-) "single_motor/GetPositionRequest")
(setf (get single_motor::GetPositionRequest :definition-)
      "uint8 id
---
uint16 position

")

(setf (get single_motor::GetPositionResponse :md5sum-) "fa82be1deaeed2877bd58e858d4dcf23")
(setf (get single_motor::GetPositionResponse :datatype-) "single_motor/GetPositionResponse")
(setf (get single_motor::GetPositionResponse :definition-)
      "uint8 id
---
uint16 position

")



(provide :single_motor/GetPosition "fa82be1deaeed2877bd58e858d4dcf23")


