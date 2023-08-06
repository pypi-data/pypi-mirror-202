if [[ $VIRTUAL_ENV ]]; then
	deactivate
fi

command rm -rf **/dist
command rm -rf **/build
command rm -rf **/*.egg-info
command rm -rf **/__pycache__
command rm -rf **/.pytest_cache
command rm -rf **/venv

echo '[cleanup] done'
