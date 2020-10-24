## [1.2.0] - 2020-10-25

### Added

- Add automatic build tests in github (`CI tests`).
- Add config `CREDENTIALS_PATH`
- Add config `DISABLED_PATH`
- Include code for sending emails (imported from `allo_mail`)
- Add command to save the credentials: `credentials <username> <password>`. The credentials are stored in plain text, but encrypted using **`ROT13`**.
- Add command to enable and disable scan: `disable` and `enable`.
- Add command to show current status of scan (if it is enabled or not): `status`.

## Changed

- Use commands instead of arguments in cli. For example, use `now` instead of `-now`.

## [1.1.0] 2020-02-03

### Added

- Add way to disable scan: create a file named `disabled` at the root dir (next to `cli.py`, `requirements.txt` and `CHANGELOG.md`).

[unreleased]: https://github.com/sralloza/lens-db/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/sralloza/lens-db/compare/v1.0.0...v1.1.0
