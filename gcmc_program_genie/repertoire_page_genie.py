import requests
import json
from wordpress_credentials import wordpress_password, wordpress_username
import warnings


def check_song_entry(song: dict):
    expected_keys = [
        "id",
        "title",
        "composer",
        "arranger",
        "description",
        "lyrics",
        "lyrics_title",
        "lyrics_cite",
        "lyrics_by",
        "source",
    ]
    for key in song.keys():
        if key not in expected_keys:
            warnings.warn("Unexpected key: {}".format(key))


class SongBlockGenerator:
    def __init__(self, song: dict):
        check_song_entry(song)
        self.song = song
        self.lines = []
        self.div_count = 0
        self.make_lines()

    def get_block_as_str(self) -> str:
        return "\n".join(self.lines)

    def make_lines(self):
        self.make_wrapper()
        self.make_title()
        self.make_authors()
        self.make_description()
        self.make_lyrics()
        while self.div_count > 0:
            self.lines.append("</div>")
            self.div_count += -1

    def make_wrapper(self):
        blob = "<div class=\"p-block-column is-vertically-aligned-top is-layout-flow wp-block-column-is-layout-flow\">"
        self.lines.append(blob)
        self.div_count += 1

    def make_title(self):
        id = self.song["id"]
        title = self.song["title"]
        line = "<div><h4 class=\"wp-block-heading has-text-align-center\" id=\"{}\">{}</h4></div>".format(id, title)
        self.lines.append(line)

    def make_authors(self):
        blerb_list = []
        composer = self.song.get("composer", "")
        if composer:
            blerb_list.append("by {}.".format(composer))
        arranger = self.song.get("arranger", "")
        if arranger:
            blerb_list.append("Arranged by {}.".format(arranger))
        lyracist = self.song.get("lyrics_by", "")
        if lyracist:
            blerb_list.append("Lyrics by {}.".format(lyracist))
        blerb = " ".join(blerb_list)
        line = "<div><h5 class=\"wp-block-heading\">{}</h5></div>".format(blerb)
        self.lines.append(line)

    def make_description(self):
        description = self.song["description"]
        line = "<p>{}</p>".format(description)
        self.lines.append(line)

    def make_lyrics(self):
        lyrics = self.song.get("lyrics", "")
        if not lyrics:
            return
        line = "<blockquote class=\"wp-block-quote has-small-font-size\">"
        l_title = self.song.get("lyric_title", "")
        if l_title:
            line += "<p><strong><strong>{}</strong></strong></p>".format(l_title)
        line += "<p>{}</p>".format(lyrics)
        l_cite = self.song.get("lyrics_cite", "")
        if l_cite:
            line += "<cite>—{}</cite>".format(l_cite)
        line += "</blockquote>"
        self.lines.append(line)


class RepertoirePageGenerator:
    songlist_div_class = "<div class=\"wp-block-group is-vertical is-layout-flex wp-container-48 wp-block-group-is-layout-flex\" style=\"border-style:none;border-width:0px;padding-top:var(--wp--preset--spacing--30);padding-right:var(--wp--preset--spacing--30);padding-bottom:var(--wp--preset--spacing--30);padding-left:var(--wp--preset--spacing--30)\">"
    kREPERTOIRE_DATA_PATH = "repertoire_data.json"
    def __init__(
            self,
            program_info: dict=None
    ):
        with open(self.kREPERTOIRE_DATA_PATH, 'r') as file:
            self.repertoire_data = json.load(file)
        self.repertoire_data = sorted(self.repertoire_data, key=lambda x: x["id"])
        self.content = []

    def generate(self):
        self.generate_rep_intro()
        self.generate_song_contents()
        print("Page generated.")

    def generate_performance_index(self):
        pass

    def generate_title(self):
        pass

    def generate_rep_intro(self):
        div_0 = "<div class=\"entry-content wp-block-post-content is-layout-flow wp-block-post-content-is-layout-flow\">"
        self.content.append(div_0)
        div_1 = "<div class=\"wp-block-group has-global-padding is-layout-constrained wp-block-group-is-layout-constrained\">"
        self.content.append(div_1)
        div_2 = "<div class=\"wp-block-group is-layout-flow wp-block-group-is-layout-flow\">"
        self.content.append(div_2)
        title = "Choral Repertoire"
        h_title = "<h1 class=\"wp-block-heading has-text-align-center\">{}</h1>".format(title)
        self.content.append(h_title)
        for foo in range(3):
            self.content.append("</div>")

    def generate_song_contents(self):
        self.content.append(self.songlist_div_class)
        for song in self.repertoire_data:
            gener = SongBlockGenerator(song)
            self.content += gener.lines
        self.content.append("</div>")

    def get_content_str(self) -> str:
        return "\n".join(self.content)


class ProgramPageGenerator:
    kWORDPRESS_API_URL = 'https://gothamcitymusic.org/wp-json/wp/v2/pages'
    def __int__(
        self,
        page_name: str,
    ):
        self.name = page_name




if __name__ == "__main__":
    wordpress_api_url = 'https://gothamcitymusic.org/wp-json/wp/v2/pages'
    gener = RepertoirePageGenerator("repertoire_data.json")
    page_content = gener.get_content_str()

    # Check if the page already exists by its title
    page_title_to_check = 'Repertoire'
    page_exists = False
    page_id = None

    # Make a GET request to list existing pages
    pages_response = requests.get(
        wordpress_api_url,
        auth=(wordpress_username, wordpress_password)
    )

    if pages_response.status_code == 200:
        existing_pages = pages_response.json()
        for page in existing_pages:
            if page['title']['rendered'] == page_title_to_check:
                page_exists = True
                page_id = page['id']
                break

    # Create a new page or update the existing page using the WordPress REST API
    page_data = {
        'title': page_title_to_check,
        'content': page_content,
        'template': 'performance_program'  # Replace with the name of your custom template file
    }

    if page_exists:
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
