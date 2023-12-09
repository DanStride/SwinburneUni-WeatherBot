import requests


class GetRequests:
    # Create a class method to handle requests, taking the url as an argument
    def make_request(self, url):
        # Make a get request using the url and put the result into the response object
        response = requests.get(url=url)

        # If successful print headers and return response object
        if response.status_code == 200:
            print(response.headers)
            return response
        # Otherwise print the status code
        else:
            print(response.status_code)
