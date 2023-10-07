#!/bin/bash

if [ ! -v __COLOR_CONFIG_SH__ ]; then
  __COLOR_CONFIG_SH__="__COLOR_CONFIG_SH__"
  # define color
  readonly COLOR_RED='\033[31m'
  readonly COLOR_GREEN='\033[32m'
  readonly COLOR_YELLOW='\033[33m'
  readonly COLOR_BLUE='\033[34m'
  readonly COLOR_MAGENTA='\033[35m'
  readonly COLOR_CYAN='\033[36m'
  readonly COLOR_WHITE='\033[37m'

  # define style
  readonly STYLE_BOLD='\033[1m'
  readonly STYLE_UNDERLINE='\033[4m'

  # define reset
  readonly RESET='\033[0m'

  # function
  red() { echo -e "${COLOR_RED}$1${RESET}"; }
  green() { echo -e "${COLOR_GREEN}$1${RESET}"; }
  yellow() { echo -e "${COLOR_YELLOW}$1${RESET}"; }
  blue() { echo -e "${COLOR_BLUE}$1${RESET}"; }
  magenta() { echo -e "${COLOR_MAGENTA}$1${RESET}"; }
  cyan() { echo -e "${COLOR_CYAN}$1${RESET}"; }
  white() { echo -e "${COLOR_WHITE}$1${RESET}"; }

  bold() { echo -e "${STYLE_BOLD}$1${RESET}"; }
  underline() { echo -e "${STYLE_UNDERLINE}$1${RESET}"; }
fi
