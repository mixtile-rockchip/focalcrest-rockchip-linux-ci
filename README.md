# Focalcrest Rockchip CI

CI/CD repository for building RK7 Rockchip Linux images.

## Supported Boards
- AZ04B
- AZ07

## Build Type
- Production Test

## How to Trigger Build
GitHub Actions -> Build -> Select Board

## Outputs
- Compressed Rockchip `raw.img` in GitHub Release (`.img.xz`)

## Required Repository Secret
- `GITLAB_TOKEN`
  - Used to access `code.focalcrest.com` during the Buildroot build
