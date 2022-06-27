# Shoreline Assignment

- Clone source code using command
    `git clone  `

- Install the required dependencies
    1. To install Python version>=3.6, use official instructions for latest bundles here:
    `https://www.python.org/downloads/`

    2. Install all the packages required for this server:
    `pip3 install -r requirements.txt`

    3. To install MongoDB community server, use official instructions for latest bundles here:
     `https://www.mongodb.com/docs/manual/administration/install-community/`

- Starting the server will make available swagger client available at 'localhost:5000'.
    To start server use:
    `python3 run.py`

- Quick NOTES about the server working:
    1. `Try Out` and then `Execute` the `/Auth/login` request to generate the JWT token.
    2. The JWT token is valid for `1Hr` Only.
    3. `Try Out` and then `Execute` the `POST` request for Device to create the device entry in the DB.
    4. `Try Out` and then `Execute` the `PUT` request for Sensor to push data to the device created above.
    5. The server follows the `Size-base NOSQL bucket` model to store the time-based data.
    6. The sensor data can be pushed only when the time frame(start and end) for that data is defined.

- Debug service
    1. To check logs of:
        `tail -f service_logs/debug.log`

- NOTE: The
    1. If set to `Azure` the behaviour of docker container will be of `Azure AD Sensor` type.
    2. If set to `OneLogin` the behaviour of docker container will be of `OneLogin Sensor` type.
