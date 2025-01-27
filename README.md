# LangChain App

## Setting up the program

1. Install pipx
2. Install poetry `pipx install poetry`
3. Install poetry-plugin-shell `pipx inject poetry-plugin-shell`
4. Install the poetry dependencies `poetry install`
5. Create a `.env` file and copy the .env.example to .env `cp .env.example .env`
6. Replace the values of the variables in the .env file with valid values

## Running the program

1. Run in development on metal `poetry run fastapi dev`
2. Run in development docker

    i. Create a docker image `docker build -t "langchain-app:latest" .`

    ii. Run the docker container from the image `docker run -d --rm -p 8000:8000 --name langchain-app --env-file .env langchain-app:latest`
