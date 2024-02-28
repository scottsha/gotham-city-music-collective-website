import requests
from wordpress_credentials import wordpress_username, wordpress_password


kWORDPRESS_URL ='https://gothamcitymusic.org'
kWORDPRESS_PAGES = kWORDPRESS_URL + '/wp-json/wp/v2/pages'


def hurl_to_wordpress_site(page_title_to_check: str, page_content: str):
    wordpress_api_url = kWORDPRESS_URL

    # Check if the page already exists by its title
    # page_exists = False
    # page_id = None

    # Make a GET request to list existing pages
    pages_response = requests.get(
        wordpress_api_url,
        auth=(wordpress_username, wordpress_password)
    )

    # if pages_response.status_code == 200:
    #     existing_pages = pages_response.json()
    #     for page in existing_pages:
    #         if page['title']['rendered'] == page_title_to_check:
    #             page_exists = True
    #             print("Overwriting existing page")
    #             page_id = page['id']
    #             break

    # Create a new page or update the existing page using the WordPress REST API
    page_data = {
        'title': page_title_to_check,
        'content': page_content,
        'template': 'performance_program'  # Replace with the name of your custom template file
    }

    if False:
        # Update the existing page
        update_response = requests.put(
            f'{wordpress_api_url}/{page_id}',
            json=page_data,
            auth=(wordpress_username, wordpress_password)
        )

        if update_response.status_code == 200:
            print(f"Page updated successfully. Page ID: {page_id}")
        else:
            print(f"Failed to update the page. Status code: {update_response.status_code}")
            print(update_response.text)
    else:
        # Create a new page
        create_response = requests.post(
            wordpress_api_url,
            json=page_data,
            auth=(wordpress_username, wordpress_password)
        )

        if create_response.status_code == 201:
            print(f"Page created successfully. Page ID: {create_response.json()['id']}")
        else:
            print(f"Failed to create the page. Status code: {create_response.status_code}")
            print(create_response.text)