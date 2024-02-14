import json

from hurl_to_wordpress_site import hurl_to_wordpress_site
from repertoire_page_genie import *

def run_repertoiress():
    genie = PerformancePageGenereator()
    content = genie.generate_html_str()
    with open("tmp.html", "w") as ff:
        ff.write(content)
    hurl_to_wordpress_site(
        page_title_to_check='repertoiress',
        page_content=content
    )


def run_13_oct_2023():
    info_path = "../concert_13_oct_2023/program_info.json"
    with open(info_path, "r") as ff:
        program_info=json.load(ff)
    genie = PerformancePageGenereator(
        program_info=program_info,
        program_leaflet_file_name="gmcm_13_oct_2023_program.pdf"
    )
    content = genie.generate_html_str()
    with open("tmp.html", "w") as ff:
        ff.write(content)
    hurl_to_wordpress_site(
        page_title_to_check='2023_oct_13_ss',
        page_content=content
    )

run_repertoiress()
run_13_oct_2023()