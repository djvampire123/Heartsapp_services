# heartsapp_services
Internal GRPC services providing NLP capabilities to heartsapp

## Services

**Get Answer Service**

**Usage**

1. ```sudo docker build ./```, Suppose you get image id -> X
2. ```sudo docker run -p 8080:8080 X``` , In the first run it will download the model
3. This is followed by the prompt that the GetAnswer Services has started, you will also
get container id -> Y
4. Run ```sudo docker stop Y```
5. In order to save the state of the container commit the changes otherwise we would have to
download the model on every restart. Save the changes by running ->
```sudo docker commit -a my_image:latest Y```
6. Now you can run the new image -> ```sudo docker run -p 8080:8080 my_image:latest```
7. To test the api run - ```python heartsapp/test_client```
