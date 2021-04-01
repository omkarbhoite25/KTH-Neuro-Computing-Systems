;; Auto-generated. Do not edit!


(when (boundp 'dynamixel_sdk_examples::SetPosition)
  (if (not (find-package "DYNAMIXEL_SDK_EXAMPLES"))
    (make-package "DYNAMIXEL_SDK_EXAMPLES"))
  (shadow 'SetPosition (find-package "DYNAMIXEL_SDK_EXAMPLES")))
(unless (find-package "DYNAMIXEL_SDK_EXAMPLES::SETPOSITION")
  (make-package "DYNAMIXEL_SDK_EXAMPLES::SETPOSITION"))

(in-package "ROS")
;;//! \htmlinclude SetPosition.msg.html


(defclass dynamixel_sdk_examples::SetPosition
  :super ros::object
  :slots (_id _position _speed _torque ))

(defmethod dynamixel_sdk_examples::SetPosition
  (:init
   (&key
    ((:id __id) 0)
    ((:position __position) 0)
    ((:speed __speed) 0)
    ((:torque __torque) 0)
    )
   (send-super :init)
   (setq _id (round __id))
   (setq _position (round __position))
   (setq _speed (round __speed))
   (setq _torque (round __torque))
   self)
  (:id
   (&optional __id)
   (if __id (setq _id __id)) _id)
  (:position
   (&optional __position)
   (if __position (setq _position __position)) _position)
  (:speed
   (&optional __speed)
   (if __speed (setq _speed __speed)) _speed)
  (:torque
   (&optional __torque)
   (if __torque (setq _torque __torque)) _torque)
  (:serialization-length
   ()
   (+
    ;; uint8 _id
    1
    ;; uint16 _position
    2
    ;; uint16 _speed
    2
    ;; uint16 _torque
    2
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint8 _id
       (write-byte _id s)
     ;; uint16 _position
       (write-word _position s)
     ;; uint16 _speed
       (write-word _speed s)
     ;; uint16 _torque
       (write-word _torque s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint8 _id
     (setq _id (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; uint16 _position
     (setq _position (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;; uint16 _speed
     (setq _speed (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;; uint16 _torque
     (setq _torque (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;;
   self)
  )

(setf (get dynamixel_sdk_examples::SetPosition :md5sum-) "122d3d32ebb831b360ed3f4fa0e1d17b")
(setf (get dynamixel_sdk_examples::SetPosition :datatype-) "dynamixel_sdk_examples/SetPosition")
(setf (get dynamixel_sdk_examples::SetPosition :definition-)
      "uint8 id
uint16 position
uint16 speed
uint16 torque

")



(provide :dynamixel_sdk_examples/SetPosition "122d3d32ebb831b360ed3f4fa0e1d17b")


