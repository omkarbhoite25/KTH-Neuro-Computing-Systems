// Generated by gencpp from file single_motor/Control.msg
// DO NOT EDIT!


#ifndef SINGLE_MOTOR_MESSAGE_CONTROL_H
#define SINGLE_MOTOR_MESSAGE_CONTROL_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace single_motor
{
template <class ContainerAllocator>
struct Control_
{
  typedef Control_<ContainerAllocator> Type;

  Control_()
    : id(0)
    , position(0)
    , speed(0)  {
    }
  Control_(const ContainerAllocator& _alloc)
    : id(0)
    , position(0)
    , speed(0)  {
  (void)_alloc;
    }



   typedef uint8_t _id_type;
  _id_type id;

   typedef uint16_t _position_type;
  _position_type position;

   typedef uint16_t _speed_type;
  _speed_type speed;





  typedef boost::shared_ptr< ::single_motor::Control_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::single_motor::Control_<ContainerAllocator> const> ConstPtr;

}; // struct Control_

typedef ::single_motor::Control_<std::allocator<void> > Control;

typedef boost::shared_ptr< ::single_motor::Control > ControlPtr;
typedef boost::shared_ptr< ::single_motor::Control const> ControlConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::single_motor::Control_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::single_motor::Control_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::single_motor::Control_<ContainerAllocator1> & lhs, const ::single_motor::Control_<ContainerAllocator2> & rhs)
{
  return lhs.id == rhs.id &&
    lhs.position == rhs.position &&
    lhs.speed == rhs.speed;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::single_motor::Control_<ContainerAllocator1> & lhs, const ::single_motor::Control_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace single_motor

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::single_motor::Control_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::single_motor::Control_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::single_motor::Control_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::single_motor::Control_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::single_motor::Control_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::single_motor::Control_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::single_motor::Control_<ContainerAllocator> >
{
  static const char* value()
  {
    return "4f46a6d27437d2790ff5c5f79fd2e3c6";
  }

  static const char* value(const ::single_motor::Control_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x4f46a6d27437d279ULL;
  static const uint64_t static_value2 = 0x0ff5c5f79fd2e3c6ULL;
};

template<class ContainerAllocator>
struct DataType< ::single_motor::Control_<ContainerAllocator> >
{
  static const char* value()
  {
    return "single_motor/Control";
  }

  static const char* value(const ::single_motor::Control_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::single_motor::Control_<ContainerAllocator> >
{
  static const char* value()
  {
    return "uint8 id\n"
"uint16 position\n"
"uint16 speed\n"
;
  }

  static const char* value(const ::single_motor::Control_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::single_motor::Control_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.id);
      stream.next(m.position);
      stream.next(m.speed);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct Control_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::single_motor::Control_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::single_motor::Control_<ContainerAllocator>& v)
  {
    s << indent << "id: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.id);
    s << indent << "position: ";
    Printer<uint16_t>::stream(s, indent + "  ", v.position);
    s << indent << "speed: ";
    Printer<uint16_t>::stream(s, indent + "  ", v.speed);
  }
};

} // namespace message_operations
} // namespace ros

#endif // SINGLE_MOTOR_MESSAGE_CONTROL_H