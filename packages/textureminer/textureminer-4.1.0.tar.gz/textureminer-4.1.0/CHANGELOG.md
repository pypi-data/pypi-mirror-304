# Textureminer Changelog

All notable changes to this project will be documented in this file.

---

<!--
## Unreleased

### Added

### Changed

### Fixed

### Removed

### Known Issues
-->

---

## 4.1.0

### Added

* Support Python 3.13 in addition to Python 3.12.

### Fixed

* Fixed missing textures when using a preview release of Minecraft Bedrock.

## 4.0.1 | 2024-10-27

### Fixed

* Fix crash due to incorrect git branch of `bedrock-samples` repository.

---

## 4.0.0 | 2024-09-05

### Added

* Support for Linux.
* Change default output directory to `~/textureminer/`.
* Disable scaling by default.
* Simplify file structure of textures by default. For example on Bedrock candles are directly in block and items directories instead of a nested `candles/` directory. Can be disabled with `--no-simple-structure` flag.
* Tests that run on GitHub Actions.
* Package typings when installing with `pip`.
* Centralized logging, `--verbose` and `--silent` flags.
* Ability to turn off color output with `--no-color` flag or `NO_COLOR=1` environment variable.

### Changed

* Removed space from title text.

## 3.1.1 | 2024-08-16

### Changed

* `--version` now gets the version dynamically from the package metadata.

### Fixed

* Fixed a crash when using Java 24w33a or later.

## 3.1.0 | 2024-08-08

### Added

* Support for snow layers.

### Fixed

* Fix stained glass pane names to be consistent with Minecraft IDs.
* Add missing stained glass panes.
* Fix animated textures not getting cropped when scaling factor is set to 1.

## 3.0.0 | 2024-08-07

### Added

* Add `--crop` flag that crops animated textures like magma and prismarine blocks to be same size as other blocks. This functionality was already present but now you can opt-out of it.
* Add `--partials` flag that creates textures for the following partial blocks: carpets, stairs, and slabs.
* Add `--replicate` flag that copies textures and renames them to match the block's name. Currently only used for glass panes.
* Create texture images for waxed copper variants. Currently you cannot turn this on, but a CLI flag might be added in the future.
* Created CI workflow to run linting and formatting checks on pull requests as will as confirming that the package builds and installs correctly.

### Changed

* Upgraded dependencies to latest versions.
* Each `Edition` instance now has its own temporary directory. This allows multiple `Edition` classes to be used simultaneously.
* Migrated to [ruff](https://github.com/astral-sh/ruff) for linting and formatting.

### Fixed

* Fixed inconsistent cleanup of temporary directories.
* Fixed duplicate logging messages.

## 2.0.2 | 2024-01-24

### Fixed

* Vulnerability in `pillow` dependency.

## 2.0.1 | 2024-01-10

### Fixed

* Changelog heading for version 2.0.0 was incorrect.

## 2.0.0 | 2024-01-10

### Added

* Add `textureminer` to path when installing with `pip`.
* Change command-line parser to `argparse`. This allows more complex arguments and flags to be added.
* Add `--version` flag to print the current version of `textureminer`.
* Add `--help` flag to print the help message.
* Add `--java`|`-j` and `--bedrock`|`-b` flags to specify the edition of Minecraft to download textures for. Uses Java Edition if neither is specified.
* Add `--scale` flag to customize the scale factor.
* Add `--output` flag to customize the output directory.
* Add `--flatten` flag to flatten the output directory.

### Changed

* Make project naming more consistent.
* Major refactor into class-based structure.
* Changed base syntax to `textureminer [version] [flags]`. If version is omitted, the latest version of Minecraft will be used.
* Default value of `DO_MERGE`, now `False`, meaning that the textures will not be flattened to a single directory.
* Default value of `UPDATE` is now `all`, meaning that the most recent version of Minecraft will be used.
* Default value of `OUTPUT_DIR` is now `~/Downloads/textureminer/`.

### Fixed

* Missing punctuation.
* Python 3.12 compatibility.

### Removed

* Remove positional edition argument. Use `--java`|`-j` and `--bedrock`|`-b` flags instead or omit to use Java Edition.

### Known Issues

* Earliest Bedrock Edition version supported is v1.19.30. This is due to the fact that the `bedrock-samples` repository was not created until then.

---

## 1.1.2 | 2023-07-07

### Changed

* Clone only the required parts of the `bedrock-samples` repository when using Bedrock Edition

### Fixed

* Java Edition being selected even when Bedrock Edition was specified
* Capitalization of edition names

---

## 1.1.0 | 2023-07-07

### Changed

* Crop large textures to 16×16 pixels

---

## 1.0.0 | 2023.06.15

### Added

* Bedrock Edition support
* CLI argument support
* Nice title for CLI entry point

### Changed

* Lots of refactoring
* Improved documentation
* Made text output more consistent and informative

### Fixed

* Clear temporary directory after use
