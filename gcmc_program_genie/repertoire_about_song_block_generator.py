import warnings
import os


def check_song_entry(song: dict):
    expected_keys = [
        "id",
        "title",
        "composer",
        "tradition",
        "arranger",
        "description",
        "lyrics",
        "lyrics_title",
        "lyrics_cite",
        "lyrics_by",
        "lyrics_translation",
        "showcase_only",
        "source",
    ]
    for key in song.keys():
        if key not in expected_keys:
            warnings.warn("Unexpected key: {}".format(key))


class AboutSongBlockGenerator:
    kLYRICS_TEXT_CONTAINER = '<td class="has-text-align-center" data-align="center">${REPLACE_LYRICS}</td>'
    kTEMPLATE_PATH = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'html_blocks/song_rep_block_template.html'
    )

    def __init__(self, song: dict):
        check_song_entry(song)
        self.song = song

    def generate(self) -> str:
        with open(self.kTEMPLATE_PATH, 'r') as ff:
            template = ff.read()
        template = template.replace('${REPLACE_SONG_ID}', self.song['id'])
        template = template.replace('${REPLACE_SONG_TITLE}', self.song['title'])
        attribution = self.generate_attribution()
        template = template.replace('${REPLACE_ATTRIBUTION}', attribution)
        template = template.replace('${REPLACE_DESCRIPTION}', self.song['description'])
        lyrics_block = self.generate_lyrics()
        template = template.replace('${REPLACE_LYRICS}', lyrics_block)
        return template

    def generate_attribution(self) -> str:
        blerb_list = []
        composer = self.song.get("composer", "")
        if composer:
            blerb_list.append("by {}.".format(composer))
        arranger = self.song.get("arranger", "")
        tradition = self.song.get("tradition", "")
        if tradition:
            blerb_list.append(tradition+".")
        if arranger:
            blerb_list.append("Arranged by {}.".format(arranger))
        lyracist = self.song.get("lyrics_by", "")
        if lyracist:
            blerb_list.append("Lyrics by {}.".format(lyracist))
        blerb = " ".join(blerb_list)
        return blerb


    def generate_lyrics(self) -> str:
        lyrics = self.song.get("lyrics", "")
        lyrics_title = self.song.get("lyrics_title", "")
        lyrics_translated = self.song.get("lyrics_translated", "")
        if not lyrics and not lyrics_translated:
            return ""
        lyr_block_list = []
        if lyrics:
            lyr_text = lyrics.replace('\n', "<br>")
            lyr_html = self.kLYRICS_TEXT_CONTAINER.replace('${REPLACE_LYRICS}', lyr_text)
            lyr_block_list.append(lyr_html)
        if lyrics_translated:
            lyr_t_text = lyrics_translated.replace('\n', "<br>")
            lyr_t_html = self.kLYRICS_TEXT_CONTAINER.replace('${REPLACE_LYRICS}', lyr_t_text)
            lyr_block_list.append(lyr_t_html)
        # lyrics_template_path = os.path.join(
        #     os.path.abspath(__file__),
        # )
        with open('html_blocks/lyrics_block_template.html', 'r') as ff:
            l_template = ff.read()
        lyr_blocks = '\n'.join(lyr_block_list)
        lyrics_blerb = l_template.replace(
            '${REPLACE_LYRICS_BLOCKS}',
            lyr_blocks
        )
        return lyrics_blerb

