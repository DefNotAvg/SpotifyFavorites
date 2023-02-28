<div id="top"></div>

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/DefNotAvg/SpotifyFavorites">
    <img src="https://pbs.twimg.com/profile_images/843246335813914625/EP5S_dWG_400x400.jpg" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">SpotifyFavorites</h3>

  <p align="center">
    Automated Spotify playlist based on your followed artists.
    <br />
    <br />
    <a href="https://github.com/DefNotAvg/SpotifyFavorites/issues">Report Bug</a>
    ·
    <a href="https://github.com/DefNotAvg/SpotifyFavorites/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

* pip
  ```sh
  pip install -r requirements.txt
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/DefNotAvg/SpotifyFavorites.git
   ```
2. Install Python packages
   ```sh
   pip install -r requirements.txt
   ```
3. Create a Spotify developer application if you don't yet have one ([reference link](https://developer.spotify.com/dashboard/applications))
4. Set your Spotify ClientId and ClientSecret as the `SPOTIPY_CLIENT_ID` and `SPOTIPY_CLIENT_SECRET` environment variables respectively ([reference doc](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html))

5. Edit config.json to your liking
   ```sh
   {
       "redirectURI": "http://localhost:8080/callback", # Obtained from https://developer.spotify.com/dashboard/applications
       "username": "yap8b0pkw7hdeqbfydk2cyj0a", # Obtained from https://www.spotify.com/us/account/overview
       "playlistId": "58iW4JvNgkpt9ezuuC3TC7", # Obtained from back-half of playlist URL (Ex: https://open.spotify.com/playlist/5GUwELpSDAMqIEqfdJmozJ)
       "scope": "playlist-modify-public", # Authorization scope for modifying the aforementioned playlistId (playlist-modify-public or playlist-modify-private)
       "lookbackDays": 14, # Maximum number of days ago a song was released to be a part of the playlist
       "explicit": true # true if explicit songs should be included and preferred to their clean counterpart, false to avoid explicit tracks altogether
   }
   ```
6. Run main.py

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Automate population of Spotify playlist from followed artists
- [x] Make recent track search more robust
- [x] Add support for explicit content preferences
- [ ] Add error handling as issues arise

See the [open issues](https://github.com/DefNotAvg/SpotifyFavorites/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Dante Arcese - [@DefNotAvg](https://twitter.com/DefNotAvg) - DefNotAvg@gmail.com

Project Link: [https://github.com/DefNotAvg/SpotifyFavorites](https://github.com/DefNotAvg/SpotifyFavorites)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/DefNotAvg/SpotifyFavorites.svg?style=for-the-badge
[contributors-url]: https://github.com/DefNotAvg/SpotifyFavorites/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/DefNotAvg/SpotifyFavorites.svg?style=for-the-badge
[forks-url]: https://github.com/DefNotAvg/SpotifyFavorites/network/members
[stars-shield]: https://img.shields.io/github/stars/DefNotAvg/SpotifyFavorites.svg?style=for-the-badge
[stars-url]: https://github.com/DefNotAvg/SpotifyFavorites/stargazers
[issues-shield]: https://img.shields.io/github/issues/DefNotAvg/SpotifyFavorites.svg?style=for-the-badge
[issues-url]: https://github.com/DefNotAvg/SpotifyFavorites/issues