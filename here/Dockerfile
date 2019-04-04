FROM alpine:3.7
RUN apk update
RUN apk add  python
RUN apk add py-pip

RUN pip install Flask
RUN pip install requests
RUN pip install --upgrade pip
WORKDIR /app
COPY . /app
ENV TEAM_ID=CC_123_456_789
EXPOSE 80
CMD ["python", "test.py"]
