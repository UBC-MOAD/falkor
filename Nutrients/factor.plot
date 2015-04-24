set multiplot
set size 0.5,0.5
set origin 0,0.5
unset key
set xrange [33 to 34.1]
set yrange [*:*]
plot './2013-57-0036.che.txt' using 8:4 with linespoints, './2013-57-0037.che.txt' using 8:4 with linespoints, './2013-57-0038.che.txt' using 8:4 with linespoints, './2013-57-0012.che.txt' using 8:4 with linespoints
set origin 0,0
unset key
plot './2013-57-0036.che.txt' using 8:14 with linespoints, './2013-57-0037.che.txt' using 8:14 with linespoints, './2013-57-0038.che.txt' using 8:14 with linespoints, './2013-57-0012.che.txt' using 8:15 with linespoints
set origin 0.5,0.
plot './2013-57-0036.che.txt' using 8:17 with linespoints, './2013-57-0037.che.txt' using 8:17 with linespoints, './2013-57-0038.che.txt' using 8:17 with linespoints, './2013-57-0012.che.txt' using 8:18 with linespoints
set origin 0.5,0.5
set yrange [20:80]
plot './2013-57-0036.che.txt' using 8:19 with linespoints, './2013-57-0037.che.txt' using 8:19 with linespoints, './2013-57-0038.che.txt' using 8:19 with linespoints, './2013-57-0012.che.txt' using 8:20 with linespoints
unset multiplot
