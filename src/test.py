import facebook

graph = facebook.GraphAPI(access_token='CAACEdEose0cBAOD6Qu8xjCLjUVcHMj7YDCHYOiMK2ZBCpf8ttJebJ2MXZBd11MkZAwiCjTZArVjMa8AtqCqQuYM2RxJvRcOB3fJZB5OYzSZA64qKuMAAMbkPx29KXbVfmPABWasZB3mfYMnblAbqLJPHkMhNJ8YsJwmc9Ohjrb3ZBOAtGUEKMOo67A5LQNuHhyYZD')

print graph.get_object(id="374496042657616")
print graph.get_object(id="http://google.com")