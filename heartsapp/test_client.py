from get_answer.get_answer_pb2_grpc import GetAnswerStub
from get_answer.get_answer_pb2 import SearchRequest
import grpc

# initialize the stub
channel = grpc.insecure_channel('127.0.0.1:8080')
stub = GetAnswerStub(channel)

QUERY='What is the part an abhyasi need to play to compel Master to push him on the spiritual path?'
# QUERY="What is Maxim 3?"
request = SearchRequest(query=QUERY)
response = stub.Search(request)
print(response)
