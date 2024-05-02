# gotham-city-music-collective-website
Website and Program generation scripts for the Gotham City Music Collective!

## Program Genie

I find it hard to keep all the performace info (who's playing and in what order) synced between program copies and web stuff.
But the Wordpress graphical interface editor makes copy and pasting really rough, so these scripts are ment to generate
a LaTeX template for the paper program (that makes a pdf), Wordpress entries for the program, and Wordpress entries for the repertoire page.
I think it's overall been worth the effort because we reuse the same songs and people often.

### How to update or make a new program

Enter the song information into the repertoire json file:

[repertoire_data.json](gcmc_program_genie%2Frepertoire_data.json)

The generation scripts pull information about songs from that file.
Make a new folder for a new concert, with a json file to keep the program info.
Follow the format in the folder [concert_1_march_2024](concert_1_march_2024) with [program_info.json](concert_1_march_2024%2Fprogram_info.json).

The generation scripts will use that program info json and the repertoire json to fill in details.

The script that generates a latex template is found at:
[program_leaflet_genie.py](gcmc_program_genie%2Fprogram_leaflet_genie.py)

That will output a roughly correct LaTeX file.
Once all the program info is correct, I make a final LaTeX file to edit little things like stray punctuation or adjust the spacing one last time.
