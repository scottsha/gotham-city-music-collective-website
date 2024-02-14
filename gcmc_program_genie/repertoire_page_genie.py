import requests
import json
from wordpress_credentials import wordpress_password, wordpress_username
import warnings
import os


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
        "showcase_only",
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
        description = self.song.get("description", "")
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

kREPERTOIRE_DATA_PATH = "repertoire_data.json"

def get_repertoire_data(

) -> dict:
    with open(kREPERTOIRE_DATA_PATH, 'r') as file:
        repertoire_data = json.load(file)
    repertoire_data = sorted(repertoire_data, key=lambda x: x["id"])
    repertoire_dict = {song["id"] : song for song in repertoire_data}
    return repertoire_dict

class SongAboutsGenerator:
    songlist_div_class = "<div class=\"wp-block-group is-vertical is-layout-flex wp-container-48 wp-block-group-is-layout-flex\" style=\"border-style:none;border-width:0px;padding-top:var(--wp--preset--spacing--30);padding-right:var(--wp--preset--spacing--30);padding-bottom:var(--wp--preset--spacing--30);padding-left:var(--wp--preset--spacing--30)\">"

    def __init__(
            self,
            program_info: dict=None
    ):
        self.repertoire_data = get_repertoire_data()

        self.content = []
        self.do_showcases = True
        self.program_info = program_info
        if self.program_info is None:
            self.do_showcases = False

    def generate(self):
        self.generate_rep_intro()
        self.generate_song_contents()
        print("Page generated.")

    def generate_rep_intro(self):
        div_0 = "<div class=\"entry-content wp-block-post-content is-layout-flow wp-block-post-content-is-layout-flow\">"
        self.content.append(div_0)
        div_1 = "<div class=\"wp-block-group has-global-padding is-layout-constrained wp-block-group-is-layout-constrained\">"
        self.content.append(div_1)
        div_2 = "<div class=\"wp-block-group is-layout-flow wp-block-group-is-layout-flow\">"
        self.content.append(div_2)
        # title = "Choral Repertoire"
        # h_title = "<h1 class=\"wp-block-heading has-text-align-center\">{}</h1>".format(title)
        # self.content.append(h_title)
        for foo in range(3):
            self.content.append("</div>")

    def generate_song_contents(self):
        self.content.append(self.songlist_div_class)
        for id, song in self.repertoire_data.items():
            # is_showcase = song.get("showcase_only", False)
            # if (not is_showcase) or self.do_showcases:
            gener = SongBlockGenerator(song)
            self.content += gener.lines
        self.content.append("</div>")

    def get_content_str(self) -> str:
        return "\n".join(self.content)

    def generate_html_str(self) -> str:
        self.generate()
        return self.get_content_str()


class PerformancePageGenereator:
    kPERFORMANCE_TEMPLATE_PATH = "html_blocks/performance_template.html"
    kREPERTOIRE_TEMPLATE_PATH = "html_blocks/repertoir_list_template.html"
    kREPLACE_MAIN_TITLE = "${REPLACE_MAIN_TITLE_BLOCK}"
    kREPLACE_SUBTITLE = "${SUBTITLE_REPLACE}"
    kREPLACE_PROGRAM_LEAFLET_PATH = "${REPLACE_PROGRAM_LEAFLET_PATH}"
    kREPLACE_INDEX_LIST_BLOB = "${REPLACE_INDEX_LIST_BLOB}"
    kREPLACE_SINGERS_BLOB = "${REPLACE_SINGERS_BLOB}"
    kREPLACE_SONG_ABOUTS = "${REPLACE_SONG_ABOUTS}"

    # def get_replace_key(self, field):
    #     return r"{$REPLACE_" + field + r"}"

    def __init__(
        self,
        program_info: dict=None,
        program_leaflet_file_name: str=None
    ):
        self.repertoire = get_repertoire_data()
        self.program_info = program_info
        if self.program_info is None:
            self.program_info = dict()
            self.template_path = self.kREPERTOIRE_TEMPLATE_PATH
        else:
            self.template_path = self.kPERFORMANCE_TEMPLATE_PATH
        with open(self.template_path, "r") as ff:
            self.template = ff.read()
        self.leaflet = program_leaflet_file_name
        self.id = self.program_info.get("id", "repertoire")
        self.url = "gothamcitymusic.org/" + self.id
        # print("Creating page ", self.id)

    def generate_main_title_block(self) -> str:
        title = self.program_info.get("title", "")
        return title

    def generate_subtitle(self) -> str:
        subs = self.program_info.get("subtitle", "")
        sub_str = "\n".join(subs)
        return sub_str

    def generate_program_leaflet_path(self) -> str:
        if self.leaflet is None:
            return ""
        leaf = "https://gothamcitymusic.org/wp-content/uploads/concert_programs/" + self.leaflet
        return leaf

    def make_index_entry(self, song_id: str, song_title: str) -> str:
        entry = '''
        <p class="has-text-align-center">
        <a href="https://gothamcitymusic.org/program#{song_id}"
        data-type="page">{song_title}</a></p>
        '''
        entry = entry.format(song_id=song_id, song_title=song_title)
        return entry

    def get_song_list(self):
        songs = self.program_info.get("song_list")
        if songs is None:
            songs = sorted(list(self.repertoire.keys()))
        return songs

    def generate_index_list_blob(self) -> str:
        songs = self.get_song_list()
        entries = []
        for song in songs:
            entry = self.make_index_entry(
                song_id=song,
                song_title=self.repertoire[song]["title"]
            )
            entries.append(entry)
        blob = "\n".join(entries)
        return blob

    def generate_singers_blob(self) -> str:
        singers_raw = self.program_info.get("singers", "")
        if not singers_raw:
            return ""
        singers_sort = sorted(
            singers_raw,
            key=lambda x: x.split(" ")[-1]
        )
        singers= [
            foo.replace("_", " ")
            for foo in singers_sort
        ]
        half_len = len(singers) // 2
        col_0 = "<br>".join(singers[:half_len])
        col_1 = "<br>".join(singers[half_len:])
        with open("html_blocks/singer_block_template.html", 'r') as ff:
            template = ff.read()
        content = template.replace("${SINGERS_COL_0}", col_0)
        content = content.replace("${SINGERS_COL_1}", col_1)
        return content

    def generate_song_abouts(self) -> str:
        genie = SongAboutsGenerator(program_info=self.program_info)
        genie.generate()
        abouts = genie.get_content_str()
        return abouts

    def generate_html_str(self) -> str:
        content = self.template.replace(
            self.kREPLACE_MAIN_TITLE,
            self.generate_main_title_block()
        )
        content = content.replace(
            self.kREPLACE_SUBTITLE,
            self.generate_subtitle()
        )
        content = content.replace(
            self.kREPLACE_PROGRAM_LEAFLET_PATH,
            self.generate_program_leaflet_path()
        )
        content = content.replace(
            self.kREPLACE_INDEX_LIST_BLOB,
            self.generate_index_list_blob()
        )
        content = content.replace(
            self.kREPLACE_SINGERS_BLOB,
            self.generate_singers_blob()
        )
        content = content.replace(
            self.kREPLACE_SONG_ABOUTS,
            self.generate_song_abouts()
        )
        return content




# class WordpressSlinger:
#     kWORDPRESS_API_URL = 'https://gothamcitymusic.org/wp-json/wp/v2/pages'
#     def __init__(
#         self,
#         page_title: str,
#         content: str
#     ):
#         self.page_title = page_title
#         # self.perforance_info = performance_info
#         self.content_str = content
#
#     # def generate(self):
#     #     content_maker = RepertoirePageGenerator(self.perforance_info)
#     #     content_maker.generate()
#     #     self.content_str = content_maker.get_content_str()
#
#     def send_page_to_site(self):
#         # Check if the page already exists by its title
#         page_exists = False
#         page_id = None
#
#         # Make a GET request to list existing pages
#         pages_response = requests.get(
#             self.kWORDPRESS_API_URL,
#             auth=(wordpress_username, wordpress_password)
#         )
#
#         if pages_response.status_code == 200:
#             existing_pages = pages_response.json()
#             for page in existing_pages:
#                 if page['title']['rendered'] == self.page_title:
#                     page_exists = True
#                     page_id = page['id']
#                     break
#
#         # Create a new page or update the existing page using the WordPress REST API
#         page_data = {
#             'title': self.page_title,
#             'content': content,
#             'template': 'performance_program'  # Replace with the name of your custom template file
#         }
#
#         if page_exists:
#             # Update the existing page
#             update_response = requests.put(
#                 f'{self.kWORDPRESS_API_URL}/{page_id}',
#                 json=page_data,
#                 auth=(wordpress_username, wordpress_password)
#             )
#
#             if update_response.status_code == 200:
#                 print(f"Page updated successfully. Page ID: {page_id}")
#             else:
#                 print(f"Failed to update the page. Status code: {update_response.status_code}")
#                 print(update_response.text)
#         else:
#             # Create a new page
#             create_response = requests.post(
#                 self.kWORDPRESS_API_URL,
#                 json=page_data,
#                 auth=(wordpress_username, wordpress_password)
#             )
#
#             if create_response.status_code == 201:
#                 print(f"Page created successfully. Page ID: {create_response.json()['id']}")
#             else:
#                 print(f"Failed to create the page. Status code: {create_response.status_code}")
#                 print(create_response.text)


if __name__ == "__main__":
    from hurl_to_wordpress_site import hurl_to_wordpress_site
    genie = PerformancePageGenereator()
    content = genie.generate_html_str()
    with open("tmp.html", "w") as ff:
        ff.write(content)
    hurl_to_wordpress_site(
        page_title_to_check='repertoiress',
        page_content=content
    )
