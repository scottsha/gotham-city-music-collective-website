import copy
import os
import json


def load_repertoire_info():
    path = "repertoire_data.json"
    with open(path, "r") as ff:
        info = json.load(ff)
    info_dict = dict()
    for song in info:
        info_dict[song["id"]] = song
    return info_dict


def format_n_sort_namelist(namelist: list[str]) -> list[str]:
    nicelist = [
        r"{" + foo.replace("_", " ") + r"}" for foo in
        sorted(
            namelist,
            key=lambda x: x.split(" ")[-1]
        )
    ]
    return nicelist

def latex_literal_wrap(x: str) -> str:
    y = x.replace('&', '\&')
    return y


def split_list(input_list, num_cols):
    quo, rem = divmod(len(input_list), num_cols)
    return [input_list[i * quo + min(i, rem):(i + 1) * quo + min(i + 1, rem)] for i in range(num_cols)]


def latex_multicol_formatting(xxs: list[str], num_cols=3) -> str:
    columns = split_list(xxs, num_cols)
    col_strs = []
    for col_entry in columns:
        col_strs.append(
            "\\\\\n".join(col_entry)
        )
    singer_txt = "\\null\n\\columnbreak\n\n".join(col_strs)
    return singer_txt


class ProgramGenerator:
    kQR_CODE_REPLACE = "<QR_CODE_PATH>"
    kSINGER_REPLACE = "<SINGERS_REPLACE>"
    kMEZZO_MEMBERS_REPLACE = "<MEZZO_MEMBERS_REPLACE>"
    kACCOMPANIMENT_REPLACE = "<ACCOMPANIMENT_REPLACE>"
    kPERFORMANCE_REPLACE = "<PERFORMANCE_REPLACE>"
    kSUBTITLE_REPLACE = "<SUBTITLE_REPLACE>"
    kDATE_REPLACE = "<DATE_REPLACE>"
    kVENUE_REPLACE = "<VENUE_REPLACE>"

    def __init__(self, dir: str):
        self.dir = dir
        self.template_path = os.path.join(self.dir, "program_template.tex")
        self.program_info_file = os.path.join(self.dir, "program_info.json")
        with open(self.program_info_file, "r") as ff:
            self.program_info = json.load(ff)
        with open(self.template_path, "r") as ff:
            self.template = ff.read()
        program_id = self.program_info.get("id")
        self.latex_generated_path = os.path.join(
            self.dir,
            "gcmc_{}_program.tex".format(program_id)
        )
        self.repertoire_info = load_repertoire_info()

    def generate_song_entry(self, song_id):
        song_info = self.repertoire_info[song_id]
        source_info = song_info.get('source', "")
        about_strs = []
        if source_info:
            about_strs.append(
                r"\mbox{from \emph{" + source_info + r"}}"
            )
        composer = song_info.get('composer', "")
        if composer:
            about_strs.append(
                r"\mbox{" + composer + r"}"
            )
        arranger = song_info.get('arranger', "")
        if arranger:
            about_strs.append(
                r"\mbox{Arr. " + arranger + r"}"
            )
        note = self.program_info.get("notes", {}).get(song_id)
        if note:
            about_strs.append(
                r"\mbox{" + note + r"}"
            )
        about_str = ". ".join(about_strs)
        title = r"\textbf{" + song_info.get('title') + r"}"
        song_entry = "\\performancepiece {<title>} {<about>}\\\\\n"
        song_entry = song_entry.replace("<title>", title)
        song_entry = song_entry.replace("<about>", about_str)
        return song_entry

    def generate_qr_code(self):
        pass

    def generate_qr_txt(self) -> str:
        return ""

    def generate_singers_txt(self) -> str:
        singers = format_n_sort_namelist(
            self.program_info.get("singers", [])
        )
        singers_txt = latex_multicol_formatting(singers)
        return singers_txt

    def generate_acompaniment_txt(self) -> str:
        acompaniment = format_n_sort_namelist(
            self.program_info.get("accompaniment", [])
        )
        acompaniment_txt = latex_multicol_formatting(acompaniment, 2)
        return acompaniment_txt

    def generate_mezzo_members_txt(self) -> str:
        mezzo = format_n_sort_namelist(
            self.program_info.get("mezzo", [])
        )
        mezzo_txt = latex_multicol_formatting(mezzo)
        return mezzo_txt

    def generate_performance_txt(self) -> str:
        song_list = self.program_info.get("song_list")
        perf = []
        for song in song_list:
            if song == "break":
                perf.append(r"\fleurons")
            else:
                song_txt = self.generate_song_entry(song)
                perf.append(
                    song_txt
                )
        performance_txt = "\n".join(perf)
        return performance_txt

    def generate(self):
        program_txt = copy.copy(self.template)
        self.generate_qr_code()
        qr_txt = self.generate_qr_txt()
        subtitle_lines = self.program_info.get("subtitle")
        subtitle = latex_literal_wrap("\\\\".join(subtitle_lines))
        program_txt = program_txt.replace(
            self.kSUBTITLE_REPLACE,
            subtitle
        )
        program_txt = program_txt.replace(
            self.kVENUE_REPLACE,
            self.program_info.get("venue")
        )
        program_txt = program_txt.replace(
            self.kDATE_REPLACE,
            self.program_info.get("date")
        )
        program_txt = program_txt.replace(
            self.kQR_CODE_REPLACE,
            qr_txt
        )
        singer_txt = self.generate_singers_txt()
        program_txt = program_txt.replace(
            self.kSINGER_REPLACE,
            singer_txt
        )
        accomaniment_text = self.generate_acompaniment_txt()
        program_txt = program_txt.replace(
            self.kACCOMPANIMENT_REPLACE,
            accomaniment_text
        )
        program_txt = program_txt.replace(
            self.kMEZZO_MEMBERS_REPLACE,
            self.generate_mezzo_members_txt()
        )
        performance_txt = self.generate_performance_txt()
        program_txt = program_txt.replace(
            self.kPERFORMANCE_REPLACE,
            performance_txt
        )
        with open(self.latex_generated_path, "w") as ff:
            ff.write(program_txt)


if __name__ == "__main__":
    genie = ProgramGenerator("/home/scott/Programs/gotham-city-music-collective-website/concert_31_may_2024")
    genie.generate()
