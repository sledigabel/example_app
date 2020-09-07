from os import environ
from redis import Redis, RedisError
from flask import Flask

app = Flask(__name__)

DEFAULT_REDIS_SERVER = "localhost"
DEFAULT_REDIS_PORT = "6379"
global redis, local_count


@app.route("/")
def hello():
    global local_count
    try:
        local_count += 1
        count = redis.get("global_connections_count")
        count = 1 if count is None else int(count) + 1
        redis.incr("global_connections_count")
    except RedisError as e:
        return "Redis error: {}".format(e), 500

    return "<html><body>HOST: {}\n<br/>\n\
        Count: {}\n<br/>\n\
        Number of apps: {}\n<br>\n\
        Page visited: {} times\n<br/>\
        <img src='https://media.giphy.com/media/u18KbOWs65HFK/giphy.gif'/>\
        <br/></body></html>".format(
        environ.get("HOSTNAME", "hostname"),
        local_count,
        len(redis.client_list()),
        count,
    )


@app.route("/healthcheck")
def healthcheck():
    try:
        redis.ping()
    except RedisError as e:
        return f"App cannot connect to Redis:{e}", 500
    return "App is healthy"


if __name__ == "__main__":

    REDIS_SERVER = environ.get("REDIS_SERVER", DEFAULT_REDIS_SERVER)
    REDIS_PORT = environ.get("REDIS_PORT", DEFAULT_REDIS_PORT)

    SERVER = "0.0.0.0"
    PORT = environ.get("PORT", 5000)
    redis = Redis(host=REDIS_SERVER, port=REDIS_PORT)

    local_count = 0
    # (re)setting redis values
    # redis.set('global_connections_count', 0)

    if not redis.ping():
        print(
            "Could not connect to REDIS @ {}:{}".format(
                REDIS_SERVER, REDIS_PORT
            )
        )
    app.run(host=SERVER, port=PORT)
