<div align="center">

[![template](https://img.shields.io/badge/Repository-template-darkred)](https://github.com/Nakama3942/template_rep)
[![GitHub license](https://img.shields.io/github/license/Nakama3942/qt_colored_logger?color=gold&style=flat-square)](https://github.com/Nakama3942/qt_colored_logger/blob/master/LICENSE)

!!!ATTENTION!!! In connection with the increase in capabilities and functionality, the library has changed its name! It is now called [Mighty Logger](https://pypi.org/project/mighty-logger/). This repository **is no longer maintained by the author**!

[![NEW PROJECT LIBRARY](https://img.shields.io/badge/NEW-PROJECT_LIBRARY-orange?style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/mighty-logger/)
[![NEW REPOSITORY](https://img.shields.io/badge/NEW-REPOSITORY-darkred?style=for-the-badge&logo=github)](https://github.com/Nakama3942/mighty_logger)

</div>

# Qt_Сolored-logger
### Content
- [Qt_Сolored-logger](#qtсolored-logger)
	- [Content](#content)
	- [Preamble](#preamble)
	- [Overview](#overview)
    - [Important releases](#important-releases)
	- [LICENSE](#license)
	- [Installation](#installation)
	- [Usage](#usage)
	- [Additional functionality](#additional-functionality)
	- [Data](#data)
	- [Troubleshooting](#troubleshooting)
	- [Authors](#authors)

## Preamble
I often came across the opinion that it is better to use not standard output to the console, but full-fledged logging... However, the standard libraries do not provide exactly what I need... Therefore, I decided to make my own library! Which will implement the functionality I need.

I was inspired by the [colored-logs](https://pypi.org/project/colored-logs/) library.

- [Content](#content)

## Overview
The library implements the formation of a beautifully formatted colored text, similar to a log, which has all the necessary information:
- Device name and registered profile, system name, etc. (this data is displayed only once at the beginning of the logging)
- Log entry time
- Log entry status
- Description of the log entry status
- Log entry type
- Entry message

Any information to the output can be turned off (according to the default, everything is included). It is also possible to change the output settings during the logging process. It is possible to change the colors of the foreground text and the background.

- [Content](#content)

## Important releases
<details><summary>See the important releases (possible spoilers)</summary>

- [x] v0.1.0 - First official release (complete basic HTML logger)
- [x] v0.2.0 - Structural update (added basic console logger with HTML base)
- [x] v0.3.0 - Background update (added background for log entries)
- [x] v0.4.0 - Buffer update (added text buffer)
- [x] v0.5.0 - PROJECT NAME CHANGED

!!!ATTENTION!!! In connection with the increase in capabilities and functionality, the library has changed its name! It is now called [Mighty Logger](https://pypi.org/project/mighty-logger/). This repository **is no longer maintained by the author**!

</details>

- [Content](#content)

## LICENSE
The full text of the license can be found at the following [link](https://github.com/Nakama3942/qt_colored_logger/blob/master/LICENSE).

> Copyright © 2023 Kalynovsky Valentin. All rights reserved.
>
> Licensed under the Apache License, Version 2.0 (the "License");
> you may not use this file except in compliance with the License.
> You may obtain a copy of the License at
>
>     http://www.apache.org/licenses/LICENSE-2.0
>
> Unless required by applicable law or agreed to in writing, software
> distributed under the License is distributed on an "AS IS" BASIS,
> WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
> See the License for the specific language governing permissions and

- [Content](#content)

## Installation
Despite the fact that the library was originally developed for use in PyQt, it does not require PyQt to be installed, since this framework for outputting to Text fields, which support not only Plain Text, uses HTML and this library simply simplifies the logging process, since the creation process already formatted strings is registered in this library.

!!!ATTENTION!!! In connection with the increase in capabilities and functionality, the library has changed its name! It is now called [Mighty Logger](https://pypi.org/project/mighty-logger/). This repository **is no longer maintained by the author**!

To install the library, enter the command:
```sh
pip install qt-colored-logger
```

## Usage
This is the simplest example of using the library:
```python
from qt_colored_logger.text import TextBuffer
from qt_colored_logger.logger import Logger

if __name__ == "__main__":
	buf = TextBuffer(115)
	logger = Logger(program_name="Test", text_buffer=buf)
	logger.MESSAGE(status_message_text="OK", message_text="Outputting the message")
```

The outputs in console will contain the following text (GitHub, PyPi and possibly some other sites do not support displaying colors in Markdown - use resources that support them, such as PyCharm):
> <span style='background-color: #;'><span style='color: #ffd700;'>-Test?entry> $███████████████^████@███████:██████████:█████:█████████:█████</span></span><br>
> <span style='background-color: #;'><span style='color: #b0e0e6;'>-?entry> </span><span style='color: #da70d6;'>*2023-04-09 12:37:07.198496 </span><span style='color: #ffa500;'>#STATUS: </span><span style='color: #ff8c00;'>OK </span><span style='color: #afeeee;'>@MESSAGE - </span><span style='color: #b0e0e6;'>Outputting the message</span></span><br>

See the USAGING.md file for more details.

- [Content](#content)

## ~~Additional functionality~~
!!!ATTENTION!!! In connection with the increase in capabilities and functionality, the library has changed its name! It is now called [Mighty Logger](https://pypi.org/project/mighty-logger/). This repository **is no longer maintained by the author**!

- [Content](#content)

## Data
See the DATA.md file.

- [Content](#content)

## Troubleshooting
!!!ATTENTION!!! In connection with the increase in capabilities and functionality, the library has changed its name! It is now called [Mighty Logger](https://pypi.org/project/mighty-logger/). This repository **is no longer maintained by the author**!

All functionality of the library has been tested by me, but if you have problems using it, the code does not work, have suggestions for optimization or advice for improving the style of the code and the name - I invite you [here](https://github.com/Nakama3942/qt_colored_logger/blob/master/CONTRIBUTING.md) and [here](https://github.com/Nakama3942/qt_colored_logger/blob/master/CODE_OF_CONDUCT.md).

- [Content](#content)

## Authors
<table align="center" style="border-width: 10; border-style: ridge">
	<tr>
		<td align="center"><a href="https://github.com/Nakama3942"><img src="https://avatars.githubusercontent.com/u/73797846?s=400&u=a9b7688ac521d739825d7003a5bd599aab74cb76&v=4" width="150px;" alt=""/><br /><sub><b>Kalynovsky Valentin</b></sub></a><sub><br />"Ideological inspirer and Author"</sub></td>
		<!--<td></td>-->
	</tr>
<!--
	<tr>
		<td></td>
		<td></td>
	</tr>
-->
</table>
