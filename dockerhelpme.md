1. Stop the Old Container

First, stop the container that is currently running.
Bash

docker stop simplex_bot

2. Remove the Stopped Container

Now, remove the old container so you can reuse its name.
Bash

docker rm simplex_bot

3. Rebuild Your Docker Image

This is the key step. Go to your project's root directory (where the Dockerfile is) and run the build command. This creates a new image with your updated code.
Bash

docker build -t simplex_bot_image .

4. Run a New Container

Finally, launch a new container from your newly built image. It will connect to your persistent volume and use your .env file just like before.
Bash

docker run -d --name simplex_bot -v simplex_data:/app/data --env-file ./.env simplex_bot_image

(Note: I've added the -d flag to run it in the background, which is typical for a bot.)

docker run --name simplex_bot -v simplex_data:/app/data --env-file ./.env simplex_bot_image

5.  docker start simplex_bot