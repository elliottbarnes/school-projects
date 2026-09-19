# Java Networking Exercise

A line-oriented Java client/server exercise by Elliott Barnes. The server accepts one client, exchanges messages terminated with an end-of-response marker, and demonstrates a simple authentication loop before echoing input.

## Build

```sh
javac BetterClient.java Server.java
```

## Run

Set non-sensitive demonstration credentials and start the server:

```sh
SCHOOL_SERVER_USERNAME=demo SCHOOL_SERVER_PASSWORD=change-me java Server
```

The server prints its ephemeral port. In another terminal:

```sh
java BetterClient localhost PORT
```

This is an educational protocol without transport encryption or production authentication. Hardcoded historical demonstration credentials were replaced with environment variables in this curated snapshot.

The source was reviewed during curation, but compilation could not be rerun because a Java runtime was unavailable in the verification environment.
