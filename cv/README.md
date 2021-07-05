create a file `/etc/udev/rules.d/99-camera.rules` with contents `SUBSYSTEM=="vchiq",MODE="0666"`

docker run
`docker run -it --privileged --device /dev/vchiq -v /opt/vc:/opt/vc --env LD_LIBRARY_PATH=/opt/vc/lib cv`

run with code mounted as volume
`docker run -it --privileged --device /dev/vchiq -v /home/pi/docker-dobby/cv/data:/data -v /opt/vc:/opt/vc -v /home/pi/docker-dobby/cv/app:/app --env LD_LIBRARY_PATH=/opt/vc/lib cv`