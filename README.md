# SoundSphere-Server
Welcome to the Soundsphere backend where the shared vinyl/LP collection of James and Connor is stored. This RESTful API is intended to create, update, and manage all things regarding the collection. We draw our vinyl/LP data from the Discogs API. We want to create a shared space for our physical collection to live online so we can share it with friends and family online. Our desire is to create a platform for other people to host their shared collections as well.

# Getting Started
The instructions below will get you up and running to develop the server and make a shared collection of your own!
**INSTALLATION**

Clone the repository locally

`git clone https://github.com/thecodekiddos/SoundSphere-Server.git`

Download [Python3](https://www.python.org/downloads/release/python-370/)

Run the `pip install -r requirements.txt` for dependencies.

Flask will be the RESTful API framework used for this Backend

Before beginning any development activate the virtual environment with the command:
`source venv/bin/activate`
When finished simply use:
`deactivate`

To run the server:
`flask run`

# Development

Create your own virtual environment for the project `virtualenv ~/PATH_TO_MY_PROJECT/venv`

Before beginning any development activate the virtual environment with the command:
`source venv/bin/activate`
When finished simply use:
`deactivate`

When adding additional modules to the project, commit the current state of the packages via: `pip freeze > requirements.txt`

# Deployment
TBD

# Built With
- [Flask](http://flask.pocoo.org): Flask python framework
- [Discogs](https://www.discogs.com/developers/#): Discogs API

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Authors

* **Connor Sheedy** - *Initial work*
* **James Viall** - *Initial work*
