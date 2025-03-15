
# MASTERBLOG API

## Description

Blog API is a simple and efficient RESTful API for managing blog posts. It allows users to create, read, sort, update, and delete posts easily. Each post includes a title, content, author, and a date along with a unique ID. The API supports search functionality to filter posts by keywords. Designed for seamless integration, it provides a reliable way to manage blog content dynamically. 🚀

### Backend 🔧💾

The API is built with Flask and uses Jinja2 for templating. It provides __RESTful__ endpoints to __create (POST)__, __read (GET)__, __update (PUT)__, and __delete (DELETE)__ blog posts. The API supports search and sorting functionality and dynamic content rendering via Jinja2. Designed for easy integration, it ensures efficient blog management with a lightweight and scalable backend.


### Frontend 🎨🖥️ 

The Blog Frontend is a dynamic and responsive web interface built with HTML, CSS, and JavaScript. It interacts with the Flask-powered Blog API to display, create, update, delete, and search blog posts. The UI features a clean design, modal-based editing, and real-time updates using fetch API. Styled with modern CSS, it ensures a smooth user experience with intuitive navigation.

## How to use 🧭

First, please make sure to install all requirements needed via 

```pip
pip install -r requirements.txt
```

Then, with the use of Flask-CORS (Cross-Origin Resource Sharing), make sure that the __backend_app.py__ runs on port:5002. 
```python
python backend/backend_app.py
```
Now the API Flask app is running on http://127.0.0.1:5002 and can be accessed via Postman or your own script, for example. For a more detailed documentation, please refer to the swagger docs on http://127.0.0.1:5002/api/docs.  <br> To use the frontend web interface, please run __frontend_app.py__ on port:5001 at the same time as the API Flask app and go visit http://127.0.0.1:5001 to interact with my beautiful interface, where you can do most of the functions already intuitively, such as read, add, delete, update and search by title and content. The service of sorting and searching by date and suthor are not implemented, yet - but we'll get there one day. 
```python
python frontend/frontend_app.py
```

## Other things

__Tried my API?__ <br> I'd love to hear your feedback!   I'm still at the start of my programming journey, so any thoughts or suggestions would mean a lot. Or if you encounter any bugs or unexpected behaviour which I haven't mentioned in my swagger docs, feel free to give me a hint!
<br>__Thanks!__

## 🤙🏼
