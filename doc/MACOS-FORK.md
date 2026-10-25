# macOS design fork

This is a fork of [dsojevic/juxtopposed-vlc](https://github.com/dsojevic/juxtopposed-vlc), with its original VLC history. The `macos-redesign` branch includes upstream `afc91a108e8203e9ce9ff73c00b835fdf4cb7b4c`: the beta.5 release plus three subsequent maintenance commits, including all 324 commits after the previous local beta.4 base. The upstream `master` branch remains available for synchronization.

The local adaptations expose the QML controls through Cocoa accessibility, forward keyboard focus/events, set stable window titles, support Qt 6.12 framework headers, open Home on idle startup, isolate explicitly requested QA profiles, add persistent Details rows and refresh add-on metadata. The new podcast/library behavior from beta.5 is retained when resolving the old patch.

## Updates that retain the design

The app checks **this fork's GitHub Releases**, `nuroso000/juxtopposed-vlc`. Its release-page and package URL validation also require that exact repository. Releases from VideoLAN, the parent fork or another repository are not offered by this channel. The update source is defined once in `modules/gui/qt/util/release_info.hpp`; regression tests check both the configured endpoint and rejection of parent-fork packages.

Automatic checks respect the existing update preference and check interval. They notify and open the selected release page. **Download and installation remain manual.** This project does not silently install unreviewed upstream packages or claim a signed automatic installer.

The previously supplied beta.4 app still contains its old endpoint. Install this fork's rebuilt app once to acquire the new update channel. From then on only releases deliberately published in this fork are eligible. A source update cannot be classified as "engine only" just by changing a setting: VLC's GUI and engine are built together. UI changes must be reviewed before the next fork release.

## Install the DMG

Download `VLC-4.0.0-beta.5-macos-arm64-r2.dmg` from this fork's release. Quit VLC, open the image, drag **VLC.app** onto **Applications**, and choose **Replace** when Finder asks about the existing `/Applications/VLC.app`. Eject the image and launch VLC from Applications. The image does not run an automatic installer or remove user media/preferences.

The app bundle and Finder display name are **VLC**. This fork keeps its own internal bundle identifier and update channel. The earlier ZIP remains available for compatibility; the DMG is the recommended macOS download.

To create the image from a verified build:

```sh
python3 extras/package/release/make-macos-dmg.py \
  "build-release-output/macos-arm64/VLC.app" \
  --output "build-release-output/VLC-4.0.0-beta.5-macos-arm64-r2.dmg"
```

The packaging script also accepts the earlier `VLC Juxtopposed.app` as input, copies it as `VLC.app`, updates the display name, re-signs the outer bundle, verifies nested signatures and creates a compressed disk image with an Applications link. Its sidecar records both the compiled source commit and packaging commit. No installed app is modified while creating the image.

## Maintain the fork

1. Fetch `upstream/master` and merge it into a separate review branch based on `macos-redesign`.
2. Review all changed GUI files, local layout/theme behavior, accessibility integration and the update repository constant. Resolve overlaps instead of replacing whole old files.
3. Build and run component tests, the update-service tests and release version/module/playback checks. Compare the real player, library and settings with the accepted reference.
4. Merge reviewed changes into `macos-redesign`, increment release identity as needed, build from that exact commit and publish a prerelease only after validation. Include source provenance and SHA-256 checksums.

This workflow preserves the chosen design by controlling what is released. It cannot promise that arbitrary future upstream GUI changes have no visual effect without review. No automatic upstream merge or automatic release publication is configured.

## Build and test

Follow [BUILD-macos.md](BUILD-macos.md) and [RELEASING.md](RELEASING.md). The local Qt 6.12 toolchain produces an arm64 app requiring macOS 27.0+. The app is ad-hoc signed without Developer ID/notarization and is an experimental community build, not an official VideoLAN release.

```sh
export PATH="$(brew --prefix bison)/bin:$(brew --prefix flex)/bin:$PATH"
JOBS=6 bash extras/package/release/build-native.sh
QT_QPA_PLATFORM=offscreen meson test -C build-release-macos --suite qt --num-processes 1 --timeout-multiplier 3 --print-errorlogs
```

Keep Homebrew Bison/Flex on PATH for subsequent Meson commands; otherwise reconfiguration can disable JSON-backed modules when it finds the old macOS system Bison. The framework-header overlay is local to the build directory. Normal app preferences are unchanged; `VLC_USERDATA_PATH` can isolate Qt settings for QA. Packages must not include private profiles or personal media. The beta.5 validation is recorded in [MACOS-VERIFICATION.md](MACOS-VERIFICATION.md). The earlier beta.4 test results are not reused as evidence for this build.

## Credit and limits

VLC by VideoLAN and contributors. Community interface by dsojevic and contributors, adapted from [VLC Redesign by Juxtopposed](https://www.figma.com/community/file/1691465999134370980/vlc-redesign), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), [video](https://youtu.be/ERFeOgqk324). Adapted for real desktop controls, native macOS integration and responsive library views. Existing software/font/dependency licenses remain in place.

Some specialist dialogs retain their VLC arrangement under the theme. Every Figma state has not received a pixel-diff certificate. Device, codec, HDR, casting and online-service support require their own testing.

## Finder document opening

Use the r2 installer or later: the first beta.5 image omitted native document declarations and Finder event forwarding.

macOS packages retain VLC's native media, URL and imported/exported type declarations. Qt handles Finder document events through `QFileOpenEvent`, queues files received during startup, and passes them to the playlist after initialization. Opening another document in an already running app uses the same path.

If a video still opens an older copy of VLC, select a video in Finder, choose Get Info, select VLC from Applications under Open with, and use Change All for that file type. The installer does not silently change associations owned by other players.
