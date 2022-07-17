<!-- ABOUT THE PROJECT -->
## About The Project
This is a simple Python implementation that detects new records from '[https://stisys.haw-hamburg.de/](https://stisys.haw-hamburg.de/)'. 
The script is checking every 10 minutes if the data has changed and then notifies you via your 'firstname.surname@haw-hamburg.de' email account.

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

To use this script an installed Python interpreter >= 3.5 is needed.
### Installation

1.  Clone the repo
 ```sh
   git clone https://github.com/nikiibarbaro/Stisys-records-checker.git
   ```
2. via cmd or terminal to install dependencies
```sh
   pip install -r requirements.txt
   ```


<!-- USAGE EXAMPLES -->
## Usage

via cmd or terminal

options:
  -h, --help  show this help message and exit
  -u U        username e.g. xxx123
  -p P        password your're using to login
  -e E        email adress where notifications being send to (optional)
```sh
   check_stisys.py -u 'username' -p 'password' -e 'emailadress'
   ```

<!-- ROADMAP -->
## TODO
- [ ] Mobile push support (Android/IOS)
	- [ ] Native Android or IOS implementation 
- [ ] Settings to display records
- [ ] Autostart or creating task using scheduler


See the [open issues](https://github.com/nikiibarbaro/Stisys-records-checker/issues) for a full list of proposed features (and known issues).

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>

