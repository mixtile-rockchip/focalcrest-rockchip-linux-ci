# Focalcrest Rockchip CI

CI/CD repository for building Rockchip Linux images.

> 📥 **[Firmware Download](https://mixtile-rockchip.github.io/focalcrest-rockchip-linux-ci/)**
> Browse and download built images by board and date.

## Supported Boards
- AZ04A
- AZ04B
- AZ05
- AZ07
- AZ08

## Build Type
- Production Test

## How to Trigger Build
GitHub Actions -> Build -> Select Board

## Outputs
- Rockchip `raw.img` in GitHub Release (`.img`)

## Required Repository Secret
- `GITLAB_TOKEN`
  - Used to access `code.focalcrest.com` during the Buildroot build
