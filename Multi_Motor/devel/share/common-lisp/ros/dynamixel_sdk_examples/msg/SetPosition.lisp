; Auto-generated. Do not edit!


(cl:in-package dynamixel_sdk_examples-msg)


;//! \htmlinclude SetPosition.msg.html

(cl:defclass <SetPosition> (roslisp-msg-protocol:ros-message)
  ((id
    :reader id
    :initarg :id
    :type cl:fixnum
    :initform 0)
   (position
    :reader position
    :initarg :position
    :type cl:fixnum
    :initform 0)
   (speed
    :reader speed
    :initarg :speed
    :type cl:fixnum
    :initform 0)
   (torque
    :reader torque
    :initarg :torque
    :type cl:fixnum
    :initform 0))
)

(cl:defclass SetPosition (<SetPosition>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <SetPosition>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'SetPosition)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name dynamixel_sdk_examples-msg:<SetPosition> is deprecated: use dynamixel_sdk_examples-msg:SetPosition instead.")))

(cl:ensure-generic-function 'id-val :lambda-list '(m))
(cl:defmethod id-val ((m <SetPosition>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader dynamixel_sdk_examples-msg:id-val is deprecated.  Use dynamixel_sdk_examples-msg:id instead.")
  (id m))

(cl:ensure-generic-function 'position-val :lambda-list '(m))
(cl:defmethod position-val ((m <SetPosition>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader dynamixel_sdk_examples-msg:position-val is deprecated.  Use dynamixel_sdk_examples-msg:position instead.")
  (position m))

(cl:ensure-generic-function 'speed-val :lambda-list '(m))
(cl:defmethod speed-val ((m <SetPosition>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader dynamixel_sdk_examples-msg:speed-val is deprecated.  Use dynamixel_sdk_examples-msg:speed instead.")
  (speed m))

(cl:ensure-generic-function 'torque-val :lambda-list '(m))
(cl:defmethod torque-val ((m <SetPosition>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader dynamixel_sdk_examples-msg:torque-val is deprecated.  Use dynamixel_sdk_examples-msg:torque instead.")
  (torque m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <SetPosition>) ostream)
  "Serializes a message object of type '<SetPosition>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'id)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'position)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'position)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'speed)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'speed)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'torque)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'torque)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <SetPosition>) istream)
  "Deserializes a message object of type '<SetPosition>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'id)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'position)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'position)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'speed)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'speed)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'torque)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'torque)) (cl:read-byte istream))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<SetPosition>)))
  "Returns string type for a message object of type '<SetPosition>"
  "dynamixel_sdk_examples/SetPosition")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetPosition)))
  "Returns string type for a message object of type 'SetPosition"
  "dynamixel_sdk_examples/SetPosition")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<SetPosition>)))
  "Returns md5sum for a message object of type '<SetPosition>"
  "122d3d32ebb831b360ed3f4fa0e1d17b")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'SetPosition)))
  "Returns md5sum for a message object of type 'SetPosition"
  "122d3d32ebb831b360ed3f4fa0e1d17b")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<SetPosition>)))
  "Returns full string definition for message of type '<SetPosition>"
  (cl:format cl:nil "uint8 id~%uint16 position~%uint16 speed~%uint16 torque~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'SetPosition)))
  "Returns full string definition for message of type 'SetPosition"
  (cl:format cl:nil "uint8 id~%uint16 position~%uint16 speed~%uint16 torque~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <SetPosition>))
  (cl:+ 0
     1
     2
     2
     2
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <SetPosition>))
  "Converts a ROS message object to a list"
  (cl:list 'SetPosition
    (cl:cons ':id (id msg))
    (cl:cons ':position (position msg))
    (cl:cons ':speed (speed msg))
    (cl:cons ':torque (torque msg))
))
