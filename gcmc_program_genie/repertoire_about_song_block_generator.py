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
        "lyrics_title_translation",
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
    kTEMPLATE_PATH = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'html_blocks/song_rep_block_template.html'
    )
    kLYRIC_PARAGRAPH_HTML = (r'${REPLACE_LYRICS}')

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

    def format_lyric_from_raw(self, lyric_text: str) -> str:
        # paragraphs = lyric_text.split('\n\n')
        # para_htmls = []
        # for para in paragraphs:
        #     phtml = para.replace('\n', '<br>')
        #     para_html = self.kLYRIC_PARAGRAPH_HTML.replace('${REPLACE_LYRICS}', phtml)
        #     para_htmls.append(para_html)
        # return '\n'.join(para_htmls)
        return lyric_text.replace("\n", "<br>")

    def generate_lyrics(self) -> str:
        lyrics = self.song.get("lyrics", "")
        lyrics_translation = self.song.get("lyrics_translation", "")
        if not lyrics and not lyrics_translation:
            return ""
        lyr_text = self.format_lyric_from_raw(lyrics)
        lyr_t_text = self.format_lyric_from_raw(lyrics_translation)
        lyrics_title = self.song.get("lyrics_title", "")
        if lyrics_title:
            lyr_text = '<b>{}</b>'.format(lyrics_title) + "<br><br>" + lyr_text
        lyrics_t_title = self.song.get("lyrics_title_translation", "")
        if lyrics_t_title:
            lyr_t_text = '<b>{}</b>'.format(lyrics_t_title) + "<br><br>" + lyr_t_text
        if lyrics and lyrics_translation:
            with open('html_blocks/lyrics_2_blocks_template.html', 'r') as ff:
                l_template = ff.read()
            lyr_html = l_template.replace('${REPLACE_LYRICS}', lyr_text)
            lyr_html = lyr_html.replace('${REPLACE_LYRICS_TRANSLATION}', lyr_t_text)
            return lyr_html
        if not lyrics:
            lyr_text = lyr_t_text
        with open('html_blocks/lyrics_block_template.html', 'r') as ff:
            l_template = ff.read()
        lyr_text = l_template.replace('${REPLACE_LYRICS}', lyr_text)
        return lyr_text
