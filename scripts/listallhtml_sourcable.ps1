function listallhtml {

param(
    [switch]
    $PageOutput
)
if ($PageOutput) {
    Get-ChildItem -Recurse -Path *.html | less
}
else {
    Get-ChildItem -Recurse *.html
}

}
