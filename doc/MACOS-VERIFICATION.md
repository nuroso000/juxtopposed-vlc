# macOS beta.5 verification

This fork includes upstream `958859ebb3f02e526fc0ec8f99336434e6143739`, 321 commits after the earlier beta.4 base, with the macOS adaptations reapplied. Build metadata shipped with the package identifies the exact source commit. The tag and source archive must match it.

## Checks and results

- Native arm64 release compilation and app packaging completed using Qt 6.12.0 on macOS 27.0.1.
- The Qt suite completed **91 passing suites out of 92**. `test_qt_message_log` remains failing in two wrapped-viewport cases, described below. No tests were skipped or disabled to hide this failure.
- The packaging Python suite completed **79 tests: 78 passed, one platform-specific skip**.
- Update-service tests passed, including the exact default GitHub endpoint and rejection of parent-fork release/package URLs.
- Packaged version, required Qt/avcodec/medialibrary modules and headless audio decoding/playback checks passed.
- Native QA used an isolated profile and synthetic media. The actual Qt window played and paused video, its time advanced, the library sidebar opened, and Settings and About were accessible with the beta.5 version displayed. The update-check control started a request; its completed result was not captured. Endpoint enforcement is covered by the update-service tests.
- Packaging uses ad-hoc signing and dependency closure checks. It does not provide Apple notarization or a Developer ID signature.

## Known failing regression

`test_qt_message_log::pruningPreservesRetainedViewportAndSelection` fails for wrapped and wrapped-filtered logs under this Qt 6.12 build. After old entries are pruned from a 5,000-line log, the viewport can move by one wrapped line. Selection and retained text checks pass. The unwrapped cases and other log tests pass. The production implementation and its assertions are retained unchanged; font substitutions or relaxed assertions are not used to turn this result green.

This limitation affects reading long diagnostic logs. It is not evidence of complete visual parity for every Figma state. Some specialist VLC dialogs retain their existing arrangement under the redesign theme.

## Platform limits

The supplied app requires Apple Silicon and macOS 27.0+. It is an experimental community prerelease. Device capture, casting, HDR, network services, every codec, older macOS releases and Intel Macs have not been certified by this local run. The existing installed VLC app is not replaced by the build process.

Automatic checks notify about eligible releases from this fork. Download and installation remain manual. Future upstream changes require review and a rebuilt fork release before they are offered through this channel.
