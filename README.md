# Mp4 SRT to MP4 Combiner

Python script that assist in combining SRT subtitle files into corresponding mp4 video files.

> Currently this script has only been developed for use on Windows but I welcome any and all pull requests. So if you feel you can improve the OS compatability I'd appreciate your help.

:heart:

- [Requires](#requires)
- [Installation](#installation)
- [Simple usage](#simple-usage)
- [Advanced usage](#advanced-usage)
- [Contributing](#contributing)

## Requires

The script relies on the `mp4box` utility from the [GPAC](https://gpac.wp.imt.fr/downloads/) software bundle. This tool must be installed prior to running this script.

Requires also Python 3.5+

Before first use make sure you install all requirements using 

```
pip install -r requirements.txt
```

## Installation
The script comes with a shell integration for Windows Explorer. Edit the associated install.reg file and update paths to both your Python installation and the location of the merge.py file on your disk. 

Then merge the registry file into your Windows registry.

You should now get two additional menu options when right clicking MP4 files that allow you to execute the script directly.


## Simple usage
Single mp4 file can be merged with its SRT subtitles by using the following syntax. 

```
python merge.py -i "D:\videos\The.Wire.S02.1080p.BluRay.x265-RARBG\The.Wire.S02E01.1080p.BluRay.x265-RARBG.mp4"
```

The program will search for SRT files to merge with the file in the following places in the listed order of preference
1. Any SRT files in the same directory  (ex. `D:\videos\The.Wire.S02.1080p.BluRay.x265-RARBG`)
2. Any SRT files in a subfolder having the same name as the mp4 file (ex. `D:\videos\The.Wire.S02.1080p.BluRay.x265-RARBG\The.Wire.S02E01.1080p.BluRay.x265-RARBG`)
3. Any SRT files in the root of the "subs" folder (ex. `D:\videos\The.Wire.S02.1080p.BluRay.x265-RARBG\subs`)
4. Any SRT files in a sub folder of "subs" having the same name as the mp4 file (ex. `D:\videos\The.Wire.S02.1080p.BluRay.x265-RARBG\subs\The.Wire.S02E01.1080p.BluRay.x265-RARBG`)

## Advanced usage

> For all options supported by this tool run `python merge.py -h`

The tool can also be instructed to attempt to locate all subtitles for all MP4 files in the same directory as the one selected. Enable this mode by setting the `-d` switch.

```
python merge.py -d -i "D:\videos\The.Wire.S02.1080p.BluRay.x265-RARBG\The.Wire.S02E01.1080p.BluRay.x265-RARBG.mp4"
```

## Contributing

I welcome any and all suggestions and fixes either through the issue system above or through pull-requests.

Although this project is small it has a [code of conduct](CODE_OF_CONDUCT.md) that I hope everyone will do their best to follow when contributing to any aspects of this project. Be it discussions, issue reporting, documentation or programming. 

If you don't want to open issues here on Github, send me your feedback by email at [mp4srtmerge@sverrirs.com](mailto:mp4srtmerge@sverrirs.com).

> _"Be excellent to each other"_
> :hatched_chick: