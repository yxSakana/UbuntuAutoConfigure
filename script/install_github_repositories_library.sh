#!/bin/bash

. script/lib/install_lib.sh

libraries=$*
installLibrariesFromGithub "${libraries[*]}" "false" %{PWD}
