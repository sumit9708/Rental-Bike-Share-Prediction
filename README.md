# Rental-Bike-Share-Prediction
Bike sharing system are a new generation of traditional bike rentals where the whole process from membership , rental and return back has become automatic.the goal here is to predict the total number of bikes available. It takes some input feature such as month name,days name , season name .. etc. In this project i have performed data cleaning and handled missing values,created best fit model using GridSearchCV, Linear regression and Random forest regressor.

### Agenda 
- Create a flask app
- Write a Docker file for flask app
- create github actions for CI/CD 
- Heroku app for flask deployment 
- Create structure for ML Project
- Build Machine learning pipeline

### Software and account Requirement.

1. [Github Account](https://github.com)
2. [Heroku Account](https://dashboard.heroku.com/login)
3. [VS Code IDE](https://code.visualstudio.com/download)
4. [GIT cli](https://git-scm.com/downloads)
5. [GIT Documentation](https://git-scm.com/docs/gittutorial)

Creating conda environment
```
conda create -p venv python==3.7 -y
```
```
conda activate venv/
```
OR 
```
conda activate venv
```

```
pip install -r requirements.txt
```

To Add files to git
```
git add .
```

OR
```
git add <file_name>
```

> Note: To ignore file or folder from git we can write name of file/folder in .gitignore file

To check the git status 
```
git status
```
To check all version maintained by git
```
git log
```

To create version/commit all changes by git
```
git commit -m "message"
```

To send version/changes to github
```
git push origin main
```

To check remote url 
```
git remote -v
```

To setup CI/CD pipeline in heroku we need 3 information
1. HEROKU_EMAIL = sumitbhagat472@gmail.com
2. HEROKU_API_KEY = f57***ef-c608-485a-8**9-1a6034*****
3. HEROKU_APP_NAME = bike-share-ml

BUILD DOCKER IMAGE
```
docker build -t <image_name>:<tagname> .
```
> Note: Image name for docker must be lowercase


To list docker image
```
docker images
```

Run docker image
```
docker run -p 5000:5000 -e PORT=5000 f8c749e73678
```

To check running container in docker
```
docker ps
```

Tos stop docker conatiner
```
docker stop <container_id>
```
```
For Jupyter Notebook to work in vs code
```
pip install ipykernel -U --user --force-reinstall
```
To read YAML file
```
pip install pyYAML
```