
(cl:in-package :asdf)

(defsystem "dynamixel_sdk_examples-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "SetLed" :depends-on ("_package_SetLed"))
    (:file "_package_SetLed" :depends-on ("_package"))
    (:file "SetPosition" :depends-on ("_package_SetPosition"))
    (:file "_package_SetPosition" :depends-on ("_package"))
  ))