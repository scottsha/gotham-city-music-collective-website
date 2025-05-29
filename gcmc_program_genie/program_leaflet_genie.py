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


class ProgramGenerator:
    kQR_CODE_REPLACE = "<QR_CODE_PATH>"
    kSINGER_REPLACE = "<SINGERS_REPLACE>"
    kPERFORMANCE_REPLACE = "<PERFORMANCE_REPLACE>"
    kSUBTITLE_REPLACE = "<SUBTITLE_REPLACE>"

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
        print("Writing to: ", self.latex_generated_path)
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
                note
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
        singers = [
            r"{" + foo.replace("_", " ") + r"}" for foo in
            sorted(
                self.program_info["singers"],
                key=lambda x: x.split(" ")[-1]
            )
        ]
        num_singers = len(singers)
        col_0_len = num_singers // 3
        col_1_len = col_0_len
        num_sing_mod3 = num_singers % 3
        if num_sing_mod3 > 0:
            col_1_len += 1
            if num_sing_mod3 == 2:
                col_0_len += 1

        col_0_singers = singers[:col_0_len]
        col_1_singers = singers[col_0_len:col_0_len + col_1_len]
        col_2_singers = singers[col_0_len + col_1_len:]
        cols_singers = [col_0_singers, col_1_singers, col_2_singers]
        col_strs = []
        for col_sing in cols_singers:
            col_strs.append(
                "\\\\\n".join(col_sing)
            )
        singer_txt = "\\vfill\\null\n\\columnbreak\n\n".join(col_strs)
        return singer_txt

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
        subtitle = "\\\\".join(subtitle_lines)
        program_txt = program_txt.replace(
            self.kSUBTITLE_REPLACE,
            subtitle
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
        performance_txt = self.generate_performance_txt()
        program_txt = program_txt.replace(
            self.kPERFORMANCE_REPLACE,
            performance_txt
        )
        with open(self.latex_generated_path, "w") as ff:
            ff.write(program_txt)


if __name__ == "__main__":
    genie = ProgramGenerator("/home/scott/Programs/gotham-city-music-collective-website/concert_2025_may_29")
    genie.generate()
