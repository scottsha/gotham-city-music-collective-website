import requests
import json
from wordpress_credentials import wordpress_password, wordpress_username
import warnings
import os
from repertoire_about_song_block_generator import AboutSongBlockGenerator, check_song_entry

kREPERTOIRE_DATA_PATH = "repertoire_data.json"


def get_repertoire_data() -> dict:
    with open(kREPERTOIRE_DATA_PATH, 'r') as file:
        repertoire_data = json.load(file)
    repertoire_data = sorted(repertoire_data, key=lambda x: x["id"])
    repertoire_dict = {song["id"]: song for song in repertoire_data}
    return repertoire_dict


class AboutSongsListGenerator:
    songlist_div_class = ' <hr class="wp-block-separator has-alpha-channel-opacity is-style-default" style="margin-top:0;margin-bottom:0"> '
    song_index_entry_format = '<a href="#${REPLACE_SONG_ID}" data-type="internal" data-id="#${REPLACE_SONG_ID}">${REPLACE_SONG_TITLE}</a>'

    def __init__(
            self,
            program_info: dict = None
    ):
        self.repertoire_data = get_repertoire_data()
        self.content = []
        self.do_showcases = True
        self.program_info = program_info
        if self.program_info is None:
            self.program_info = {}
        if self.program_info:
            self.do_showcases = False
        self.about_song_blocks = []
        self.song_index_list = []

    def get_song_list(self):
        songs = self.program_info.get("song_list")
        if songs is None:
            songs = sorted(list(self.repertoire_data.keys()))
        return songs

    def get_song_index_entry_html(self, song_id: str, song_title: str) -> str:
        entry = self.song_index_entry_format.replace("${REPLACE_SONG_ID}", song_id)
        entry = entry.replace("${REPLACE_SONG_TITLE}", song_title)
        return entry

    def populate(self):
        self.about_song_blocks = []
        self.song_index_list = []
        songs = self.get_song_list()
        for song_id in songs:
            song = self.repertoire_data[song_id]
            song_title = song['title']
            self.song_index_list.append(
                self.get_song_index_entry_html(song_id, song_title)
            )
            about_generator = AboutSongBlockGenerator(song)
            about_block = about_generator.generate()
            self.about_song_blocks.append(about_block)

    def get_song_index_html(self):
        return '<br>'.join(self.song_index_list)

    def get_about_song_blocks_html(self):
        return self.songlist_div_class.join(self.about_song_blocks)


class RepertoirePageGenerator:
    kREPLACE_MAIN_TITLE = "${REPLACE_MAIN_TITLE_BLOCK}"
    kREPLACE_SUBTITLE = "${SUBTITLE_REPLACE}"
    kREPLACE_PROGRAM_LEAFLET_PATH = "${REPLACE_PROGRAM_LEAFLET_PATH}"
    kREPLACE_INDEX_LIST_BLOB = "${REPLACE_SONG_INDEX_LIST}"
    kREPLACE_SINGERS_BLOB = "${REPLACE_SINGERS_BLOB}"
    kREPLACE_SONG_ABOUTS = "${REPLACE_ABOUT_SONG_BLOCKS}"

    def __init__(
            self,
            html_template: str,
            program_info: dict = None,
            program_leaflet_file_name: str = None,
    ):
        self.template = html_template
        self.repertoire = get_repertoire_data()
        self.program_info = program_info
        if self.program_info is None:
            self.program_info = dict()
        self.leaflet = program_leaflet_file_name
        self.id = self.program_info.get("id", "repertoire")
        self.url = "gothamcitymusic.org/" + self.id

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
        singers = [
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
            self.kREPLACE_SINGERS_BLOB,
            self.generate_singers_blob()
        )
        about_generator = AboutSongsListGenerator()
        about_generator.populate()
        song_index = about_generator.get_song_index_html()
        content = content.replace(
            self.kREPLACE_INDEX_LIST_BLOB,
            song_index
        )
        song_abouts = about_generator.get_about_song_blocks_html()
        content = content.replace(
            self.kREPLACE_SONG_ABOUTS,
            song_abouts
        )
        return content


def example_generate_repertoire():
    from hurl_to_wordpress_site import hurl_to_wordpress_site
    with open("/gcmc_program_genie/html_blocks/repertoire_template.html", 'r') as ff:
        template = ff.read()
    genie = RepertoirePageGenerator(
        html_template=template,
    )
    content = genie.generate_html_str()
    with open("tmp.html", "w") as ff:
        ff.write(content)
    # with open("tmp.html", "r") as ff:
    #     content = ff.read()
    hurl_to_wordpress_site(
        page_title_to_check='repertoire_ss_testing',
        page_content=content
    )


if __name__ == "__main__":
    example_generate_repertoire()
