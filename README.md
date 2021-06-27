# kaizen-backend
Backend for Kaizen that helps you to provide a productive environment while studying vifdeos on Youtube.

This code currently exposes the following endpoints:
 - `/api/register/`
 - `/api/login/`
 
 To test **register** api:
 - ```bash
      curl -X POST "http://localhost:8000/api/register/?username={USERNAME}&password={PASSWORD}" -H  "accept: application/json" -d ""```
 
 To test **login** api:
 - ```bash
    curl -X POST "http://localhost:8000/api/login/?username={USERNAME}&password={PASSWORD}" -H  "accept: application/json" -d ""```

Or simply go to `/api/docs` and test the APIs using swagger :)
