# macOS design fork

This is a fork of [dsojevic/juxtopposed-vlc](https://github.com/dsojevic/juxtopposed-vlc), with its original VLC history. The `macos-redesign` branch includes upstream `958859ebb3f02e526fc0ec8f99336434e6143739` (4.0.0-beta.5), including all 321 commits after the previous local beta.4 base. The upstream `master` branch remains available for synchronization.

The local adaptations expose the QML controls through Cocoa accessibility, forward keyboard focus/events, set stable window titles, support Qt 6.12 framework headers, open Home on idle startup, isolate explicitly requested QA profiles, add persistent Details rows and refresh add-on metadata. The new podcast/library behavior from beta.5 is retained when resolving the old patch.

## Updates that retain the design

The app checks **this fork's GitHub Releases**, `nuroso000/juxtopposed-vlc`. Its release-page and package URL validation also require that exact repository. Releases from VideoLAN, the parent fork or another repository are not offered by this channel. The update source is defined once in `modules/gui/qt/util/release_info.hpp`; regression tests check both the configured endpoint and rejection of parent-fork packages.

Automatic checks respect the existing update preference and check interval. They notify and open the selected release page. **Download and installation remain manual.** This project does not silently install unreviewed upstream packages or claim a signed automatic installer.

The previously supplied beta.4 app still contains its old endpoint. Install this fork's rebuilt app once to acquire the new update channel. From then on only releases deliberately published in this fork are eligible. A source update cannot be classified as "engine only" just by changing a setting: VLC's GUI and engine are built together. UI changes must be reviewed before the next fork release.

## Maintain the fork

1. Fetch `upstream/master` and merge it into a separate review branch based on `macos-redesign`.
2. Review all changed GUI files, local layout/theme behavior, accessibility integration and the update repository constant. Resolve overlaps instead of replacing whole old files.
3. Build and run component tests, the update-service tests and release version/module/playback checks. Compare the real player, library and settings with the accepted reference.
4. Merge reviewed changes into `macos-redesign`, increment release identity as needed, build from that exact commit and publish a prerelease only after validation. Include source provenance and SHA-256 checksums.

This workflow preserves the chosen design by controlling what is released. It cannot promise that arbitrary future upstream GUI changes have no visual effect without review. No automatic upstream merge or automatic release publication is configured.

## Build and test

Follow [BUILD-macos.md](BUILD-macos.md) and [RELEASING.md](RELEASING.md). The local Qt 6.12 toolchain produces an arm64 app requiring macOS 27.0+. The app is ad-hoc signed without Developer ID/notarization and is an experimental community build, not an official VideoLAN release.

```sh
JOBS=6 bash extras/package/release/build-native.sh
QT_QPA_PLATFORM=offscreen meson test -C build-release-macos --suite qt --num-processes 1 --timeout-multiplier 3 --print-errorlogs
```

The framework-header overlay is local to the build directory. Normal app preferences are unchanged; `VLC_USERDATA_PATH` can isolate Qt settings for QA. Packages must not include private profiles or personal media. The new beta.5 source needs fresh validation; the earlier beta.4 test results are not evidence for this build.

## Credit and limits

VLC by VideoLAN and contributors. Community interface by dsojevic and contributors, adapted from [VLC Redesign by Juxtopposed](https://www.figma.com/community/file/1691465999134370980/vlc-redesign), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), [video](https://youtu.be/ERFeOgqk324). Adapted for real desktop controls, native macOS integration and responsive library views. Existing software/font/dependency licenses remain in place.

Some specialist dialogs retain their VLC arrangement under the theme. Every Figma state has not received a pixel-diff certificate. Device, codec, HDR, casting and online-service support require their own testing.
