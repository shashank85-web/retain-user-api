# CHANGES.md

## Major Issues Identified
- No input validation on POST/PUT
- Raw SQL logic in controller
- No password hashing
- No error handling
- Poor code structure and separation

## Changes Made
- Introduced `models`, `routes`, `schemas`, and `utils` folders
- Used `marshmallow` for input validation
- Added bcrypt hashing for passwords
- Added meaningful status codes and error messages
- Separated business logic from routing

## Assumptions / Trade-offs
- Used SQLite for simplicity
- Did not implement pagination or advanced search

## What I'd Do With More Time
- Add JWT token authentication
- Add unit test coverage
- Dockerize the app

## AI Tools Used
- ChatGPT (used for initial structure planning and validation code)
