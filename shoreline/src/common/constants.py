class GenericConstants:
    # Functional
    AUTHSECRET = 'shoreline-super+secret'
    JWT_EXPIRATION_TIME = 3600  # in seconds

    # Generic
    MESSAGE = 'Message'
    FAULTSTRING = 'faultstring'
    MIMETYPE = 'application/json'
    
    # LOGs
    FAILED_TO_FETCH_DEVICE = 'Failed to Fetch device data'
    FAILED_TO_CREATE_DEVICE = 'Failed to create new device'
    FAILED_TO_UPDATE_DEVICE = 'Failed to update device'
    FAILED_TO_FETCH_SENSOR = 'Failed to Fetch sensor data'
    FAILED_TO_UPDATE_SENSOR = 'Failed to update sensor'
    INVALID_DEVICE_ID = 'Invalid device ID'
    INVALID_SENSOR_TYPE = 'Invalid sensor type'
    INVALID_TIMESTAMP = 'Invalid timestamp. Allowed format "%d/%m/%Y %H:%M:%S"'
    MISSING_TIME_INTERVAL = 'Missing time interval for sensor data. ' \
                            '"start" and "end" required.'
    DEVICE_UPDATED = 'Device data updated successfully'
    SENSOR_UPDATED = 'Sensor data updated successfully'
    DATA_NOT_FOUND = 'Data NOT found for provided time interval. ' \
                     'Alternatively, You can query without timestamps to get ' \
                     'sensor data'
