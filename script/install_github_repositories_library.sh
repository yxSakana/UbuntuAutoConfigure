#!/bin/bash

. script/lib/install_lib.sh

installLibrariesFromGithub "${libraries[*]}" "false"
