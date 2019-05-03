#!/bin/bash

# alias doodle="docker run -v $(pwd)/samples:/nd/samples -v $(pwd)/frames:/nd/frames -it neural-doodle-cc-19"
docker run -v $(pwd)/samples:/nd/samples -v $(pwd)/frames:/nd/frames -it neural-doodle-cc-19 --style samples/style.png --content samples/face.png --output samples/result.png --device=cuda* --phases=4 --iterations=80