# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

## [0.3.1] - 2023-04-12

### Added

- Add changelog and test cases to sdist.

## [0.3.0] - 2023-04-12

### Added

- Improve API by not requiring entering another context manager.

### Fixed

- Fix bad method call in `SafeTensors.metadata`.
- Prevent UNIX file descriptor / Windows handle exhaustion by recycling the same memory map for multiple tensors (rather than creating an independent one for every tensor).
