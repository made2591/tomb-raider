## Tomb Raider
Thanks to [ezand](https://github.com/ezand/spring-boot-gradle-docker-boilerplate)

### Usage:

```bash
./gradlew buildDocker
docker run -d -p 8080:8080 spring-boot-gradle-docker-boilerplate
```
Then go to [http://localhost:8080](http://localhost:8080)

### Places to rename stuff:
* README.md
* settings.gradle
* src/main/java
* src/main/docker/Dockerfile
* src/main/resources/logback.xml
