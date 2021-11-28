# fast-api-sample
fast api smaple project by jin 


# Requirement
- Running PostgreSQL Docker 
    ```
    docker run -p 5432:5432 --name postgres -e POSTGRES_PASSWORD=1q2w3e4r -d postgres
    ```
  
- Connect PostgreSQL Docker and Run blow query
    ```
    DROP TABLE IF EXISTS links;
    CREATE TABLE links (
          id SERIAL PRIMARY KEY,
          url VARCHAR(255) NOT NULL,
          name VARCHAR(255) NOT NULL,
          description VARCHAR (255),
              last_update DATE
    );
    
    INSERT INTO links (url, name) VALUES('https://www.postgresqltutorial.com','PostgreSQL Tutorial');

    SELECT * FROM links;
    ```
# Run Command
```
$ python main.py
```

# Connect Swagger UI
- http://127.0.0.1:8080/docs

