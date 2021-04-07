#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/omkar/KTH-Neuro-Computing-Systems/Multi_Motor/src/dynamixel_sdk"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/omkar/KTH-Neuro-Computing-Systems/Multi_Motor/install/lib/python3/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/omkar/KTH-Neuro-Computing-Systems/Multi_Motor/install/lib/python3/dist-packages:/home/omkar/KTH-Neuro-Computing-Systems/Multi_Motor/build/lib/python3/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/omkar/KTH-Neuro-Computing-Systems/Multi_Motor/build" \
    "/usr/bin/python3" \
    "/home/omkar/KTH-Neuro-Computing-Systems/Multi_Motor/src/dynamixel_sdk/setup.py" \
     \
    build --build-base "/home/omkar/KTH-Neuro-Computing-Systems/Multi_Motor/build/dynamixel_sdk" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/omkar/KTH-Neuro-Computing-Systems/Multi_Motor/install" --install-scripts="/home/omkar/KTH-Neuro-Computing-Systems/Multi_Motor/install/bin"