#!/bin/bash

# Runs Neural doodle to create a doodle from provided content and style images
# Neural doodle can not run in detached mode so there is no way to have a container in background
docker run -v $(pwd)/samples:/nd/samples -v $(pwd)/frames:/nd/frames -it neural-doodle-cc-19 --style samples/style.png --content samples/face.png --output samples/result.png --device=cuda* --phases=4 --iterations=80