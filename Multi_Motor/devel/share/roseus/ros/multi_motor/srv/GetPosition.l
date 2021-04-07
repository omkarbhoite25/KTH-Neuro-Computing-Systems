;; Auto-generated. Do not edit!


(when (boundp 'multi_motor::GetPosition)
  (if (not (find-package "MULTI_MOTOR"))
    (make-package "MULTI_MOTOR"))
  (shadow 'GetPosition (find-package "MULTI_MOTOR")))
(unless (find-package "MULTI_MOTOR::GETPOSITION")
  (make-package "MULTI_MOTOR::GETPOSITION"))
(unless (find-package "MULTI_MOTOR::GETPOSITIONREQUEST")
  (make-package "MULTI_MOTOR::GETPOSITIONREQUEST"))
(unless (find-package "MULTI_MOTOR::GETPOSITIONRESPONSE")
  (make-package "MULTI_MOTOR::GETPOSITIONRESPONSE"))

(in-package "ROS")





(defclass multi_motor::GetPositionRequest
  :super ros::object
  :slots (_id ))

(defmethod multi_motor::GetPositionRequest
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

(defclass multi_motor::GetPositionResponse
  :super ros::object
  :slots (_position ))

(defmethod multi_motor::GetPositionResponse
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

(defclass multi_motor::GetPosition
  :super ros::object
  :slots ())

(setf (get multi_motor::GetPosition :md5sum-) "fa82be1deaeed2877bd58e858d4dcf23")
(setf (get multi_motor::GetPosition :datatype-) "multi_motor/GetPosition")
(setf (get multi_motor::GetPosition :request) multi_motor::GetPositionRequest)
(setf (get multi_motor::GetPosition :response) multi_motor::GetPositionResponse)

(defmethod multi_motor::GetPositionRequest
  (:response () (instance multi_motor::GetPositionResponse :init)))

(setf (get multi_motor::GetPositionRequest :md5sum-) "fa82be1deaeed2877bd58e858d4dcf23")
(setf (get multi_motor::GetPositionRequest :datatype-) "multi_motor/GetPositionRequest")
(setf (get multi_motor::GetPositionRequest :definition-)
      "uint8 id
---
uint16 position

")

(setf (get multi_motor::GetPositionResponse :md5sum-) "fa82be1deaeed2877bd58e858d4dcf23")
(setf (get multi_motor::GetPositionResponse :datatype-) "multi_motor/GetPositionResponse")
(setf (get multi_motor::GetPositionResponse :definition-)
      "uint8 id
---
uint16 position

")



(provide :multi_motor/GetPosition "fa82be1deaeed2877bd58e858d4dcf23")


