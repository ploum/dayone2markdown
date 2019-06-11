# dayone2markdown
Converting DayOne journals into markdown files

Work in progress.

## usage

1. Export you DayOne journal as JSON and unzip the folder.
2. Put the script in the unzipped folder.
3. Run the script `./do2md.py Journal.json`

## Results :

1. Each entry is now converted to an MD file. Name of the file is the date-time of the entry.
2. A title is added as the date-time
3. Pictures are inserted with a relative path ( photos/)
4. Tags are inserted in the text as " #tag" (if they were not previously)
5. Location of an entry is written at the end of the file with both address and coordinates.


## Limitations

1. If there are two entries at the same second, one will be lost.
2. Metadata other than tags, time and location are lost.
