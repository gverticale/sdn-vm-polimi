#!/bin/bash

# Detect the OS
case "$(uname -s)" in
   Darwin)
      echo "Detected macOS"
      export DISPLAY_ENV="host.docker.internal:0"
      export X11_VOLUME="/tmp/.X11-unix:/tmp/.X11-unix:rw"
      ;;

   Linux)
      echo "Detected Linux"
      export DISPLAY_ENV="${DISPLAY}"
      export X11_VOLUME="/tmp/.X11-unix:/tmp/.X11-unix"
      ;;

   CYGWIN*|MINGW32*|MSYS*|MINGW*)
      echo "Detected Windows"
      export DISPLAY_ENV="${DISPLAY}"
      export X11_VOLUME="/tmp/.X11-unix:/tmp/.X11-unix"
      ;;
esac