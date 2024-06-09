## Flask Application 

Project Structure
```
your_project/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── db.py
│   ├── openai_client.py
│   ├── utils.py
├── role_info.txt
├── .env
├── config.py
├── app.py
├── environment.yml
```

This is a flask application design to handle chatbot api calls and responses.
Before running the application, you need to install the required packages by running the following command:

```bash
conda env create -f environment.yml
conda activate flask
```

To run the application, run the following command:

```bash
python app.py
```

