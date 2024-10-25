Official repository: <https://github.com/coletdjnz/yt-dlp-ytse>

# YouTube Streaming Experiments (YTSE)

Experimental YouTube streaming features for yt-dlp.

> [!CAUTION]
> These features are experimental. They may change without notice.

<!-- TOC -->
* [YouTube Streaming Experiments (YTSE)](#youtube-streaming-experiments-ytse)
  * [Features](#features)
  * [Installing](#installing)
    * [pip/pipx](#pippipx)
  * [Usage](#usage)
    * [UMP Downloader](#ump-downloader)
  * [Acknowledgements](#acknowledgements)
<!-- TOC -->

## Features

- [UMP Downloader](#ump-downloader)

## Installing

**Requires yt-dlp `2024.10.22` or above.**

If yt-dlp is installed through `pip` or `pipx`, you can install the plugin with the following:

### pip/pipx

```
pipx inject yt-dlp yt-dlp-ytse
```
or

```
python3 -m pip install -U yt-dlp-ytse
```


<!--
### Manual install

1. Download the latest release zip from [releases](https://github.com/coletdjnz/yt-dlp-ytse/releases) 

2. Add the zip to one of the [yt-dlp plugin locations](https://github.com/yt-dlp/yt-dlp#installing-plugins)

    - User Plugins
        - `${XDG_CONFIG_HOME}/yt-dlp/plugins` (recommended on Linux/macOS)
        - `~/.yt-dlp/plugins/`
        - `${APPDATA}/yt-dlp/plugins/` (recommended on Windows)
    
    - System Plugins
       -  `/etc/yt-dlp/plugins/`
       -  `/etc/yt-dlp-plugins/`
    
    - Executable location
        - Binary: where `<root-dir>/yt-dlp.exe`, `<root-dir>/yt-dlp-plugins/`

For more locations and methods, see [installing yt-dlp plugins](https://github.com/yt-dlp/yt-dlp#installing-plugins) 

-->

If installed correctly, you should see the YTSE YouTubeIE plugin override in `yt-dlp -v` output:

    [debug] Extractor Plugins: YTSE (YoutubeIE)


## Usage


### UMP Downloader

Enable UMP formats:

`--extractor-args youtube:formats=ump`

Prioritize with UMP formats:

`--extractor-args youtube:formats=ump`

Debug UMP messages:

`--extractor-args youtube:ump_debug=1`


## Acknowledgements

- [googlevideo](https://github.com/LuanRT/googlevideo) by [@LuanRT](https://github.com/LuanRT) 