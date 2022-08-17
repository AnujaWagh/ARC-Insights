from flask import Flask, Response, stream_with_context
import time
import uuid
import random
from faker import Faker
fake = Faker()
APP = Flask(__name__)


@APP.route("/very_large_request/<int:rowcount>", methods=["GET"])
def get_large_request(rowcount):
    """retunrs N rows of data"""
    def f():
        """The generator of mock data"""
        for _i in range(rowcount):
            time.sleep(.01)
            # txid = uuid.uuid4()
            # print(txid)
            id = random.randint(1, 100)
            print(id)
            firstname = fake.first_name()
            print(firstname)
            lastname = fake.last_name()
            print(lastname)
            # email = "{firstname}.{lastname}@{fake.domain_name()".format(firstname=firstname, lastname=lastname, fake=Faker())
            email = f"{firstname}.{lastname}@{fake.domain_name()}"
            print(email)
            # yield "{} {} {}\n".format(id, firstname, lastname, email)
            yield f"('{id}', '{firstname}', '{lastname}',{email})\n"
           

    return Response(stream_with_context(f()))

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5000
    APP.run(host=host, port=port)
    APP.run(debug=True)