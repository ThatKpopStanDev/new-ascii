


clear_console() {
    echo -e "\033[H\033[J"
}


SONG=$1
SIZE=$2

if [ -z "$SONG" ] || [ -z "$SIZE" ]; then
    echo "Error: It is necessary to pass the 'song' and 'size' parameters."
    exit 1
fi


curl "http://localhost:8080/?song=$SONG&size=$SIZE"


clear_console