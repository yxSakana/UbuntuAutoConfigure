#!/bin/bash

if [ ! -v _LOG_SH__ ]; then
  __COLOR_CONFIG_SH__="__COLOR_CONFIG_SH__"
  # define color
  readonly COLOR_GREY='\033[90m'
  readonly COLOR_RED='\033[91m'
  readonly COLOR_GREEN='\033[92m'
  readonly COLOR_YELLOW='\033[93m'
  readonly COLOR_BLUE='\033[94m'
  readonly COLOR_MAGENTA='\033[95m'
  readonly COLOR_CYAN='\033[96m'
  readonly COLOR_WHITE='\033[97m'

  # define style
  readonly STYLE_BOLD='\033[1m'
  readonly STYLE_UNDERLINE='\033[4m'

  # define reset
  readonly RESET='\033[0m'

  # function
  # logger level
  log_debug() { echo -e "${COLOR_GREY}  [DEBUG] $1${RESET}"; }
  log_info() { echo -e "${COLOR_GREEN}  [INFO] $1${RESET}"; }
  log_warning() { echo -e "${COLOR_YELLOW}  [WARNING] $1${RESET}"; }
  log_error() { echo -e "${COLOR_RED}  [ERROR] $1${RESET}"; }

  blue() { echo -e "${COLOR_BLUE}$1${RESET}"; }
  magenta() { echo -e "${COLOR_MAGENTA}$1${RESET}"; }
  cyan() { echo -e "${COLOR_CYAN}$1${RESET}"; }
  white() { echo -e "${COLOR_WHITE}$1${RESET}"; }

  bold() { echo -e "${STYLE_BOLD}$1${RESET}"; }
  underline() { echo -e "${STYLE_UNDERLINE}$1${RESET}"; }
fi