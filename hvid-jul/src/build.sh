docker build --tag hvidjul .
docker run -it -d --rm --name hvidjul hvidjul

# Copy out relevant sources
docker container cp hvidjul:/lib/x86_64-linux-gnu/libc.so.6 extracted/libc.so.6
docker container cp hvidjul:/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2 extracted/ld-linux-x86-64.so.2
docker container cp hvidjul:/interpret extracted/interpret
docker container cp hvidjul:/interpret-debug extracted/interpret-debug

docker stop hvidjul
