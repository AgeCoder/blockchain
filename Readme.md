#### Command Reference

** Add your subscribe_key and publish_key in backend/pubsub.py before you start**

**Activate the virtual environment**
```
blockchain-env/bin/activate
```

**Install all packages**
```
pip install -r requirements.txt
```

**Run the tests**

Make sure to activate the virtual environment.

```
python -m pytest backend/tests
```

**Run the application and API**

Make sure to activate the virtual environment.

```
python -m backend.app
```

**Run a peer instance**

Make sure to activate the virtual environment.

```
export PEER=True && python3 -m backend.app
```

**Run the frontend**

In the frontend directory:
```
npm run start
```

**Seed the backend with data**

Make sure to activate the virtual environment.

```
export SEED_DATA=True && python3 -m backend.app