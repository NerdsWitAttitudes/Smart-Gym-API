# Smart-Gym-API
REST API for the N.W.A Smart Gym

Getting Started
---------------

Either use your own brain or follow the following guidelines:

- `mkdir -p ~/env`
- `virtualenv -p python3 ~/env/smart_gym_api` or whatever you want to call your virtual environment
- `mkdir -p ~/projects`
- `git clone git@github.com:NerdsWitAttitudes/Smart-Gym-API.git ~/projects/smart-gym-api`
- `source ~/env/smart_gym_api/bin/activate`
- `pip install -e ~/projects/smart-gym-api`
- `cp ~/projects/smart-gym-api/settings.ini.dist ~/projects/smart-gym-api/{yourname}.ini`

Fill in the .ini file you just made. Ask one of your team members for help.

Finally:
- `pserve --reload ~/projects/smart-gym-api/{yourname}.ini`
